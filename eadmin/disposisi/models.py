from django.db import models
from django.contrib.auth.models import User


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
    subject = models.CharField(max_length=255)
    information = models.CharField(max_length=255)
    memo_state = models.ForeignKey(MemoState, on_delete=models.PROTECT)
    sender = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    type = models.ForeignKey(MemoType, on_delete=models.PROTECT)
    trait = models.ForeignKey(MemoTrait, on_delete=models.PROTECT)
    category = models.ForeignKey(MemoCategory, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
