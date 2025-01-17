from app.helpers.split_text_recursive import split_text_recursive
from app.helpers.gemini_embedding import gemini_embedding
from app.lancedb import TextEmbeddingSchema
from app.lancedb import add_record
from app.helpers.sqlite_db import save_note
from uuid import uuid4


async def create(note: str) -> dict:
    # Generate a unique ID for the note
    note_id = str(uuid4())
    
    # Save the full note to SQLite
    save_note(note_id, note)

    # Split the text into chunks for vector storage
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
            note_id=note_id,  # Reference to the original note
        )

        # Add the record to the list
        lance_db_records.append(item)

    # Add the records to the table
    await add_record(
        table_name="notes",
        records=lance_db_records,
    )
    print("Embedding Processed")
    
    return {
        "id": note_id,
        "content": note
    }
