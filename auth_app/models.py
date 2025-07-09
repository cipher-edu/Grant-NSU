# auth_app/models.py
from decimal import Decimal  # <-- YECHIM UCHUN IMPORT
from django.db import models
from django.utils import timezone
from django.conf import settings # Foydalanuvchi modelini olish uchun (agar Student o'rniga standart User ishlatilsa)
import os # Fayl nomini tozalash uchun
from uuid import uuid4 # Unikal fayl nomlari uchun
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

# --- Mavjud Student modeli (o'zgarishsiz qoldiriladi) ---
class Student(models.Model):
    username = models.CharField(
        max_length=150, unique=True,
        verbose_name="Foydalanuvchi nomi (login)",
        help_text="Tizimga kirish uchun foydalaniladigan login (Talaba ID raqami)"
    )
    student_id_number = models.CharField(max_length=50, unique=True, null=True, blank=True,
                                         verbose_name="Talaba ID raqami (API)",
                                         help_text="API dan olingan talabaning ID raqami")
    api_user_hash = models.CharField(max_length=255, unique=True, null=True, blank=True,
                                     verbose_name="API foydalanuvchi hash",
                                     help_text="API dagi foydalanuvchi uchun unikal SHA256 hash")
    first_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ismi")
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Familiyasi") # API dagi 'second_name'
    patronymic = models.CharField(max_length=100, blank=True, null=True, verbose_name="Otasining ismi") # API dagi 'third_name'
    full_name_api = models.CharField(max_length=255, blank=True, null=True, verbose_name="To'liq F.I.Sh. (API)")
    short_name_api = models.CharField(max_length=100, blank=True, null=True, verbose_name="Qisqa F.I.Sh. (API)")

    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Talabning surati (URL)")
    birth_date_timestamp = models.BigIntegerField(null=True, blank=True, verbose_name="Tug'ilgan sana (timestamp)")
    passport_pin = models.CharField(max_length=50, blank=True, null=True, verbose_name="Pasport PIN")
    passport_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Pasport raqami")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    phone = models.CharField(max_length=30, blank=True, null=True, verbose_name="Telefon raqami")

    gender_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="Jinsi kodi")
    gender_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Jinsi")

    university_name_api = models.CharField(max_length=255, blank=True, null=True, verbose_name="Universitet nomi (API)")

    # Specialty (Mutaxassislik)
    specialty_id_api = models.CharField(max_length=100, blank=True, null=True, verbose_name="Mutaxassislik ID (API)")
    specialty_code_api = models.CharField(max_length=50, blank=True, null=True, verbose_name="Mutaxassislik kodi (API)")
    specialty_name_api = models.CharField(max_length=255, blank=True, null=True, verbose_name="Mutaxassislik nomi (API)")

    # Student Status
    student_status_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="Talaba status kodi")
    student_status_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Talaba statusi")

    # Education Form (Ta'lim shakli)
    education_form_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="Ta'lim shakli kodi")
    education_form_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ta'lim shakli")

    # Education Type (Ta'lim turi)
    education_type_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="Ta'lim turi kodi")
    education_type_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ta'lim turi")

    # Payment Form (To'lov shakli)
    payment_form_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="To'lov shakli kodi")
    payment_form_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="To'lov shakli")

    # Group
    group_id_api = models.IntegerField(null=True, blank=True, verbose_name="Guruh ID (API)")
    group_name_api = models.CharField(max_length=100, blank=True, null=True, verbose_name="Guruh nomi (API)")
    group_education_lang_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="Guruh ta'lim tili kodi")
    group_education_lang_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Guruh ta'lim tili")

    # Faculty
    faculty_id_api = models.IntegerField(null=True, blank=True, verbose_name="Fakultet ID (API)")
    faculty_name_api = models.CharField(max_length=255, blank=True, null=True, verbose_name="Fakultet nomi (API)")
    faculty_code_api = models.CharField(max_length=50, blank=True, null=True, verbose_name="Fakultet kodi (API)")

    # Education Language (Asosiy ta'lim tili, guruhnikidan farqli bo'lishi mumkin)
    education_lang_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="Ta'lim tili kodi")
    education_lang_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Ta'lim tili")

    # Level (Kurs)
    level_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="Kurs kodi") # API dagi 'level.code'
    level_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Kurs nomi") # API dagi 'level.name' (kurs nomi)

    # Semester
    semester_id_api = models.IntegerField(null=True, blank=True, verbose_name="Semestr ID (API)")
    semester_code_api = models.CharField(max_length=10, blank=True, null=True, verbose_name="Semestr kodi (API)")
    semester_name_api = models.CharField(max_length=100, blank=True, null=True, verbose_name="Semestr nomi (API)")
    semester_is_current = models.BooleanField(null=True, blank=True, verbose_name="Joriy semestr")
    semester_education_year_code = models.CharField(max_length=20, blank=True, null=True, verbose_name="Semestr o'quv yili kodi")
    semester_education_year_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Semestr o'quv yili nomi")
    semester_education_year_is_current = models.BooleanField(null=True, blank=True, verbose_name="Joriy o'quv yili (semestr)")

    avg_gpa = models.CharField(max_length=10, blank=True, null=True, verbose_name="O'rtacha ball (GPA)") # String sifatida, chunki '3.50'
    password_is_valid_api = models.BooleanField(null=True, blank=True, verbose_name="Parol to'g'riligi (API)")

    address_api = models.TextField(blank=True, null=True, verbose_name="Manzil (API)")

    # Country
    country_code_api = models.CharField(max_length=10, blank=True, null=True, verbose_name="Davlat kodi (API)")
    country_name_api = models.CharField(max_length=100, blank=True, null=True, verbose_name="Davlat nomi (API)")

    # Province (Viloyat)
    province_code_api = models.CharField(max_length=20, blank=True, null=True, verbose_name="Viloyat kodi (API)")
    province_name_api = models.CharField(max_length=100, blank=True, null=True, verbose_name="Viloyat nomi (API)")

    # District (Tuman)
    district_code_api = models.CharField(max_length=20, blank=True, null=True, verbose_name="Tuman kodi (API)")
    district_name_api = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tuman nomi (API)")

    # Social Category
    social_category_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="Ijtimoiy toifa kodi")
    social_category_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ijtimoiy toifa nomi")

    # Accommodation (Turar joyi)
    accommodation_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="Turar joy kodi")
    accommodation_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Turar joy nomi")

    validate_url_api = models.URLField(max_length=500, blank=True, null=True, verbose_name="Validatsiya havolasi (API)")

    # Tizim uchun ma'lumotlar
    last_login_api = models.DateTimeField(null=True, blank=True, verbose_name="Oxirgi kirish (API)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqti")

    def __str__(self):
        return self.full_name_api or f"{self.last_name or ''} {self.first_name or ''}".strip() or self.username

    class Meta:
        verbose_name = "Talaba (API)"
        verbose_name_plural = "Talabalar (API)"
        ordering = ['-updated_at', 'last_name', 'first_name']

    @property
    def get_birth_date_display(self):
        if self.birth_date_timestamp:
            try:
                dt_object = timezone.datetime.fromtimestamp(self.birth_date_timestamp, tz=timezone.get_current_timezone())
                return dt_object.strftime('%d-%m-%Y')
            except (ValueError, TypeError, OSError): # Potensial xatoliklarni ushlash
                return "Noma'lum sana (xato)"
        return None

