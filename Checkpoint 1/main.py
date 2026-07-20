import os
import time
import json
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from pydantic import BaseModel, ValidationError

# 1. API İnteqrasiyası 
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("XƏTA: OPENAI_API_KEY .env faylında tapılmadı!")

client = OpenAI(api_key=api_key)


# 5. Çıxış Parsing/Validasiyası üçün Pydantic Modeli 
class SummaryResponse(BaseModel):
    summary: str
    sentiment: str
    key_points: list[str]


def summarize_text(user_input: str):
    # 2. Prompt Engineering
    system_prompt = (
        "Sən peşəkar bir mətn xülasələşdirici köməkçisən. "
        "İstifadəçinin verdiyi mətni xülasə etməli, tonunu (sentiment) təyin etməli və əsas bəndləri çıxarmalısan.\n\n"
        "MÜTLƏQ aşağıdakı JSON formatında cavab verməlisən. Cavaba heç bir əlavə giriş və ya izahedici mətn əlavə etmə.\n"
        "JSON Format nümunəsi (Few-Shot):\n"
        "{\n"
        '  "summary": "Mətnin qısa xülasəsi bura yazılır.",\n'
        '  "sentiment": "Müsbət/Mənfi/Neytral",\n'
        '  "key_points": ["Bənd 1", "Bənd 2"]\n'
        "}"
    )

    # 4. Xata İdarəetməsi 
    max_retries = 3
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            print(f"\n--- LLM Sorğusu Göndərilir (Cəhd {attempt + 1}) ---")

            start_time = time.time()

            # 3. Streaming Cavab İdarəetməsi
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                response_format={"type": "json_object"},
                stream=True
            )

            full_content = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    content_piece = chunk.choices[0].delta.content
                    full_content += content_piece
                    print(content_piece, end="", flush=True)

            print("\n-------------------------------------------")

            # 5. Çıxış Parsing/Validasiyas
            try:
                parsed_json = json.loads(full_content)
                validated_data = SummaryResponse(**parsed_json)
            except (json.JSONDecodeError, ValidationError) as e:
                print(f"Format xətası baş verdi, yenidən cəhd olunur... Xəta: {e}")
                continue

            # 6. Əsas Cost/Token və Vaxt Məlumatlılığı
            estimated_tokens = int(len(full_content.split()) * 1.3)
            estimated_cost = (estimated_tokens / 1_000_000) * 0.60
            duration = time.time() - start_time

            print(f"\n[LOG] Sorğu müddəti: {duration:.2f} saniyə")
            print(f"[LOG] Təxmini çıxış token sayı: {estimated_tokens}")
            print(f"[LOG] Təxmini sorğu xərci: ${estimated_cost:.6f}\n")

            return validated_data.model_dump()

        except OpenAIError as e:
            print(f"API Xətası: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                print("Maksimum cəhd sayına çatıldı. Sorğu uğursuz oldu.")
                return None


# Tətbiqi yoxlamaq üçün test mətni
if __name__ == "__main__":
    test_text = (
        "Süni intellekt texnologiyaları son illərdə sürətlə inkişaf edir. "
        "Xüsusilə böyük dil modelləri (LLM) biznes proseslərinin avtomatlaşdırılmasında "
        "və müştəri xidmətlərində inqilab yaradıb. Lakin bu texnologiyaların tətbiqi "
        "zamanı məlumat təhlükəsizliyi və yüksək API xərcləri kimi çətinliklər hələ də qalmaqdadır."
    )

    result = summarize_text(test_text)
    if result:
        print("Uğurla Validasiya Olunmuş JSON Nəticəsi:")
        print(json.dumps(result, indent=4, ensure_ascii=False))