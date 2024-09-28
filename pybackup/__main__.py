from typing import List
from .BackupPath import BackupPath
from pathlib import Path
import typer


app = typer.Typer()


@app.command()
def backupAll(
    backup_destination: Path = Path("~/pybackup/"), dryrun: bool = False
) -> None:
    """
    Add your files and directories to pybackup/__main__.py to start.
    """
    paths: List[BackupPath] = [
        BackupPath(
            Path(path).expanduser(),
            backup_destination.expanduser(),
            dryrun,
        )
        # Set your paths that you want to back up below as shown
        for path in [
            # "~/Documents",
            # "~/Pictures",
        ]
    ]

    for path in paths:
        typer.echo(path)

    typer.echo("Starting backups...")
    for path in paths:
        path.new_backup()
    typer.echo("Finished all backups.")


if __name__ == "__main__":
    app()
