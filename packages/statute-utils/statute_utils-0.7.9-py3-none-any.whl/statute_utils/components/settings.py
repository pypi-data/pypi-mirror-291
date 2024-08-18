from pathlib import Path
from urllib.parse import ParseResult

import click
from environs import Env
from sqlite_utils import Database

env = Env()
env.read_env()

SOURCE: ParseResult = env.url("SOURCE", "https://lawsql.com")
""" Where to source the tree files"""

CODE_DIR: Path = env.path("CODE_DIR", "../corpus-codifications")
""" Where to store and source codification *.yml files locally """

STAT_DIR: Path = env.path("STAT_DIR", "../corpus-statutes")
""" Where to store and source statute *.yml files locally """

CASE_DIR: Path = env.path("CASE_DIR", "../corpus-decisions")
""" Where to store and source decision / opinion *.md files locally """

DB_FILE: str = env("DB_FILE", "/data/main.db")
""" Where to store the main database """

TREE_GLOB: str = env("TREE_GLOB", "**/*/*.yml")
""" Pattern to use to detect both codification and statute *.yml files
within `CODE_DIR` and `STAT_DIR`, respectively"""

CASE_GLOB: str = env("CASE_GLOB", "*/*/*/*.md")
""" Pattern to use to detect the ponencia *.md file within `CASE_DIR`."""


@click.group()
def cli():
    """Extensible wrapper of commands starting from statute-utils."""
    pass


@cli.command()
@click.option("--db-name", type=str, default=DB_FILE, help="Filename of db")
def source(db_name: str) -> Database:
    """Prepare existing db path by first deleting it creating a new one in WAL-mode.

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
