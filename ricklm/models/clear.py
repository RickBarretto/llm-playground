
import contextlib
import gc
from pathlib import Path
import shutil


def release_gpu():
    """Free GPU/CPU memory used by the current pipeline."""
    gc.collect()
    with contextlib.suppress(ImportError):
        import torch

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

def clear_storage(model_id: str) -> None:
    """Remove the local cache for a Hugging Face model to save disk space (e.g., on Colab)."""
    from huggingface_hub.constants import HF_HOME

    owner, name = model_id.split("/", 1)
    cache_dir = Path(HF_HOME) / "hub" / f"models--{owner}--{name}"
    if cache_dir.exists():
        shutil.rmtree(cache_dir, ignore_errors=True)