# auth_app/models.py

import os
from uuid import uuid4
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Mavjud 'Student' modeli joylashgan ilova nomini to'g'ri ko'rsating
# from auth_app.models import Student

# --- Mavjud Student modeli (o'zgarishsiz qoldiriladi) ---

def grant_document_path(instance, filename):
    """Arizaga yuklangan fayllar uchun unikal yo'l yaratadi."""
    student_id = instance.application.student.student_id_number or instance.application.student.id
    academic_year = instance.application.academic_year.year.replace('/', '-')
    _, extension = os.path.splitext(filename)
    unique_filename = f"{uuid4().hex}{extension}"
    return f'grants/{academic_year}/{student_id}/documents/{unique_filename}'

def appeal_document_path(instance, filename):
    """Apellyatsiyaga yuklangan fayllar uchun unikal yo'l yaratadi."""
    student_id = instance.appeal.application.student.student_id_number or instance.appeal.application.student.id
    academic_year = instance.appeal.application.academic_year.year.replace('/', '-')
    _, extension = os.path.splitext(filename)
    unique_filename = f"{uuid4().hex}{extension}"
    return f'appeals/{academic_year}/{student_id}/{unique_filename}'


class AcademicYear(models.Model):
    """O'quv yillarini saqlash uchun model."""
    year = models.CharField(
        max_length=9, unique=True, verbose_name="O'quv yili",
        help_text="Format: YYYY/YYYY (masalan, 2024/2025)"
    )
    is_active_for_application = models.BooleanField(
        default=False, verbose_name="Arizalar uchun faolmi?",
        help_text="Agar 'True' bo'lsa, talabalar shu o'quv yili uchun ariza topshira oladi."
    )
    def __str__(self): return self.year
    class Meta:
        verbose_name = "O'quv yili"
        verbose_name_plural = "O'quv yillari"
        ordering = ['-year']


