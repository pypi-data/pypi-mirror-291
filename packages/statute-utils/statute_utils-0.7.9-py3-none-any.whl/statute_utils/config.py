from pathlib import Path

import click
from sqlite_utils import Database

from .components import STAT_DIR, cli


def setup_local_statute_db(
    basepath: Path, db_name: str = "data/statute_files.db"
) -> Database:
    """Create an sqlite database which lists statutes found in a given directory,
    e.g. ../corpus-statutes"""
    Path(db_name).unlink(missing_ok=True)
    Path("data").mkdir(exist_ok=True)
    db = Database(db_name, use_counts_table=True)
    if not db["statutes"].exists():
        rows = []
        for item in basepath.glob("**/[0-9].yml"):
            cat, num, date, variant = item.parts[-4:]
            v = variant.split(".")[0]
            rows.append(
                {
                    "id": "-".join([cat, num, date, v]),
                    "cat": cat,
                    "num": num,
                    "date": date,
                    "variant": variant.split(".")[0],
                    "size": item.stat().st_size,
                }
            )
        db["statutes"].insert_all(rows, pk="id", ignore=True)  # type: ignore
        db["statutes"].create_index(  # type: ignore
            columns={"cat", "num"},
            index_name="idx_statutes_cat_num",
            if_not_exists=True,
        )
        db["statutes"].create_index(  # type: ignore
            columns={"cat", "num", "date"},
            index_name="idx_statutes_cat_num_date",
            if_not_exists=True,
        )
    return db


def get_local_statute_db():
    db = Database("statute_files.db")
    if db["statutes"].exists():
        return db
    return None


@cli.command()
@click.option(
    "--folder",
    type=Path,
    default=STAT_DIR,
    required=True,
    help="Location of raw files to create database",
)
def interim_db(folder: Path, target: str = "data/statute_files.db"):
    """Fast-creation of interim statute files db based on `STAT_DIR`

    Args:
        folder (str): Origin of statute files
        target (str, optional): Where to save db.
            Defaults to "data/statute_files.db".
    """
    setup_local_statute_db(folder, target)
