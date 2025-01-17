from app.notes.semantic_search import semantic_search
from app.helpers.gemini_chat import gemini_chat


async def rag_answer(text: str):
    notes = await semantic_search(text)
    # Convert the notes to string format
    notes_str = "\n".join([note.text for note in notes])
    answer = await gemini_chat(text, notes_str)
    return answer
