AI Mətn Analizi və Xülasələndirmə Aləti

Bu layihə, OpenAI API və Pydantic vasitəsilə mətni analiz edən, onun əsas xülasəsini, sentimentini (tonunu) və vacib bəndlərini çıxaran Python tətbiqidir.
#Özəlliklər
Structured Outputs (Pydantic):Gələn cavabın dəqiq JSON strukturunda olması təmin edilib.
Few-Shot Prompting:Modelə daha dəqiq analiz apara bilməsi üçün sistemə nümunələr verilmişdir.
Streaming Support:Real vaxt rejimində token axını izlənilir.
Error Handling & Retry:Şəbəkə kəsintiləri və Rate Limit xətalarına qarşı dayanıqlı dayaq sistemi qurulub. #Quraşdırılma
Kitabxanaları quraşdırın:
pip install -r requirements.txt
