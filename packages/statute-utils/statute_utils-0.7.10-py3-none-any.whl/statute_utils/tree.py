import datetime
import logging
from abc import ABC, abstractmethod
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any, NamedTuple, Self

import yaml
from rich.progress import track
from sqlite_utils.db import Database, Table

from .components import (
    StatuteSerialCategory,
    create_fts_snippet_column,
    create_unit_heading,
    set_node_ids,
)
from .components.db import add_idx, check_table
from .models import Rule
from .templater import html_tree_from_hierarchy


class TreePath(NamedTuple):
    """An interim structure that contains common utilities to unpack a
    given tree-based path from a corpus- repository containing
    *.yml files.

    Assumes strict path routing structure: `cat` / `num` / `date` / `variant`.yml,
    e.g. `ra/386/1946-06-18/1.yml` where each file contains the following metadata, the
    mandatory ones being "title" and "units". See example:

    ```yaml
    title: An Act to Ordain and Institute the Civil Code of the Philippines
    units:
    - item: Container 1
        caption: Preliminary Title
        units:
        - item: Chapter 1
            caption: Effect and Application of Laws
            units:
            - item: Article 1
                content: >-
                This Act shall be known as the "Civil Code of the Philippines."
                (n)
            - item: Article 2
                content: >-
                Laws shall take effect after fifteen days following the
                completion of their publication either in the Official
                Gazette or in a newspaper of general circulation in the
                Philippines, unless it is otherwise provided. (1a)
    ```

    It's possible for there to be other fields.

    ## Naming Statutes

    ### Route

    !!! note "Path Formula"

        `category` / `number` / `date`

    Each subfolder within has the following routing path to each file. Broken down:

    partial | note
    --:|:--
    `category` | lower-cased statute category e.g. 'act', 'ra', 'rule_am', 'sc_cir' etc.
    `number` | lower-cased serial identifier of the statute category
    `date` | isoformat

    > re: `eo` as category, only popular Executive Orders are included by `statute-patterns` since it's difficult to determine
    > EOs which have legislative imprimatur vs. purely executive orders.

    ### Create file based on variant

    > e.g. `1.yml`

    There may be different variants of the same statute, even if distinguished by date. The variant provides
    the ability to make a route unique and this becomes the name of the file, e.g. `1.yml`

    ## Naming Codifications

    ### Route

    !!! note "Path Formula"

        `category` / `number` / `date`

    Each subfolder within has the following routing path to each file. Broken down:

    partial | note
    --:|:--
    `category` | lower-cased statute category e.g. 'act', 'ra', 'rule_am', 'sc_cir' etc.
    `number` | lower-cased serial identifier of the statute category

    ### Create file based on author identifier

    e.g. `mv-civil-v1.yml`

    partial | note
    --:|:--
    `id` | lower-cased short-hand identifier of the author, e.g. `mv`
    `name` | author established id of the codification, e.g. `civil`
    `v` | version of the codification released, e.g. `v1`

    """  # noqa: E501

    category: StatuteSerialCategory
    num: str
    date: datetime.date
    slug: str

    @property
    def serial_title(self) -> str:
        serial = self.category.serialize(self.num)
        if not serial:
            raise ValueError(f"Unserialized {self.num}= from {self.category=}")
        return serial

    @property
    def searchable_serial_titles(self) -> list[str]:
        searchables = self.category.searchable(self.num)
        if not searchables:
            raise ValueError(f"No searchables of {self.num}= from {self.category=}")
        return searchables

    @property
    def as_rule(self) -> Rule:
        rule = Rule(cat=self.category, num=self.num)
        if not rule:
            raise ValueError(f"No rule from {self.category=} and {self.num=}")
        return rule

    @classmethod
    def load(cls, path: Path) -> dict:
        """Convert flat file text into nested JSON object"""
        content = path.read_bytes()
        result = yaml.safe_load(content)
        if not isinstance(result, dict):
            raise ValueError(
                f"JSON conversion of {path=} must result in an initial dict."
            )

        title = result.get("title")
        if not title:
            raise KeyError(f"No title in {path=}")

        units = result.get("units")
        if not units:
            raise KeyError(f"No units in {path=}")

        return result

    @classmethod
    def unpack(cls, path: Path):
        """Convert flat yml file into interim TreePath instance."""
        cat, num, date, slug = path.parts[-4:]
        category = StatuteSerialCategory(cat)
        if not category:
            raise ValueError(f"No category from {cat=}")
        return cls(
            category=category,
            num=num,
            date=datetime.date.fromisoformat(date),
            slug=slug.removesuffix(".yml"),
        )

    @classmethod
    def generate_material_paths(
        cls,
        units: list[dict[str, Any]],
        extra_data: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Adds material paths to each node in the tree with the root
        node given special features: it's marked with a material path `id`
        of `1.`

        Args:
            units (list[dict[str, Any]]): Each node in the tree.
            extra_data (dict[str, Any] | None, optional): If any extra data is supplied,
                this is made part of the root node. Defaults to None.

        Returns:
            list[dict[str, Any]]: Identified nodes containing
                material path-based ids.
        """
        set_node_ids(units)
        root = {"id": "1.", "units": units}
        if extra_data:
            root |= extra_data
        return [root]

    @classmethod
    def flatten(
        cls, key: str, id: str, units: list[dict[str, Any]], heading: str = ""
    ) -> Iterator[dict[str, str | None]]:
        """Recursive function to flatten tree-like structure from *.yml file.

        Each material path gets its own item, caption, and content fields with
        extracted heading / snippetable columns from such fields.

        Snippetable column becomes a searchable FTS summary of caption + content

        Heading column makes identifable the subtree involved with item + caption

        Args:
            key (str): Name of key to serve as the column name
            id (str): The root parent id
            units (list[dict[str, Any]]): The list of units that ought to be parsed
            heading (str, optional): Heading column makes identifable the
                subtree involved with item + caption. Defaults to "".

        Yields:
            Iterator[dict[str, str | None]]: Enables list of rows for table insertion
        """
        for unit in units:
            present_heading = create_unit_heading(unit, heading)
            yield {
                key: id,
                "material_path": unit["id"],  # enable subtree
                "heading": present_heading,  # identify subtree
                "item": unit.get("item"),
                "caption": unit.get("caption"),
                "content": unit.get("content"),
                "snippetable": create_fts_snippet_column(unit),  # enable searchability
            }
            if subunits := unit.get("units"):
                yield from cls.flatten(
                    key,
                    id,
                    subunits,
                    present_heading,
                )


class TreeContent(NamedTuple):
    """Each `TreePath` file should contain `units`.

    All nodes in the prospective tree database should be marked by a material path.

    ## Root

    The `units` key is manipulated to add a root node.

    - This is useful for repeals and other changes since affecting the root node, affects all nodes.
    - This is also useful for extra data like search content.
    - The root node for every key should be `1.`

    ## Html

    - A special `html` field exists for the purpose of performance.
    - Since some units are overly large, this creates an unstyled html blob that semantically represents the tree object.
    - Helper functions are used to build the tree object
    - The functions can be re-used via Jinja / Django filters downstream.

    ## Full-text-search (fts)

    - Each of the nodes can be searchable.
    - The `fts` key will represent a generator of rows that can be inserted into a separate table.
    - Each row of this variant will contain a reference back to the main container.
    """  # noqa: E501

    units: list[dict[str, Any]]
    fts: Iterator[dict[str, Any]]
    html: str

    @classmethod
    def contextualize(
        cls,
        unit_parent_column_name: str,
        root_id: str,
        units: list[dict[str, Any]],
        extra_data: dict[str, Any] | None = None,
    ) -> Self:
        """Generate variants of content.

        Args:
            unit_parent_column_name (str): Will be used to generate the column key,
                e.g. if prefix is "statute", the column id will be "statute_id"
            root_id (str): Each material path generated should have a reference back
                to the root id
            units (list[dict[str, Any]]): The units to consume and process.
            extra_data (dict[str, Any] | None, optional): Any content to be included
                as part of the root node. Defaults to None.

        Returns:
            TreeContent: "Immutable" container hosting various variants of same content.
        """
        mp_units = TreePath.generate_material_paths(
            units=units,
            extra_data=extra_data,
        )

        fts_mp_units = TreePath.flatten(
            key=unit_parent_column_name,
            id=root_id,
            units=mp_units,
        )

        sans_root = mp_units[0]["units"]

        html_tree = html_tree_from_hierarchy(sans_root)

        return cls(
            units=mp_units,
            fts=fts_mp_units,  # includes extra data when searching for content
            html=html_tree,  # excludes extra data in rendering content
        )


@dataclass(frozen=True)
class TreeBase(ABC):
    """Common properties and methods to be inherited by main tree structure."""

    id: str
    rule: Rule
    date: datetime.date
    units: list[dict]
    size: int

    def __str__(self) -> str:
        return f"{self.__class__.__name__.lower()}: {self.id}"

    @property
    def base(self) -> dict[str, Any]:
        """Base columns that contain identifying metadata."""
        return {
            "id": self.id,
            "cat": self.rule.cat.value,
            "num": self.rule.num,
            "date": self.date,
            "size": self.size,
        }

    def set_content(self, extra_data: dict[str, Any] | None = None) -> TreeContent:
        """Base columns that contain the main units."""
        return TreeContent.contextualize(
            unit_parent_column_name=self.__class__.set_common_root_pk(),
            root_id=self.id,
            units=self.units,
            extra_data=extra_data,
        )

    @classmethod
    def set_root_table_name(cls):
        """How to name the table for roots, e.g. if
        a `Codification`, the table name should be `codifications`."""
        return cls.__name__.lower() + "s"

    def get_root_table(self, db: Database) -> Table:
        """The typecasted table for roots."""
        tbl_name = self.__class__.set_root_table_name()
        return check_table(db[tbl_name])

    def add_root(self, db: Database, record: dict[str, Any]):
        """Common insertion method into a root table."""
        tbl = self.get_root_table(db)
        try:
            tbl.insert(record=record, ignore=True)  # type: ignore
        except Exception as e:
            raise ValueError(f"Bad {self.__class__.__name__} record; {e=}")

    @classmethod
    def set_unit_table_name(cls):
        """How to name table for units, e.g. if
        a `Codification`, the table name should be `codification_units`."""
        return cls.__name__.lower() + "_units"

    @classmethod
    def set_common_root_pk(cls):
        """How to name foreign key to reference the root, e.g. if
        a `Codification`,the foreign key name should be `codification_id`."""
        return cls.__name__.lower() + "_id"

    def get_unit_table(self, db: Database) -> Table:
        """The typecasted table for units."""
        tbl_name = self.__class__.set_unit_table_name()
        return check_table(db[tbl_name])

    def add_units(self, db: Database, records: Iterator[dict[str, Any]]):
        """Common insertion method into a units table."""
        root_id_key = self.__class__.set_common_root_pk()  # see fk in units table
        tbl = self.get_unit_table(db)
        dated_records = (record | {"date": self.date} for record in records)
        try:
            tbl.insert_all(  # type: ignore
                dated_records,
                hash_id="id",  # type: ignore
                hash_id_columns=(root_id_key, "material_path"),  # type: ignore
                ignore=True,  # type: ignore
            )
        except Exception as e:
            raise ValueError(f"Bad units of {self.__class__.__name__} record; {e=}")

    @classmethod
    @abstractmethod
    def from_file(cls, file: Path) -> Self:
        """Each tree must instantiate from a file object."""
        ...

    @abstractmethod
    def to_row(self, db: Database):
        """Each tree must make table rows for both:

        1. [create_root_table][statute_utils.tree.TreeBase.create_root_table] and
        2. [create_unit_fts_table][statute_utils.tree.TreeBase.create_unit_fts_table].

        The relation of `cls.from_file()` to this function:

        ```mermaid
        flowchart LR
            file["`cls.from_file()`"]
            db["`self.to_row()`"]
            file --interim processes--> db
        ```
        """
        ...

    @classmethod
    def create_base_tables(cls, db: Database) -> tuple[Table, Table]:
        """Pair a root and units table.

        The root table must be created per parent, see [create_root_table][statute_utils.tree.TreeBase.create_root_table]

        The units table, however, can be created implicitly,
        see [create_unit_fts_table][statute_utils.tree.TreeBase.create_unit_fts_table].

        Args:
            db (Database): Where to create the tables

        Returns:
            tuple[Table, Table]: Pair of tables, root and unit
        """  # noqa: E501
        root_table = cls.create_root_table(db)
        units_table = cls.create_unit_fts_table(
            db=db,
            root_tbl_name=cls.set_root_table_name(),
            unit_tbl_name=cls.set_unit_table_name(),
            unit_fk=cls.set_common_root_pk(),
        )
        return (root_table, units_table)

    @classmethod
    def from_folder_to_db(cls, db: Database, folder: str, pattern: str):
        files = list(Path(folder).glob(pattern))
        for file in track(files, description=cls.set_root_table_name()):
            try:
                tree = cls.from_file(file=file)
                tree.to_row(db=db)
            except Exception as e:
                logging.error(f"Failed {cls.__name__} from {file=}; {e=}")

    @classmethod
    @abstractmethod
    def create_root_table(cls, db: Database) -> Table:
        """Each container tree renderable via its `html` property.
        must have its own implementation for generating its fields.
        """
        ...

    @classmethod
    def create_unit_fts_table(
        cls,
        db: Database,
        unit_tbl_name: str,
        root_tbl_name: str,
        unit_fk: str,
    ) -> Table:
        """Create a unit table to host fts-based rows.

        Args:
            db (Database): Where the table is to be created
            unit_tbl_name (str): The name of the units table
            root_tbl_name (str): Each table needs to have a foreign key relationship
                with its parent root table
            unit_fk (str): The relationship to `root_tbl_name` will be through the
                key defined in `unit_fk`.

        Returns:
            Table: Hosts units which contain snippets that can be searched via
                sqlite's full-text-search (FTS) extension
        """
        mp_key = "material_path"
        db[unit_tbl_name].create(  # type: ignore
            columns={
                "id": str,
                unit_fk: str,  # referring to either statute_id or codification_id
                mp_key: str,
                "heading": str,
                "item": str,
                "caption": str,
                "content": str,
                "snippetable": str,  # combination of caption + content for search
                "date": datetime.date,  # date of root to sort arbitrary units
            },
            pk="id",
            foreign_keys=[(unit_fk, root_tbl_name, "id")],
            not_null={unit_fk, mp_key, "date"},
            if_not_exists=True,
        )
        for idx in (
            {unit_fk, "date"},
            {"date"},
            {mp_key},
            {unit_fk, mp_key},
        ):
            add_idx(db[unit_tbl_name], idx)

        return check_table(db[unit_tbl_name])

    @classmethod
    @abstractmethod
    def source(cls, db_name: str, folder: str, pattern: str):
        """Initializes statutes from source *.yml files.

        Each tree object originating from a file can be converted
        into a database row that will fill up the tables created
        in:

        1. [create_root_table()][statute_utils.tree.TreeBase.create_root_table]; and
        2. [create_unit_table()][statute_utils.tree.TreeBase.create_unit_fts_table].

        Args:
            db_name (str): Name of the database file to use.
            folder (str): Where the *.yml files are found.
            pattern (str): What glob pattern to use to detect the yml files.
        """
        ...
