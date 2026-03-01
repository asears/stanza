"""
Subagent coordination for ANN (missing annotation) warnings in stanza/models.

Scopes are divided by model subfolder groups to avoid conflicts.
Each subagent processes one scope with focused rule constraints.

Constraint: ONLY add type hints when confident about the type.
Do not use Any or guess at types—skip uncertain annotations entirely.
"""

SUBAGENT_SCOPES = {
    "scope-1-entry-and-common": {
        "description": "Top-level entry scripts and common infrastructure modules",
        "folders": [
            "stanza/models/classifier.py",
            "stanza/models/constituency_parser.py",
            "stanza/models/tokenizer.py",
            "stanza/models/charlm.py",
            "stanza/models/lang_identifier.py",
            "stanza/models/lemmatizer.py",
            "stanza/models/mwt_expander.py",
            "stanza/models/ner_tagger.py",
            "stanza/models/parser.py",
            "stanza/models/tagger.py",
            "stanza/models/wl_coref.py",
            "stanza/models/identity_lemmatizer.py",
            "stanza/models/classifiers/",
            "stanza/models/common/",
        ],
        "rules": ["ANN001", "ANN201", "ANN204", "ANN002", "ANN003"],
        "constraint": "Only add hints when type is clear from context (imports, assignments, etc)"
    },
    
    "scope-2-depparse-langid-lemma-mwt": {
        "description": "Dependency parsing, language ID, lemmatization, MWT subfolders",
        "folders": [
            "stanza/models/depparse/",
            "stanza/models/langid/",
            "stanza/models/lemma/",
            "stanza/models/mwt/",
        ],
        "rules": ["ANN001", "ANN201", "ANN204", "ANN002", "ANN003"],
        "constraint": "Only add hints when type is clear from context (imports, assignments, etc)"
    },
    
    "scope-3-ner-pos-tokenization": {
        "description": "NER, POS tagging, tokenization subfolders",
        "folders": [
            "stanza/models/ner/",
            "stanza/models/pos/",
            "stanza/models/tokenization/",
        ],
        "rules": ["ANN001", "ANN201", "ANN204", "ANN002", "ANN003"],
        "constraint": "Only add hints when type is clear from context (imports, assignments, etc)"
    },

    "scope-4-constituency-coref-lemma-classifier": {
        "description": "Constituency parsing, coreference resolution, lemma classifier subfolders",
        "folders": [
            "stanza/models/constituency/",
            "stanza/models/coref/",
            "stanza/models/lemma_classifier/",
        ],
        "rules": ["ANN001", "ANN201", "ANN204", "ANN002", "ANN003"],
        "constraint": "Only add hints when type is clear from context (imports, assignments, etc)"
    },
}

CONSTRAINTS = [
    "Use lowercase built-in generics: list, tuple, dict, set (not List, Tuple, etc)",
    "Use PEP 604 unions: X | None instead of Union[X, None] or Optional[X]",
    "Use from __future__ import annotations if adding | unions",
    "DO NOT add type hints if uncertain—skip rather than use Any or guess",
    "Focus on public methods and critical internal functions",
    "Preserve any existing type hints—only fill clear gaps",
]

if __name__ == "__main__":
    print("ANN Warning Remediation Scopes")
    print("=" * 50)
    for scope_name, scope_info in SUBAGENT_SCOPES.items():
        print(f"\n{scope_name}")
        print(f"  Description: {scope_info['description']}")
        print(f"  Folders: {scope_info['folders']}")
        print(f"  Rules: {', '.join(scope_info['rules'])}")
        print(f"  Constraint: {scope_info['constraint']}")
    
    print("\n\nGlobal Constraints:")
    for constraint in CONSTRAINTS:
        print(f"  • {constraint}")
