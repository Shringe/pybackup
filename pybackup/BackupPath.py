from pathlib import Path
from datetime import date
from typing import Tuple, List
import typer
import shutil


class BackupPath:
    def __init__(self, src: Path, backup_dir: Path, dryrun: bool = False) -> None:
        """Contains source and destination paths with backup functionality"""
        self.src: Path = src
        self.dest: Path = backup_dir / src.name
        self.backup_dir: Path = backup_dir
        self.dryrun: bool = dryrun

        self.format_char: str = "__"

    def __repr__(self) -> str:
        return f"""
                Source: {self.src}, exists={self.src.exists()}
                Destination: {self.dest}, exists={self.dest.exists()}
                """

    def new_backup(self, maximum_attempts: int = 50) -> bool:
        """Creates new backup. Returns True if succesful."""
        all_passed, all_exists, enough_space = self.verify_paths(not self.dryrun)
        typer.echo(f"self.verify_paths: {all_passed=}, {all_exists=}, {enough_space=}")
        if not all_passed:
            return False

        backup_attempt: int = -1
        while backup_attempt < maximum_attempts:
            backup_attempt += 1

            current_attempt: Path = self.construct_backup_path(backup_attempt)
            if current_attempt.exists():
                continue

            typer.echo(f"Copying {self.src} to {current_attempt}...")
            if not self.dryrun:
                shutil.copytree(self.src, current_attempt, symlinks=True)
            typer.echo(f"Finished copying to {current_attempt}")

            return True
        else:
            raise Exception(f"Ran in to {maximum_attempts=} limit. Exiting script.")
            exit(1)
            return False

    def verify_paths(self, raise_error: bool = True) -> Tuple[bool, bool, bool]:
        """Verifies backup source and location for a new backup."""
        all_exists: bool = BackupPath.verify_paths_exist(self.src, self.backup_dir)
        if not all_exists and raise_error:
            raise FileNotFoundError("Source or destination not found.")

        enough_space: bool = BackupPath.verify_space_for_copy(self.src, self.backup_dir)
        if not enough_space and raise_error:
            raise Exception("Insufficient disk space to create a new backup.")

        all_passed: bool = all_exists and enough_space
        return (all_passed, all_exists, enough_space)

    def construct_backup_path(self, number: int) -> Path:
        """Creates path for new backup with it's number. E.X.: Documents/Documents__2__2024-09-27"""
        return self.dest / (
            self.dest.name
            + self.format_char
            + str(number)
            + self.format_char
            + str(date.today())
        )

    def deconstruct_backup_name(self, number: int) -> Tuple[str, str]:
        """Takes a backup number and returns its name, and date taken."""
        backup_name: Path = self.construct_backup_path(number)
        if not backup_name.exists():
            raise FileNotFoundError("Backup instance doesn't exist.")

        info: List[str] = backup_name.name.split(self.format_char)
        if len(info) != 3:
            raise Exception(
                f"Avoid usind '{self.format_char}' charator in backup names. "
            )

        name: str = info[0]
        date: str = info[2]

        return name, date

    @staticmethod
    def verify_paths_exist(*paths: Path) -> bool:
        """Returns True if all paths found."""
        for path in paths:
            if not path.exists():
                return False
        return True

    @staticmethod
    def verify_space_for_copy(src: Path, dest: Path) -> bool:
        return BackupPath.get_directory_size(src) < shutil.disk_usage(dest)[2]

    @staticmethod
    def get_directory_size(path: Path) -> int:
        """Calculate the total size of the directory in bytes."""
        total_size: int = 0
        for item in path.glob("**/*"):
            if item.is_file():
                total_size += item.stat().st_size
        return total_size
