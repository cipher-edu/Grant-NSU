#--- START OF FILE admin.py ---

from django.contrib import admin, messages
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from .models import (
    Student, AcademicYear, GrantApplication, SocialActivityEvaluation,
    ApplicationDocument, Appeal, AppealDocument
)

# --- Mavjud StudentAdmin (O'zgarishsiz qoldiriladi) ---
# ... (Siz taqdim etgan to'liq StudentAdmin kodi shu yerda turadi) ...
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # ... barcha kod ...
    list_per_page = 20
    list_max_show_all = 1000
    list_display = (
        'username', 'student_id_number', 'api_user_hash',
        'first_name', 'last_name', 'patronymic', 'full_name_api', 'short_name_api',
        'get_image_preview', 'birth_date_timestamp', 'passport_pin', 'passport_number', 'email', 'phone',
        'gender_code', 'gender_name', 'university_name_api',
        'specialty_id_api', 'specialty_code_api', 'specialty_name_api',
        'student_status_code', 'student_status_name',
        'education_form_code', 'education_form_name',
        'education_type_code', 'education_type_name',
        'payment_form_code', 'payment_form_name',
        'group_id_api', 'group_name_api', 'group_education_lang_code', 'group_education_lang_name',
        'faculty_id_api', 'faculty_name_api', 'faculty_code_api',
        'education_lang_code', 'education_lang_name',
        'level_code', 'level_name',
        'semester_id_api', 'semester_code_api', 'semester_name_api', 'semester_is_current',
        'semester_education_year_code', 'semester_education_year_name', 'semester_education_year_is_current',
        'avg_gpa', 'password_is_valid_api', 'address_api',
        'country_code_api', 'country_name_api',
        'province_code_api', 'province_name_api',
        'district_code_api', 'district_name_api',
        'social_category_code', 'social_category_name',
        'accommodation_code', 'accommodation_name',
        'validate_url_api', 'last_login_api', 'created_at', 'updated_at'
    )
    list_filter = (
        'faculty_name_api', 
        'level_name', 
        'education_form_name', 
        'student_status_name',
        'last_login_api',
        'updated_at',
        'created_at'
    )
    search_fields = (
        'username', 
        'first_name', 
        'last_name', 
        'student_id_number', 
        'full_name_api',
        'faculty_name_api', 
        'group_name_api',
        'email',
        'phone'
    )
    ordering = ('-updated_at', 'last_name', 'first_name')
    readonly_fields_list = [
        'username', 'student_id_number', 'api_user_hash',
        'first_name', 'last_name', 'patronymic', 'full_name_api', 'short_name_api',
        'get_image_preview',
        'birth_date_timestamp', 'get_birth_date_display_admin',
        'passport_pin', 'passport_number', 'email', 'phone', 
        'gender_code', 'gender_name', 'university_name_api',
        'specialty_id_api', 'specialty_code_api', 'specialty_name_api',
        'student_status_code', 'student_status_name', 'education_form_code',
        'education_form_name', 'education_type_code', 'education_type_name',
        'payment_form_code', 'payment_form_name', 'group_id_api', 'group_name_api',
        'group_education_lang_code', 'group_education_lang_name', 'faculty_id_api',
        'faculty_name_api', 'faculty_code_api', 'education_lang_code',
        'education_lang_name', 'level_code', 'level_name', 'semester_id_api',
        'semester_code_api', 'semester_name_api', 'semester_is_current',
        'semester_education_year_code', 'semester_education_year_name',
        'semester_education_year_is_current', 'avg_gpa', 'password_is_valid_api',
        'address_api', 'country_code_api', 'country_name_api', 'province_code_api',
        'province_name_api', 'district_code_api', 'district_name_api',
        'social_category_code', 'social_category_name', 'accommodation_code',
        'accommodation_name', 'validate_url_api', 
        'last_login_api_formatted_detail',
        'created_at_formatted_detail', 
        'updated_at_formatted_detail'
    ]
    readonly_fields = tuple(readonly_fields_list)

    fieldsets = (
        ('Asosiy Login Ma\'lumotlari', {
            'fields': ('username', 'student_id_number', 'api_user_hash')
        }),
        ('Shaxsiy Ma\'lumotlar (API)', {
            'fields': (
                'get_image_preview', 
                ('full_name_api', 'short_name_api'), 
                ('first_name', 'last_name', 'patronymic'),
                ('birth_date_timestamp', 'get_birth_date_display_admin'),
                'gender_name', 
                ('passport_pin', 'passport_number'), 
                'email', 'phone', 'address_api'
            )
        }),
        ('Universitet Ma\'lumotlari (API)', {
            'fields': (
                'university_name_api', 
                ('faculty_name_api', 'faculty_code_api'),
                ('specialty_name_api', 'specialty_code_api'), 
                'education_type_name', 'education_form_name',
                'education_lang_name', 'level_name', 
                ('group_name_api', 'group_education_lang_name'),
                ('semester_name_api', 'semester_is_current', 'semester_education_year_name'),
                'payment_form_name', 'student_status_name', 'avg_gpa', 
                'password_is_valid_api'
            )
        }),
        ('Manzil va Ijtimoiy Holat (API)', {
            'fields': (
                'country_name_api', 'province_name_api', 'district_name_api',
                'social_category_name', 'accommodation_name'
            )
        }),
        ('Tizim Ma\'lumotlari', {
            'fields': (
                'last_login_api_formatted_detail', 
                ('created_at_formatted_detail', 'updated_at_formatted_detail'), 
                'validate_url_api_link'
            ),
            'classes': ('collapse',),
        }),
    )

    def _format_datetime_for_admin(self, dt_value):
        if dt_value:
            local_tz = timezone.get_current_timezone()
            return timezone.localtime(dt_value, local_tz).strftime('%d-%m-%Y %H:%M:%S')
        return "Noma'lum"

    @admin.display(description='Oxirgi Kirish (API)', ordering='last_login_api')
    def last_login_api_formatted(self, obj):
        return self._format_datetime_for_admin(obj.last_login_api)
    
    @admin.display(description='Oxirgi Kirish (API)')
    def last_login_api_formatted_detail(self, obj):
        return self._format_datetime_for_admin(obj.last_login_api)

    @admin.display(description='Yaratilgan Vaqti')
    def created_at_formatted_detail(self, obj):
        return self._format_datetime_for_admin(obj.created_at)

    @admin.display(description='Yangilangan Vaqti', ordering='updated_at')
    def updated_at_formatted(self, obj):
        return self._format_datetime_for_admin(obj.updated_at)

    @admin.display(description='Yangilangan Vaqti')
    def updated_at_formatted_detail(self, obj):
        return self._format_datetime_for_admin(obj.updated_at)

    @admin.display(description='To\'liq F.I.Sh.', ordering='last_name')
    def get_full_name_display(self, obj):
        return obj.full_name_api or f"{obj.last_name or ''} {obj.first_name or ''}".strip() or obj.username

    @admin.display(description='Talabning surati ', empty_value="-Rasm yo'q-")
    def get_image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px; border-radius: 5px;" />', obj.image_url)
        return self.get_image_preview.empty_value
    
    @admin.display(description='Tug\'ilgan sana (Formatlangan)', ordering='birth_date_timestamp')
    def get_birth_date_display_admin(self, obj):
        if obj.birth_date_timestamp:
            try:
                dt_object = timezone.datetime.fromtimestamp(obj.birth_date_timestamp, tz=timezone.get_current_timezone())
                return dt_object.strftime('%d-%m-%Y')
            except (ValueError, TypeError, OSError):
                return "Noma'lum sana (xato)"
        return "-"


    @admin.display(description='API Validatsiya Havolasi')
    def validate_url_api_link(self, obj):
        if obj.validate_url_api:
            return format_html('<a href="{0}" target="_blank">Havola</a>', obj.validate_url_api)
        return "-"

    @admin.display(description='Profil To\'liqligi', boolean=True)
    def is_profile_complete(self, obj):
        required_fields = [
            obj.first_name, obj.last_name, 
            obj.student_id_number,
            obj.faculty_name_api, obj.level_name
        ]
        return all(field is not None and str(field).strip() != '' for field in required_fields)

    actions = ['refresh_selected_students_data_from_api_action']

    @admin.action(description="Tanlangan talabalar ma'lumotlarini API dan yangilash")
    def refresh_selected_students_data_from_api_action(self, request, queryset):
        admin_api_token = getattr(settings, 'HEMIS_ADMIN_API_TOKEN', None)        
        if not admin_api_token:
            self.message_user(request, "Ma'muriy API tokeni (HEMIS_ADMIN_API_TOKEN) sozlanmalarda topilmadi.", messages.ERROR)
            return
        
        updated_count = 0
        failed_students_info = []

        if updated_count > 0:
            self.message_user(request, f"{updated_count} ta talaba ma'lumotlari muvaffaqiyatli yangilandi.", messages.SUCCESS)
        elif queryset.exists():
             self.message_user(request, "Talaba ma'lumotlarini yangilash funksiyasi to'liq sozlanmagan yoki xatolik yuz berdi.", messages.WARNING)
        else:
            self.message_user(request, "Yangilash uchun talabalar tanlanmadi.", messages.INFO)

