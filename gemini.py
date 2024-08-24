import google.generativeai as genai  # type: ignore
import os
from dotenv import load_dotenv
import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("API key not found. Make sure 'GEMINI_API_KEY' is set in your environment variables.")

genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-1.5-flash')

def generate(prompt: str) -> str:
    enhanced_prompt = (
        "Respond in a friendly and conversational tone. "
        "The program has already greeted the user, so no need to say hello again. "
        "This is the only response you will ever send to the user, so don't "
        "say something like 'What's making you smile today?'. "
        f"Here is the user's input: {prompt}. "
        "If the user's input is in all lowercase, respond in all lowercase. "
        "If the user's input is properly formatted, respond with proper formatting. "
        "Always finish your response by asking the user what they need help with."
    )
    response = model.generate_content(enhanced_prompt)
    return response.text.strip()
