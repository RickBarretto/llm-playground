from ricklm.features.github.push import push_to_github

from attrs import frozen

@frozen(kw_only=True)
class GitHub:
    repo: str
    token: str
    username: str
    email: str
    branch: str = "main"

    def push(self, message: str) -> None:
        push_to_github(
            repo=self.repo,
            branch=self.branch,
            message=message,
            root=Path("."),
        )
