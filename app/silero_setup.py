import subprocess
import pathlib
import torch


def ensure_silero_repo(repo_dir: str, repo_url: str):
    """
    Clone Silero repo if not present.
    """
    repo = pathlib.Path(repo_dir)

    if (repo / "hubconf.py").exists():
        return

    repo.parent.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        ["git", "clone", "--depth", "1", repo_url, repo_dir],
        check=True,
    )


def ensure_silero_model(repo_dir: str, package_url: str):
    """
    Download Silero .pt model if missing.
    """
    filename = package_url.split("/")[-1]
    path = pathlib.Path(repo_dir) / filename

    if not path.exists():
        torch.hub.download_url_to_file(package_url, str(path))
