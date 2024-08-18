import logging
import sqlite3
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import click
from sqlite_utils.db import Table, View


def extract_gravatars(v: Any, file: Path) -> list[str]:
    gravatars = []
    if not v:
        raise KeyError(f"No gravatar identifiers in {file=}")
    if isinstance(v, str):
        gravatars.append(v)
    elif isinstance(v, list):
        gravatars = v
    else:
        raise ValueError(f"Improper gravatars type in {file=}")
    if not gravatars:
        raise ValueError(f"Missing author gravatars in {file=}")
    return gravatars


def check_table(tbl) -> Table:
    """Results in a `sqlite_utils.db.Table` casting."""
    if isinstance(tbl, Table):
        return tbl
    raise ValueError("Must be a valid table.")


def check_view(v) -> View:
    """Results in a `sqlite_utils.db.View` casting."""
    if isinstance(v, View):
        return v
    raise ValueError("Must be a valid view.")


def add_idx(tbl, cols: Iterable):
    """Add an index to the databasebased on a fixed naming convention."""
    if isinstance(tbl, Table):
        tbl.create_index(
            columns=cols,
            index_name=f"idx_{tbl.name.lower()}_{'_'.join(list(cols))}",
            if_not_exists=True,
        )


def run_sql_file(conn: Any, file: Path, prefix_expr: str | None = None):
    if not isinstance(conn, sqlite3.Connection):
        raise Exception("Could not get connection.")
    msg = f"Run {file=}..."
    logging.info(msg)
    click.echo(msg)
    cur = conn.cursor()
    sql = file.read_text()
    if prefix_expr:
        sql = "\n".join((prefix_expr, sql))
    cur.execute(sql)
    conn.commit()


def run_sql_folder(db_name: str, folder: Path, pattern: str = "*.sql"):
    """Assumes that a folder contains `*.sql` files that can be executed against the
    database represented by `db_name`.
    """
    msg = "Run special sql files..."
    logging.info(msg)
    click.echo(msg)

    con = sqlite3.connect(db_name)
    cur = con.cursor()
    recipes = folder.glob(pattern)
    for recipe_file in recipes:
        sub_msg = f"script: {recipe_file=}"
        logging.info(sub_msg)
        click.echo(sub_msg)

        sql = recipe_file.read_text()
        cur.execute(sql)
        con.commit()
    con.close()
