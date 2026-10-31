import os

import psycopg
import pytest

from emporio.config import Settings
from emporio.models import Plan
from emporio.provider import Embeddings
from emporio.store import Store

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        os.getenv("ARTEFACT_RUN_INTEGRATION") != "1",
        reason="Defina ARTEFACT_RUN_INTEGRATION=1 para serviços reais.",
    ),
]


def test_live_catalog_obeys_price_stock_and_injection_boundaries():
    store = Store(Settings.load())
    rows = store.products(Plan(route="catalog", category="Violões", max_price=1000))
    assert rows and all(float(p["final_price"]) <= 1000 and p["stock_quantity"] > 0 for p in rows)
    assert store.products(Plan(route="catalog", query="'; DROP TABLE products; --")) == []


@pytest.mark.parametrize("table", ["customers", "orders", "order_items"])
def test_live_reader_cannot_read_individual_data(table):
    store = Store(Settings.load())
    with pytest.raises(psycopg.errors.InsufficientPrivilege):
        with store.connection() as conn:
            conn.execute(f"SELECT * FROM artefact.{table} LIMIT 0")


def test_live_reader_cannot_write_even_with_readonly_disabled():
    s = Settings.load()
    with psycopg.connect(s.database_url, connect_timeout=10) as conn:
        assert not conn.execute(
            "SELECT has_table_privilege(current_user,'artefact.products','INSERT,UPDATE,DELETE')"
        ).fetchone()[0]
        with pytest.raises(psycopg.errors.InsufficientPrivilege):
            conn.execute("UPDATE artefact.products SET stock_quantity=stock_quantity WHERE false")


def test_live_policy_retrieval_recovers_return_page():
    s = Settings.load()
    vectors, _ = Embeddings(s).embed(["Em quantos dias posso devolver uma compra online?"])
    sources = Store(s).policies(vectors[0])
    assert any(p["page"] == 4 and "7 (sete) dias" in p["content"] for p in sources)
