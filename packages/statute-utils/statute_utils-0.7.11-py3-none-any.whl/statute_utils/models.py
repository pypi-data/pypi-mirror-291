import datetime
import re
from collections.abc import Iterator
from dataclasses import dataclass
from functools import cached_property
from re import Pattern
from typing import NamedTuple

from slugify import slugify
from sqlite_utils.db import Database

from .components import (
    DB_FILE,
    StatuteSerialCategory,
    make_regex_readable,
    set_mini_statute_files_table,
)


@dataclass(frozen=True)
class Rule:
    """A `Rule` is detected if it matches either a named pattern or a serial pattern.
    Each rule maps to a category `cat` and number `num`.
    """  # noqa: E501

    cat: StatuteSerialCategory
    num: str

    def __repr__(self) -> str:
        return f"<Rule: {self.cat.value} {self.num}>"

    def __str__(self) -> str:
        return self.cat.serialize(self.num) or f"{self.cat.value=} {self.num=}"

    @property
    def slug(self) -> str:
        return slugify(
            " ".join([self.cat.value, self.num.lower()]), separator="_", lowercase=True
        )

    @property
    def serial_title(self):
        return StatuteSerialCategory(self.cat.value).serialize(self.num)

    @cached_property
    def date(self) -> datetime.date | None:
        """Get the earliest date corresponding to the instance."""
        db = Database(DB_FILE)
        if db["statutes"].exists():
            return self.extract_rule_date(db)
        else:
            mini = set_mini_statute_files_table()
            return self.extract_rule_date(mini.db)

    def extract_rule_date(
        self,
        db: Database,
        table_name: str = "statutes",
    ) -> datetime.date | None:
        """Whether using the main database or the mini variant, the same query can
        be applied in extracting the earliest date in a table of rules."""
        results = db.execute_returning_dicts(
            f"""--sql
            select min(s.date) min_date
            from {table_name} s
            where s.cat = :cat and s.num = :num
            group by s.cat, s.num;
            """,
            params={"cat": self.cat.value.lower(), "num": self.num.lower()},
        )
        if results:
            return datetime.date.fromisoformat(results[0]["min_date"])
        return None


class NamedPattern(NamedTuple):
    name: str
    regex_base: str
    rule: Rule
    matches: list[str] | None = None
    excludes: list[str] | None = None
    options: list[Rule] | None = None

    @property
    def regex(self) -> str:
        return make_regex_readable(rf"(?P<{self.group_name}>{self.regex_base})")

    @property
    def pattern(self) -> Pattern:
        return re.compile(self.regex, re.X)

    @property
    def group_name(self) -> str:
        return self.rule.slug


class SerialPattern(NamedTuple):
    """The word _serial_ is employed because the documents representing rules are numbered consecutively.

    Each serial pattern refers to a statute category, e.g. `RA`, `CA`, etc. matched with an identifier, e.g. 386.

    Field | Description | Example
    --:|:--|:--
    `cat` | [`Statute Category`][statute-category-model] | StatuteSerialCategory.RepublicAct
    `regex_bases` | How do we pattern the category name? | ["r.a. no.", "Rep. Act. No."]
    `regex_serials` | What digits are allowed | ["386", "11114"]
    `matches` | Usable in parametized tests to determine whether the pattern declared matches the samples | ["Republic Act No. 7160", "R.A. 386 and 7160" ]
    `excludes` | Usable in parametized tests to determine that the full pattern will not match | ["Republic Act No. 7160:", "RA 9337-"]
    """  # noqa: E501

    cat: StatuteSerialCategory
    regex_bases: list[str]
    regex_serials: list[str]
    matches: list[str] | None = None
    excludes: list[str] | None = None

    @property
    def lines(self) -> Iterator[str]:
        """Each regex string produced matches the serial rule. Note the line break
        needs to be retained so that when printing `@regex`, the result is organized.
        """
        for base in self.regex_bases:
            for idx in self.regex_serials:
                yield rf"""({base}\s*{idx})
                """

    @property
    def group_name(self) -> str:
        return rf"serial_{self.cat.value}"

    @property
    def regex(self) -> str:
        return rf"(?P<{self.group_name}>{r'|'.join(self.lines)})"

    @property
    def pattern(self) -> Pattern:
        return re.compile(self.regex, re.X)

    @property
    def digits_in_match(self) -> Pattern:
        return re.compile(r"|".join(self.regex_serials))
