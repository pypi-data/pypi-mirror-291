from enum import Enum
from pathlib import Path
import random
import re


def read_wordlist(name: str) -> list[str]:
    current_file = Path(__file__).resolve()
    parent_dir = current_file.parent
    wordlist_path = parent_dir / f"{name}"
    return wordlist_path.read_text().splitlines()


class Wordlist(str, Enum):
    ADJECTIVES = "adjective"
    COLOURS = "colour"
    ANIMALS = "animal"
    VERBS = "verb"
    ADVERBS = "adverb"


WORDLISTS = {
    Wordlist.ADJECTIVES: read_wordlist("./lists/adjectives.txt"),
    Wordlist.COLOURS: read_wordlist("./lists/colours.txt"),
    Wordlist.ANIMALS: read_wordlist("./lists/animal-plurals.txt"),
    Wordlist.VERBS: read_wordlist("./lists/verbs.txt"),
    Wordlist.ADVERBS: read_wordlist("./lists/adverbs.txt"),
}

MAX_N = 10


def total_possibilities(wordlists: list[Wordlist], start: int = 1) -> int:
    total = start
    for wordlist in wordlists:
        total *= len(WORDLISTS.get(wordlist, []))
    return total


# Expected entropy: 30 * 253 * 200 = 1,518,000
def short_human_id(seed: str | None = None) -> str:
    return human_id(
        format="<n>-<adjective>-<animal>",
        seed=seed,
    )


def human_id(
    seed: str | None = None,
    *,
    format: str = "<n>-<adjective>-<animal>-<verb>-<adverb>",
    custom_wordlists: dict | None = None,
) -> str:
    rng = random.Random(seed)
    
    # Combine default wordlists with custom wordlists
    all_wordlists = WORDLISTS.copy()
    if custom_wordlists:
        all_wordlists.update(custom_wordlists)
    
    def replace_token(match):
        token = match.group(1)
        if token == 'n':
            return str(rng.randint(2, MAX_N + 2))
        elif token in all_wordlists:
            return rng.choice(all_wordlists[token])
        else:
            raise ValueError(f"Unknown token in format string: {token}")
    
    return re.sub(r'<(\w+)>', replace_token, format)
