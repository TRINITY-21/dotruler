"""Plugin registry for output adapters."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from airules.outputs.base import BaseRenderer

_REGISTRY: dict[str, type[BaseRenderer]] = {}


def register(target_id: str):
    """Decorator to register an output adapter."""

    def decorator(cls: type[BaseRenderer]) -> type[BaseRenderer]:
        _REGISTRY[target_id] = cls
        return cls

    return decorator


def get_renderer(target_id: str) -> type[BaseRenderer]:
    """Get a renderer class by target ID."""
    if target_id not in _REGISTRY:
        available = ", ".join(sorted(_REGISTRY))
        raise KeyError(f"Unknown target '{target_id}'. Available: {available}")
    return _REGISTRY[target_id]


def list_targets() -> dict[str, type[BaseRenderer]]:
    """Return all registered targets."""
    return dict(_REGISTRY)
