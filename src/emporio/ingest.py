"""Valido as fontes e preparo a carga; o atendimento nunca abre os CSVs."""

import csv
import hashlib
import json
import re
import secrets
from datetime import date
from decimal import Decimal
from pathlib import Path
from urllib.parse import quote, urlsplit, urlunsplit

import psycopg
from dotenv import set_key
from psycopg import sql
from psycopg.types.json import Jsonb
from pypdf import PdfReader

from emporio.config import ROOT, Settings

TABLES = ("categories", "products", "promotions", "customers", "orders", "order_items")
IDS = {
    "categories": "category_id",
    "products": "product_id",
    "promotions": "promotion_id",
    "customers": "customer_id",
    "orders": "order_id",
}
RELATIONS = (
    ("products", "category_id", "categories", "category_id"),
    ("promotions", "product_id", "products", "product_id"),
    ("orders", "customer_id", "customers", "customer_id"),
    ("order_items", "order_id", "orders", "order_id"),
    ("order_items", "product_id", "products", "product_id"),
)


def load_sources(directory: Path) -> tuple[dict, dict]:
    """Não altero o arquivo original nem preencho fatos ausentes."""
    data, report = {}, {"tables": {}, "issues": []}
    for table in TABLES:
        files = list(directory.glob(f"* - {table}.csv"))
        if not files:
            if table in ("customers", "orders", "order_items"):
                report["tables"][table] = {"rows": 0, "omitted": "fonte privada opcional ausente"}
                data[table] = []
                continue
            raise ValueError(f"Arquivo obrigatório ausente: {table}.csv")
        if len(files) != 1:
            raise ValueError(f"Mais de uma fonte para {table}.")
        with files[0].open(encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.DictReader(stream))
        if not rows or None in rows[0]:
            raise ValueError(f"CSV vazio ou inválido: {table}")
        nulls = {k: sum(not (r.get(k) or "").strip() for r in rows) for k in rows[0]}
        key = IDS.get(table)
        if key and len({r[key] for r in rows}) != len(rows):
            raise ValueError(f"Identificador duplicado: {table}")
        converted = []
        for row in rows:
            item = {}
            for k, value in row.items():
                value = value.strip()
                if not value:
                    item[k] = None
                elif k.endswith("_id") or k in ("quantity", "stock_quantity"):
                    item[k] = int(value)
                elif k in ("price_brl", "total_brl", "discount_percent"):
                    item[k] = Decimal(value)
                    if not item[k].is_finite() or item[k] < 0:
                        raise ValueError(f"Valor numérico inválido em {table}.{k}")
                elif k in ("created_at", "order_date", "estimated_delivery"):
                    item[k] = date.fromisoformat(value)
                elif k == "specs":
                    item[k] = json.loads(value)
                elif k == "is_active":
                    if value not in ("0", "1"):
                        raise ValueError("is_active deve ser 0 ou 1.")
                    item[k] = value == "1"
                else:
                    item[k] = value
            converted.append(item)
        data[table] = converted
        report["tables"][table] = {
            "rows": len(rows),
            "nulls": {k: v for k, v in nulls.items() if v},
        }
    for table, key, target, target_key in RELATIONS:
        valid = {r[target_key] for r in data[target]}
        if any(r[key] not in valid for r in data[table]):
            raise ValueError(f"Referência ausente em {table}.{key}")
    if len({(r["order_id"], r["product_id"]) for r in data["order_items"]}) != len(
        data["order_items"]
    ):
        raise ValueError("Item de pedido duplicado.")
    report["notes"] = [
        "Campos ausentes permanecem NULL; não inferi recebimento a partir da previsão.",
        "Não há vigência por data nas promoções: is_active pertence ao snapshot.",
        "Clientes e pedidos não são consultáveis pela identidade do atendimento.",
    ]
    return data, report


def extract_chunks(path: Path) -> list[dict]:
    source_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    chunks = []
    for page, pdf_page in enumerate(PdfReader(path).pages, 1):
        text = " ".join(pdf_page.extract_text().split())
        text = re.sub(r"\s+Página\s+\d+\s*$", "", text)
        for start in range(0, len(text), 1100):
            content = text[max(0, start - 200) : start + 1300]
            title = re.search(r"\d+(?:\.\d+)?\.?(?:\s+[A-ZÀ-Ý][\wÀ-ÿ]+){1,7}", content)
            chunks.append(
                {
                    "chunk_id": hashlib.sha256(
                        f"{source_hash}:{page}:{start}".encode()
                    ).hexdigest(),
                    "page": page,
                    "section": title.group() if title else f"Página {page}",
                    "content": content,
                    "source_hash": source_hash,
                }
            )
    return chunks


