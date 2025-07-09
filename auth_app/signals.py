# auth_app/signals.py (faylga qo'shimchalar)

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from .models import GrantApplication, Appeal, Notification, Student

@receiver(post_save, sender=GrantApplication)
def grant_application_notifications(sender, instance, created, **kwargs):
    """Grant arizalari bilan bog'liq bildirishnomalarni yaratadi."""
    # 1. Talaba yangi ariza topshirganda
    if created and instance.status == GrantApplication.ApplicationStatus.SUBMITTED:
        # Barcha adminlarga (yoki maxsus komissiya guruhiga) xabar yuborish
        admin_group = Group.objects.filter(name='Komissiya').first() # "Komissiya" nomli guruh bo'lishi kerak
        if admin_group:
            for user in admin_group.user_set.all():
                Notification.objects.create(
                    recipient=user,
                    actor=instance.student,
                    verb=Notification.NotificationVerb.APPLICATION_SUBMITTED,
                    target=instance,
                    description=f"{instance.student} tomonidan yangi grant arizasi (# {instance.id}) topshirildi."
                )

    # 2. Ariza holati admin tomonidan o'zgartirilganda (lekin yangi yaratilmaganda)
    if not created:
        # Ariza egasiga xabar yuborish
        # Student modelida 'user' degan OneToOneField bo'lishi kerak yoki moslashtirish kerak
        try:
            # Student modelining o'zi User bo'lmasa, uni topish logikasi kerak.
            # Shartli ravishda studentning o'zi 'recipient' deb olamiz, lekin bu User modeliga bog'lanishi kerak.
            # Agar sizda Student va User alohida bo'lsa, bu joyni o'zgartirish kerak.
            # Misol uchun, Student.user orqali.
            recipient_user = instance.student # Bu joyda Student modeliga bog'liq.
                                              # Agar Student=User bo'lsa, to'g'ri.
                                              # Aks holda, recipient_user = instance.student.user bo'lishi kerak
            Notification.objects.create(
                recipient=recipient_user,
                verb=Notification.NotificationVerb.STATUS_CHANGED,
                target=instance,
                description=f"Sizning #{instance.id}-sonli arizangiz holati '{instance.get_status_display()}' ga o'zgartirildi."
            )
        except Exception as e:
            # logger.error(...)
            pass


@receiver(post_save, sender=Appeal)
def appeal_notifications(sender, instance, created, **kwargs):
    """Apellyatsiyalar bilan bog'liq bildirishnomalar."""
    # 1. Yangi apellyatsiya berilganda
    if created:
         admin_group = Group.objects.filter(name='Komissiya').first()
         if admin_group:
            for user in admin_group.user_set.all():
                Notification.objects.create(
                    recipient=user,
                    actor=instance.application.student,
                    verb=Notification.NotificationVerb.APPEAL_SUBMITTED,
                    target=instance,
                    description=f"Ariza #{instance.application.id} bo'yicha yangi apellyatsiya kelib tushdi."
                )

    # 2. Apellyatsiya bo'yicha qaror qabul qilinganda
    if instance.outcome and not created:
        try:
            recipient_user = instance.application.student
            Notification.objects.create(
                recipient=recipient_user,
                verb=Notification.NotificationVerb.APPEAL_DECIDED,
                target=instance,
                description=f"Sizning #{instance.application.id}-sonli arizangiz bo'yicha bergan apellyatsiyangiz natijasi: '{instance.get_outcome_display()}'."
            )
        except:
            pass