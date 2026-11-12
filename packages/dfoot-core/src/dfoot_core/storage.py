"""Storage abstraction for the bronze and silver layers.

The rest of the code only talks to the `Storage` interface below, so the same
pipeline runs against the local filesystem (dev, CI) or Cloudflare R2 (prod).
Paths are always relative, "/"-separated keys such as "bronze/events/123.json".
"""

import builtins
from pathlib import Path
from typing import TYPE_CHECKING, Protocol

import boto3
import duckdb
from botocore.exceptions import ClientError

from dfoot_core.settings import Settings

if TYPE_CHECKING:  # type stubs only, not needed at runtime
    from mypy_boto3_s3 import S3Client


class Storage(Protocol):
    """What every storage backend must provide."""

    def write_bytes(self, path: str, data: bytes) -> None: ...

    def read_bytes(self, path: str) -> bytes: ...

    def exists(self, path: str) -> bool: ...

    # `list` as a method name shadows the built-in inside this class body,
    # hence `builtins.list` in the annotation.
    def list(self, prefix: str = "") -> builtins.list[str]: ...

    def uri_for(self, path: str) -> str:
        """A location DuckDB can read directly (local path or r2:// URL)."""
        ...


class LocalStorage:
    """Files under a root directory (LOCAL_DATA_DIR)."""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def _full_path(self, path: str) -> Path:
        full = (self.root / path).resolve()
        # Refuse keys like "../../etc/passwd" that would escape the root.
        if not full.is_relative_to(self.root):
            raise ValueError(f"path escapes the storage root: {path!r}")
        return full

    def write_bytes(self, path: str, data: bytes) -> None:
        full = self._full_path(path)
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_bytes(data)

    def read_bytes(self, path: str) -> bytes:
        return self._full_path(path).read_bytes()

    def exists(self, path: str) -> bool:
        return self._full_path(path).is_file()

    def list(self, prefix: str = "") -> builtins.list[str]:
        keys = (p.relative_to(self.root).as_posix() for p in self.root.rglob("*") if p.is_file())
        return sorted(k for k in keys if k.startswith(prefix))

    def uri_for(self, path: str) -> str:
        return str(self._full_path(path))


class R2Storage:
    """Objects in a Cloudflare R2 bucket, through R2's S3-compatible API."""

    def __init__(self, settings: Settings) -> None:
        # Settings has already checked these are set when the backend is "r2".
        assert settings.r2_bucket and settings.r2_secret_access_key
        self.bucket = settings.r2_bucket
        self._client: S3Client = boto3.client(
            "s3",
            endpoint_url=f"https://{settings.r2_account_id}.r2.cloudflarestorage.com",
            aws_access_key_id=settings.r2_access_key_id,
            aws_secret_access_key=settings.r2_secret_access_key.get_secret_value(),
            region_name="auto",  # R2 has no regions; "auto" is what it expects
        )

    def write_bytes(self, path: str, data: bytes) -> None:
        self._client.put_object(Bucket=self.bucket, Key=path, Body=data)

    def read_bytes(self, path: str) -> bytes:
        return self._client.get_object(Bucket=self.bucket, Key=path)["Body"].read()

    def exists(self, path: str) -> bool:
        try:
            self._client.head_object(Bucket=self.bucket, Key=path)
        except ClientError as error:
            if error.response.get("Error", {}).get("Code") in ("404", "NoSuchKey"):
                return False
            raise
        return True

    def list(self, prefix: str = "") -> builtins.list[str]:
        # list_objects_v2 returns at most 1000 keys per call: the paginator loops for us.
        pages = self._client.get_paginator("list_objects_v2").paginate(
            Bucket=self.bucket, Prefix=prefix
        )
        return sorted(obj["Key"] for page in pages for obj in page.get("Contents", []))

    def uri_for(self, path: str) -> str:
        return f"r2://{self.bucket}/{path}"


def get_storage(settings: Settings | None = None) -> Storage:
    """The backend selected by STORAGE_BACKEND."""
    settings = settings or Settings()
    if settings.storage_backend == "r2":
        return R2Storage(settings)
    return LocalStorage(settings.local_data_dir)


def duckdb_connect(
    database: str = ":memory:", settings: Settings | None = None
) -> duckdb.DuckDBPyConnection:
    """A DuckDB connection able to read the URIs returned by `Storage.uri_for`.

    In R2 mode, loads the httpfs extension and registers an R2 secret so that
    `SELECT * FROM 'r2://bucket/...'` works. The secret is temporary: it lives
    in memory for this connection only and is never written to disk.
    """
    settings = settings or Settings()
    connection = duckdb.connect(database)
    if settings.storage_backend == "r2":
        assert settings.r2_secret_access_key
        connection.install_extension("httpfs")
        connection.load_extension("httpfs")
        # CREATE SECRET doesn't accept bound parameters: quote the values ourselves.
        connection.execute(
            f"""
            CREATE OR REPLACE SECRET dfoot_r2 (
                TYPE r2,
                KEY_ID {_sql_literal(settings.r2_access_key_id or "")},
                SECRET {_sql_literal(settings.r2_secret_access_key.get_secret_value())},
                ACCOUNT_ID {_sql_literal(settings.r2_account_id or "")}
            )
            """
        )
    return connection


def _sql_literal(value: str) -> str:
    """A SQL string literal ('it''s'): single quotes are escaped by doubling them."""
    return "'" + value.replace("'", "''") + "'"