class GrantApplication(models.Model):
    """Talabaning grant uchun bergan arizasini ifodalovchi markaziy model."""
    class ApplicationType(models.TextChoices):
        DIFFERENTIATED = 'DIFFERENTIATED', "Tabaqalashtirilgan (qayta taqsimlash)"
        ADDITIONAL_STATE = 'ADDITIONAL_STATE', "Qo'shimcha davlat granti"
        UNIVERSITY_FUNDED = 'UNIVERSITY_FUNDED', "OTM granti (moliyaviy mustaqil)"

    class ApplicationStatus(models.TextChoices):
        DRAFT = 'DRAFT', "Qoralama"
        SUBMITTED = 'SUBMITTED', "Topshirilgan"
        ACADEMIC_REVIEW = 'ACADEMIC_REVIEW', "Akademik komissiyada"
        SOCIAL_REVIEW = 'SOCIAL_REVIEW', "Ijtimoiy komissiyada"
        SPECIAL_COMMISSION_REVIEW = 'SPECIAL_COMMISSION_REVIEW', "Maxsus komissiyada"
        COUNCIL_REVIEW = 'COUNCIL_REVIEW', "Kengashda"
        APPROVED = 'APPROVED', "Tasdiqlangan"
        REJECTED = 'REJECTED', "Rad etilgan"
        APPEALED = 'APPEALED', "Apellyatsiya berilgan"

    class FinalGrantType(models.TextChoices):
        FULL = 'FULL', "To'liq ta'lim granti"
        PARTIAL = 'PARTIAL', "To'liq bo'lmagan ta'lim granti"
        PERCENTAGE = 'PERCENTAGE', "Foizli (OTM granti)"
        NONE = 'NONE', "Grant ajratilmagan"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grant_applications', verbose_name="Talaba")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT, verbose_name="O'quv yili")
    application_type = models.CharField(max_length=20, choices=ApplicationType.choices, verbose_name="Ariza turi")
    status = models.CharField(max_length=30, choices=ApplicationStatus.choices, default=ApplicationStatus.DRAFT, verbose_name="Ariza holati")
    gpa_from_hemis = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="GPA (HEMIS tizimidan)")
    
    academic_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, verbose_name="Akademik ball (maks. 80)")
    social_activity_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, verbose_name="Ijtimoiy faollik balli (maks. 20)")
    total_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, verbose_name="Umumiy ball (maks. 100)")

    final_grant_type = models.CharField(max_length=15, choices=FinalGrantType.choices, blank=True, null=True, verbose_name="Yakuniy grant turi")
    final_grant_percentage = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="OTM granti foizi (%)", help_text="Faqat 'OTM granti' uchun to'ldiriladi")
    rejection_reason = models.TextField(blank=True, null=True, verbose_name="Rad etish sababi")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqti")

    def save(self, *args, **kwargs):
        if self.gpa_from_hemis:
            self.academic_score = self.gpa_from_hemis * Decimal('16.0') # Har ehtimolga qarshi buni ham Decimal qilamiz
        
        # Hisoblashdan oldin turlarni bir xil qilish
        academic = self.academic_score or Decimal('0.0')
        social = self.social_activity_score or Decimal('0.0')
        
        self.total_score = academic + social
        super().save(*args, **kwargs)
    pass

    @property
    def is_appealable(self):
        """Arizaga apellyatsiya berish mumkinligini tekshiradi."""
        final_statuses = [self.ApplicationStatus.APPROVED, self.ApplicationStatus.REJECTED]
        return self.status in final_statuses and not hasattr(self, 'appeal')

    def __str__(self):
        return f"Ariza #{self.id} - {self.student}"

    class Meta:
        verbose_name = "Grant uchun ariza"
        verbose_name_plural = "Grant uchun arizalar"
        ordering = ['-academic_year', '-total_score']
        unique_together = ('student', 'academic_year', 'application_type')


