#Çıxış Parsing və Validasiyası
Bu layihə, Böyük Dil Modellərindən (LLM) gələn cavabların strukturlaşdırılmasını (JSON) və yarana biləcək korrupt (zədələnmiş) cavabların təhlükəsiz şəkildə tutulmasını nümayiş etdirir.
#Özəlliklər
- Structured Outputs (OpenAI): Modelin çıxışı birbaşa generasiya mərhəsində müəyyən edilmiş Pydantic sxeminə məcbur edilir.
- Tip və Sxem Validasiyası:Cavabın daxilindəki məlumat tipləri (str, list və s.) Pydantic tərəfindən avtomatik yoxlanılır.
- Korrupt Cavab İdarəetməsi: Model təsadüfən səhv və ya natamam JSON qaytararsa, sistem `ValidationError` blokuna düşür, xəta təhlükəsiz loglanır və tətbiqin çökməsinin (runtime crash) qarşısı alınır.
#Quraşdırılma və İşə salınma

1. Lazımi kitabxanaları yükləyin:
   ```bash
   pip install -r requirements.txt
