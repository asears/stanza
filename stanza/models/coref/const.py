""" Contains type aliases for coref module """

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import torch


EPSILON = 1e-7
LARGE_VALUE = 1000  # used instead of inf due to bug #16762 in pytorch

Doc = dict[str, Any]
Span = tuple[int, int]


@dataclass
class CorefResult:
    coref_scores: torch.Tensor | None = None                  # [n_words, k + 1]
    coref_y: torch.Tensor | None = None                       # [n_words, k + 1]
    rough_y: torch.Tensor | None = None                       # [n_words, n_words]

    word_clusters: list[list[int]] | None = None
    span_clusters: list[list[Span]] | None = None

    rough_scores: torch.Tensor | None = None                  # [n_words, n_words]
    span_scores: torch.Tensor | None = None                   # [n_heads, n_words, 2]
    span_y: tuple[torch.Tensor, torch.Tensor] | None = None   # [n_heads] x2

    zero_scores: torch.Tensor | None = None
