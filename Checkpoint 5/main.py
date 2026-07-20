import os
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError
from dotenv import load_dotenv

# .env faylından API açarını yükləyirik
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 1. Gözlənilən JSON strukturunu Pydantic modeli ilə təyin edirik
class TextAnalysis(BaseModel):
    summary: str = Field(description="Mətnin xülasəsi")
    sentiment: str = Field(description="Mətnin tonu")
    key_points: list[str] = Field(description="Əsas bəndlərin siyahısı")

# 2. Sırf Validasiya və Korrupt (Zədəli) cavabları tutan funksiya
def parse_and_validate_output(user_input: str):
    try:
        # Structured Outputs dəstəyi ilə API sorğusu göndərilir
        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Mətni analiz et və JSON olaraq qaytar."},
                {"role": "user", "content": user_input}
            ],
            response_format=TextAnalysis
        )
        # Əgər hər şey düzgündürsə, JSON avtomatik parse olunub qaytarılır
        return response.choices[0].message.parsed

    except ValidationError as e:
        # TAPSIRIQ TƏLƏBİ: Model zədəli və ya sxemə uymayan JSON qaytarsa, bura işə düşür
        print("\n[ALERT] Korrupt və ya sxemə uyğun olmayan cavab tutuldu!")
        print(f"Validasiya Xətası Detalları: {e.json()}")
        return None
        
    except Exception as e:
        print(f"Digər xəta: {e}")
        return None

# Test işə salınması
if __name__ == "__main__":
    sample_text = "Süni intellekt sürətlə inkişaf edir, bu həm faydalı, həm də risklidir."
    
    print("--- Sırf Çıxış Parsing / Validasiya Testi ---")
    result = parse_and_validate_output(sample_text)
    
    if result:
        print(f"Uğurlu Parse Olundu! Xülasə: {result.summary}")
