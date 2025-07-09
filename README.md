Albatta, sizning loyihangiz endi "So'rovnoma" emas, balki "Grantlar Tizimi" bo'lganini hisobga olib, README.md faylini to'liq qayta yozib, yangi funksionallikka mos, professional va tushunarli ko'rinishga keltiraman.

🎓 Grantlarni Taqsimlash Tizimi
Oliy ta'lim muassasalari uchun grantlarni shaffof boshqarish va taqsimlash platformasi

![alt text](https://img.shields.io/badge/Django-4.2-blue?logo=django&logoColor=white)


![alt text](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)


![alt text](https://img.shields.io/badge/PostgreSQL-14-blue?logo=postgresql&logoColor=white)


![alt text](https://img.shields.io/badge/Celery-5.x-green?logo=celery)


![alt text](https://img.shields.io/badge/Tailwind_CSS-3.x-blue?logo=tailwindcss&logoColor=white)


![alt text](https://img.shields.io/badge/Litsenziya-MIT-green)

Ushbu loyiha O'zbekiston Respublikasi Vazirlar Mahkamasining tegishli qarori asosida, oliy ta'lim muassasalarida talabalarga grantlarni adolatli va shaffof taqdim etish hamda qayta taqsimlash jarayonlarini to'liq avtomatlashtirish uchun ishlab chiqilgan. Tizim talabalarga o'z yutuqlarini yuklash, arizalarini kuzatib borish va apellyatsiya berish imkonini beradi. Komissiya a'zolari uchun esa baholash jarayonini osonlashtiradigan qulay admin paneli mavjud.

✨ Asosiy Imkoniyatlar

Tashqi API orqali Autentifikatsiya: Talabalar HEMIS tizimidagi login va parollari orqali xavfsiz tarzda tizimga kiradilar.

Nizomga To'liq Moslik: Tizim grantlarni taqsimlash bo'yicha barcha mezonlar, jumladan, akademik ko'rsatkich (GPA) va 11 banddan iborat ijtimoiy faollikni baholashni to'liq qo'llab-quvvatlaydi.

Dinamik Ariza Topshirish: Talabalar grant turini tanlab, o'z yutuqlarini (diplom, sertifikat va h.k.) tasdiqlovchi hujjatlarni osongina yuklay oladilar.

Interaktiv Admin Paneli: Komissiya a'zolari uchun maxsus ishlab chiqilgan panelda arizalarni ko'rish, talaba yuklagan hujjatlarni tekshirish va baholash varaqasini to'ldirish jarayoni maksimal darajada qulaylashtirilgan.

Bildirishnomalar Tizimi: Ariza holati o'zgarganda yoki yangi hodisa yuz berganda, talabalar va adminlarga real vaqtda bildirishnomalar yuboriladi.

Apellyatsiya Jarayoni: Arizasi natijasidan norozi bo'lgan talabalar uchun tizim orqali apellyatsiya berish va uni ko'rib chiqish mexanizmi joriy etilgan.

Asinxron Vazifalar (Celery): Bildirishnomalarni yuborish va kelajakda hisobotlarni yaratish kabi operatsiyalar fonda bajariladi, bu esa tizimning doimiy tez ishlashini ta'minlaydi.

Zamonaviy va Adaptiv Dizayn: Tailwind CSS va Alpine.js yordamida yaratilgan interfeys barcha qurilmalarda mukammal ishlaydi.

⚙️ Texnologiyalar Steki
Kategoriya	Texnologiya
Backend	Django, Django REST Framework, Simple JWT, Django Channels
Frontend	HTML5, Tailwind CSS, Alpine.js, JavaScript
Ma'lumotlar Baza	PostgreSQL (Production), SQLite3 (Development)
Asinxron Vazifalar	Celery, Redis (Broker va Natijalar uchun)
Server	Gunicorn / uWSGI, Nginx, Daphne (Channels uchun)
🔧 O'rnatish va Ishga Tushirish

Loyihani lokal kompyuteringizda ishga tushirish uchun quyidagi qadamlarni bajaring:

1. Loyihani yuklab oling va papkaga o'ting:

Generated bash
git clone https://github.com/sizning-username/grant-system.git
cd grant-system


2. Virtual muhit yaratish va aktivlashtirish:

Generated bash
# Windows: python -m venv venv && venv\Scripts\activate
# MacOS/Linux: python3 -m venv venv && source venv/bin/activate
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

3. Kerakli kutubxonalarni o'rnating:

Generated bash
pip install -r requirements.txt
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

4. Muhit o'zgaruvchilarini sozlang:
.env.example faylidan nusxa olib, .env nomli yangi fayl yarating va uni o'zingizning ma'lumotlaringiz (API manzili, maxfiy kalit va h.k.) bilan to'ldiring.

Generated bash
cp .env.example .env
# nano .env yoki boshqa muharrir bilan tahrirlang
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

5. Ma'lumotlar bazasini sozlang (migratsiyalar):

Generated bash
python manage.py migrate
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

6. Superuser (admin) yarating:

Generated bash
python manage.py createsuperuser
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

7. Admin panelida kerakli guruhlarni yarating:
Tizim to'g'ri ishlashi uchun admin paneliga kirib, "Groups" bo'limida Komissiya nomli guruh yarating va unga baholashda qatnashadigan adminlarni qo'shing.

🚀 Loyihani Ishga Tushirish

Loyihani to'liq ishga tushirish uchun 2 ta alohida terminal oynasi kerak bo'ladi.

1-Terminal: Celery worker'ni ishga tushirish (Bildirishnomalar va fon vazifalari uchun)

Generated bash
celery -A your_project_name worker -l info
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

your_project_name o'rniga loyihangizning asosiy papkasi nomini yozing.

2-Terminal: Django serverini ishga tushirish

Generated bash
python manage.py runserver
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Endi loyiha http://127.0.0.1:8000/ manzilida ishlayotgan bo'lishi kerak.

🐳 Docker yordamida Ishga Tushirish

Production muhiti uchun Docker'dan foydalanish tavsiya etiladi.

1. Docker imijlarini yaratish va konteynerlarni ishga tushirish:

Generated bash
docker-compose up -d --build
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

2. Migratsiyalarni bajarish va admin yaratish:
Konteynerlar ishga tushgandan so'ng, quyidagi buyruqlarni bajaring:

Generated bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Admin paneliga kirib, Komissiya guruhini yaratishni unutmang.

Asosiy sahifa: http://localhost:8000/

Admin panel: http://localhost:8000/admin/

📂 Loyiha Strukturasi
Generated code
├── auth_app/                # Asosiy ilova
│   ├── migrations/
│   ├── services/            # Tashqi API bilan ishlash uchun servislar
│   ├── tasks.py             # Celery vazifalari
│   ├── templates/           # HTML shablonlar
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   └── ...
├── your_project_name/       # Loyihaning asosiy sozlamalari
│   ├── settings.py
│   ├── urls.py
│   └── celery.py
├── manage.py
├── requirements.txt
├── .env
├── docker-compose.yml
└── README.md
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END
📜 Litsenziya

Ushbu loyiha MIT litsenziyasi ostida tarqatiladi. Batafsil ma'lumot uchun LICENSE faylini ko'ring.