def migrate_and_load(settings: Settings, directory: Path) -> dict:
    data, report = load_sources(directory)
    with psycopg.connect(settings.database_url, connect_timeout=10) as conn:
        for path in sorted((ROOT / "database/migrations").glob("*.sql")):
            conn.execute(path.read_text(), prepare=False)
        for table in TABLES:
            for row in data[table]:
                names = list(row)
                conflict = [IDS[table]] if table in IDS else ["order_id", "product_id"]
                updates = [n for n in names if n not in conflict]
                statement = sql.SQL(
                    "INSERT INTO artefact.{} ({}) VALUES ({}) ON CONFLICT ({}) DO UPDATE SET {}"
                ).format(
                    sql.Identifier(table),
                    sql.SQL(",").join(map(sql.Identifier, names)),
                    sql.SQL(",").join(sql.Placeholder() for _ in names),
                    sql.SQL(",").join(map(sql.Identifier, conflict)),
                    sql.SQL(",").join(
                        sql.SQL("{}=EXCLUDED.{}").format(sql.Identifier(k), sql.Identifier(k))
                        for k in updates
                    ),
                )
                values = [Jsonb(v) if isinstance(v, dict) else v for v in row.values()]
                conn.execute(statement, values)
    return report


def provision_reader(settings: Settings) -> str:
    """Crio uma identidade independente e não reutilizo o administrador no agente."""
    role, password = "artefact_reader", secrets.token_urlsafe(32)
    with psycopg.connect(settings.database_url, connect_timeout=10) as conn:
        existing = conn.execute("SELECT 1 FROM pg_roles WHERE rolname=%s", (role,)).fetchone()
        if not existing:
            conn.execute(
                sql.SQL("CREATE ROLE {} LOGIN NOINHERIT PASSWORD {}").format(
                    sql.Identifier(role), sql.Literal(password)
                )
            )
        else:
            # Reexecuções preservam o login criado anteriormente e seu segredo local.
            from dotenv import dotenv_values

            current = dotenv_values(ROOT / ".env.local").get("ARTEFACT_APP_DB_URL")
            if not current:
                raise ValueError("Identidade já existe sem conexão local; não alterei sua senha.")
        conn.execute(
            sql.SQL("GRANT USAGE ON SCHEMA artefact, extensions TO {}").format(sql.Identifier(role))
        )
        conn.execute(
            sql.SQL("REVOKE ALL ON ALL TABLES IN SCHEMA artefact FROM {}").format(
                sql.Identifier(role)
            )
        )
        conn.execute(
            sql.SQL(
                "GRANT SELECT ON artefact.categories, artefact.products, artefact.promotions, "
                "artefact.policy_chunks TO {}"
            ).format(sql.Identifier(role))
        )
    if existing:
        return current
    parts = urlsplit(settings.database_url)
    user = role + ("." + parts.username.split(".", 1)[1] if "." in parts.username else "")
    url = urlunsplit(
        (
            parts.scheme,
            f"{user}:{quote(password)}@{parts.hostname}:{parts.port or 5432}",
            parts.path,
            parts.query,
            "",
        )
    )
    set_key(str(ROOT / ".env.local"), "ARTEFACT_APP_DB_URL", url)
    (ROOT / ".env.local").chmod(0o600)
    return url


def index_policies(settings: Settings, path: Path) -> dict:
    """Reuso vetores da mesma fonte/modelo para evitar cobrar a reindexação idêntica."""
    from emporio.provider import Embeddings

    chunks = extract_chunks(path)
    with psycopg.connect(settings.database_url, connect_timeout=10) as conn:
        existing = {
            row[0]
            for row in conn.execute(
                "SELECT chunk_id FROM artefact.policy_chunks WHERE source_hash=%s AND model=%s",
                (chunks[0]["source_hash"], settings.embedding_model),
            )
        }
    missing = [c for c in chunks if c["chunk_id"] not in existing]
    event = None
    if missing:
        vectors, event = Embeddings(settings).embed([c["content"] for c in missing])
        with psycopg.connect(settings.database_url, connect_timeout=10) as conn:
            for chunk, vector in zip(missing, vectors):
                conn.execute(
                    """
                    INSERT INTO artefact.policy_chunks
                    (chunk_id,page,section,content,source_hash,model,embedding)
                    VALUES (%s,%s,%s,%s,%s,%s,%s::extensions.vector)
                    ON CONFLICT(chunk_id) DO UPDATE SET
                    content=EXCLUDED.content,embedding=EXCLUDED.embedding,model=EXCLUDED.model
                """,
                    (
                        chunk["chunk_id"],
                        chunk["page"],
                        chunk["section"],
                        chunk["content"],
                        chunk["source_hash"],
                        settings.embedding_model,
                        "[" + ",".join(map(str, vector)) + "]",
                    ),
                )
            conn.execute(
                "DELETE FROM artefact.policy_chunks WHERE source_hash<>%s",
                (chunks[0]["source_hash"],),
            )
    return {
        "pages": len({c["page"] for c in chunks}),
        "chunks": len(chunks),
        "new_embeddings": len(missing),
        "embedding_model": settings.embedding_model,
        "dimensions": settings.embedding_dimensions,
        "usage": event.model_dump() if event else None,
    }
