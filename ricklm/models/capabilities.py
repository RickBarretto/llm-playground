from ricklm.models._base import Model

def normalize(response: str) -> str:
    return response.strip().replace("\\n", "\n").replace("\\t", "\t")

class GeneratesText(Model):

    def text(self, prompt: str) -> str:
        pipe = self.pipeline("text-generation")
        messages = [{"role": "user", "content": prompt},]
        response = pipe(messages, max_new_tokens=512, do_sample=True, temperature=0.7)
        self.pipeline.cache_clear()
        return normalize(response[0]["generated_text"][-1]["content"])