# auth_app/models.py (ApplicationDocument modelini o'zgartiramiz)

class ApplicationDocument(models.Model):
    """Talaba tomonidan arizaga ilova qilingan bitta tasdiqlovchi hujjat."""

    class EvaluationCriterion(models.TextChoices):
        # 2-ilovadagi 11 ta mezon uchun tanlovlar
        CRITERION_1 = 'C1', "1. Kitobxonlik madaniyati"
        CRITERION_2 = 'C2', "2. “5 muhim tashabbus” ishtiroki"
        CRITERION_3 = 'C3', "3. Akademik o‘zlashtirish (bonus)"
        CRITERION_4 = 'C4', "4. Odob-axloq qoidalari"
        CRITERION_5 = 'C5', "5. Musobaqa va tanlovlar"
        CRITERION_6 = 'C6', "6. Davomat"
        CRITERION_7 = 'C7', "7. “Ma’rifat darslari”"
        CRITERION_8 = 'C8', "8. Volontyorlik"
        CRITERION_9 = 'C9', "9. Madaniy tadbirlar"
        CRITERION_10 = 'C10', "10. Sport va sog‘lom turmush tarzi"
        CRITERION_11 = 'C11', "11. Boshqa ma’naviy faoliyat"
        # Boshqa grant turlari uchun umumiy hujjatlar
        OTHER_DOC = 'OTHER', "Boshqa (Maxsus toifa, OTM granti va h.k.)"
    
    application = models.ForeignKey(GrantApplication, on_delete=models.CASCADE, related_name='documents', verbose_name="Ariza")
    
    # YANGI MAYDON: Hujjat qaysi mezonga tegishli ekanligini belgilaydi
    evaluation_criterion = models.CharField(
        max_length=5,
        choices=EvaluationCriterion.choices,
        verbose_name="Hujjat tegishli bo'lgan mezon",
        help_text="Yuklayotgan hujjatingiz qaysi faoliyat turiga oid ekanligini tanlang."
    )
    
    description = models.CharField(
        max_length=255,
        verbose_name="Hujjatning qisqacha tavsifi",
        help_text="Masalan, 'Respublika fan olimpiadasi diplomi, 1-o'rin'"
    )
    file = models.FileField(upload_to=grant_document_path, verbose_name="Hujjat fayli")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"{self.get_evaluation_criterion_display()} - {self.application.student}"
    
    class Meta:
        verbose_name = "Arizaga ilova qilingan hujjat"
        verbose_name_plural = "Arizaga ilova qilingan hujjatlar"
        ordering = ['evaluation_criterion']


