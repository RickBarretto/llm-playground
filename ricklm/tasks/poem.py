import attrs

from ricklm.models.capabilities import GeneratesText

@attrs.frozen(kw_only=True)
class Poem:
    model: GeneratesText = attrs.field(alias="by")
    style: str = attrs.field()
    title: str = attrs.field(default="", alias="titled")

    @property
    def prompt(self) -> str:
        title_part = f' intitulado "{self.title}"' if self.title else ""
        return f"Escreva um poema no estilo de {self.style}{title_part}."
    
    def full(self) -> str:
        return "\n".join([
            "Model",
            str(self.model),
            "Prompt:", 
            self.prompt,
            "",
            "Poema:",
            self.model.text(self.prompt)
        ])
    
    def __str__(self) -> str:
        return self.model.text(self.prompt)
