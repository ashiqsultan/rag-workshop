from app.helpers.split_text_recursive import split_text_recursive
from app.helpers.gemini_embedding import gemini_embedding
from app.lancedb import get_or_create_table
from app.lancedb import TextEmbeddingSchema
from app.lancedb import add_record
from uuid import uuid4


async def create(note: str) -> bool:
    # Split the text into chunks
    chunks = split_text_recursive(note)

    # Create an empty list for records
    lance_db_records: list[TextEmbeddingSchema] = []

    # Process each chunk
    for i, chunk in enumerate(chunks, 1):
        print(f"Processing chunk {i} of {len(chunks)}")

        # Generate the embedding for each chunk
        embedding = await gemini_embedding(chunk)
        if embedding is None:
            raise Exception("Failed to generate embeddings")

        # Create the record
        item = TextEmbeddingSchema(
            id=str(uuid4()),
            text=chunk,  # The text of the chunk
            vector=embedding,  # The embedding Array of the chunk
        )

        # Add the record to the list
        lance_db_records.append(item)

    # Add the records to the table
    await add_record(
        table_name="notes",
        records=lance_db_records,
    )
    print("Embedding Processed")
    return True
