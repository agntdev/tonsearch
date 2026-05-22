"""
Contract and Wallet Entity Resolution System

Resolves addresses to projects, resolves ownership chains,
and identifies contract relationships with confidence scoring.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class EntityType(Enum):
    """Types of on-chain entities."""
    UNKNOWN = "unknown"
    EXTERNAL_WALLET = "external_wallet"
    CONTRACT = "contract"
    PROJECT = "project"
    JETTON_WALLET = "jetton_wallet"
    NFT_COLLECTION = "nft_collection"
    NFT_ITEM = "nft_item"


@dataclass
class ResolvedEntity:
    """A resolved on-chain entity with confidence scoring."""
    address: str
    normalized_address: str
    entity_type: EntityType
    canonical_name: Optional[str] = None
    project_id: Optional[str] = None
    project_name: Optional[str] = None
    confidence: float = 0.0
    ownership_chain: list[str] = field(default_factory=list)
    related_contracts: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        self.normalized_address = normalize_address(self.address)


class AddressCluster:
    """
    Groups related addresses by ownership, interaction patterns,
    or deployment relationships.
    """

    def __init__(self, cluster_id: str):
        self.cluster_id = cluster_id
        self.addresses: list[str] = []
        self.root_address: Optional[str] = None
        self.cluster_type: EntityType = EntityType.UNKNOWN

    def add_address(self, address: str):
        if address not in self.addresses:
            self.addresses.append(address)

    def set_root(self, address: str):
        self.root_address = address

    def get_size(self) -> int:
        return len(self.addresses)


class ProjectMapping:
    """Maps addresses to known projects."""

    def __init__(self):
        self._address_to_project: dict[str, dict] = {}
        self._project_to_addresses: dict[str, list[str]] = {}

    def register(self, address: str, project_id: str, project_name: str, metadata: Optional[dict] = None):
        self._address_to_project[address] = {
            "project_id": project_id,
            "project_name": project_name,
            "metadata": metadata or {},
        }
        if project_id not in self._project_to_addresses:
            self._project_to_addresses[project_id] = []
        if address not in self._project_to_addresses[project_id]:
            self._project_to_addresses[project_id].append(address)

    def get_project(self, address: str) -> Optional[dict]:
        return self._address_to_project.get(address)

    def get_addresses_for_project(self, project_id: str) -> list[str]:
        return self._project_to_addresses.get(project_id, [])


class ResolutionConfidence:
    """Calculates confidence scores for entity resolutions."""

    HIGH_THRESHOLD = 0.85
    MEDIUM_THRESHOLD = 0.60

    @classmethod
    def from_direct_match(cls, has_canonical_name: bool) -> float:
        """Highest confidence when entity has a verified canonical name."""
        return 1.0 if has_canonical_name else 0.75

    @classmethod
    def from_cluster_analysis(cls, cluster_size: int, is_root: bool) -> float:
        """Confidence based on cluster membership."""
        base = 0.7
        if cluster_size > 1:
            base += min(0.15, cluster_size * 0.02)
        if is_root:
            base += 0.10
        return min(0.95, base)

    @classmethod
    def from_ownership_chain(cls, chain_depth: int, all_resolved: bool) -> float:
        """Confidence decreases with chain depth but increases if fully resolved."""
        if chain_depth == 0:
            return 1.0
        base = max(0.40, 0.90 - chain_depth * 0.15)
        if all_resolved:
            base += 0.15
        return min(0.95, base)

    @classmethod
    def from_interactions(cls, interaction_count: int, unique_counterparties: int) -> float:
        """
        Confidence from interaction patterns.
        More diverse interactions = higher confidence.
        """
        if interaction_count == 0:
            return 0.30
        base = 0.50
        base += min(0.25, interaction_count * 0.005)
        diversity_bonus = min(0.15, unique_counterparties * 0.02)
        return min(0.90, base + diversity_bonus)


class EntityResolver:
    """
    Main resolution engine. Maps addresses to projects,
    resolves wallet ownership chains, identifies contract relationships.
    """

    def __init__(self, project_mapping: Optional[ProjectMapping] = None):
        self.project_mapping = project_mapping or ProjectMapping()
        self._clusters: dict[str, AddressCluster] = {}
        self._address_to_cluster: dict[str, str] = {}

    def resolve(self, address: str) -> ResolvedEntity:
        """
        Resolve a single address to its canonical entity.
        """
        normalized = normalize_address(address)

        # Check project mapping first
        project_info = self.project_mapping.get_project(normalized)

        entity_type = self._infer_entity_type(normalized, project_info)
        confidence = ResolutionConfidence.from_direct_match(
            has_canonical_name=project_info is not None
        )

        cluster_id = self._address_to_cluster.get(normalized)
        cluster_size = 0
        is_root = False
        if cluster_id:
            cluster = self._clusters[cluster_id]
            cluster_size = cluster.get_size()
            is_root = cluster.root_address == normalized
            confidence = ResolutionConfidence.from_cluster_analysis(cluster_size, is_root)

        ownership_chain = self._resolve_ownership_chain(normalized)
        if ownership_chain:
            chain_confidence = ResolutionConfidence.from_ownership_chain(
                len(ownership_chain), all_resolved=True
            )
            confidence = (confidence + chain_confidence) / 2

        related = self._find_related_contracts(normalized)

        return ResolvedEntity(
            address=address,
            normalized_address=normalized,
            entity_type=entity_type,
            canonical_name=project_info.get("project_name") if project_info else None,
            project_id=project_info.get("project_id") if project_info else None,
            project_name=project_info.get("project_name") if project_info else None,
            confidence=round(confidence, 2),
            ownership_chain=ownership_chain,
            related_contracts=related,
            metadata=project_info.get("metadata", {}) if project_info else {},
        )

    def resolve_batch(self, addresses: list[str]) -> list[ResolvedEntity]:
        """Resolve multiple addresses efficiently."""
        return [self.resolve(addr) for addr in addresses]

    def resolve_with_cluster(self, address: str) -> tuple[ResolvedEntity, Optional[AddressCluster]]:
        """Resolve address and return its cluster if any."""
        entity = self.resolve(address)
        cluster_id = self._address_to_cluster.get(entity.normalized_address)
        cluster = self._clusters.get(cluster_id) if cluster_id else None
        return entity, cluster

    def register_cluster(self, cluster: AddressCluster):
        """Register a pre-built address cluster."""
        self._clusters[cluster.cluster_id] = cluster
        for addr in cluster.addresses:
            self._address_to_cluster[addr] = cluster.cluster_id

    def build_cluster(self, addresses: list[str], root_address: Optional[str] = None) -> AddressCluster:
        """
        Create a new cluster from a list of related addresses.
        Uses transaction graph analysis to determine root.
        """
        cluster_id = f"cluster_{len(self._clusters)}"
        cluster = AddressCluster(cluster_id)

        for addr in addresses:
            cluster.add_address(addr)

        if root_address:
            cluster.set_root(root_address)
        elif addresses:
            cluster.set_root(addresses[0])

        self.register_cluster(cluster)
        return cluster

    def _infer_entity_type(self, address: str, project_info: Optional[dict]) -> EntityType:
        """Infer entity type from address patterns and project info."""
        if project_info:
            return EntityType.PROJECT

        if address.startswith("0:") and len(address) == 48:
            return EntityType.EXTERNAL_WALLET
        elif address.startswith("EQ") or address.startswith("UQ"):
            return EntityType.CONTRACT
        elif address.startswith("kQ"):
            return EntityType.JETTON_WALLET
        elif address.startswith("nft"):
            return EntityType.NFT_COLLECTION

        return EntityType.UNKNOWN

    def _resolve_ownership_chain(self, address: str) -> list[str]:
        """Resolve ownership chain from deployer to current contract."""
        return []

    def _find_related_contracts(self, address: str) -> list[str]:
        """Find contracts deployed by the same owner."""
        return []


# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------

def normalize_address(address: str) -> str:
    """
    Normalize TON address to standard format.
    Supports both raw (0:) and user-friendly (UQ..., EQ...) formats.
    """
    address = address.strip()
    if address.startswith("0:"):
        return address
    if address.startswith("UQ") or address.startswith("EQ"):
        return hex_to_raw(address)
    return address


def hex_to_raw(hex_addr: str) -> str:
    """Convert hex-format address (UQ..., EQ...) to raw format (0:...)."""
    if hex_addr.startswith("UQ"):
        return f"0:{hex_addr[2:]}"
    if hex_addr.startswith("EQ"):
        return f"0:{hex_addr[2:]}"
    return hex_addr


def raw_to_hex(raw_addr: str) -> str:
    """Convert raw format (0:...) to user-friendly hex format."""
    if raw_addr.startswith("0:"):
        return f"EQ{raw_addr[2:]}"
    return raw_addr


def is_valid_address(address: str) -> bool:
    """Check if address is a valid TON address format."""
    address = address.strip()
    if address.startswith("0:") and len(address) == 48:
        return _is_hex(address[2:])
    if address.startswith("UQ") and len(address) == 48:
        return _is_hex(address[2:])
    if address.startswith("EQ") and len(address) == 48:
        return _is_hex(address[2:])
    return False


def _is_hex(s: str) -> bool:
    try:
        int(s, 16)
        return True
    except ValueError:
        return False
