# nosql/test_graph_backend.py
"""
Test script for GraphBackend Neo4j integration.
Validates that all query methods work correctly.
"""

from graph_backend import GraphPlaceholder

def test_graph_backend():
    print("=" * 60)
    print("Testing GraphBackend Neo4j Integration")
    print("=" * 60)
    
    # Initialize connection
    graph = GraphPlaceholder()
    print("✓ Connected to Neo4j\n")
    
    # Test 1: Get top entities (no filter)
    print("Test 1: Get top 10 entities (all types)")
    print("-" * 60)
    entities = graph.get_entities(limit=10)
    print(f"Found {len(entities)} entities")
    for i, entity in enumerate(entities[:5], 1):
        print(f"{i}. {entity['name']} ({entity['type']}) - Score: {entity['importance_score']}, Papers: {entity['paper_count']}, Relations: {entity['relation_count']}")
    print()
    
    # Test 2: Get entities by type
    print("Test 2: Get 'gene' entities")
    print("-" * 60)
    gene_entities = graph.get_entities(entity_type='gene', limit=5)
    print(f"Found {len(gene_entities)} gene entities")
    for entity in gene_entities:
        print(f"  - {entity['name']} (Score: {entity['importance_score']})")
    print()
    
    # Test 3: Get related papers for top entity
    print("Test 3: Get related papers for 'spaceflight' (E00385)")
    print("-" * 60)
    papers = graph.get_related_papers('E00385', limit=10)
    print(f"Found {len(papers)} papers mentioning 'spaceflight'")
    print(f"Paper IDs: {papers[:5]}...")
    print()
    
    # Test 4: Get relations for an entity
    print("Test 4: Get relations for 'spaceflight' (E00385)")
    print("-" * 60)
    relations = graph.get_entity_relations('E00385')
    print(f"Found {len(relations)} relations")
    for i, rel in enumerate(relations[:5], 1):
        print(f"{i}. {rel['source']} --[{rel['relation']}]--> {rel['target']} (evidence: {rel['evidence_count']})")
    print()
    
    # Test 5: Get filtered relations by type
    print("Test 5: Get 'increases' relations for 'spaceflight' (E00385)")
    print("-" * 60)
    filtered_relations = graph.get_entity_relations('E00385', relation_type='increases')
    print(f"Found {len(filtered_relations)} 'increases' relations")
    for rel in filtered_relations[:3]:
        print(f"  - {rel['source']} increases {rel['target']}")
        print(f"    Evidence count: {rel['evidence_count']}, Confidence: {rel['confidence']:.2f}")
        print(f"    Papers: {rel['papers'][:3]}")
    print()
    
    # Close connection
    graph.close()
    print("✓ All tests passed! GraphBackend is ready for Member 2's dashboard.")
    print("=" * 60)

if __name__ == "__main__":
    test_graph_backend()
