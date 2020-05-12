from django.contrib import admin

from .models import Agency, WorkUnit, Position, Account, Attachment, MemoState, MemoType, MemoTrait, MemoCategory, Memo


# Register your models here.

class AgencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'description', 'created_at', 'updated_at')


class WorkUnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'agency', 'description', 'created_at', 'updated_at')


class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'work_unit', 'description', 'created_at', 'updated_at')


class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'nip', 'position', 'work_unit', 'agency', 'created_at', 'updated_at')


class MemoStateAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'previous_state', 'next_state', 'authorized_changer', 'description', 'created_at', 'updated_at')


class MemoTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')


class MemoTraitAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')


class MemoCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')


class MemoAdmin(admin.ModelAdmin):
    list_display = (
        'subject', 'information', 'memo_state', 'sender', 'author', 'type', 'trait', 'category', 'created_at',
        'updated_at')


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'file', 'memo', 'created_at', 'updated_at')


admin.site.register(Agency, AgencyAdmin)
admin.site.register(WorkUnit, WorkUnitAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(MemoState, MemoStateAdmin)
admin.site.register(MemoType, MemoTypeAdmin)
admin.site.register(MemoTrait, MemoTraitAdmin)
admin.site.register(MemoCategory, MemoCategoryAdmin)
admin.site.register(Memo, MemoAdmin)
admin.site.register(Attachment, AttachmentAdmin)
