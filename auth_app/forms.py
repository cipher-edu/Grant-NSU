# auth_app/forms.py

import logging
from django import forms
from django.core.exceptions import ValidationError
from .models import *

logger = logging.getLogger(__name__)


# --- Foydalanuvchi autentifikatsiyasi uchun forma ---

class LoginForm(forms.Form):
    """Foydalanuvchidan login va parol olish uchun standart forma."""
    username = forms.CharField(
        label="Login (ID Raqam)",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-input', # HTMLga stil berish uchun
            'placeholder': 'Talaba ID raqamingizni kiriting'
        })
    )
    password = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Parolingiz'
        })
    )

# grant_app/forms.py

from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet
from .models import GrantApplication, ApplicationDocument, Appeal, AppealDocument, AcademicYear

class GrantApplicationForm(forms.ModelForm):
    """Talabaning yangi grant uchun ariza topshirish formasi."""
    class Meta:
        model = GrantApplication
        fields = ['application_type']
        widgets = {
            'application_type': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Faqat aktiv o'quv yillari uchun ariza berish imkoniyatini qoldirish
        # Bu logikani view'da qilish afzalroq. Formada faqat ko'rinishni sozlaymiz.
        self.fields['application_type'].label = "Ariza turini tanlang"


# auth_app/forms.py (ApplicationDocumentForm va FormSet'ni yangilaymiz)

class ApplicationDocumentForm(forms.ModelForm):
    """Arizaga bitta hujjat yuklash uchun forma."""
    class Meta:
        model = ApplicationDocument
        # YANGI MAYDONNI QO'SHDIK
        fields = ['evaluation_criterion', 'description', 'file']
        widgets = {
            # YANGI MAYDON UCHUN WIDGET
            'evaluation_criterion': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'description': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Hujjat tavsifi (masalan, Respublika olimpiadasi diplomi)'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control form-control-sm'}),
        }
        labels = {
            'evaluation_criterion': "Hujjat qaysi mezonga oid?",
            'description': "Hujjat tavsifi",
            'file': "Faylni tanlang"
        }

class ApplicationDocumentBaseFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        seen = set()
        duplicates = set()
        for form in self.forms:
            if self.can_delete and form.cleaned_data.get('DELETE', False):
                continue
            criterion = form.cleaned_data.get('evaluation_criterion')
            if not criterion:
                continue
            if criterion in seen and criterion != 'OTHER':
                duplicates.add(criterion)
            seen.add(criterion)
        if duplicates:
            from django.core.exceptions import ValidationError
            # Add a non-field error for the whole formset (shows at the top)
            self._non_form_errors = self.non_form_errors()  # ensure property exists
            self._non_form_errors.append(
                "❗️ Xatolik: Bir mezon uchun bir martadan ortiq hujjat yuklab bo'lmaydi. Iltimos, mezonlarni takrorlamang!"
            )
            raise ValidationError(
                "❗️ Xatolik: Bir mezon uchun bir martadan ortiq hujjat yuklab bo'lmaydi. Iltimos, mezonlarni takrorlamang!"
            )

# FormSet o'zgarishsiz qoladi, u formadan avtomatik oladi.
ApplicationDocumentFormSet = inlineformset_factory(
    GrantApplication,
    ApplicationDocument,
    form=ApplicationDocumentForm,
    formset=ApplicationDocumentBaseFormSet,  # <-- custom formset
    extra=1,
    can_delete=True,
    min_num=1, # Kamida bitta hujjat yuklashni majburiy qilish
    validate_min=True
)

class AppealForm(forms.ModelForm):
    """Apellyatsiya arizasi uchun forma."""
    class Meta:
        model = Appeal
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Apellyatsiya sababini batafsil yozing...'
            }),
        }
        labels = {
            'reason': "Apellyatsiya sababi"
        }

# Apellyatsiyaga bir nechta hujjat yuklash uchun formset
AppealDocumentFormSet = inlineformset_factory(
    Appeal,
    AppealDocument,
    fields=('description', 'file'),
    extra=1,
    can_delete=True
)