class SocialActivityEvaluation(models.Model):
    """
    Nizomning 2-ilovasidagi "MEZONLAR" asosida talabaning ijtimoiy faolligini baholash varaqasi.
    Ushbu model komissiya a'zolari tomonidan to'ldiriladi.
    """
    # --- Mezonlar uchun maksimal ball konstatalari ---
    MAX_POINTS_READING = 20
    MAX_POINTS_INITIATIVES = 20
    MAX_POINTS_ACADEMIC_BONUS = 10
    MAX_POINTS_ETHICS = 5
    MAX_POINTS_COMPETITION = 10
    MAX_POINTS_ATTENDANCE = 5
    MAX_POINTS_ENLIGHTENMENT = 10
    MAX_POINTS_VOLUNTEERING = 5
    MAX_POINTS_CULTURAL = 5
    MAX_POINTS_SPORTS = 5
    MAX_POINTS_OTHER = 5

    application = models.OneToOneField(GrantApplication, on_delete=models.CASCADE, related_name='social_evaluation', verbose_name="Ariza")

    # --- Nizom 2-ilovasidagi 11 ta mezon uchun baholash maydonlari ---
    reading_culture_points = models.PositiveSmallIntegerField(default=0, verbose_name="1. Kitobxonlik madaniyati", help_text=f"Maksimal ball: {MAX_POINTS_READING}", validators=[MinValueValidator(0), MaxValueValidator(MAX_POINTS_READING)])
    five_initiatives_points = models.PositiveSmallIntegerField(default=0, verbose_name="2. “5 muhim tashabbus” doirasidagi to‘garaklarda faol ishtiroki", help_text=f"Maksimal ball: {MAX_POINTS_INITIATIVES}", validators=[MinValueValidator(0), MaxValueValidator(MAX_POINTS_INITIATIVES)])
    academic_progress_bonus_points = models.PositiveSmallIntegerField(default=0, verbose_name="3. Talabaning akademik o‘zlashtirishi", help_text=f"Maksimal ball: {MAX_POINTS_ACADEMIC_BONUS}", validators=[MinValueValidator(0), MaxValueValidator(MAX_POINTS_ACADEMIC_BONUS)])
    ethics_adherence_points = models.PositiveSmallIntegerField(default=0, verbose_name="4. Talabaning oliy ta’lim tashkilotining ichki tartib qoidalari va Odob-axloq kodeksiga rioya etishi", help_text=f"Maksimal ball: {MAX_POINTS_ETHICS}", validators=[MinValueValidator(0), MaxValueValidator(MAX_POINTS_ETHICS)])
    competition_results_points = models.PositiveSmallIntegerField(default=0, verbose_name="5. Xalqaro, respublika, viloyat miqyosidagi ko‘rik-tanlov, fan olimpiadalari va sport musobaqalarida erishgan natijalari", help_text=f"Maksimal ball: {MAX_POINTS_COMPETITION}", validators=[MinValueValidator(0), MaxValueValidator(MAX_POINTS_COMPETITION)])
    attendance_points = models.PositiveSmallIntegerField(default=0, verbose_name="6. Talabaning darslarga to‘liq va kechikmasdan kelishi", help_text=f"Maksimal ball: {MAX_POINTS_ATTENDANCE}", validators=[MinValueValidator(0), MaxValueValidator(MAX_POINTS_ATTENDANCE)])
    enlightenment_lessons_points = models.PositiveSmallIntegerField(default=0, verbose_name="7. Talabalarning “Ma’rifat darslari”dagi faol ishtiroki", help_text=f"Maksimal ball: {MAX_POINTS_ENLIGHTENMENT}", validators=[MinValueValidator(0), MaxValueValidator(MAX_POINTS_ENLIGHTENMENT)])
    volunteering_points = models.PositiveSmallIntegerField(default=0, verbose_name="8. Volontyorlik va jamoat ishlaridagi faolligi", help_text=f"Maksimal ball: {MAX_POINTS_VOLUNTEERING}", validators=[MinValueValidator(0), MaxValueValidator(MAX_POINTS_VOLUNTEERING)])
    cultural_events_points = models.PositiveSmallIntegerField(default=0, verbose_name="9. Teatr va muzey, xiyobon, kino, tarixiy qadamjolarga tashriflar", help_text=f"Maksimal ball: {MAX_POINTS_CULTURAL}", validators=[MinValueValidator(0), MaxValueValidator(MAX_POINTS_CULTURAL)])
    sports_lifestyle_points = models.PositiveSmallIntegerField(default=0, verbose_name="10. Talabalarning sport bilan shug‘ullanishi va sog‘lom turmush tarziga amal qilishi", help_text=f"Maksimal ball: {MAX_POINTS_SPORTS}", validators=[MinValueValidator(0), MaxValueValidator(MAX_POINTS_SPORTS)])
    other_activities_points = models.PositiveSmallIntegerField(default=0, verbose_name="11. Ma’naviy-ma’rifiy sohaga oid boshqa yo‘nalishlardagi faolligi", help_text=f"Maksimal ball: {MAX_POINTS_OTHER}", validators=[MinValueValidator(0), MaxValueValidator(MAX_POINTS_OTHER)])
    
    # --- Baholovchi uchun qo'shimcha ma'lumotlar ---
    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Baholovchi (komissiya a'zosi)", help_text="Admin panelida avtomatik belgilanadi")
    evaluator_comment = models.TextField(blank=True, verbose_name="Baholovchi izohi", help_text="Ballarni asoslash uchun qo'shimcha izohlar")
    evaluation_date = models.DateTimeField(null=True, blank=True, verbose_name="Baholangan sana")


    @property
    def total_raw_score(self):
        """Mezonlar bo'yicha yig'ilgan jami xom ballni hisoblaydi (maks. 100)."""
        return sum([
            self.reading_culture_points, self.five_initiatives_points,
            self.academic_progress_bonus_points, self.ethics_adherence_points,
            self.competition_results_points, self.attendance_points,
            self.enlightenment_lessons_points, self.volunteering_points,
            self.cultural_events_points, self.sports_lifestyle_points,
            self.other_activities_points
        ])

    @property
    def final_score(self):
        """Nizomning 15-bandiga asosan 20 ballik tizimga o'tkazilgan yakuniy ball."""
        # YECHIM: Bo'lishda `Decimal` turidan foydalanish
        return Decimal(self.total_raw_score) / Decimal('5.0')

    def save(self, *args, **kwargs):
        # Bu yerdagi qiymat endi `Decimal` bo'ladi
        self.application.social_activity_score = self.final_score 
        self.application.save() # Asosiy arizadagi ballarni yangilash
        if self.evaluator and not self.evaluation_date: self.evaluation_date = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self): return f"Baholash varaqasi (Ariza #{self.application.id})"
    
    class Meta:
        verbose_name = "Ijtimoiy faollikni baholash"
        verbose_name_plural = "Ijtimoiy faollikni baholashlar"


