import re
from enum import StrEnum, auto
from typing import NamedTuple


class StatuteTitleCategory(StrEnum):
    """
    A Rule in the Philippines involves various denominations.
    It can be referred to by its

    1. `official` title
    2. `serial` title
    3. `short` title
    4. `alias` titles
    4. `searchable` titles

    Consider something like the _Maceda Law_ which can be dissected as follows:

    Category | Mandatory | Nature | Description | Example | Matching Strategy
    --:|:--:|:--:|:--|:--|--:
    `official` | yes | official | full length title | _AN ACT TO PROVIDE PROTECTION TO BUYERS OF REAL ESTATE ON INSTALLMENT PAYMENTS_ | [Statute Details][statutes]
    `serial` | yes | official | `Statute Category` + serial identifier. | _Republic Act No. 6552_ | Serial Pattern regex matching
    `short`  | no | official | may be declared in body of statute | _Realty Installment Buyer Act_ | [A helper function] [extract-short-title]
    `alias`  | no | unofficial | popular, undocumented means of referring to a statute | _Maceda Law_ | Named Pattern regex matching
    `searchables`  | no | unofficial | easy way for users to reference via search | ra 6552 | --
    """  # noqa: E501

    Official = auto()
    Serial = auto()
    Alias = auto()
    Short = auto()
    Searchable = auto()