# --- Yangi modellar uchun Admin klasslar ---
from django.contrib import admin, messages
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from .models import (
    Student, AcademicYear, GrantApplication, SocialActivityEvaluation,
    ApplicationDocument, Appeal, AppealDocument
)
@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('year', 'is_active_for_application')
    list_editable = ('is_active_for_application',)
    actions = ['activate_for_application', 'deactivate_for_application']

    @admin.action(description="Tanlangan o'quv yil(lar)ini arizalar uchun FAOLLASHTIRISH")
    def activate_for_application(self, request, queryset):
        # Boshqa barcha yillarni nofaol qilish
        AcademicYear.objects.exclude(pk__in=queryset.values_list('pk', flat=True)).update(is_active_for_application=False)
        updated_count = queryset.update(is_active_for_application=True)
        self.message_user(request, f"{updated_count} ta o'quv yili faollashtirildi.", messages.SUCCESS)

    @admin.action(description="Tanlangan o'quv yil(lar)ini NOFAOL qilish")
    def deactivate_for_application(self, request, queryset):
        queryset.update(is_active_for_application=False)
        self.message_user(request, f"{queryset.count()} ta o'quv yili nofaol holatga o'tkazildi.", messages.WARNING)


class ApplicationDocumentInline(admin.TabularInline):
    """Arizaga ilova qilingan hujjatlarni ko'rish uchun inline."""
    model = ApplicationDocument
    extra = 0
    # Komissiya uchun eng kerakli ma'lumotlar
    fields = ('evaluation_criterion', 'description', 'file_link')
    readonly_fields = ('evaluation_criterion', 'description', 'file_link')
    verbose_name = "Talaba tomonidan yuklangan hujjat"
    verbose_name_plural = "Talaba tomonidan yuklangan hujjatlar"

    @admin.display(description="Faylni ko'rish")
    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank" class="button">Ko\'rish</a>', obj.file.url)
        return "Fayl yo'q"
    
    def has_add_permission(self, request, obj=None):
        return False # Admin panelidan hujjat qo'shishni taqiqlash

    def has_delete_permission(self, request, obj=None):
        return False # Admin panelidan hujjat o'chirishni taqiqlash


