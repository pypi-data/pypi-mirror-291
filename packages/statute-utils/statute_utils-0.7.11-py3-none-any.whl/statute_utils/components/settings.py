from pathlib import Path
from urllib.parse import ParseResult

import click
from environs import Env
from sqlite_utils.db import Database, Table

from .db import add_idx, check_table

env = Env()
env.read_env()

### MAIN

DATA_DIR: str = env("DATA_DIR", "data")
""" Where to store main / temp databases. """

DB_FILE: str = env("DB_FILE", "data/main.db")
""" Where to store the main database """

SOURCE: ParseResult = env.url("SOURCE", "https://lawsql.com")
""" Where to source the tree files"""

### TREES

CODE_DIR: Path = env.path("CODE_DIR", "../corpus-codifications")
""" Where to store and source codification *.yml files locally """

STAT_DIR: Path = env.path("STAT_DIR", "../corpus-statutes")
""" Where to store and source statute *.yml files locally """

STAT_TMP: str = f"{DATA_DIR}/stats.db"
""" Interim statutes database for fast querying."""

TREE_GLOB: str = env("TREE_GLOB", "**/*/*.yml")
""" Pattern to use to detect both codification and statute *.yml files
within `CODE_DIR` and `STAT_DIR`, respectively"""


def set_mini_statute_files_table(
    base_path: Path = STAT_DIR,
    base_pattern: str = TREE_GLOB,
    db_name: str = STAT_TMP,
) -> Table:
    """Quickly lists statutes found in directory without populating content."""
    Path(DATA_DIR).mkdir(exist_ok=True)
    Path(db_name).unlink(missing_ok=True)

    db = Database(db_name, use_counts_table=True)
    if not db["statutes"].exists():
        rows = []
        for item in base_path.glob(base_pattern):
            cat, num, date, variant = item.parts[-4:]
            v = variant.split(".")[0]
            rows.append(
                {
                    "id": "-".join([cat, num, date, v]),
                    "cat": cat,
                    "num": num,
                    "date": date,
                    "variant": v,
                    "size": item.stat().st_size,
                }
            )
        db["statutes"].insert_all(rows, pk="id", ignore=True)  # type: ignore
        for idx in (
            {"size"},
            {"date"},
            {"cat", "num"},
            {"cat", "num", "date"},
            {"cat", "num", "date", "variant"},
        ):
            add_idx(db["statutes"], idx)
    return check_table(db["statutes"])


### DECISIONS

CASE_DIR: Path = env.path("CASE_DIR", "../corpus-decisions")
""" Where to store and source decision / opinion *.md files locally """

CASE_GLOB: str = env("CASE_GLOB", "*/*/*/*.md")
""" Pattern to use to detect the ponencia *.md file within `CASE_DIR`."""

CASE_TMP: str = f"{DATA_DIR}/cases.db"
""" Interim decisions database for fast querying."""


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
