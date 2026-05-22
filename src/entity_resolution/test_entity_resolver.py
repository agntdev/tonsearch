"""
Test suite for Contract/Wallet Entity Resolution System.
Tests with 1000+ sample addresses covering various entity types,
address formats, clusters, and confidence scoring scenarios.
"""

import pytest

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


class TestAddressNormalization:
    """Test address normalization utilities."""

    def test_normalize_raw_address(self):
        addr = "0:6cf686df95e060375a92184754b364f16b5b3b175c331b339ba6a27bd639adf2"
        assert normalize_address(addr) == addr

    def test_normalize_eq_address(self):
        eq_addr = "EQB9TriH0AKlUaUBtio0QbSnjM66nxKm0tCukadidwCVCYr-"
        result = normalize_address(eq_addr)
        assert result.startswith("0:")

    def test_normalize_uq_address(self):
        uq_addr = "UQCqnetXpRfQq3BJ_cml5LsR9juPgANd7QdUCWNJLs7v27J5"
        result = normalize_address(uq_addr)
        assert result.startswith("0:")

    def test_normalize_with_whitespace(self):
        addr = "  0:6cf686df95e060375a92184754b364f16b5b3b175c331b339ba6a27bd639adf2  "
        assert normalize_address(addr) == addr.strip()


class TestHexRawConversion:
    """Test hex-to-raw and raw-to-hex conversions."""

    def test_eq_to_raw(self):
        eq_addr = "EQB9TriH0AKlUaUBtio0QbSnjM66nxKm0tCukadidwCVCYr-"
        raw = hex_to_raw(eq_addr)
        assert raw.startswith("0:")
        assert len(raw) == 48

    def test_uq_to_raw(self):
        uq_addr = "UQCqnetXpRfQq3BJ_cml5LsR9juPgANd7QdUCWNJLs7v27J5"
        raw = hex_to_raw(uq_addr)
        assert raw.startswith("0:")
        assert len(raw) == 48

    def test_raw_to_eq(self):
        raw_addr = "0:6cf686df95e060375a92184754b364f16b5b3b175c331b339ba6a27bd639adf2"
        eq = raw_to_hex(raw_addr)
        assert eq.startswith("EQ")


class TestAddressValidation:
    """Test address validation."""

    def test_valid_raw_address(self):
        addr = "0:6cf686df95e060375a92184754b364f16b5b3b175c331b339ba6a27bd639adf2"
        assert is_valid_address(addr) is True

    def test_valid_eq_address(self):
        addr = "EQB9TriH0AKlUaUBtio0QbSnjM66nxKm0tCukadidwCVCYr-"
        assert is_valid_address(addr) is True

    def test_valid_uq_address(self):
        addr = "UQCqnetXpRfQq3BJ_cml5LsR9juPgANd7QdUCWNJLs7v27J5"
        assert is_valid_address(addr) is True

    def test_invalid_address_short(self):
        addr = "0:short"
        assert is_valid_address(addr) is False

    def test_invalid_address_bad_hex(self):
        addr = "0:gggg686df95e060375a92184754b364f16b5b3b175c331b339ba6a27bd639adf2"
        assert is_valid_address(addr) is False


class TestEntityResolverBasic:
    """Test basic entity resolution."""

    def test_resolve_wallet_address(self):
        resolver = EntityResolver()
        addr = "0:6cf686df95e060375a92184754b364f16b5b3b175c331b339ba6a27bd639adf2"
        result = resolver.resolve(addr)
        assert result.address == addr
        assert result.entity_type == EntityType.EXTERNAL_WALLET
        assert result.confidence >= 0.0

    def test_resolve_contract_address(self):
        resolver = EntityResolver()
        addr = "EQB9TriH0AKlUaUBtio0QbSnjM66nxKm0tCukadidwCVCYr-"
        result = resolver.resolve(addr)
        assert result.entity_type == EntityType.CONTRACT

    def test_resolve_jetton_address(self):
        resolver = EntityResolver()
        addr = "kQAAAAAAAAAAV"
        result = resolver.resolve(addr)
        assert result.entity_type == EntityType.JETTON_WALLET

    def test_resolve_batch(self):
        resolver = EntityResolver()
        addresses = [
            "0:6cf686df95e060375a92184754b364f16b5b3b175c331b339ba6a27bd639adf2",
            "EQB9TriH0AKlUaUBtio0QbSnjM66nxKm0tCukadidwCVCYr-",
        ]
        results = resolver.resolve_batch(addresses)
        assert len(results) == 2
        assert all(isinstance(r, ResolvedEntity) for r in results)


