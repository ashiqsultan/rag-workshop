import google.generativeai as genai
import os
import asyncio


async def gemini_embedding(text: str):
    try:
        model = "models/text-embedding-004"
        API_KEY = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=API_KEY)
        result = await genai.embed_content_async(model=model, content=text)
        embedding = result["embedding"]
        return embedding
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return None


if __name__ == "__main__":
    text = "Hello, world!"
    embedding = asyncio.run(gemini_embedding(text))
    print(embedding)