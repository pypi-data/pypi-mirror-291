from pathlib import Path

import click
from sqlite_utils import Database

from .config import DB_FILE, STAT_DIR, STAT_TMP, set_mini_statute_files_table


@click.group()
def cli():
    """Extensible wrapper of commands."""
    pass


@cli.command()
@click.option("--db-name", type=str, default=DB_FILE, help="Filename of db")
def source(db_name: str) -> Database:
    """Prepare existing statute db path by first deleting it creating
    a new one in WAL-mode.

    Args:
        db_name (str): e.g. "x.db", or "data/main.db"

    Returns:
        Database: The configured database object.
    """
    Path("data").mkdir(exist_ok=True)

    if not db_name.endswith((".sqlite", ".db")):
        raise ValueError("Expects either an *.sqlite, *.db suffix")

    _db_file = Path(db_name)
    _db_file.unlink(missing_ok=True)

    db = Database(filename_or_conn=_db_file, use_counts_table=True)
    db.enable_wal()
    return db


@cli.command()
@click.option(
    "--folder",
    type=Path,
    default=STAT_DIR,
    required=True,
    help="Location of raw files to create database",
)
@click.option(
    "--target",
    type=str,
    default=STAT_TMP,
    required=True,
    help="Location of raw files to create database",
)
def interim_db(folder: Path, target: str):
    """Fast-creation of interim statute files db based on `STAT_DIR`

    Args:
        folder (Path): Origin of statute files
        target (Path): Where to save db.
            Defaults to STAT_TMP.
    """
    set_mini_statute_files_table(base_path=folder, db_name=target)


if __name__ == "__main__":
    cli()  # search @cli.command
