import attrs

from src.models.capabilities import GeneratesText

@attrs.frozen(kw_only=True)
class Poem:
    model: GeneratesText = attrs.field(alias="by")
    style: str = attrs.field()
    title: str = attrs.field(default="", alias="titled")
    
    def __str__(self) -> str:
        title_part = f' intitulado "{self.title}"' if self.title else ""
        prompt = f"Escreva um poema no estilo de {self.style}{title_part}."
        return self.model.text(prompt)
