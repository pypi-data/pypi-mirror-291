# statute-utils

![Github CI](https://github.com/justmars/statute-utils/actions/workflows/ci.yml/badge.svg)

Philippine statutory law:

1. pattern matching
2. unit retrieval
3. database creation
4. template creation

> [!IMPORTANT]
> When modifying a database structure, consider four inter-related parts:
>
> 1. The pythonic object, e.g. `NamedTuple`
> 2. The representation of such in the prospective database
> 3. The documentation of the pythonic object found in `/docs`
> 4. The use of all of the above in downstream [decision-utils](https://github.com/justmars/decision-utils).

## Run

```sh
just --list # see recipes
just start # install
just dumpenv # configure .env

builder # list command line recipes from pyproject.toml script
builder interim-db # show statute files in /data

just build-trees # creates base on .env-based DB_FILE
```

## Dev

```sh
just dumpenv
```

In `/components/settings.py`, can see the following partial code:

```py
SOURCE: ParseResult = env.url("SOURCE")
CODE_DIR: Path = env.path("CODE_DIR")
STAT_DIR: Path = env.path("STAT_DIR")
CASE_DIR: Path = env.path("CASE_DIR", Path().cwd())
```

The following values become available globally:

value | type | note
-- | -- | --
`CODE_DIR` | `pathlib.Path` | for `TreePath` and `Codification`
`STAT_DIR` | `pathlib.Path` | for `TreePath` and `Statute`
`CASE_DIR` | `pathlib.Path` | in anticipation of [decision-utils](https://github.com/justmars/decision-utils)
`SOURCE` | `urllib.parse.ParseResult` | must run `SOURCE.geturl()` for `Listing` (also in anticipation of [decision-utils](https://github.com/justmars/decision-utils))

Included folders:

> [!NOTE]
> If `statute-utils` is imported into a third-party library, it needs to include the `/templates` folder and `/sql` folder. These doe not include any `*.py` files and are thus referenced in `MANIFEST.IN`.

## Docs

```sh
mkdocs serve
```
