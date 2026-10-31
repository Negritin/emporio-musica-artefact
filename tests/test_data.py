import csv
import shutil

import pytest

from emporio.config import ROOT
from emporio.ingest import extract_chunks, load_sources


def test_public_sources_load_without_private_files():
    data, report = load_sources(ROOT / "Arquivos")
    assert len(data["products"]) == 65
    assert len(data["categories"]) == 9
    assert len(data["promotions"]) == 25
    assert report["issues"] == []


@pytest.mark.parametrize("problem", ["duplicate", "foreign_key", "invalid_bool", "invalid_number"])
def test_invalid_source_rejected_before_database(tmp_path, problem):
    for name in ("categories", "products", "promotions"):
        original = next((ROOT / "Arquivos").glob(f"* - {name}.csv"))
        shutil.copy(original, tmp_path)
    name = "promotions" if problem == "invalid_bool" else "products"
    path = next(tmp_path.glob(f"* - {name}.csv"))
    with path.open() as stream:
        rows = list(csv.DictReader(stream))
    if problem == "duplicate":
        rows.append(rows[0])
    elif problem == "foreign_key":
        rows[0]["category_id"] = "999999"
    elif problem == "invalid_bool":
        rows[0]["is_active"] = "sim"
    else:
        rows[0]["price_brl"] = "NaN"
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with pytest.raises(ValueError):
        load_sources(tmp_path)


def test_manual_chunks_preserve_pages_and_conflicting_rules():
    chunks = extract_chunks(ROOT / "Arquivos/políticas_da_loja.pdf")
    assert {c["page"] for c in chunks} == set(range(1, 9))
    page3 = " ".join(c["content"] for c in chunks if c["page"] == 3)
    assert "12x" in page3 and "80,00" in page3 and "100,00" in page3
    assert len({c["chunk_id"] for c in chunks}) == len(chunks)
    assert len({c["source_hash"] for c in chunks}) == 1
