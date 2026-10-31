"""Consultas parametrizadas com a identidade restrita do atendimento."""

import re
from contextlib import contextmanager
from decimal import ROUND_HALF_UP, Decimal

import psycopg
from psycopg.rows import dict_row

from emporio.config import Settings
from emporio.models import Plan

ACCENTS = "áàâãäéèêëíìîïóòôõöúùûüç"
PLAIN = "aaaaaeeeeiiiiooooouuuuc"


def normalized_sql(column: str) -> str:
    # column é sempre uma constante interna; valores de usuário são parâmetros.
    return f"translate(lower({column}), '{ACCENTS}', '{PLAIN}')"


def normalize(value: str) -> str:
    return value.lower().translate(str.maketrans(ACCENTS, PLAIN))


def money(value: Decimal) -> str:
    return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


class Store:
    def __init__(self, settings: Settings):
        self.settings = settings

    @contextmanager
    def connection(self):
        with psycopg.connect(
            self.settings.database_url,
            connect_timeout=10,
            row_factory=dict_row,
            application_name="artefact_atendimento",
            prepare_threshold=None,
        ) as conn:
            conn.read_only = True
            conn.execute("SET LOCAL statement_timeout='7s'")
            conn.execute("SET LOCAL search_path=artefact,extensions,pg_catalog")
            yield conn

    def products(self, plan: Plan) -> list[dict]:
        conditions, params = [], []
        if plan.available_only:
            conditions.append("p.status='active' AND p.stock_quantity>0")
        if plan.category:
            conditions.append(normalized_sql("c.name") + "=%s")
            params.append(normalize(plan.category))
        for token in plan.query.split()[:6]:
            token = normalize(token).replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
            conditions.append(normalized_sql("p.name") + " LIKE %s")
            params.append("%" + token + "%")
        price = "round(p.price_brl*(1-coalesce(promo.discount_percent,0)/100),2)"
        for bound, operator in ((plan.max_price, "<="), (plan.min_price, ">=")):
            if bound is not None:
                conditions.append(price + operator + "%s")
                params.append(Decimal(str(bound)))
        where = " AND ".join(conditions) or "true"
        query = f"""
            SELECT p.product_id,p.name,p.price_brl,p.stock_quantity,p.status,p.description,p.specs,
                   c.name AS category,coalesce(promo.discount_percent,0) AS discount_percent,
                   {price} AS final_price
            FROM artefact.products p JOIN artefact.categories c USING(category_id)
            LEFT JOIN LATERAL (
                SELECT discount_percent FROM artefact.promotions pr
                WHERE pr.product_id=p.product_id AND pr.is_active
                ORDER BY discount_percent DESC LIMIT 1
            ) promo ON true
            WHERE {where} ORDER BY final_price,p.product_id LIMIT 8
        """
        with self.connection() as conn:
            rows = conn.execute(query, params).fetchall()
        for row in rows:
            if plan.route == "hybrid":
                row["pix_price"] = money(
                    row["final_price"]
                    if row["discount_percent"]
                    else row["price_brl"] * Decimal("0.95")
                )
            for key in ("price_brl", "final_price", "discount_percent"):
                row[key] = money(row[key])
        if (
            rows
            and not plan.available_only
            and any(r["status"] != "active" or r["stock_quantity"] == 0 for r in rows)
        ):
            alternatives = self.products(Plan(route=plan.route, category=rows[0]["category"]))
            original_ids = {r["product_id"] for r in rows}
            rows.extend(
                dict(r, alternative=True)
                for r in alternatives[:3]
                if r["product_id"] not in original_ids
            )
        return rows[:8]

    def policies(self, vector: list[float], query: str = "") -> list[dict]:
        encoded = "[" + ",".join(str(x) for x in vector) + "]"
        with self.connection() as conn:
            hits = conn.execute(
                """
                SELECT chunk_id,page,section,content,source_hash,
                       embedding <=> %s::vector AS distance
                FROM artefact.policy_chunks
                WHERE model=%s ORDER BY embedding <=> %s::vector LIMIT 4
            """,
                (encoded, self.settings.embedding_model, encoded),
            ).fetchall()
            if not hits:
                return []
            # Recupero as páginas relacionadas para não omitir condições conflitantes.
            pages = {h["page"] for h in hits[:3]}
            if re.search(r"whats|telefone|contato|e-?mail", normalize(query)):
                pages.update((1, 2, 6))
            if 3 in pages:
                pages.add(6)
            if 4 in pages:
                pages.update((5, 7))
            if 7 in pages:
                pages.add(4)
            rows = conn.execute(
                """
                SELECT chunk_id,page,section,content,source_hash FROM artefact.policy_chunks
                WHERE page=ANY(%s) AND model=%s ORDER BY page,chunk_id
            """,
                (sorted(pages), self.settings.embedding_model),
            ).fetchall()
        return [dict(row, source="políticas_da_loja.pdf") for row in rows]
