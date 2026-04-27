from pathlib import Path

from ricklm.features.github.push import push_to_github

from attrs import frozen

__all__ = ["GitHub", 'Path']

cwd = None

def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=cwd,
        check=True, capture_output=True, text=True,
    )

def acess_token(token: str, repo: str) -> str:
    remote = f"https://x-access-token:{token}@github.com/{repo}.git"
    return remote

def is_git_repo(path: Path) -> bool:
    return (path / ".git").exists()

def config_git_identity(path: Path, name: str, email: str) -> None:
    git("config", "user.email", email)
    git("config", "user.name", name)

def is_staged(path: Path) -> bool:
    diff = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=path, capture_output=True,
    )
    return diff.returncode == 0

def commit_and_push(path: Path, remote: str, branch: str, message: str) -> None:
    git("remote", "set-url", "origin", remote)
    git("add", "poems/")
    git("add", "evaluations/")

    if is_staged(path):
        print("No new evaluation files to commit.")
        return

    git("commit", "-m", message)
    git("push", "origin", branch)
    print(f"Pushed generated poems to {remote} ({branch})")

@frozen(kw_only=True)
class GitHub:
    repo: str
    token: str
    username: str
    email: str
    root: Path = Path(".")
    branch: str = "main"

    def push(self, message: str) -> None:
        global cwd
        cwd = str(self.root)
        remote = acess_token(self.token, self.repo)

        if not is_git_repo(self.root):
            raise RuntimeError(
                f"{self.root} is not a git repository. "
                "Make sure the repo was cloned first."
            )

        config_git_identity(self.root, self.username, self.email)
        commit_and_push(self.root, remote, self.branch, message)