class TestProjectMapping:
    """Test project mapping functionality."""

    def test_register_and_lookup(self):
        mapping = ProjectMapping()
        addr = "0:6cf686df95e060375a92184754b364f16b5b3b175c331b339ba6a27bd639adf2"
        project_id = "proj_001"
        project_name = "TestProject"

        mapping.register(addr, project_id, project_name)
        info = mapping.get_project(addr)

        assert info is not None
        assert info["project_id"] == project_id
        assert info["project_name"] == project_name

    def test_get_addresses_for_project(self):
        mapping = ProjectMapping()
        addr1 = "0:addr1"
        addr2 = "0:addr2"
        project_id = "proj_002"

        mapping.register(addr1, project_id, "Project")
        mapping.register(addr2, project_id, "Project")

        addresses = mapping.get_addresses_for_project(project_id)
        assert len(addresses) == 2
        assert addr1 in addresses
        assert addr2 in addresses

    def test_unknown_address_returns_none(self):
        mapping = ProjectMapping()
        assert mapping.get_project("0:unknown") is None


class TestEntityResolverWithProjectMapping:
    """Test entity resolution with project mapping."""

    def test_resolve_mapped_address(self):
        mapping = ProjectMapping()
        addr = "0:mapped12345678901234567890123456789012345678901234"
        mapping.register(addr, "proj_001", "MyProject", {"tvl": 1000000})

        resolver = EntityResolver(project_mapping=mapping)
        result = resolver.resolve(addr)

        assert result.entity_type == EntityType.PROJECT
        assert result.project_id == "proj_001"
        assert result.project_name == "MyProject"
        assert result.canonical_name == "MyProject"
        assert result.confidence == 1.0


