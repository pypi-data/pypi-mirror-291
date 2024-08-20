import datetime
from collections.abc import Iterator
from pathlib import Path
from typing import Any, NamedTuple

import frontmatter
from citation_utils import Citation
from sqlite_utils.db import Database, Table

from .config import CASE_DIR
from .db import add_idx, check_table


class CitationPath(NamedTuple):
    """Each decision's is dependent on a `CitationPath`.

    Files would need to be downloaded from the [repo](https://github.com/justmars/corpus-decisions)
    and passed through [from_file][md_db.decision.Decision.from_file] to generate the instance.

    ## Route

    !!! note "Path Formula"

        `category` / `number` / `date`

    Each subfolder within has the following routing path to each file. Broken down:

    partial | note
    --:|:--
    `category` | lower-cased docket e.g. 'gr', 'am', etc.
    `number` | lower-cased serial identifier of the docket
    `date` | isoformat

    ## Ponencia File

    !!! note "Naming Convention"

        `main*.*`

    There are three varieties of main files. How they're named gives a clue as to their authorship, if available.

    prefix | type | note
    --:|:--:|:--
    route/`main-pc` | `md` | per curiam, main opinion
    route/`main-<digit>` | `md` | identified writer, main opinion
    route/`main` | `md` | unidentified main opinion

    ## Opinions Folder

    !!! note "Naming Convention"

        `/opinion/` `<digit>.*` within route

    Within the route, it's possible to have related opinions to the main file, it will have the following formula:

    prefix | type | note
    --:|:--:|:--
    route/`opinion/<digit>` | `md` |  writer id separate opinion
    """  # noqa: E501

    id: str
    cite: Citation
    post: frontmatter.Post

    def set_row(self) -> dict[str, Any]:
        """Set an insertable citation row by removing the `id` property
        since this will be replaced by the default hasher.

        Returns:
            dict[str, Any]: Row that goes into the citations table.
        """
        record = self.cite.make_docket_row()
        if not record:
            raise ValueError(f"Bad docket record: {self.id}")
        record.pop("id")
        return record

    def add_citation(self, db: Database) -> Table:
        """Insert row processed by `set_row()`.

        Args:
            db (Database): The source database to detect the citations table.

        Returns:
            Table: Return the table instance (which will contain the last inserted pk)
        """  # noqa: E501
        return check_table(
            db["citations"].insert(  # type: ignore
                record=self.set_row(),
                hash_id="id",
                hash_id_columns=("cat", "num", "date"),
                ignore=True,
            )
        )

    @classmethod
    def create_table(cls, db: Database):
        db["citations"].create(  # type: ignore
            columns={
                "id": str,
                "cat": str,
                "num": str,
                "date": str,
                "scra": str,
                "phil": str,
                "offg": str,
            },
            pk="id",
            not_null={"cat", "num", "date"},
            if_not_exists=True,
        )
        for idx in (
            {"date"},
            {"cat", "num"},
            {"cat", "num", "date"},
            {"scra"},
            {"phil"},
            {"offg"},
        ):
            add_idx(db["citations"], idx)  # type: ignore

    @classmethod
    def from_file(cls, file: Path):
        """Based on the path of a `Decision`, generate instance. Note
        that the citation id will be used as the unique primary key
        of the prospective `Decision` object."""
        cat, num, date, _ = file.parts[-4:]
        post = frontmatter.load(str(file))
        cite = Citation.from_docket_row(
            cat=cat,
            num=num,
            date=date,
            opt_phil=post.get("phil"),  # type: ignore
            opt_scra=post.get("scra"),  # type: ignore
            opt_offg=post.get("offg"),  # type: ignore
        )
        id = cite.set_slug()
        if not id:
            raise Exception("Could not generate decision id.")
        if not cite.docket_date:
            raise Exception("Could not generate decision date.")
        return cls(id=id, post=post, cite=cite)

    @classmethod
    def update_citations_table(cls, db: Database):
        """After correlations are done, can now generate the full text of citations
        based on the value of the updated rows."""
        if not db["citations"].exists():
            raise NotImplementedError("Missing citations table to update.")
        db["citations"].add_column("cite", col_type=str)  # type: ignore
        for row in db["citations"].rows:
            id = row.pop("id")
            del row["cite"]
            cite = Citation.make_citation_string(**row)
            db["citations"].update(id, updates={"cite": cite})  # type: ignore

    @classmethod
    def path_as_record(cls, path: Path) -> dict[str, str | int | bool]:
        """Based [authorship rules][base.author.Author.from_file],
        create a usable record to examine justices vis-a-vis decisions.
        """  # noqa: E501
        record: dict[str, str | int | bool] = {}
        prefix = path.parts[-4:]
        category = prefix[0]
        number = prefix[1]
        date = prefix[2]
        year = date.split("-")[0]  # first digit
        record = {"cat": category, "num": number, "date": date, "year": year}
        main_file = prefix[3].removesuffix(".md")
        main_file_bits = main_file.split("-")

        if len(main_file_bits) > 1:
            if main_file_bits[1] == "pc":
                record |= {"pc": True}
            elif main_file_bits[1].isdigit():
                record |= {"justice_id": int(main_file_bits[1])}
        return record

    @classmethod
    def extract_path_date(cls, file: Path) -> datetime.date:
        """Get date string based on the path"""
        _, _, date_str, _ = file.parts[-4:]
        if "/opinion/" in str(file):
            _, _, date_str, _, _ = file.parts[-5:]
        return datetime.date.fromisoformat(date_str)

    @classmethod
    def extract_paths_by_year(cls, year: int) -> Iterator[Path]:
        return CASE_DIR.glob(f"**/{str(year)}-*/**/*.md")

    @classmethod
    def create_interim_decision_table(cls, db: Database, table_name: str) -> Table:
        """Resembles `Citation` content + `title` since this is what is initially parsed
        from third-party sites. From `cat`, `num,` and `date`, it becomes possible to
        create a `path` field that is usable in both [cls.path_as_record()][base.citation.CitationPath.path_as_record]
        and [cls.from_file()][base.citation.CitationPath.from file].
        """  # noqa: E501
        tbl = db[table_name]
        tbl.create(  # type: ignore
            columns={
                "id": int,
                "cat": str,
                "num": str,
                "date": str,
                "year": int,
                "title": str,
                "path": str,  # relative path where file ought to be stored locally
            },
            pk="id",
            not_null=("cat", "num", "date", "year", "title", "path"),
            if_not_exists=True,
        )
        for idx in (
            {"cat", "num", "date"},
            {"cat", "num"},
            {"cat"},
            {"num"},
            {"date"},
            {"year"},
        ):
            add_idx(tbl, idx)  # type: ignore
        return check_table(tbl)