class Appeal(models.Model):
    """Nizomning 20-bandiga muvofiq, apellyatsiya arizalarini saqlash uchun model."""
    class AppealStatus(models.TextChoices):
        SUBMITTED = 'SUBMITTED', "Topshirilgan"
        REVIEWING = 'REVIEWING', "Ko'rib chiqilmoqda"
        CLOSED = 'CLOSED', "Yopilgan"
    class AppealOutcome(models.TextChoices):
        SATISFIED = 'SATISFIED', "Qanoatlantirildi"
        REJECTED = 'REJECTED', "Rad etildi"
        PARTIALLY_SATISFIED = 'PARTIALLY_SATISFIED', "Qisman qanoatlantirildi"

    application = models.OneToOneField(GrantApplication, on_delete=models.CASCADE, related_name='appeal', verbose_name="Apellyatsiya qilinayotgan ariza")
    reason = models.TextField(verbose_name="Apellyatsiya sababi/mazmuni")
    status = models.CharField(max_length=20, choices=AppealStatus.choices, default=AppealStatus.SUBMITTED, verbose_name="Apellyatsiya holati")
    outcome = models.CharField(max_length=25, choices=AppealOutcome.choices, blank=True, null=True, verbose_name="Apellyatsiya yakuniy natijasi")
    decision_comment = models.TextField(blank=True, null=True, verbose_name="Komissiya qarori bo'yicha izoh")
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='reviewed_appeals', null=True, blank=True, verbose_name="Ko'rib chiquvchi")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Topshirilgan vaqti")
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name="Ko'rib chiqilgan vaqti")

    def save(self, *args, **kwargs):
        if self.outcome and not self.reviewed_at:
            self.reviewed_at = timezone.now()
            self.status = self.AppealStatus.CLOSED
        super().save(*args, **kwargs)

    def __str__(self): return f"Apellyatsiya (Ariza #{self.application.id})"
    class Meta:
        verbose_name = "Apellyatsiya arizasi"
        verbose_name_plural = "Apellyatsiya arizalari"
        ordering = ['-submitted_at']


