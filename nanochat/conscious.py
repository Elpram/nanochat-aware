"""Utilities for configuring consciousness-inspired features."""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar, Dict, Optional


@dataclass(frozen=True)
class ConsciousConfig:
    """Lightweight container for consciousness-inspired hyperparameters."""

    reentry_steps: int = 0
    ignite_topk: int = 0
    gate_mode: str = "none"

    VALID_GATE_MODES: ClassVar[tuple[str, ...]] = ("none", "token", "head")

    def __post_init__(self) -> None:  # noqa: D401 - simple validation helper
        if self.reentry_steps < 0:
            raise ValueError("reentry_steps must be non-negative")
        if self.ignite_topk < 0:
            raise ValueError("ignite_topk must be non-negative")
        if self.gate_mode not in self.VALID_GATE_MODES:
            raise ValueError(
                f"gate_mode must be one of {', '.join(self.VALID_GATE_MODES)}"
            )

    def to_dict(self) -> Dict[str, object]:
        return {
            "reentry_steps": self.reentry_steps,
            "ignite_topk": self.ignite_topk,
            "gate_mode": self.gate_mode,
        }

    def with_overrides(
        self,
        *,
        reentry_steps: Optional[int] = None,
        ignite_topk: Optional[int] = None,
        gate_mode: Optional[str] = None,
    ) -> "ConsciousConfig":
        data = self.to_dict()
        if reentry_steps is not None:
            data["reentry_steps"] = reentry_steps
        if ignite_topk is not None:
            data["ignite_topk"] = ignite_topk
        if gate_mode is not None:
            data["gate_mode"] = gate_mode
        return ConsciousConfig(**data)

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, object]]) -> "ConsciousConfig":
        if data is None:
            data = {}
        filtered = {
            key: data[key]
            for key in ("reentry_steps", "ignite_topk", "gate_mode")
            if key in data and data[key] is not None
        }
        return cls(**filtered)

    @classmethod
    def from_model_config(cls, config: object) -> "ConsciousConfig":
        if config is None:
            return cls()
        payload: Dict[str, object] = {}
        for key in ("reentry_steps", "ignite_topk", "gate_mode"):
            if hasattr(config, key):
                payload[key] = getattr(config, key)
        return cls(**payload)

    @classmethod
    def from_model(cls, model: object) -> "ConsciousConfig":
        return cls.from_model_config(getattr(model, "config", None))
