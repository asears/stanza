"""
Coordination plan for type-hint updates under stanza/models using 3 subagents.

This file documents folder scopes and constraints so runs are repeatable.
"""

from __future__ import annotations

SUBAGENT_SCOPES: dict[str, list[str]] = {
    "subagent_1": [
        "stanza/models/__init__.py",
        "stanza/models/_training_logging.py",
        "stanza/models/charlm.py",
        "stanza/models/classifier.py",
        "stanza/models/constituency_parser.py",
        "stanza/models/identity_lemmatizer.py",
        "stanza/models/lang_identifier.py",
        "stanza/models/lemmatizer.py",
        "stanza/models/mwt_expander.py",
        "stanza/models/ner_tagger.py",
        "stanza/models/parser.py",
        "stanza/models/tagger.py",
        "stanza/models/tokenizer.py",
        "stanza/models/wl_coref.py",
    ],
    "subagent_2": [
        "stanza/models/constituency",
        "stanza/models/depparse",
        "stanza/models/langid",
        "stanza/models/lemma",
        "stanza/models/mwt",
        "stanza/models/ner",
        "stanza/models/pos",
        "stanza/models/tokenization",
    ],
    "subagent_3": [
        "stanza/models/coref",
        "stanza/models/lemma_classifier",
    ],
}

CONSTRAINTS: list[str] = [
    "Use modern typing styles with built-in list/tuple/set/dict and PEP604 unions (|).",
    "Use typing.Any only when concrete type is not clear.",
    "Prefer minimal, localized edits.",
    "Do not change runtime behavior.",
    "Add from __future__ import annotations only where needed.",
]

if __name__ == "__main__":
    for name, scope in SUBAGENT_SCOPES.items():
        print(name)
        for entry in scope:
            print(f"  - {entry}")
