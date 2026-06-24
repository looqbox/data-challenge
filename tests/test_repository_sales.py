import pytest
import pandas as pd
from src.models.repositories.sales_repository import SalesRepository


@pytest.fixture(scope="module")
def repo():
    return SalesRepository()


# ── sem filtros ─────────────────────────────────────────────────────────────

def test_sem_filtros_retorna_dataframe(repo):
    result = repo.read_db(product_code=None, store_code=None, data_range=None)
    print("\n=== sem filtros ===")
    print(result.head(5))
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0
    assert list(result.columns) == ["STORE_CODE", "PRODUCT_CODE", "DATE", "SALES_VALUE", "SALES_QTY"]


# ── filtro só por produto ────────────────────────────────────────────────────

def test_so_product_code(repo):
    result = repo.read_db(product_code=18, store_code=None, data_range=None)
    print("\n=== só product_code=18 ===")
    print(result.head(5))
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0
    assert result["PRODUCT_CODE"].unique().tolist() == [18]


# ── filtro só por loja ───────────────────────────────────────────────────────

def test_so_store_code(repo):
    result = repo.read_db(product_code=None, store_code=1, data_range=None)
    print("\n=== só store_code=1 ===")
    print(result.head(5))
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0
    assert result["STORE_CODE"].unique().tolist() == [1]


# ── filtro só por data — início e fim ───────────────────────────────────────

def test_data_inicio_e_fim(repo):
    result = repo.read_db(product_code=None, store_code=None, data_range=["2019-01-01", "2019-01-31"])
    print("\n=== data início e fim ===")
    print(result.head(5))
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0
    assert result["DATE"].min() >= "2019-01-01"
    assert result["DATE"].max() <= "2019-01-31"


# ── filtro só por data — só início ──────────────────────────────────────────

def test_data_so_inicio(repo):
    result = repo.read_db(product_code=None, store_code=None, data_range=["2019-06-01", None])
    print("\n=== só data início ===")
    print(result.head(5))
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0
    assert result["DATE"].min() >= "2019-06-01"


# ── filtro só por data — só fim ─────────────────────────────────────────────

def test_data_so_fim(repo):
    result = repo.read_db(product_code=None, store_code=None, data_range=[None, "2019-03-31"])
    print("\n=== só data fim ===")
    print(result.head(5))
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0
    assert result["DATE"].max() <= "2019-03-31"


# ── combinações ─────────────────────────────────────────────────────────────

def test_produto_e_loja(repo):
    result = repo.read_db(product_code=18, store_code=1, data_range=None)
    print("\n=== produto + loja ===")
    print(result.head(5))
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0
    assert result["PRODUCT_CODE"].unique().tolist() == [18]
    assert result["STORE_CODE"].unique().tolist() == [1]


def test_produto_e_data(repo):
    result = repo.read_db(product_code=18, store_code=None, data_range=["2019-01-01", "2019-01-31"])
    print("\n=== produto + data ===")
    print(result.head(5))
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0
    assert result["PRODUCT_CODE"].unique().tolist() == [18]
    assert result["DATE"].min() >= "2019-01-01"
    assert result["DATE"].max() <= "2019-01-31"


def test_loja_e_data(repo):
    result = repo.read_db(product_code=None, store_code=1, data_range=["2019-01-01", "2019-01-31"])
    print("\n=== loja + data ===")
    print(result.head(5))
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0
    assert result["STORE_CODE"].unique().tolist() == [1]
    assert result["DATE"].min() >= "2019-01-01"
    assert result["DATE"].max() <= "2019-01-31"


def test_todos_os_filtros(repo):
    result = repo.read_db(product_code=18, store_code=1, data_range=["2019-01-01", "2019-01-31"])
    print("\n=== todos os filtros ===")
    print(result.head(5))
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0
    assert result["PRODUCT_CODE"].unique().tolist() == [18]
    assert result["STORE_CODE"].unique().tolist() == [1]
    assert result["DATE"].min() >= "2019-01-01"
    assert result["DATE"].max() <= "2019-01-31"