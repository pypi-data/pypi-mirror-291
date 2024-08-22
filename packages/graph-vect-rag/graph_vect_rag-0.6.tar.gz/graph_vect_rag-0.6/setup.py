from setuptools import setup, find_packages

setup(
    name="graph_vect_rag",
    version=0.6,
    packages=find_packages(),
    install_requires=[
        "llama-index",
        "llama-index-llms-groq",
        "llama-index-embeddings-huggingface",
        "llama-index-graph-stores-neo4j",
        "sentence-transformers",
        "python-dotenv",
        "setuptools",
    ],
    description="A Python package for hybrid Graph + Vector RAG using completely Open Source tools",
    project_urls={
        "Source": "https://github.com/RithikRaj64/graph-vect-rag",
        "Bug Tracker": "https://github.com/RithikRaj64/graph-vect-rag/issues",
    },
)