class AppealDocument(models.Model):
    """Apellyatsiya arizasiga ilova qilingan qo'shimcha tasdiqlovchi hujjat."""
    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE, related_name='documents', verbose_name="Apellyatsiya arizasi")
    description = models.CharField(max_length=255, verbose_name="Qisqacha tavsif")
    file = models.FileField(upload_to=appeal_document_path, verbose_name="Hujjat fayli")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.description} (Apellyatsiya #{self.appeal.id})"
    class Meta:
        verbose_name = "Apellyatsiya hujjati"
        verbose_name_plural = "Apellyatsiya hujjatlari"


# auth_app/models.py (faylning oxiriga qo'shiladi)

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Notification(models.Model):
    """
    Tizim bo'yicha foydalanuvchilarga yuboriladigan bildirishnomalar uchun model.
    GenericForeignKey yordamida har qanday modelga (Ariza, Apellyatsiya) bog'lana oladi.
    """
    class NotificationVerb(models.TextChoices):
        APPLICATION_SUBMITTED = 'APPLICATION_SUBMITTED', "Yangi ariza topshirildi"
        STATUS_CHANGED = 'STATUS_CHANGED', "Holat o'zgardi"
        APPEAL_SUBMITTED = 'APPEAL_SUBMITTED', "Yangi apellyatsiya kelib tushdi"
        APPEAL_DECIDED = 'APPEAL_DECIDED', "Apellyatsiya bo'yicha qaror qabul qilindi"
        GENERAL_ANNOUNCEMENT = 'GENERAL_ANNOUNCEMENT', "Umumiy e'lon"

    # Kimga yuborilgani (Recipient)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications', verbose_name="Qabul qiluvchi")
    
    # Kim tomonidan yuborilgani (Actor) (ixtiyoriy)
    actor_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='actor_notifications', null=True, blank=True)
    actor_object_id = models.PositiveIntegerField(null=True, blank=True)
    actor = GenericForeignKey('actor_content_type', 'actor_object_id')

    verb = models.CharField(max_length=50, choices=NotificationVerb.choices, verbose_name="Bildirishnoma turi")
    
    # Qaysi obyekt haqida (Target) (ixtiyoriy)
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='target_notifications', null=True, blank=True)
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    
    description = models.TextField(blank=True, verbose_name="Tavsif")
    
    read = models.BooleanField(default=False, verbose_name="O'qilganmi?")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.target:
            return f"{self.actor} {self.verb} {self.target} -> {self.recipient}"
        return f"{self.verb} -> {self.recipient}"

    class Meta:
        verbose_name = "Bildirishnoma"
        verbose_name_plural = "Bildirishnomalar"
        ordering = ['-timestamp']