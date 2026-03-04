import attrs

from ricklm.models.capabilities import GeneratesText

@attrs.frozen(kw_only=True)
class Poem:
    model: GeneratesText = attrs.field(alias="by")
    style: str = attrs.field()
    title: str = attrs.field(default="", alias="titled")
    context: str = attrs.field(default="", alias="knowing")
    examples: list[str] = attrs.field(factory=list, alias="eg")


    def __enter__(self):
        self.model.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.model.__exit__(exc_type, exc_val, exc_tb)

    @property
    def prompt(self) -> str:
        title_part = f' intitulado "{self.title}"' if self.title else ""
        context_part = f" considerando o contexto: {self.context}" if self.context else ""
        examples_part = f" com os seguintes exemplos: {'\n\n---\n\n'.join(self.examples)}" if self.examples else ""
        return f"Escreva um poema original no estilo de {self.style}{title_part}{context_part}{examples_part}."
    
    @property
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
