"""#167 — pyannote-audio 3.x passes the removed `use_auth_token` kwarg to
huggingface_hub.hf_hub_download (HF Hub 1.x only accepts `token`), breaking
diarization. Verify the compat shim translates the kwarg and that pyannote
actually binds the wrapped function."""
import pytest

from services.model_manager import _ensure_pyannote_hf_token_compat


def test_shim_translates_use_auth_token_to_token(monkeypatch):
    import huggingface_hub

    seen = {}

    def fake(*args, token=None, **kwargs):
        # Mimic HF Hub 1.x: `use_auth_token` is no longer accepted.
        if "use_auth_token" in kwargs:
            raise TypeError(
                "hf_hub_download() got an unexpected keyword argument 'use_auth_token'"
            )
        seen["token"] = token
        return "downloaded"

    monkeypatch.setattr(huggingface_hub, "hf_hub_download", fake, raising=False)
    monkeypatch.setattr(huggingface_hub, "snapshot_download", fake, raising=False)

    _ensure_pyannote_hf_token_compat()

    # The wrapped fn must translate the dead kwarg instead of raising.
    result = huggingface_hub.hf_hub_download(repo_id="r", filename="f", use_auth_token="secret")
    assert result == "downloaded"
    assert seen["token"] == "secret"


def test_shim_is_idempotent(monkeypatch):
    import huggingface_hub

    def fake(*args, token=None, **kwargs):
        return token

    monkeypatch.setattr(huggingface_hub, "hf_hub_download", fake, raising=False)
    _ensure_pyannote_hf_token_compat()
    once = huggingface_hub.hf_hub_download
    _ensure_pyannote_hf_token_compat()
    twice = huggingface_hub.hf_hub_download
    assert once is twice  # not re-wrapped
    assert getattr(twice, "_ov_uat_shim", False) is True


def test_pyannote_binds_the_shim():
    """The real proof: after the shim, pyannote's own `hf_hub_download`
    reference translates `use_auth_token` rather than raising."""
    _ensure_pyannote_hf_token_compat()
    # importorskip imports the module (or skips) — and since the shim patched
    # huggingface_hub first, pyannote's `from huggingface_hub import
    # hf_hub_download` (pipeline.py:34) binds the wrapped fn. (Also avoids the
    # CodeQL "possibly-uninitialized local" false positive from a try/skip.)
    _pp = pytest.importorskip("pyannote.audio.core.pipeline")
    assert getattr(_pp.hf_hub_download, "_ov_uat_shim", False), (
        "pyannote.audio.core.pipeline.hf_hub_download is not the use_auth_token shim"
    )


def test_pyannote_metadata_works_with_torchaudio_210(tmp_path):
    """pyannote 3.x must import and read metadata after TorchAudio removed info."""
    import numpy as np
    import soundfile as sf

    _ensure_pyannote_hf_token_compat()
    from pyannote.audio.core.io import Audio, get_torchaudio_info
    wav_path = tmp_path / "clip.wav"
    sf.write(wav_path, np.zeros(1600, dtype="float32"), 16000)
    metadata = get_torchaudio_info({"audio": str(wav_path)})
    assert metadata.sample_rate == 16000
    assert metadata.num_frames == 1600
    assert Audio().get_duration(str(wav_path)) == pytest.approx(0.1)
