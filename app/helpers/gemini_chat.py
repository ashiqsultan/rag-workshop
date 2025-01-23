import os
import google.generativeai as genai
import json
from google.generativeai.types import generation_types

ERROR_MESSAGE = "Sorry, I'm having trouble processing your request. Please try again later."

async def gemini_chat(user_message: str, knowledge_base: str):
    try:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])

        system_instruction = f"""
        You are an helpful assistant. Answer user questions using the provided knowledge base.

        KNOWLEDGEBASE BEGINS
        {knowledge_base}
        KNOWLEDGEBASE ENDS

        Don't make up an answer. If the question is not related to the knowledge base, just say "I don't know"
        Output Instructions:
        The Output must be a JSON in the following format
        {{"reply": "string"}}
        """

        generation_config = generation_types.GenerationConfig(
            temperature=1,
            top_p=0.95,
            top_k=40,
            max_output_tokens=8192,
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "properties": {"reply": {"type": "string"}},
                "required": ["reply"],
            },
        )

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash-8b",
            generation_config=generation_config,
            system_instruction=system_instruction,
        )

        chat_session = model.start_chat(history=[])
        response = await chat_session.send_message_async(user_message)
        json_response = json.loads(response.text)
        if "reply" in json_response:
            return json_response["reply"]
        else:
            return ERROR_MESSAGE

    except Exception as e:
        print(f"Error in gemini_chat: {e}")
        # Gracefully handle the error
        return ERROR_MESSAGE
