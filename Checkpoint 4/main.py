import os
import time
import openai
from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# .env faylındakı mühit dəyişənlərini yükləyirik
load_dotenv()

# OpenAI müştərisini başladırıq
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 1. Pydantic Modeli: Cavabın strukturunu təyin edirik
class TextAnalysis(BaseModel):
    summary: str = Field(description="Mətnin əsas ideyasını qısaca izah edən xülasə")
    sentiment: str = Field(description="Mətnin tonu: POSITIVE, NEGATIVE və ya NEUTRAL")
    key_points: list[str] = Field(description="Mətnin içindəki ən vacib məqamların siyahısı")

# Xəta İdarəetməsi və Təkrar Cəhd (Retry) ilə Strukturlu Analiz Funksiyası (Checkpoint 4 üçün)
def analyze_text_with_retry(user_input: str, retries=3, delay=2):
    system_prompt = (
        "Sən peşəkar bir Mətn Analizi və Xülasələndirmə AI assistentisən. "
        "Sənə təqdim olunan mətni analiz etməli və tələb olunan JSON strukturuna uyğun cavab verməlisən."
    )

    for attempt in range(retries):
        try:
            response = client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": "Bu gün aldığım məhsul çox keyfiyyətsiz çıxdı. Həm çatdırılma gecikdi, həm də qutusu cırılmışdı. Heç kəsə məsləhət görmürəm, pullarım boşa getdi."},
                    {"role": "assistant", "content": '{"summary": "İstifadəçi aldığı məhsulun keyfiyyətindən, çatdırılma gecikməsindən və qablaşdırmadan narazıdır.", "sentiment": "NEGATIVE", "key_points": ["Məhsul keyfiyyətsizdir.", "Çatdırılmada gecikmə baş verib.", "Qablaşdırma zədəlidir."]}'},
                    {"role": "user", "content": f"Aşağıdakı mətni analiz et və JSON olaraq qaytar:\n{user_input}"}
                ],
                response_format=TextAnalysis,
                temperature=0.2,
                timeout=10.0  # Şəbəkə gecikmələrinə qarşı timeout
            )
            return response.choices[0].message.parsed

        except openai.APITimeoutError:
            print(f"Xəta: Timeout baş verdi. Cəhd {attempt + 1}/{retries}...")
        except openai.RateLimitError:
            print(f"Xəta: Rate limit aşıldı. {delay} saniyə gözlənilir...")
            time.sleep(delay)
        except openai.APIStatusError as e:
            print(f"API Status Xətası (Kod: {e.status_code}): {e.message}")
            break
        except openai.APIError as e:
            print(f"Ümumi OpenAI API Xətası: {e}")
            break
        except Exception as e:
            print(f"Gözlənilməz xəta: {e}")
            break
        
        # Exponential backoff məntiqi ilə gözləmə müddətini artırırıq
        time.sleep(delay * (attempt + 1))
        
    print("Maksimum cəhd sayına ulaşıldı, sorğu uğursuz oldu.")
    return None

# Streaming (Axınlı) Analiz Funksiyası
def analyze_text_stream(user_input: str):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Sən peşəkar bir Mətn Analizi assistentisən."},
                {"role": "user", "content": f"Mətni analiz et:\n{user_input}"}
            ],
            stream=True
        )
        print("AI Real-Time Cavabı: ", end="", flush=True)
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="", flush=True)
        print("\n")
    except Exception as e:
        print(f"Streaming zamanı xəta baş verdi: {e}")

# Test Hissəsi
if __name__ == "__main__":
    test_text = (
        "Süni intellekt texnologiyaları son illərdə sürətlə inkişaf edir. "
        "Bu texnologiya bir çox sahədə işləri asanlaşdırsa da, bəzi peşələrin sıradan çıxması "
        "və işsizlik riskini də özü ilə gətirir. Təhsil və tibb sahəsində isə böyük dönüş yaradıb."
    )
    
    print("--- XƏTA İDARƏETMƏLİ STRUKTURLU ANALİZ ---")
    result = analyze_text_with_retry(test_text)
    if result:
        print(f"Xülasə: {result.summary}")
        print(f"Ton (Sentiment): {result.sentiment}")
        print("Əsas Bəndlər:")
        for point in result.key_points:
            print(f"- {point}")
            
    print("\n----------------------------------\n")
    
    print("--- STREAMING (AXINLI) ANALİZ ---")
    analyze_text_stream(test_text)
