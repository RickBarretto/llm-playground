from transformers import Pipeline, pipeline

from ricklm.models._base import Model

def normalize(response: str) -> str:
    return response.strip().replace("\\n", "\n").replace("\\t", "\t")

class GeneratesText(Model):
    _pipe: Pipeline | None = None

    def __enter__(self):
        self._pipe = self.pipeline("text-generation")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.pipeline.cache_clear()
        self._pipe = None

    def text(self, prompt: str) -> str:
        if self._pipe is None:
            self._pipe = self.pipeline("text-generation")

        messages = [{"role": "user", "content": prompt},]
        response = self._pipe(messages, max_new_tokens=512, do_sample=True, temperature=0.7)
        return normalize(response[0]["generated_text"][-1]["content"])
