AI Mətn Xülasələşdirici və Analiz Aləti

Bu layihə, OpenAI API-dan istifadə edərək daxil edilən mətnlərin qısa xülasəsini (summary), tonunu (sentiment) və əsas bəndlərini (key points) çıxaran Python proqramıdır. Cavablar Pydantic vasitəsilə validasiya olunur və real vaxt rejimində (streaming) konsola çıxarılır.

Features (Özəlliklər)

Təhlükəsiz API İdarəetməsi: API açarları .env faylında saxlanılır və .gitignore vasitəsilə qorunur.
Structured JSON Output:OpenAI JSON modu və Pydantic modelləri ilə qəti strukturlaşdırılmış və yoxlanılmış cavab mexanizmi.
Real-time Streaming:Cavabın real vaxtda hissə-hissə ekrana yazdırılması.
Xəta və Cəhd İdarəetməsi (Retry Mechanism):** API xətaları zamanı avtomatik cəhd etmə mexanizmi.
Log və Metriklər: Sorğunun icra müddəti, təxmini token sayı və xərci ($) hesablanaraq konsolda göstərilir. Konfiqurasiya (Quraşdırılma)
Kitabxanaların quraşdırılması Terminalda layihə qovluğuna keçid edin və lazımi kitabxanaları yükləyin:
pip install -r requirements.txt