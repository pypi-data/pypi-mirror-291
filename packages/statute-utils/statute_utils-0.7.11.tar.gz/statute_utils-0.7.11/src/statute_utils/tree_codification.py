import datetime
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import click
from rich.progress import Progress
from sqlite_utils.db import Database, Table, View

from .components import (
    CODE_DIR,
    DB_FILE,
    TREE_GLOB,
    add_idx,
    check_table,
    check_view,
    cli,
    extract_gravatars,
    fetch_values_from_key,
    run_sql_file,
)
from .tree import TreeBase, TreeContent, TreePath


@dataclass(frozen=True)
class Codification(TreeBase):
    """A codification is a refined [Statute][statutes] interconnecting them together. It is human-curated, hence
    containing a supplied `title`, `description`, and list of `gravatar profile ids`.

    ## Files

    Requires specifically formatted codification Path.

    Files would need to be downloaded from the [repo](https://github.com/justmars/corpus-codifications)
    and passed through [from_file][statute_utils.tree.TreeBase.from_file] to generate the instance.

    ## Tables

    The instance generates [@metadata][statute_utils.tree_codification.Codification.metadata] and [@content][statute_utils.tree_codification.Codification.content],
    to populate tables:

    1. `codifications`,
    2. `codification_units`,
    3. `codification_authors`, and
    4. `codification_statutes`
    """  # noqa: E501

    title: str
    description: str
    gravatars: list[str]

    ###
    ### AUTHOR ROWS
    ###

    @classmethod
    def set_author_table_name(cls) -> str:
        return "codification_authors"

    @property
    def author_records(self):
        """Codifications can be authored by multiple individuals represented by their
        public gravatar profile."""
        return (
            {"codification_id": self.id, "author_id": author}
            for author in self.gravatars
        )

    def add_authors(self, db: Database):
        tbl_name = self.__class__.set_author_table_name()
        try:
            db[tbl_name].insert_all(  # type: ignore
                records=self.author_records,
                hash_id="id",  # type: ignore
                ignore=True,  # type: ignore
            )
        except Exception as e:
            raise ValueError(f"Bad {tbl_name}; {e=}")

    ###
    ### STATUTE INCLUSIONS
    ###

    @classmethod
    def set_composition_table_name(cls) -> str:
        """See in relation to [add_composition_rows][statute_utils.tree_codification.Codification.add_composition_rows]."""  # noqa: E501
        return "codification_statutes"

    def extract_events(self) -> Iterator[dict]:
        """Each unit may contain a history of events. To ensure that strings do not
        contain miscellaneous content, this runs a check on each event key prior to
        yielding the event.
        """
        data = {"units": self.units}
        histories = fetch_values_from_key(data=data, key="history")
        for event_list in histories:
            for event in event_list:
                for key, value in event.items():
                    if isinstance(value, str):
                        event[key] = value.strip()
                yield event

    def add_composition_rows(self, db: Database):
        """See in relation to [create_composition_table][statute_utils.tree_codification.Codification.create_composition_table]."""  # noqa: E501
        tbl_name = self.__class__.set_composition_table_name()
        events = self.extract_events()
        included_statutes = {evt["statute"] for evt in events if evt.get("statute")}
        db[tbl_name].insert_all(  # type: ignore
            records=(
                (
                    {"codification_id": self.id} | statute_row
                    for text in included_statutes
                    for statute_row in db["statute_titles"].rows_where(
                        where="text = ?",
                        where_args=(text,),
                        select="statute_id",
                    )
                )
            ),
            pk="id",  # type: ignore
        )

    @classmethod
    def create_composition_table(cls, db: Database) -> Table:
        """Each [Codification][codifications] consists of various [Statutes][statutes]."""  # noqa: E501
        tbl_name = cls.set_composition_table_name()
        fk = cls.set_common_root_pk()
        db[tbl_name].create(  # type: ignore
            columns={"id": int, fk: str, "statute_id": str},
            pk="id",
            foreign_keys=[
                (fk, cls.set_root_table_name(), "id"),
                ("statute_id", "statutes", "id"),
            ],
            not_null={fk, "statute_id"},
            if_not_exists=True,
        )

        for idx in ({fk, "statute_id"},):
            add_idx(db[tbl_name], idx)

        return check_table(db[tbl_name])

    @classmethod
    def create_statutes_affecting_codifications_view(cls, db: Database) -> View:
        """A more detailed view of the created reference table."""  # noqa: E501
        _view = "view_statutes_affecting_codifications"
        db[_view].drop(ignore=True)
        run_sql_file(
            conn=db.conn,
            file=Path(__file__).parent / "sql" / (_view + ".sql"),
            prefix_expr=f"create view {_view} as",
        )
        return check_view(db[_view])

    ###
    ### LOCAL TO DB
    ###

    @property
    def metadata(self) -> dict[str, Any]:
        """Root-based metadata."""
        return self.base | {
            "title": self.title.strip(),
            "description": self.description.strip(),
        }

    @property
    def content(self) -> TreeContent:
        """Unit-based column data."""
        return self.set_content()

    def to_row(self, db: Database):
        row = self.metadata | self.content._asdict()
        fts = row.pop("fts")
        starters = ("const-1987", "civil", "penal", "labor", "civpro")
        for starter in starters:
            if starter in row["id"]:
                row["is_starter"] = True

        self.add_root(db, record=row)
        self.add_units(db, records=fts)
        self.add_authors(db)
        self.add_composition_rows(db)

    @classmethod
    def from_file(cls, file: Path):
        treepath = TreePath.unpack(file)
        data = TreePath.load(file)
        rule = treepath.as_rule
        date = treepath.date
        id = file.stem
        gravatars = extract_gravatars(v=data["gravatars"], file=file)
        return cls(
            id=id,
            title=data["title"],
            description=data["description"],
            date=date,
            rule=rule,
            units=data["units"],
            gravatars=gravatars,
            size=file.stat().st_size,
        )

    @classmethod
    def create_root_table(cls, db: Database) -> Table:
        tbl_name = cls.set_root_table_name()

        db[tbl_name].create(  # type: ignore
            columns={
                "id": str,
                "cat": str,
                "num": str,
                "title": str,
                "description": str,
                "date": datetime.date,
                "units": str,
                "html": str,
                "size": int,
                "is_starter": bool,  # used to signify free use in client
            },
            pk="id",
            not_null={
                "cat",
                "num",
                "title",
                "description",
                "date",
                "units",
                "size",
                "html",
            },
            defaults={"is_starter": False},
            if_not_exists=True,
        )

        for idx in (
            {"size"},
            {"date"},
            {"cat", "num"},
            {"cat", "num", "date"},
            {"is_starter"},
        ):
            add_idx(db[tbl_name], idx)

        return check_table(db[tbl_name])

    @classmethod
    def source(cls, db_name: str, folder: str, pattern: str):
        db = Database(filename_or_conn=db_name, use_counts_table=True)
        if not db["statutes"].exists():
            raise NotImplementedError("statutes table needs to exist first.")
        # initialize related db-tables before adding files from folder
        root_tbl, units_tbl = cls.create_base_tables(db)
        _ = cls.create_composition_table(db)
        cls.from_folder_to_db(
            db=db,
            folder=folder,
            pattern=pattern,
        )
        with Progress() as progress:
            task = progress.add_task("post-statute-processing", total=4)
            while not progress.finished:
                progress.console.print("Enabling fts")
                units_tbl.enable_fts(["snippetable"], replace=True)
                root_tbl.enable_fts(["title", "description"], replace=True)
                progress.update(task, advance=1)

                progress.console.print("Indexing fks")
                db.index_foreign_keys()
                progress.update(task, advance=1)

                progress.console.print("Adding statutes_affecting_codifications_view")
                cls.create_statutes_affecting_codifications_view(db)
                progress.update(task, advance=1)

                # clean
                progress.console.print("Vacuuming")
                db.vacuum()
                progress.update(task, advance=1)


@cli.command()
@click.option("--db-name", type=str, default=DB_FILE)
@click.option("--folder", type=Path, default=CODE_DIR)
@click.option("--pattern", type=str, default=TREE_GLOB)
def source_codifications(db_name: str, folder: str, pattern: str):
    """Create codification tables and populate with *.yml files from `--folder`."""
    Codification.source(db_name=db_name, folder=folder, pattern=pattern)
