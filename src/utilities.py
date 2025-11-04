from langchain_community.graphs.graph_document import (
    Node as BaseNode,
    Relationship as BaseRelationship,
    GraphDocument,
)
from graph_components import Node, Relationship, Property, knowledgeGraph

def format_property_key(key: str) -> str:
    """Format property key to meet Neo4j requirements"""
    words = key.split()
    if not words:
        return key
    first_word = words[0].lower()
    capitalized_words = [word.capitalize() for word in words[1:]]
    return "".join([first_word] + capitalized_words)

def porps_to_dict(props) -> dict:
    """Convert list of Property objects to dictionary"""
    properties = {}
    if not props:
        return {}
    for prop in props:
        properties[format_property_key(prop.key)] = prop.value
    return properties

def map_to_base_node(node: Node) -> BaseNode:
    """Map custom Node to BaseNode"""
    properties = {}
    if node.properties:
        properties = porps_to_dict(node.properties)
    # Add name property for better Cypher statement generation
    properties["name"] = node.id.title()
    return BaseNode(
        id=node.id,
        labels=node.labels,
        properties=properties,
    )

def map_to_base_relationship(rel: Relationship) -> BaseRelationship:
    """Map the KnowledgeGraph Relationship to BaseRelationship"""
    source = map_to_base_node(rel.source)
    target = map_to_base_node(rel.target)
    properties = {}
    if rel.properties:
        properties = porps_to_dict(rel.properties)
    return BaseRelationship(
        source=source, target=target, type=rel.type, properties=properties
    )