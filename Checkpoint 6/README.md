#Əsas Cost/Token Məlumatlılığı
Bu layihə, OpenAI API sorğuları zamanı xərclənən tokenlərin real vaxt rejimində monitorinqini və maliyyət təxminlərinin (Cost Tracking) hesablanmasını təmin edir.
#Layihənin Prinsipləri
- Token Analitikası (Observability): Hər sorğunun sonunda `usage` obyekti vasitəsilə giriş (prompt) və çıxış (completion) tokenləri qranulyar səviyyədə izlənilir.
- FinOps (Maliyyə Monitorinqi):`gpt-4o-mini` modelinin cari qiymət strukturuna əsasən hər sorğunun maliyyə xərci dollar qarşılığı ilə hesablanır və loglanır.
#Quraşdırılma
1. Asılılıqları quraşdırın:
   ```bash
   pip install -r requirements.txt
