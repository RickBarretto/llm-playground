import attrs
from transformers import Pipeline, pipeline

from ricklm.models._base import Model

def normalize(response: str) -> str:
    return response.strip().replace("\\n", "\n").replace("\\t", "\t")

class GeneratesText(Model):
    _pipe: Pipeline | None = None

    def __enter__(self):
        return attrs.evolve(self, _pipe=self._pipe)

    def __exit__(self, exc_type, exc_value, traceback):
        self.pipeline.cache_clear()
        object.__setattr__(self, "_pipe", None)

    def text(self, prompt: str) -> str:
        if self._pipe is None:
            raise RuntimeError("Pipeline not initialized. Use 'with' statement to initialize the model.")

        messages = [{"role": "user", "content": prompt},]
        response = self._pipe(messages, max_new_tokens=512, do_sample=True, temperature=0.7)
        return normalize(response[0]["generated_text"][-1]["content"])
