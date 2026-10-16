"""Skip tests that cannot run on Hedera, with a reason for each."""

import tomllib
from pathlib import Path
from typing import List, Tuple

import pytest

DEFAULT_SKIP_LIST = "docs/hedera/hedera_skips.toml"


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add the Hedera skip list option."""
    group = parser.getgroup(
        "hedera_skips",
        "Arguments for skipping tests that are not applicable to Hedera",
    )
    group.addoption(
        "--hedera-skip-list",
        action="store",
        dest="hedera_skip_list",
        default=DEFAULT_SKIP_LIST,
        help=(
            "TOML file with `[[skip]]` entries (`prefix`, `reason`), "
            "relative to the pytest root dir unless absolute. Tests whose "
            "node id starts with `prefix` are skipped with `reason`. "
            f"Default: {DEFAULT_SKIP_LIST}"
        ),
    )


def _load_skip_list(config: pytest.Config) -> List[Tuple[str, str]]:
    """Load `(prefix, reason)` pairs from the skip list file."""
    path = Path(config.getoption("hedera_skip_list"))
    if not path.is_absolute():
        path = config.rootpath / path
    if not path.exists():
        raise pytest.UsageError(f"Hedera skip list not found: {path}")
    with path.open("rb") as f:
        data = tomllib.load(f)
    return [(entry["prefix"], entry["reason"]) for entry in data["skip"]]


def pytest_collection_modifyitems(
    config: pytest.Config, items: List[pytest.Item]
) -> None:
    """Add a skip marker to every test that matches the skip list."""
    skips = _load_skip_list(config)
    for item in items:
        for prefix, reason in skips:
            if item.nodeid.startswith(prefix):
                item.add_marker(pytest.mark.skip(reason=reason))
                break
