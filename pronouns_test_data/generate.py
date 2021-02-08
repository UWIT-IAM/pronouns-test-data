from __future__ import annotations

import os
import random
import string
from enum import Enum
from typing import List, Optional

import typer

from pronouns_test_data.models import (
    GeneratedTestData,
    PronounTestCase,
    ValidCharacters,
)


def generate_jargon(valid_chars: str, length: int) -> str:
    return "".join([random.choice(valid_chars) for _ in range(length)])


def generate_test_data() -> GeneratedTestData:
    return GeneratedTestData(
        test_cases=[
            PronounTestCase(
                uwnetid="javerage",
                pronoun="they/them/their/theirs/themself",
                use_case="The full expression of a single pronoun set. "
                "Also, this netid should be registered for some university classes.",
            ),
            PronounTestCase(
                uwnetid="uwitpn01",
                pronoun="she/her/hers; they/them/theirs",
                use_case="A consistently formatted list of two pronoun sets.",
            ),
            PronounTestCase(
                uwnetid="uwitpn02",
                pronoun="he him his",
                use_case="A single, atypically formatted pronoun set.",
            ),
            PronounTestCase(
                uwnetid="uwitpn03",
                pronoun="she, her, hers or they/them",
                use_case="Two atypically and inconsistently formatted pronoun sets.",
            ),
            PronounTestCase(
                uwnetid="uwitpn04",
                pronoun="please use my name",
                use_case="Guidance in place of a declared pronoun set, with no punctuation.",
            ),
            PronounTestCase(
                uwnetid="uwitpn05",
                pronoun="i am exploring this. please ask me!",
                use_case="Guidance in place of a declared pronoun set, with punctuation.",
            ),
            PronounTestCase(
                uwnetid="uwitpn06",
                pronoun="they/them/theirs;they/them/theirs;they/them/theirs",
                use_case="A consistently formatted pronoun set that is (accidentally?) pasted three times, with no spaces.",
            ),
            PronounTestCase(
                uwnetid="uwitpn07",
                pronoun="she/they",
                use_case="A common shorthand expression of two pronoun sets.",
            ),
            PronounTestCase(
                uwnetid="uwitpn08",
                pronoun="ze/hir",
                use_case="A common shorthand expression of two neo-pronoun sets.",
            ),
            PronounTestCase(
                uwnetid="uwitpn09",
                pronoun="fae/r or they/themself",
                use_case='One neo-pronoun shorthand and one shorthand expression of the "they" pronoun set, each with its '
                "own shorthand syntax",
            ),
            PronounTestCase(
                uwnetid="uwitpn10",
                pronoun='""el"&maybe "els" or just ask?',
                use_case="A pronoun, plus guidance, with inconsistent punctuation.",
            ),
            PronounTestCase(
                uwnetid="uwitpn11",
                pronoun=generate_jargon(ValidCharacters.valid_ascii(), 12),
                use_case="12 randomly generated characters (very common length)",
            ),
            PronounTestCase(
                uwnetid="uwitpn12",
                pronoun=generate_jargon(ValidCharacters.valid_ascii(), 16),
                use_case="16 randomly generated characters (very common length)",
            ),
            PronounTestCase(
                uwnetid="uwitpn13",
                pronoun=generate_jargon(ValidCharacters.valid_ascii(), 32),
                use_case="32 randomly generated characters (uncommon length)",
            ),
            PronounTestCase(
                uwnetid="uwitpn14",
                pronoun=generate_jargon(ValidCharacters.valid_ascii(), 64),
                use_case="64 randomly generated characters (unlikely length)",
            ),
            PronounTestCase(
                uwnetid="uwitpn15",
                pronoun=generate_jargon(ValidCharacters.valid_ascii(), 128),
                use_case="128 randomly generated characters (very unlikely length)",
            ),
            PronounTestCase(
                uwnetid="uwitpn16",
                pronoun=generate_jargon(ValidCharacters.valid_ascii(), 140),
                use_case="140 (max. length) randomly generated characters (very unlikely length)",
            ),
            PronounTestCase(
                uwnetid="uwitpn17",
                pronoun=generate_jargon(ValidCharacters.valid_punctuation(), 140),
                use_case="140 characters of only punctuation, to test text wrapping",
            ),
            PronounTestCase(
                uwnetid="uwitpn18",
                pronoun=generate_jargon(string.digits, 140),
                use_case="140 characters of only punctuation, to test text wrapping",
            ),
        ]
    )


def app(
    out: Optional[str] = typer.Option(
        None,
        "--out",
        "-o",
        help="The relative or absolute path name for the JSON output.",
    ),
    auto_confirm: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Use this if you don't want to confirm file " "overwrites.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Use this if you don't want to see the generated data.",
    ),
):
    if quiet and not out:
        raise typer.Exit(
            "No possible output. Please remove the --quiet/-q flag or provide an --output/-o "
            "target. Exiting."
        )

    test_cases = generate_test_data().json(by_alias=True, indent=4)

    if not quiet:
        typer.echo(test_cases)

    if out:
        if os.path.exists(out) and not auto_confirm:
            typer.confirm(
                f"WARNING: File '{out}' already exists. Do you want to overwrite it?",
                abort=True,  # If the user says "no," the program will exit.
            )
        with open(out, "w") as f:
            f.write(test_cases)
            typer.echo(f"Wrote test data to '{out}'.")


if __name__ == "__main__":
    typer.run(app)
