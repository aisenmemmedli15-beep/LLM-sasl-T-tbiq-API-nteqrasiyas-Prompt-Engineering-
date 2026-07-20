import os
from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class TextAnalysis(BaseModel):
    summary: str = Field(description="Mətnin xülasəsi")
    sentiment: str = Field(description="Mətnin tonu")
    key_points: list[str] = Field(description="Əsas bəndlər")

def analyze_with_token_tracking(user_input: str):
    # gpt-4o-mini üçün cari qiymətlər (1M token başına dollarla)
    INPUT_PRICE_PER_1K = 0.00015 / 1000
    OUTPUT_PRICE_PER_1K = 0.0006 / 1000

    try:
        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_input}],
            response_format=TextAnalysis
        )
        
        # TAPSIRIQ TƏLƏBİ: Token istifadəsinin API-dan götürülməsi
        usage = response.usage
        prompt_tokens = usage.prompt_tokens
        completion_tokens = usage.completion_tokens
        total_tokens = usage.total_tokens
        
        # Xərcin hesablanması
        cost = (prompt_tokens * INPUT_PRICE_PER_1K) + (completion_tokens * OUTPUT_PRICE_PER_1K)
        
        print(f"\n[TOKEN LOG]")
        print(f"Giriş (Prompt) Token: {prompt_tokens}")
        print(f"Çıxış (Completion) Token: {completion_tokens}")
        print(f"Toplam Token: {total_tokens}")
        print(f"Təxmini Xərc: ${cost:.6f}")
        
        return response.choices[0].message.parsed

    except Exception as e:
        print(f"Xəta baş verdi: {e}")
        return None

if __name__ == "__main__":
    analyze_with_token_tracking("Süni intellekt layihələrində xərclərin idarə olunması vacibdir.")
