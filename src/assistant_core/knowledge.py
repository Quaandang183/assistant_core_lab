import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path

from assistant_core.errors import DataError

STOPWORDS = frozenset(
    {"a", "an", "the", "is", "are", "of", "to", "for", "and", "or", "in", "on", "at", "what", "where", "how", "do", "i"}
)


def _words(text: str) -> set[str]:
    return {w for w in re.findall(r"\w+", text.lower()) if w not in STOPWORDS}


@dataclass(frozen=True)
class Office:
    name: str
    room: str
    hours: str


class OfficeDirectory:
    def __init__(self, offices: dict[str, Office]):
        self._offices = offices

    @classmethod
    def from_csv(cls, path: Path) -> "OfficeDirectory":
        try:
            with path.open(encoding="utf-8", newline="") as f:
                rows = list(csv.DictReader(f))
            return cls({r["name"].lower(): Office(r["name"], r["room"], r["hours"]) for r in rows})
        except FileNotFoundError as exc:
            raise DataError(f"office file not found: {path}") from exc
        except KeyError as exc:
            raise DataError(f"office file {path} is missing column {exc}") from exc

    @property
    def names(self) -> set[str]:
        return set(self._offices)

    def all(self) -> list[Office]:
        """All offices, sorted by name (used by GET /v1/offices)."""
        return sorted(self._offices.values(), key=lambda o: o.name)

    def find(self, text: str) -> Office | None:
        t = text.lower()
        return next((o for name, o in self._offices.items() if name in t), None)


@dataclass(frozen=True)
class Rule:
    id: str
    title: str
    text: str


class Handbook:
    def __init__(self, rules: list[Rule]):
        self._rules = rules

    @classmethod
    def from_json(cls, path: Path) -> "Handbook":
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            return cls([Rule(id=r["id"], title=r["title"], text=r["text"]) for r in raw])
        except FileNotFoundError as exc:
            raise DataError(f"handbook file not found: {path}") from exc
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            raise DataError(f"handbook file {path} is malformed: {exc}") from exc

    def search(self, query: str) -> Rule | None:
        """Keyword overlap baseline: title words count double. Returns None if nothing matches."""
        q = _words(query)
        best, best_score = None, 0
        for rule in self._rules:
            score = 2 * len(q & _words(rule.title)) + len(q & _words(rule.text))
            if score > best_score:
                best, best_score = rule, score
        return best
