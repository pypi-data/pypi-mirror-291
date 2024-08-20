from pathlib import Path
import subprocess


def add_path_to_shell(path: Path):
    try:
        subprocess.run(["fish_add_path", path], capture_output=True)
        return True
    except FileNotFoundError:
        pass

    if Path.home() / ".bash_profile":
        subprocess.run(
            [
                "echo",
                f"'export PATH={path}:$PATH'",
                ">>",
                "~/.bash_profile",
            ],
            capture_output=True,
        )
    elif Path.home() / ".bashrc":
        subprocess.run(
            [
                "echo",
                f"'export PATH={path}:$PATH'",
                ">>",
                "~/.bashrc",
            ],
            capture_output=True,
        )
    elif Path.home() / ".zshrc":
        subprocess.run(
            [
                "echo",
                f"'export PATH={path}:$PATH'",
                ">>",
                "~/.zshrc",
            ],
            capture_output=True,
        )
    elif Path.home() / ".profile":
        subprocess.run(
            [
                "echo",
                f"'export PATH={path}:$PATH'",
                ">>",
                "~/.profile",
            ],
            capture_output=True,
        )
    elif Path.home() / ".bash_login":
        subprocess.run(
            [
                "echo",
                f"'export PATH={path}:$PATH'",
                ">>",
                "~/.bash_login",
            ],
            capture_output=True,
        )
    else:
        raise Exception(f"Failed to add {path} to PATH")
