AI Mətn Analizi və Xülasələndirmə Aləti

Bu layihə, OpenAI API və Pydantic vasitəsilə daxil edilən mətnlərin strukturlaşdırılmış analizini aparan Python proqramıdır. Sistem verilən mətndən qısa xülasə çıxarır, mətnin tonunu (sentiment) təyin edir və əsas bəndləri siyahı şəklində təqdim edir. Özəlliklər

Strukturlu JSON Çıxışı:OpenAI-ın parse metodu və Pydantic modelləri sayəsində cavabların dəqiq strukturda alınması.
Few-Shot Prompting:AI-ın verilən tapşırığı daha dəqiq anlaması üçün sistemə nümunə promptların ötürülməsi.
Təhlükəsizlik:API açarlarının .env faylı daxilində qorunması. Quraşdırılma
Layihə qovluğuna keçid edin və lazım olan kitabxanaları yükləyin:
pip install -r requirements.txt