from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from django_fsm import transition, FSMIntegerField


# Create your models here.
class Agency(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    description = models.CharField(max_length=255, default='Description')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class WorkUnit(models.Model):
    name = models.CharField(max_length=255)
    agency = models.ForeignKey(Agency, on_delete=models.PROTECT)
    description = models.CharField(max_length=255, default='Description')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255)
    work_unit = models.ForeignKey(WorkUnit, on_delete=models.PROTECT)
    description = models.CharField(max_length=255, default='Description')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    nip = models.CharField(max_length=255)
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    work_unit = models.ForeignKey(WorkUnit, on_delete=models.PROTECT)
    agency = models.ForeignKey(Agency, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MemoState(models.Model):
    name = models.CharField(max_length=255)
    previous_state = models.ForeignKey('self', on_delete=models.PROTECT, related_name='fk_previous_state', null=True)
    next_state = models.ForeignKey('self', on_delete=models.PROTECT, related_name='fk_next_state', null=True)
    authorized_changer = models.ForeignKey(User, on_delete=models.PROTECT)
    description = models.CharField(max_length=255, default='Description')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MemoType(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, default='Description')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MemoTrait(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, default='Description')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MemoCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, default='Description')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Memo(models.Model):
    STATUS_PEREKAMAN_SURAT = 0
    STATUS_DISTRIBUSI_KABAG = 1
    STATUS_DISPOSISI_KASUBAG = 2
    STATUS_DISPOSISI_PELAKSANA = 3
    STATUS_CHOICES = (
        (STATUS_PEREKAMAN_SURAT, 'Perekaman Surat'),
        (STATUS_DISTRIBUSI_KABAG, 'Distribusi Kabag'),
        (STATUS_DISPOSISI_KASUBAG, 'Disposisi Kasubag'),
        (STATUS_DISPOSISI_PELAKSANA, 'Disposisi Pelaksana'),
    )
    subject = models.CharField(max_length=255)
    information = models.CharField(max_length=255)
    state = FSMIntegerField(choices=STATUS_CHOICES, default=STATUS_PEREKAMAN_SURAT, protected=True)
    sender = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    type = models.ForeignKey(MemoType, on_delete=models.PROTECT)
    trait = models.ForeignKey(MemoTrait, on_delete=models.PROTECT)
    category = models.ForeignKey(MemoCategory, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @transition(field=state, source=STATUS_PEREKAMAN_SURAT, target=STATUS_DISTRIBUSI_KABAG)
    def status_perekaman_surat_to_status_distribusi_kabag(self):
        pass

    @transition(field=state, source=STATUS_DISTRIBUSI_KABAG, target=STATUS_DISPOSISI_KASUBAG)
    def status_distribusi_kabag_to_status_disposisi_kasubag(self):
        pass

    @transition(field=state, source=STATUS_DISPOSISI_KASUBAG, target=STATUS_DISPOSISI_PELAKSANA)
    def status_disposisi_kasubag_to_status_disposisi_pelaksana(self):
        pass

    def __str__(self):
        return self.subject


class Attachment(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    file = models.FileField(upload_to='attachment/')
    memo = models.ForeignKey(Memo, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MemoSimple(models.Model):
    STATUS_PEREKAMAN_SURAT = 0
    STATUS_DISTRIBUSI_KABAG = 1
    STATUS_DISPOSISI_KASUBAG = 2
    STATUS_DISPOSISI_PELAKSANA = 3
    STATUS_CHOICES = (
        (STATUS_PEREKAMAN_SURAT, 'Perekaman Surat'),
        (STATUS_DISTRIBUSI_KABAG, 'Distribusi Kabag'),
        (STATUS_DISPOSISI_KASUBAG, 'Disposisi Kasubag'),
        (STATUS_DISPOSISI_PELAKSANA, 'Disposisi Pelaksana'),
    )
    STATUS_TRANSITIONS = (
        (0, 'status_perekaman_surat_to_status_distribusi_kabag'),
        (1, 'status_distribusi_kabag_to_status_disposisi_kasubag'),
        (2, 'status_disposisi_kasubag_to_status_disposisi_pelaksana'),
    )
    subject = models.CharField(max_length=255)
    information = models.CharField(max_length=255)
    state = FSMIntegerField(choices=STATUS_CHOICES, default=STATUS_PEREKAMAN_SURAT, protected=True)
    sender = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('disposisi:memo-simple-list')

    @transition(field=state, source=STATUS_PEREKAMAN_SURAT, target=STATUS_DISTRIBUSI_KABAG,
                permission='disposisi.to_status_distribusi_kabag')
    def status_perekaman_surat_to_status_distribusi_kabag(self):
        pass

    @transition(field=state, source=STATUS_DISTRIBUSI_KABAG, target=STATUS_DISPOSISI_KASUBAG,
                permission='disposisi.to_status_disposisi_kasubag')
    def status_distribusi_kabag_to_status_disposisi_kasubag(self):
        pass

    @transition(field=state, source=STATUS_DISPOSISI_KASUBAG, target=STATUS_DISPOSISI_PELAKSANA,
                permission='disposisi.to_status_disposisi_pelaksana')
    def status_disposisi_kasubag_to_status_disposisi_pelaksana(self):
        pass

    def __str__(self):
        return self.subject
