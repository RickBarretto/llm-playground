from models._base import Model

class GeneratesText(Model):

    def text(self, prompt: str) -> str:
        pipe = self.pipeline("text-generation")
        messages = [{"role": "user", "content": prompt},]
        return pipe(messages, max_new_tokens=512, do_sample=True, temperature=0.7)
