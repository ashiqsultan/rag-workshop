from typing import List
from lancedb.pydantic import Vector, LanceModel
import lancedb
from pydantic import BaseModel


class TextEmbeddingSchema(LanceModel):
    id: str  # Unique identifier for the record
    text: str  # Chunk of text from the document
    vector: Vector(768)  # 768 is the dimension for gemini text-embedding-004


class VectorSearchResult(BaseModel):
    text: str
    doc_id: str


DB_PATH = "lance_storage/default-db"


# Function to create and get table
async def get_or_create_table(table_name: str = "default_table"):
    # Connect to local LanceDB
    db = await lancedb.connect_async(DB_PATH)

    # Create table if it doesn't exist
    try:
        table = await db.open_table(table_name)
    except:
        table = await db.create_table(table_name, schema=TextEmbeddingSchema)
    return table


async def add_record(table_name: str, records: list[TextEmbeddingSchema]):
    try:
        table = await get_or_create_table(table_name)
        await table.add(records)
    except Exception as e:
        print("Error in add_record: ")
        print(e)
        raise e


async def delete_records_by_doc_id(table_name: str, doc_id: str) -> bool:
    try:
        table = await get_or_create_table(table_name)
        await table.delete(where=f"doc_id = '{doc_id}'")
        print(f"Deleted records with doc_id: {doc_id}")
        return True
    except Exception as e:
        print(f"Error deleting records by doc_id: {e}")
        return False


async def vector_search(
    table_name: str,
    query_vector: List[float],
    limit: int = 10,
) -> List[VectorSearchResult]:
    try:
        table = await get_or_create_table(table_name)
        results = (
            await table.vector_search(query_vector)
            .select(["text", "id"])
            .limit(limit)
            .to_pandas()
        )
        return [VectorSearchResult(**row) for row in results.to_dict("records")]
    except Exception as e:
        print(f"Error in vector_search: {e}")
        return []
