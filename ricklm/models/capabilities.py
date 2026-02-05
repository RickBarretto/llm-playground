from transformers import pipeline

from ricklm.models._base import Model

def normalize(response: str) -> str:
    return response.strip().replace("\\n", "\n").replace("\\t", "\t")

class GeneratesText(Model):
    _pipe: pipeline | None = None

    def __enter__(self):
        self._pipe = pipeline("text-generation")
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._pipe.cache_clear()

    def text(self, prompt: str) -> str:
        messages = [{"role": "user", "content": prompt},]
        response = self._pipe(messages, max_new_tokens=512, do_sample=True, temperature=0.7)
        return normalize(response[0]["generated_text"][-1]["content"])
