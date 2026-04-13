import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

def calculate_cost(prompt_tokens, response_tokens):
    cost_per_1m_input = 0.075
    cost_per_1m_output = 0.30
    
    input_cost = (prompt_tokens / 1_000_000) * cost_per_1m_input
    output_cost = (response_tokens / 1_000_000) * cost_per_1m_output
    total_cost = input_cost + output_cost
    
    return total_cost

def ask_gemini(prompt_text):
    print(f"\n--- Запит до AI ---")
    print(f"Запит: {prompt_text}\n")
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt_text,
    )
    
    print("--- Відповідь AI ---")
    print(response.text)
    
    usage = response.usage_metadata
    prompt_tokens = usage.prompt_token_count
    resp_tokens = usage.candidates_token_count
    
    total_cost = calculate_cost(prompt_tokens, resp_tokens)
    
    print("\n--- Статистика використання ---")
    print(f"Витрачено токенів на запит: {prompt_tokens}")
    print(f"Витрачено токенів на відповідь: {resp_tokens}")
    print(f"Загальна вартість: ${total_cost:.6f}")

if __name__ == "__main__":
    prompt_ua = "Що таке штучний інтелект? В кінці відповіді наведіть список джерел із посиланнями."
    ask_gemini(prompt_ua)
    
    prompt_en = "What is artificial intelligence? At the end of your answer, provide a list of sources with references."
    ask_gemini(prompt_en)
