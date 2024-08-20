
import pytest
from humane.humanid import human_id, short_human_id


def test_humanid_and_short_common() -> None:
    assert human_id("test") == "12-hilarious-salmons-jumped-gleefully"
    
    assert short_human_id("test") in human_id("test")

@pytest.mark.parametrize("custom_format", [
    "<n> <adjective> <animal> <verb> <adverb>",
    "<n>-<adjective>-<animal>",
    "<n> <adjective>",
    "<n>",
    "Run <n> - <adjective> <animal> <verb> <adverb>",
])
def test_custom_human_id(custom_format: str) -> None:
    assert human_id(
        format=custom_format,
    )

@pytest.mark.parametrize(
    ("custom_format", "wordlist"),
    [
        ("<n> <adjective> <owl>",
        {
            "owl": [
                "owl",
                "crow",
                "raven",
                "parrot",
                "bird",
            ]
        })
    ]
)
def test_custom_human_id_with_wordlist(custom_format: str, wordlist: dict) -> None:
    assert human_id(
        format=custom_format,
        custom_wordlists=wordlist,
    )   
