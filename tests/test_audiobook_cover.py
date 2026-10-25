"""Audiobook cover-upload endpoint (`POST /audiobook/cover`).

Calls the handler directly (constructing an UploadFile) rather than through
TestClient(app), so it doesn't import main+torch (which segfaults locally).
"""
from __future__ import annotations

import asyncio
import io
import os

import pytest
from fastapi import HTTPException, UploadFile
from PIL import Image

from api.routers.audiobook import audiobook_cover


def _upload(name: str, data: bytes) -> UploadFile:
    return UploadFile(io.BytesIO(data), filename=name)


def _image_bytes(format: str = "JPEG") -> bytes:
    output = io.BytesIO()
    Image.new("RGB", (8, 8), "blue").save(output, format=format)
    return output.getvalue()


def test_cover_upload_saves(tmp_path, monkeypatch):
    import core.config as cfg
    monkeypatch.setattr(cfg, "OUTPUTS_DIR", str(tmp_path))
    res = asyncio.run(audiobook_cover(_upload("cover.jpg", _image_bytes())))
    assert res["path"].endswith(".jpg")
    assert os.path.isfile(res["path"])
    assert res["path"].startswith(str(tmp_path))
    with Image.open(res["path"]) as saved:
        saved.load()
        assert saved.format == "JPEG"


def test_cover_upload_rejects_invalid_image_with_jpeg_extension(tmp_path, monkeypatch):
    import core.config as cfg
    monkeypatch.setattr(cfg, "OUTPUTS_DIR", str(tmp_path))
    with pytest.raises(HTTPException) as error:
        asyncio.run(audiobook_cover(_upload("cover.jpg", b"not actually an image")))
    assert error.value.status_code == 422
    assert not list(tmp_path.glob("audiobook_covers/*"))


def test_cover_upload_rejects_image_format_mismatch(tmp_path, monkeypatch):
    import core.config as cfg
    monkeypatch.setattr(cfg, "OUTPUTS_DIR", str(tmp_path))
    with pytest.raises(HTTPException) as error:
        asyncio.run(audiobook_cover(_upload("cover.jpg", _image_bytes("PNG"))))
    assert error.value.status_code == 422


def test_cover_upload_rejects_bad_type():
    with pytest.raises(HTTPException) as ei:
        asyncio.run(audiobook_cover(_upload("c.txt", b"hi")))
    assert ei.value.status_code == 400


def test_cover_upload_rejects_oversize(tmp_path, monkeypatch):
    import core.config as cfg
    monkeypatch.setattr(cfg, "OUTPUTS_DIR", str(tmp_path))
    with pytest.raises(HTTPException) as ei:
        asyncio.run(audiobook_cover(_upload("big.png", b"\x89PNG" + b"0" * (8 * 1024 * 1024 + 1))))
    assert ei.value.status_code == 400


def test_cover_upload_rejects_empty(tmp_path, monkeypatch):
    import core.config as cfg
    monkeypatch.setattr(cfg, "OUTPUTS_DIR", str(tmp_path))
    with pytest.raises(HTTPException):
        asyncio.run(audiobook_cover(_upload("empty.jpg", b"")))