class StatuteSerialCategory(StrEnum):
    """
    It would be difficult to identify rules if they were arbitrarily named
    without a fixed point of reference. For instance the _Civil Code of the
    Philippines_,  an arbitrary collection of letters, would be hard to find
    if laws were organized alphabetically.

    Fortunately, each Philippine `serial`-title rule belongs to an
    assignable `StatuteSerialCategory`:

    Serial Category `name` | Shorthand `value`
    --:|:--
    Republic Act | ra
    Commonwealth Act | ca
    Act | act
    Constitution | const
    Spain | spain
    Batas Pambansa | bp
    Presidential Decree | pd
    Executive Order | eo
    Letter of Instruction | loi
    Veto Message | veto
    Rules of Court | roc
    Bar Matter | rule_bm
    Administrative Matter | rule_am
    Resolution en Banc | rule_reso
    Circular OCA | oca_cir
    Circular SC | sc_cir

    This is not an official reference but
    rather a non-exhaustive taxonomy of Philippine legal rules mapped to
    a `enum.Enum` object.

    Enum | Purpose
    --:|:--
    `name` | for _most_ members, can "uncamel"-ized to produce serial title
    `value` | (a) folder for discovering path / (b) category usable in the database table

    Using this model simplifies the ability to navigate rules. Going back to
    the _Civil Code_ described above, we're able to describe it as follows:

    Aspect | Description
    --:|:--
    serial title | _Republic Act No. 386_
    assumed folder path |`/ra/386`
    category | ra
    id | 386

    Mapped to its `Rule` counterpart we get:

    Field | Value | Description
    :--:|:--:|:--
    `cat`| ra | Serial statute category
    `id` | 386 | Serial identifier of the category

    ## Purpose

    Knowing the path to a `Rule`, we can later [extract its contents][statutes].

    Examples:
        >>> StatuteSerialCategory
        <enum 'StatuteSerialCategory'>
        >>> StatuteSerialCategory._member_map_
        {'RepublicAct': 'ra', 'CommonwealthAct': 'ca', 'Act': 'act', 'Constitution': 'const', 'Spain': 'spain', 'BatasPambansa': 'bp', 'PresidentialDecree': 'pd', 'ExecutiveOrder': 'eo', 'LetterOfInstruction': 'loi', 'VetoMessage': 'veto', 'RulesOfCourt': 'roc', 'BarMatter': 'rule_bm', 'AdministrativeMatter': 'rule_am', 'ResolutionEnBanc': 'rule_reso', 'CircularOCA': 'oca_cir', 'CircularSC': 'sc_cir'}
    """  # noqa: E501

    RepublicAct = "ra"
    CommonwealthAct = "ca"
    Act = "act"
    Constitution = "const"
    Spain = "spain"
    BatasPambansa = "bp"
    PresidentialDecree = "pd"
    ExecutiveOrder = "eo"
    LetterOfInstruction = "loi"
    VetoMessage = "veto"
    RulesOfCourt = "roc"
    BarMatter = "rule_bm"
    AdministrativeMatter = "rule_am"
    ResolutionEnBanc = "rule_reso"
    CircularOCA = "oca_cir"
    CircularSC = "sc_cir"

    def __repr__(self) -> str:
        """Uses value of member `ra` instead of Enum default
        `<StatuteSerialCategory.RepublicAct: 'ra'>`. It becomes to
        use the following conventions:

        Examples:
            >>> StatuteSerialCategory('ra')
            'ra'
            >>> StatuteSerialCategory.RepublicAct
            'ra'

        Returns:
            str: The value of the Enum member
        """
        return str.__repr__(self.value)

    def serialize(self, idx: str) -> str | None:
        """Given a member item and a valid serialized identifier, create a serial title.

        Note that the identifier must be upper-cased to make this consistent
        with the textual convention, e.g.

        Examples:
            >>> StatuteSerialCategory.PresidentialDecree.serialize('570-a')
            'Presidential Decree No. 570-A'
            >>> StatuteSerialCategory.AdministrativeMatter.serialize('03-06-13-sc')
            'Administrative Matter No. 03-06-13-SC'

        Args:
            idx (str): The number to match with the category

        Returns:
            str | None: The serialized text, e.g. `category` + `idx`
        """

        def uncamel(cat: StatuteSerialCategory):
            """See [Stack Overflow](https://stackoverflow.com/a/9283563)"""
            x = r"((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))"
            return re.sub(x, r" \1", cat.name)

        match self:  # noqa: E999 ; ruff complains but this is valid Python
            case StatuteSerialCategory.Spain:
                small_idx = idx.lower()
                if small_idx in ["civil", "penal"]:
                    return f"Spanish {idx.title()} Code"
                elif small_idx == "commerce":
                    return "Code of Commerce"
                raise SyntaxWarning(f"{idx=} invalid serial of {self}")

            case StatuteSerialCategory.Constitution:
                if idx.isdigit() and int(idx) in [1935, 1973, 1987]:
                    return f"{idx} Constitution"
                raise SyntaxWarning(f"{idx=} invalid serial of {self}")

            case StatuteSerialCategory.RulesOfCourt:
                if idx in ["1918", "1940", "1964"]:
                    return f"{idx} Rules of Court"
                elif idx in ["cpr"]:
                    return "Code of Professional Responsibility"
                raise SyntaxWarning(f"{idx=} invalid serial of {self}")

            case StatuteSerialCategory.VetoMessage:
                """No need to specify No.; understood to mean a Republic Act"""
                return f"Veto Message - {idx}"

            case StatuteSerialCategory.ResolutionEnBanc:
                """The `idx` needs to be a specific itemized date."""
                return f"Resolution of the Court En Banc dated {idx}"

            case StatuteSerialCategory.CircularSC:
                return f"SC Circular No. {idx}"

            case StatuteSerialCategory.CircularOCA:
                return f"OCA Circular No. {idx}"

            case StatuteSerialCategory.AdministrativeMatter:
                """Handle special rule with variants: e.g.`rule_am 00-5-03-sc-1`
                and `rule_am 00-5-03-sc-2`
                """
                am = uncamel(self)
                small_idx = idx.lower()
                if "sc" in small_idx:
                    if small_idx.endswith("sc"):
                        return f"{am} No. {small_idx.upper()}"
                    elif sans_var := re.search(r"^.*-sc(?=-\d+)", small_idx):
                        return f"{am} No. {sans_var.group().upper()}"
                return f"{am} No. {small_idx.upper()}"

            case StatuteSerialCategory.BatasPambansa:
                if idx.isdigit():
                    return (  # there are no -A -B suffixes in BPs
                        f"{uncamel(self)} Blg. {idx}"
                    )

            case _:
                # no need to uppercase pure digits
                target_digit = idx if idx.isdigit() else idx.upper()
                return f"{uncamel(self)} No. {target_digit}"

    def searchable(self, num: str) -> list[str]:
        """Given the value `<v>` of a category (lowercased, as saved in the database),
        use `StatuteSerialCategory(<v>)`. This will get the proper category. Use the
        category alongside the passed `num`.

        Examples:
            >>> civ = StatuteSerialCategory('ra')
            >>> civ.searchable('386')
            ['ra 386', 'rep act no. 386', 'r.a. no. 386', 'r.a. 386']
            >>> civ = StatuteSerialCategory('rule_am')
            >>> civ.searchable('00-2-03-sc')
            ['am 00-2-03-sc', 'a.m. no. 00-2-03-sc', 'a.m. 00-2-03-sc', 'admin matter no. 00-2-03-sc']
        """  # noqa: E501
        match self:
            case StatuteSerialCategory.RepublicAct:
                return [
                    f"ra {num}",
                    f"rep act no. {num}",
                    f"r.a. no. {num}",
                    f"r.a. {num}",
                ]
            case StatuteSerialCategory.CommonwealthAct:
                return [
                    f"ca {num}",
                    f"commonwealth act no. {num}",
                    f"c.a. no. {num}",
                    f"c.a. {num}",
                ]
            case StatuteSerialCategory.Act:
                return [
                    f"act of congress {num}",
                ]
            case StatuteSerialCategory.BatasPambansa:
                return [
                    f"bp {num}",
                    f"b.p. no. {num}",
                    f"b.p. blg. {num}",
                    f"batas pambansa {num}",
                    f"batas pambansa blg. {num}",
                ]
            case StatuteSerialCategory.ExecutiveOrder:
                return [
                    f"eo {num}",
                    f"e.o. no. {num}",
                    f"exec order {num}",
                    f"exec. order no. {num}",
                ]
            case StatuteSerialCategory.PresidentialDecree:
                return [
                    f"pd {num}",
                    f"p.d. no. {num}",
                    f"pres decree {num}",
                    f"pres. dec. {num}",
                    f"pres. decree {num}",
                ]
            case StatuteSerialCategory.LetterOfInstruction:
                return [
                    f"loi {num}",
                    f"l.o.i. {num}",
                    f"l.o.i. no. {num}",
                ]
            case StatuteSerialCategory.Spain:
                return [
                    f"spanish {num}",
                    f"old {num}",
                ]
            case StatuteSerialCategory.RulesOfCourt:
                return [
                    f"{num} roc",
                ]
            case StatuteSerialCategory.Constitution:
                return [
                    f"{num} const",
                ]
            case StatuteSerialCategory.AdministrativeMatter:
                return [
                    f"am {num}",
                    f"a.m. no. {num}",
                    f"a.m. {num}",
                    f"admin matter no. {num}",
                ]
            case StatuteSerialCategory.BarMatter:
                return [
                    f"bm {num}",
                    f"b.m. no. {num}",
                    f"b.m. {num}",
                    f"bar matter no. {num}",
                ]
            case StatuteSerialCategory.CircularOCA:
                return [
                    f"oca {num}",
                    f"oca ipi {num}",
                    f"oca ipi no. {num}",
                ]
            case StatuteSerialCategory.CircularSC:
                return [
                    f"sc cir {num}",
                    f"sc cir. no. {num}",
                    f"sc cir. no. {num}",
                ]
            case _:
                return [f"{self.value} {num}"]

    def cite(self, num: str) -> str | None:
        """Given the value `<v>` of a category (lowercased, as saved in the database),
        use `StatuteSerialCategory(<v>)`. This will get the proper category. Use the
        category alongside the passed `num`.

        Examples:
            >>> civ = StatuteSerialCategory('ra')
            >>> civ.cite('386')
            'R.A. No. 386'
            >>> spain = StatuteSerialCategory('spain')
            >>> spain.cite('penal')
            'Spanish Penal Code'
            >>> roc = StatuteSerialCategory('roc')
            >>> roc.cite('1964')
            '1964 Rules of Court'

        Args:
            num (str): The serialized instance of the category

        Returns:
            str | None: A representation of the category for use in citations.
        """
        match self:
            case StatuteSerialCategory.Spain:
                if num == "civil":
                    return "Spanish Civil Code"
                elif num == "penal":
                    return "Spanish Penal Code"
                elif num == "commerce":
                    return "Code of Commerce"
                return None
            case StatuteSerialCategory.Act:
                return f"Act No. {num.upper()}"
            case StatuteSerialCategory.BatasPambansa:
                return f"B.P. Blg. {num.upper()}"
            case StatuteSerialCategory.VetoMessage:
                return f"Veto Message - R.A. No. {num.upper()}"
            case StatuteSerialCategory.Constitution:
                return f"{num} Constitution"
            case StatuteSerialCategory.RulesOfCourt:
                return f"{num} Rules of Court"
            case StatuteSerialCategory.AdministrativeMatter:
                return f"A.M. No. {num.upper()}"
            case StatuteSerialCategory.BarMatter:
                return f"B.M. No. {num.upper()}"
            case StatuteSerialCategory.ResolutionEnBanc:
                return f"Resolution of the Court En Banc dated {num}"
            case StatuteSerialCategory.CircularOCA:
                return f"OCA Circular No. {num.upper()}"
            case StatuteSerialCategory.CircularSC:
                return f"SC Circular No. {num.upper()}"
            case _:
                ...
                base = ".".join([i for i in self.value]).upper()
                return f"{base}. No. {num.upper()}"


class StatuteTitle(NamedTuple):
    """Will be used to populate the database; assumes a fixed `statute_id`."""

    category: StatuteTitleCategory
    text: str

    @classmethod
    def generate(
        cls,
        official: str | None = None,
        serial: str | None = None,
        short: str | list[str] | None = None,
        aliases: list[str] | None = None,
        searchables: list[str] | None = None,
    ):
        if official:
            yield cls(category=StatuteTitleCategory.Official, text=official)

        if serial:
            yield cls(category=StatuteTitleCategory.Serial, text=serial)

        if aliases:
            for title in aliases:
                if title and title != "":
                    yield cls(category=StatuteTitleCategory.Alias, text=title)

        if searchables:
            for title in searchables:
                if title and title != "":
                    yield cls(category=StatuteTitleCategory.Searchable, text=title)

        if short:
            if isinstance(short, list):
                for bit in short:
                    yield cls(category=StatuteTitleCategory.Short, text=bit)
            elif isinstance(short, str):
                yield cls(category=StatuteTitleCategory.Short, text=short)
