from typing import Any
from app.lancedb import VectorSearchResult
from app.lancedb import vector_search
from app.helpers.gemini_embedding import gemini_embedding

async def semantic_search(text: str) -> list[VectorSearchResult]:
    # Get the embedding for the text
    embedding = await gemini_embedding(text)
    if embedding is None:
        raise Exception("Failed to generate embeddings")

    # Get the similar notes
    notes = await vector_search("notes", embedding)
    return notes
