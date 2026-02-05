from ricklm.models._base import Model

class GeneratesText(Model):

    def text(self, prompt: str) -> str:
        pipe = self.pipeline("text-generation")
        messages = [{"role": "user", "content": prompt},]
        response = pipe(messages, max_new_tokens=512, do_sample=True, temperature=0.7)
        return response[0]["generated_text"][-1]["content"]
