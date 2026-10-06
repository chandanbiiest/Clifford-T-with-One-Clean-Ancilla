from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Sequence


def neglog_survival(error_probability: float) -> float:
    if not 0.0 <= error_probability < 1.0:
        raise ValueError("error_probability must satisfy 0 <= p < 1")
    return -math.log1p(-error_probability)


def survival_from_loss(loss: float) -> float:
    if loss < 0:
        raise ValueError("loss must be nonnegative")
    return math.exp(-loss)


def exact_removed_work_threshold(epsilon_t: float, epsilon_cx: float,
                                 removed_t: int = 4, removed_cx: int = 2) -> float:
    """Maximum isolated measurement-error probability with equal survival.

    Solves 1-eps_M = (1-eps_T)^removed_t (1-eps_CX)^removed_cx,
    before correction, reset, and idle penalties are added.
    """
    survival = (1.0 - epsilon_t) ** removed_t * (1.0 - epsilon_cx) ** removed_cx
    return 1.0 - survival


def first_order_removed_work_threshold(epsilon_t: float, epsilon_cx: float,
                                       removed_t: int = 4, removed_cx: int = 2) -> float:
    return removed_t * epsilon_t + removed_cx * epsilon_cx


def latency_break_even(static_dt: float, candidate_dt: float,
                       static_ncx: float, candidate_ncx: float,
                       tau_t: float = 1.0, tau_cx: float = 0.2) -> float:
    return (static_dt - candidate_dt) * tau_t + (static_ncx - candidate_ncx) * tau_cx


@dataclass(frozen=True)
class Label:
    name: str
    values: tuple[float, ...]


def pareto_front(labels: Sequence[Label]) -> list[Label]:
    """Return labels that are not component-wise dominated (all minimized)."""
    out: list[Label] = []
    for i, a in enumerate(labels):
        dominated = False
        for j, b in enumerate(labels):
            if i == j:
                continue
            le_all = all(x <= y for x, y in zip(b.values, a.values))
            lt_any = any(x < y for x, y in zip(b.values, a.values))
            if le_all and lt_any:
                dominated = True
                break
        if not dominated:
            out.append(a)
    return out
