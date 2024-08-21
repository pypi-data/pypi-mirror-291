from setuptools import setup, find_packages

setup(
    name="graph_vect_rag",
    version=0.4,
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
)
