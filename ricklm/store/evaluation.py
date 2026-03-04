import attrs

# Creates :id/:task-model/blind-eval.md
@attrs.frozen(kw_only=True)
class BlindEvaluation:
    id: str
    task: Task
    iterations: int = 3
    judge: str


# Creates :id/:task-model/blind-eval.md
@attrs.frozen(kw_only=True)
class Evaluation:
    id: str
    task: Task
    iterations: int = 3
    judge: str
