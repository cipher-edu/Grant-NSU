# Grant-NSU: Grantlarni Boshqarish Tizimi

## Umumiy Ma'lumot
Grant-NSU — oliy ta'lim muassasalari uchun talabalar grant arizalarini boshqarish va baholashga mo'ljallangan zamonaviy, qulay va xavfsiz veb-ilova. Tizim orqali talabalar ariza topshiradi, hujjat yuklaydi va natijani kuzatadi. Administratorlar arizalarni ko'rib chiqadi, ball beradi va bildirishnomalar yuboradi.

## Asosiy Imkoniyatlar
- Talabalar uchun ro'yxatdan o'tish va autentifikatsiya (ID yoki SSO orqali)
- Grant arizasini to'ldirish va hujjatlarni dinamik yuklash
- Ijtimoiy faollik mezonlari bo'yicha qat'iy tekshiruv (takror mezonlarga yo'l qo'yilmaydi, maksimal ball nazorati)
- Barcha asosiy modellar uchun UUID asosida xavfsiz identifikatsiya
- Real vaqt rejimida bildirishnomalar (ariza holati va admin harakatlari uchun)
- Moslashuvchan va zamonaviy UI (formsetlar, fayl preview, mobilga mos)
- Admin panel: arizalarni ko'rish, tahrirlash, ball berish
- Apellyatsiya (norozilik) arizasi va hujjat yuklash
- Fayllarni xavfsiz saqlash (PDF, JPG, PNG, DOC, DOCX, 5MB gacha)
- Ko'p tilli interfeys (O'zbek, Rus, Ingliz)
- Docker yordamida tez va oson o'rnatish

## Texnologiyalar
- Python 3.10+
- Django 4.x
- Django REST Framework
- Celery (fon vazifalar va bildirishnomalar uchun)
- PostgreSQL (tavsiya etiladi) yoki SQLite
- Tailwind CSS (CDN orqali)
- Alpine.js (dinamik UI uchun)
- Docker & docker-compose

## Tez Ishga Tushirish
### 1. Repodan yuklab oling
```bash
git clone https://github.com/cipher-edu/Grant-NSU.git
cd Grant-NSU
```

### 2. Virtual muhit yaratish va faollashtirish
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 4. Muhit o'zgaruvchilarini sozlash
- `.env.example` faylini `.env` nomi bilan nusxa oling va sozlamalarni to'ldiring (bazaga ulanish, secret key, email va h.k.).

### 5. Migratsiyalarni bajarish
```bash
python manage.py migrate
```

### 6. Superuser yaratish
```bash
python manage.py createsuperuser
```

### 7. Serverni ishga tushirish
```bash
python manage.py runserver
```

### 8. (Ixtiyoriy) Docker bilan ishga tushirish
```bash
docker-compose up --build
```

## Foydalanish
- `http://localhost:8000/` — asosiy sahifa.
- Talabalar: tizimga kirib, grant arizasini to'ldiradi va hujjat yuklaydi.
- Adminlar: `/admin/` orqali arizalarni ko'rib chiqadi, ball beradi, boshqaradi.
- Muhim harakatlar uchun bildirishnomalar headerda ko'rinadi.

## Asosiy Qoidalar
- Har bir ijtimoiy faollik mezoni uchun faqat bitta hujjat yuklash mumkin (UI va backendda qat'iy nazorat).
- Faqat ruxsat etilgan fayl turlari va hajmi qabul qilinadi.
- Baholashda maksimal balldan oshib ketish mumkin emas.
- Barcha obyektlar (Studentdan tashqari) UUID orqali boshqariladi.

## Loyiha Tuzilmasi
- `auth_app/` — Asosiy Django ilova (model, view, forma, admin, API)
- `external_auth_project/` — Loyihaning sozlamalari, celery, URLlar
- `templates/` — Barcha HTML shablonlar (grant, apellyatsiya, admin, partials)
- `static/` — Statik fayllar (CSS, JS, rasm)
- `media/` — Yuklangan hujjatlar
- `requirements.txt` — Python kutubxonalari
- `Dockerfile`, `docker-compose.yml` — Docker uchun

## Kengaytirish va Moslashtirish
- Yangi grant turi yoki mezon qo'shish uchun: `ApplicationDocument.EvaluationCriterion` (models.py) ni yangilang.
- Bildirishnoma logikasini o'zgartirish uchun: `auth_app/admin.py` va `auth_app/models.py` fayllarini tahrirlang.
- UI dizaynini o'zgartirish uchun: `templates/auth_app/` va `static/` papkalarini tahrirlang.

## Testlash
- Barcha testlarni ishga tushirish:
```bash
python manage.py test
```

## Yordam va Aloqa
Savollar, muammolar yoki takliflar uchun GitHub Issues yoki Pull Request orqali murojaat qiling.

---
© 2025 Cipher Education. Barcha huquqlar himoyalangan.