class SocialActivityEvaluationInline(admin.StackedInline):
    """Ijtimoiy faollikni baholash uchun maxsus inline."""
    model = SocialActivityEvaluation
    extra = 0 # Yangi bo'sh forma qo'shmaslik
    
    # Baholash maydonlarini ikki ustunga ajratish uchun
    fieldsets = (
        ("Ijtimoiy faollikni baholash (2-ilova bo'yicha)", {
            'fields': (
                ('reading_culture_points', 'five_initiatives_points'),
                ('academic_progress_bonus_points', 'ethics_adherence_points'),
                ('competition_results_points', 'attendance_points'),
                ('enlightenment_lessons_points', 'volunteering_points'),
                ('cultural_events_points', 'sports_lifestyle_points'),
                'other_activities_points',
                'evaluator_comment'
            )
        }),
        ('Hisoblangan Natijalar (Avtomatik)', {
            'fields': ('total_raw_score_display', 'final_score_display', 'evaluator', 'evaluation_date'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('total_raw_score_display', 'final_score_display', 'evaluator', 'evaluation_date')

    @admin.display(description="Jami xom ball (maks. 100)")
    def total_raw_score_display(self, obj):
        return obj.total_raw_score

    @admin.display(description="Yakuniy ball (maks. 20)")
    def final_score_display(self, obj):
        return f"{obj.final_score:.2f}"

    # formni saqlashdan oldin baholovchini belgilash
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.evaluator:
                instance.evaluator = request.user
        super().save_formset(request, form, formset, change)


@admin.register(GrantApplication)
class GrantApplicationAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_select_related = ('student', 'academic_year')
    inlines = [SocialActivityEvaluationInline, ApplicationDocumentInline]

    list_display = (
        'id', 'student_link', 'academic_year', 'application_type', 'colored_status',
        'gpa_from_hemis', 'academic_score', 'social_activity_score', 'total_score',
        'colored_final_grant_type', 'has_appeal'
    )
    list_filter = (
        'status', 'final_grant_type', 'application_type', 'academic_year',
        'student__faculty_name_api', 'student__level_name'
    )
    search_fields = (
        'id', 'student__first_name', 'student__last_name', 'student__student_id_number'
    )
    readonly_fields = (
        'student_link', 'academic_score', 'social_activity_score', 'total_score', 'created_at', 'updated_at'
    )
    fieldsets = (
        ('Ariza ma\'lumotlari', {
            'fields': ('student_link', ('application_type', 'status'), 'academic_year', 'gpa_from_hemis')
        }),
        ('Baholash Natijalari (Avtomatik hisoblanadi)', {
            'fields': (('academic_score', 'social_activity_score'), 'total_score'),
        }),
        ('Yakuniy Natija (Kengash tomonidan belgilanadi)', {
            'fields': ('final_grant_type', 'final_grant_percentage', 'rejection_reason'),
        }),
        ('Tizim Ma\'lumotlari', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    actions = ['mark_as_special_commission', 'mark_as_council_review', 'mark_as_approved', 'mark_as_rejected']

    @admin.display(description="Talaba", ordering='student__last_name')
    def student_link(self, obj):
        url = reverse("admin:auth_app_student_change", args=[obj.student.pk])
        return format_html('<a href="{}">{}</a>', url, obj.student)

    @admin.display(description="Holati", ordering='status')
    def colored_status(self, obj):
        colors = {
            'DRAFT': 'gray', 'SUBMITTED': 'orange', 'ACADEMIC_REVIEW': 'blue',
            'SOCIAL_REVIEW': 'blue', 'SPECIAL_COMMISSION_REVIEW': 'purple',
            'COUNCIL_REVIEW': 'darkcyan', 'APPROVED': 'green', 'REJECTED': 'red',
            'APPEALED': 'darkred'
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: white; background-color: {}; padding: 3px 7px; border-radius: 5px;">{}</span>',
            color, obj.get_status_display()
        )

    @admin.display(description="Yakuniy Grant", ordering='final_grant_type')
    def colored_final_grant_type(self, obj):
        if not obj.final_grant_type: return "-"
        colors = {'FULL': 'green', 'PARTIAL': 'darkgoldenrod', 'PERCENTAGE': 'blue', 'NONE': 'red'}
        color = colors.get(obj.final_grant_type, 'black')
        text = obj.get_final_grant_type_display()
        if obj.final_grant_type == 'PERCENTAGE' and obj.final_grant_percentage:
            text += f" ({obj.final_grant_percentage}%)"
        return format_html('<span style="font-weight: bold; color: {};">{}</span>', color, text)

    @admin.display(description="Apellyatsiya", boolean=True)
    def has_appeal(self, obj):
        return hasattr(obj, 'appeal')

    def _update_status(self, request, queryset, status):
        updated_count = queryset.update(status=status)
        status_display = GrantApplication.ApplicationStatus(status).label
        self.message_user(request, f"{updated_count} ta ariza holati '{status_display}' ga o'zgartirildi.", messages.SUCCESS)

    @admin.action(description="Holatni 'Maxsus komissiyaga yuborish'")
    def mark_as_special_commission(self, request, queryset):
        self._update_status(request, queryset, GrantApplication.ApplicationStatus.SPECIAL_COMMISSION_REVIEW)

    @admin.action(description="Holatni 'Kengashga yuborish'")
    def mark_as_council_review(self, request, queryset):
        self._update_status(request, queryset, GrantApplication.ApplicationStatus.COUNCIL_REVIEW)

    @admin.action(description="Tanlanganlarni TASDIQLASH")
    def mark_as_approved(self, request, queryset):
        self._update_status(request, queryset, GrantApplication.ApplicationStatus.APPROVED)

    @admin.action(description="Tanlanganlarni RAD ETISH")
    def mark_as_rejected(self, request, queryset):
        self._update_status(request, queryset, GrantApplication.ApplicationStatus.REJECTED)


class AppealDocumentInline(admin.TabularInline):
    model = AppealDocument
    extra = 0
    fields = ('description', 'file_link')
    readonly_fields = ('description', 'file_link')
    
    @admin.display(description="Faylni ko'rish")
    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">Ko\'rish</a>', obj.file.url)
        return "Fayl yo'q"
        
    def has_add_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False


@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_select_related = ('application__student', 'application__academic_year')
    inlines = [AppealDocumentInline]

    list_display = ('id', 'application_link', 'colored_status', 'colored_outcome', 'submitted_at', 'reviewed_by')
    list_filter = ('status', 'outcome', 'submitted_at')
    search_fields = ('application__student__full_name_api', 'application__id')
    readonly_fields = ('application_link', 'submitted_at', 'reviewed_at', 'reviewed_by')
    
    fieldsets = (
        ('Apellyatsiya Ma\'lumotlari', {
            'fields': ('application_link', ('status', 'submitted_at'), 'reason')
        }),
        ('Komissiya Qarori', {
            'fields': ('outcome', 'decision_comment', ('reviewed_by', 'reviewed_at'))
        })
    )
    
    def save_model(self, request, obj, form, change):
        if 'outcome' in form.changed_data and form.cleaned_data['outcome'] and not obj.reviewed_by:
            obj.reviewed_by = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description="Asosiy Ariza", ordering='application__id')
    def application_link(self, obj):
        url = reverse("admin:auth_app_grantapplication_change", args=[obj.application.pk])
        return format_html('<a href="{}">Ariza #{} ({})</a>', url, obj.application.id, obj.application.student)

    @admin.display(description="Holati", ordering='status')
    def colored_status(self, obj):
        color = 'orange' if obj.status == 'SUBMITTED' else 'blue' if obj.status == 'REVIEWING' else 'green'
        return format_html('<span style="color: white; background-color: {}; padding: 3px 7px; border-radius: 5px;">{}</span>', color, obj.get_status_display())

    @admin.display(description="Natija", ordering='outcome')
    def colored_outcome(self, obj):
        if not obj.outcome: return "-"
        colors = {'SATISFIED': 'green', 'REJECTED': 'red', 'PARTIALLY_SATISFIED': 'darkgoldenrod'}
        color = colors.get(obj.outcome, 'black')
        return format_html('<span style="font-weight: bold; color: {};">{}</span>', color, obj.get_outcome_display())