class TestAddressClustering:
    """Test address clustering functionality."""

    def test_build_cluster(self):
        resolver = EntityResolver()
        addresses = [
            "0:addr1AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
            "0:addr2AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
            "0:addr3AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        ]
        cluster = resolver.build_cluster(addresses, root_address=addresses[0])

        assert cluster.get_size() == 3
        assert cluster.root_address == addresses[0]

    def test_resolve_with_cluster(self):
        resolver = EntityResolver()
        addresses = [
            "0:rootABBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",
            "0:child1CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
        ]
        cluster = resolver.build_cluster(addresses, root_address=addresses[0])

        result, returned_cluster = resolver.resolve_with_cluster(addresses[0])
        assert returned_cluster is not None
        assert returned_cluster.cluster_id == cluster.cluster_id


class TestConfidenceScoring:
    """Test confidence scoring calculations."""

    def test_direct_match_high_confidence(self):
        confidence = ResolutionConfidence.from_direct_match(has_canonical_name=True)
        assert confidence == 1.0

    def test_direct_match_low_confidence(self):
        confidence = ResolutionConfidence.from_direct_match(has_canonical_name=False)
        assert confidence == 0.75

    def test_cluster_analysis_single_address(self):
        confidence = ResolutionConfidence.from_cluster_analysis(
            cluster_size=1, is_root=False
        )
        assert confidence == 0.7

    def test_cluster_analysis_large_cluster(self):
        confidence = ResolutionConfidence.from_cluster_analysis(
            cluster_size=10, is_root=True
        )
        assert confidence > 0.7

    def test_ownership_chain_direct(self):
        confidence = ResolutionConfidence.from_ownership_chain(
            chain_depth=0, all_resolved=True
        )
        assert confidence == 1.0

    def test_ownership_chain_deep(self):
        confidence = ResolutionConfidence.from_ownership_chain(
            chain_depth=5, all_resolved=True
        )
        assert confidence >= 0.40

    def test_interactions_high_diversity(self):
        confidence = ResolutionConfidence.from_interactions(
            interaction_count=100, unique_counterparties=50
        )
        assert confidence > 0.5


class TestLargeScaleResolution:
    """
    Test with 1000+ sample addresses.
    Simulates real-world address diversity.
    """

    def test_resolve_1000_wallet_addresses(self):
        resolver = EntityResolver()
        base_addr = "0:000000000000000000000000000000000000000000000000"

        results = []
        for i in range(1000):
            addr = f"0:{i:042d}"
            results.append(resolver.resolve(addr))

        assert len(results) == 1000
        assert all(r.entity_type == EntityType.EXTERNAL_WALLET for r in results)
        assert all(r.confidence >= 0.0 for r in results)

    def test_resolve_500_contract_addresses(self):
        resolver = EntityResolver()
        results = []
        for i in range(500):
            addr = f"EQ{i:042d}"
            results.append(resolver.resolve(addr))

        assert len(results) == 500
        assert all(r.entity_type == EntityType.CONTRACT for r in results)

    def test_resolve_500_mixed_addresses(self):
        resolver = EntityResolver()
        results = []
        for i in range(500):
            if i % 3 == 0:
                addr = f"0:{i:042d}"
            elif i % 3 == 1:
                addr = f"EQ{i:042d}"
            else:
                addr = f"UQ{i:042d}"
            results.append(resolver.resolve(addr))

        assert len(results) == 500
        assert all(isinstance(r, ResolvedEntity) for r in results)

    def test_batch_resolve_1000_plus_500(self):
        resolver = EntityResolver()
        addresses = []
        for i in range(1500):
            if i < 1000:
                addresses.append(f"0:{i:042d}")
            else:
                addresses.append(f"EQ{(i - 1000):042d}")

        results = resolver.resolve_batch(addresses)
        assert len(results) == 1500

    def test_project_mapping_100_projects(self):
        mapping = ProjectMapping()
        for i in range(100):
            addr = f"0:project{i:040d}"
            mapping.register(addr, f"proj_{i}", f"Project {i}", {"id": i})

        resolver = EntityResolver(project_mapping=mapping)

        for i in range(100):
            addr = f"0:project{i:040d}"
            result = resolver.resolve(addr)
            assert result.project_id == f"proj_{i}"
            assert result.confidence == 1.0

    def test_cluster_analysis_50_clusters(self):
        resolver = EntityResolver()
        for cluster_id in range(50):
            addresses = [f"0:c{cluster_id:02d}addr{i:036d}" for i in range(10)]
            resolver.build_cluster(addresses, root_address=addresses[0])

        assert len(resolver._clusters) == 50

        for cluster_id in range(50):
            addresses = [f"0:c{cluster_id:02d}addr{i:036d}" for i in range(10)]
            for addr in addresses[:2]:
                result, cluster = resolver.resolve_with_cluster(addr)
                assert cluster is not None
                assert cluster.get_size() == 10


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_resolve_unknown_address(self):
        resolver = EntityResolver()
        result = resolver.resolve(
            "0:FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
        )
        assert result.entity_type == EntityType.UNKNOWN
        assert result.confidence == 0.75

    def test_empty_cluster(self):
        cluster = AddressCluster("empty_cluster")
        assert cluster.get_size() == 0

    def test_cluster_without_root(self):
        cluster = AddressCluster("no_root")
        cluster.add_address("0:addr1")
        cluster.add_address("0:addr2")
        assert cluster.root_address is None

    def test_resolve_batch_empty(self):
        resolver = EntityResolver()
        results = resolver.resolve_batch([])
        assert len(results) == 0


class TestOwnershipChain:
    """Test ownership chain resolution scenarios."""

    def test_ownership_chain_integration(self):
        resolver = EntityResolver()
        addr = "0:owner1234567890123456789012345678901234567890123456789"
        result = resolver.resolve(addr)
        assert isinstance(result.ownership_chain, list)

    def test_related_contracts_integration(self):
        resolver = EntityResolver()
        addr = "0:contract12345678901234567890123456789012345678901234"
        result = resolver.resolve(addr)
        assert isinstance(result.related_contracts, list)


class TestMetadata:
    """Test metadata propagation."""

    def test_metadata_from_project_mapping(self):
        mapping = ProjectMapping()
        addr = "0:withmeta1234567890123456789012345678901234567890123"
        metadata = {"tvl": 1000000, "category": "DeFi", "audit": True}
        mapping.register(addr, "proj", "Test", metadata)

        resolver = EntityResolver(project_mapping=mapping)
        result = resolver.resolve(addr)

        assert result.metadata["tvl"] == 1000000
        assert result.metadata["category"] == "DeFi"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
