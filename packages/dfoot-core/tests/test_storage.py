"""Tests for the local backend only: no test may ever call R2."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from dfoot_core.settings import Settings
from dfoot_core.storage import LocalStorage, duckdb_connect, get_storage


@pytest.fixture(autouse=True)
def isolated_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Ignore any real .env file or R2 variables present on the developer's machine."""
    monkeypatch.chdir(tmp_path)  # Settings reads .env from the working directory
    for name in Settings.model_fields:
        monkeypatch.delenv(name.upper(), raising=False)


@pytest.fixture
def storage(tmp_path: Path) -> LocalStorage:
    return LocalStorage(tmp_path)


def test_write_then_read_roundtrip(storage: LocalStorage) -> None:
    storage.write_bytes("bronze/events/1.json", b'{"id": 1}')
    assert storage.read_bytes("bronze/events/1.json") == b'{"id": 1}'


def test_exists(storage: LocalStorage) -> None:
    assert not storage.exists("bronze/a.json")
    storage.write_bytes("bronze/a.json", b"")
    assert storage.exists("bronze/a.json")
    assert not storage.exists("bronze")  # a directory is not an object


def test_list_filters_by_prefix_and_sorts(storage: LocalStorage) -> None:
    for key in ("silver/x.parquet", "bronze/b.json", "bronze/a.json"):
        storage.write_bytes(key, b"")
    assert storage.list("bronze/") == ["bronze/a.json", "bronze/b.json"]
    assert storage.list() == ["bronze/a.json", "bronze/b.json", "silver/x.parquet"]


def test_uri_for_is_an_absolute_local_path(storage: LocalStorage, tmp_path: Path) -> None:
    assert storage.uri_for("silver/x.parquet") == str(tmp_path.resolve() / "silver/x.parquet")


def test_paths_cannot_escape_the_root(storage: LocalStorage) -> None:
    with pytest.raises(ValueError, match="escapes"):
        storage.write_bytes("../outside.txt", b"")


def test_get_storage_returns_local_backend(tmp_path: Path) -> None:
    settings = Settings(storage_backend="local", local_data_dir=tmp_path)
    assert isinstance(get_storage(settings), LocalStorage)


def test_r2_backend_requires_credentials() -> None:
    # Validation happens before any client is created: nothing reaches the network.
    with pytest.raises(ValidationError, match="R2_BUCKET"):
        Settings(storage_backend="r2", r2_account_id="x", r2_access_key_id="x")


def test_duckdb_reads_a_uri_from_local_storage(storage: LocalStorage) -> None:
    storage.write_bytes("silver/numbers.csv", b"n\n1\n2\n")
    connection = duckdb_connect(settings=Settings(storage_backend="local"))
    total = connection.execute(
        "SELECT sum(n) FROM read_csv(?)", [storage.uri_for("silver/numbers.csv")]
    ).fetchone()
    assert total == (3,)
