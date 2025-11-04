import os
import openai
import getpass
from langchain_openai import ChatOpenAI
from langchain.graphs import Neo4jGraph
from langchain.chains.openai_functions import (
    create_openai_fn_chain,
    create_structured_output_chain,
)
from langchain.prompts import ChatPromptTemplate
from typing import List, Dict, Any, Optional

from src.graph_components import knowledgeGraph
from src.utilities import map_to_base_node, map_to_base_relationship

# Neo4j connection details
url = "bolt://localhost:7687"
username ="neo4j"
password = "pleaseletmein"

def get_extraction_chain(llm: ChatOpenAI, 
                         allowed_nodes: Optional[List[str]]=None, allowed_rels: Optional[List[str]]=None, 
                         prompt_template: str="Extract the knowledge graph from the following text:"):
    """Create an extraction chain for knowledge graph extraction"""
    prompt = ChatPromptTemplate.from_messages([(
          "system",
          """# Knowledge Graph Instructions for GPT-4
## 1. Overview
You are a top-tier algorithm designed for extracting information in structured formats to build a knowledge graph.
- **Nodes** represent entities and concepts. They're akin to Wikipedia nodes.
- The aim is to achieve simplicity and clarity in the knowledge graph, making it accessible for a vast audience.
## 2. Labeling Nodes
- **Consistency**: Ensure you use basic or elementary types for node labels.
  - For example, when you identify an entity representing a person, always label it as **"person"**. Avoid using more specific terms like "mathematician" or "scientist".
- **Node IDs**: Never utilize integers as node IDs. Node IDs should be names or human-readable identifiers found in the text.
'- **Allowed Node Labels:**' + {allowed_nodes_combined}
'- **Allowed Relationship Types**:' +  {allowed_rels_combined}
## 3. Handling Numerical Data and Dates
- Numerical data, like age or other related information, should be incorporated as attributes or properties of the respective nodes.
- **No Separate Nodes for Dates/Numbers**: Do not create separate nodes for dates or numerical values. Always attach them as attributes or properties of nodes.
- **Property Format**: Properties must be in a key-value format.
- **Quotation Marks**: Never use escaped single or double quotes within property values.
- **Naming Convention**: Use camelCase for property keys, e.g., `birthDate`.
## 4. Coreference Resolution
- **Maintain Entity Consistency**: When extracting entities, it's vital to ensure consistency.
If an entity, such as "John Doe", is mentioned multiple times in the text but is referred to by different names or pronouns (e.g., "Joe", "he"),
always use the most complete identifier for that entity throughout the knowledge graph. In this example, use "John Doe" as the entity ID.
Remember, the knowledge graph should be coherent and easily understandable, so maintaining consistency in entity references is crucial.
## 5. Strict Compliance
Adhere to the rules strictly. Non-compliance will result in termination.
          """.format(allowed_nodes_combined= ", ".join(allowed_nodes) if allowed_nodes else ""
                     , allowed_rels_combined=", ".join(allowed_rels) if allowed_rels else "")),
            ("human", "Use the given format to extract information from the following input: {input}"),
            ("human", "Tip: Make sure to answer in the correct format"),
    ])
    return create_structured_output_chain(llm, prompt, verbose=False)
    

def main():
    # Set up
    APIKEY = input("Enter your OpenAI API Key: ")
    os.environ["OPENAI_API_KEY"] = APIKEY
    llm = ChatOpenAI(
        model="gpt-5o-mini",
        temperature=0,
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    graph = Neo4jGraph(
        url=url,
        username=username,
        password=password,
    )

if __name__ == "__main__":
    main()
