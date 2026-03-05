from pathlib import Path

from ricklm.features.github.push import push_to_github

from attrs import frozen

__all__ = ["GitHub", 'Path']

@frozen(kw_only=True)
class GitHub:
    repo: str
    token: str
    username: str
    email: str
    root: Path = Path(".")
    branch: str = "main"

    def push(self, message: str) -> None:
        push_to_github(
            token=self.token,
            name=self.username,
            email=self.email,
            repo=self.repo,
            branch=self.branch,
            message=message,
            root=self.root,
        )
