#AI Mətn Analizi və Xülasələndirmə Aləti

Bu layihə, OpenAI API və Pydantic vasitəsilə mətni analiz edən, onun əsas xülasəsini, sentimentini (tonunu) və vacib bəndlərini çıxaran Python tətbiqidir. Layihədə həm strukturlu JSON çıxışı, həm də Streaming (axınlı) cavab idarəetməsi reallaşdırılıb.

#Özəlliklər
- Structured Outputs (Pydantic): Gələn cavabın dəqiq JSON strukturunda olması təmin edilib.
- Few-Shot Prompting:Modelə daha dəqiq analiz apara bilməsi üçün nümunələr verilmişdir.
- Streaming Support:Böyük mətnlərin cavabını gözləmədən real vaxt rejimində token axını izlənilir.

#Quraşdırılma

1. Kitabxanaları quraşdırın:
   ```bash
   pip install -r requirements.txt