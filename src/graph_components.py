from langchain_community.graphs.graph_document import (
    Node as BaseNode,
    Relationship as BaseRelationship,
    GraphDocument,
)
from langchain.schema import Document
from typing import List, Dict, Any, Optional
from langchain.pydantic_v1 import Field, BaseModel

class Property(BaseModel):
    """A single property consisting of key and value"""
    key: str = Field(..., description="The property key")
    value: str = Field(..., description="The property value")

class Node(BaseNode):
    """A graph node with properties"""
    properties: Optional[List[Property]] = Field(None, description="List of properties for the node")

class Relationship(BaseRelationship):
    """A graph relationship with properties"""
    properties: Optional[List[Property]] = Field(None, description="List of properties for the relationship")

class knowledgeGraph(BaseModel):
    """A knowledge graph consisting of nodes and relationships"""
    nodes: List[Node] = Field(..., description="List of nodes in the graph")
    rels: List[Relationship] = Field(..., description="List of relationships in the graph")
