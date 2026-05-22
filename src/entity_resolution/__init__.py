"""Entity resolution module for TonSearch."""

from .entity_resolver import (
    AddressCluster,
    EntityResolver,
    EntityType,
    ProjectMapping,
    ResolutionConfidence,
    ResolvedEntity,
    hex_to_raw,
    is_valid_address,
    normalize_address,
    raw_to_hex,
)

__all__ = [
    "EntityResolver",
    "ProjectMapping",
    "AddressCluster",
    "ResolvedEntity",
    "EntityType",
    "normalize_address",
    "hex_to_raw",
    "raw_to_hex",
    "is_valid_address",
    "ResolutionConfidence",
]
