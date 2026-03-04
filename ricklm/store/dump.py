import attrs

# Creates :id/:task-model/output.md
@attrs.frozen(kw_only=True)
class Output:
    id: str
    task: Task
    iterations: int = 3
