import os
from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# .env faylındakı mühit dəyişənlərini yükləyirik
load_dotenv()

# OpenAI müştərisini başladırıq (API açarını .env faylından avtomatik oxuyur)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 1. Pydantic Modeli: Cavabın strukturunu təyin edirik
class TextAnalysis(BaseModel):
    summary: str = Field(description="Mətnin əsas ideyasını qısaca izah edən xülasə")
    sentiment: str = Field(description="Mətnin tonu: POSITIVE, NEGATIVE və ya NEUTRAL")
    key_points: list[str] = Field(description="Mətnin içindəki ən vacib məqamların siyahısı")

def analyze_text(user_input: str):
    # 2. Sistem təlimatı (System Prompt)
    system_prompt = (
        "Sən peşəkar bir Mətn Analizi və Xülasələndirmə AI assistentisən. "
        "Sənə təqdim olunan mətni analiz etməli və tələb olunan JSON strukturuna uyğun cavab verməlisən."
    )

    try:
        # 3. OpenAI API sorğusu (System, Few-shot və User Prompt daxil olmaqla)
        response = client.beta.chat.completions.parse(
            model="gpt-4o-mini",  # və ya istifadə etdiyiniz digər model
            messages=[
                # System Prompt
                {"role": "system", "content": system_prompt},
                
                # Few-Shot Nümunə (Nümunə 1 - User)
                {"role": "user", "content": "Bu gün aldığım məhsul çox keyfiyyətsiz çıxdı. Həm çatdırılma gecikdi, həm də qutusu cırılmışdı. Heç kəsə məsləhət görmürəm, pullarım boşa getdi."},
                # Few-Shot Nümunə (Nümunə 1 - Assistant)
                {"role": "assistant", "content": '{"summary": "İstifadəçi aldığı məhsulun keyfiyyətindən, çatdırılma gecikməsindən və qablaşdırmadan narazıdır.", "sentiment": "NEGATIVE", "key_points": ["Məhsul keyfiyyətsizdir.", "Çatdırılmada gecikmə baş verib.", "Qablaşdırma zədəlidir."]}'},
                
                # Real User Prompt (İstifadəçinin daxil etdiyi əsas mətn)
                {"role": "user", "content": f"Aşağıdakı mətni analiz et və JSON olaraq qaytar:\n{user_input}"}
            ],
            response_format=TextAnalysis, # Pydantic modelini bura bağlayırıq
            temperature=0.2 # Cavabın daha stabil və strukturlu olması üçün
        )

        # Strukturlu cavabı geri qaytarırıq
        return response.choices[0].message.parsed

    except Exception as e:
        print(f"Xəta baş verdi: {e}")
        return None

# Proqramı yoxlamaq üçün nümunə mətn
if __name__ == "__main__":
    test_text = (
        "Süni intellekt texnologiyaları son illərdə sürətlə inkişaf edir. "
        "Bu texnologiya bir çox sahədə işləri asanlaşdırsa da, bəzi peşələrin sıradan çıxması "
        "və işsizlik riskini də özü ilə gətirir. Təhsil və tibb sahəsində isə böyük dönüş yaradıb."
    )
    
    print("Mətn analiz edilir...\n")
    result = analyze_text(test_text)
    
    if result:
        print("--- ANALİZ NƏTİCƏSİ ---")
        print(f"Xülasə: {result.summary}")
        print(f"Ton (Sentiment): {result.sentiment}")
        print("Əsas Bəndlər:")
        for point in result.key_points:
            print(f"- {point}")