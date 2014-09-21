from django.contrib import admin

from attendance.models import Member, AccessCard, LoggingEvent


# Customised model admin objects
class MemberAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Registration', {'fields': ['student_id', 'reg_date']}),
        ('Identity', {'fields': ['f_name', 'l_name']}),
        ('Status', {'fields': ['checked_in']}),
        ('Contact details', {'fields': []}), # TODO: admin should also see and update address, phone, card, ... in the same form
    ]
    list_display = ('student_id', 'f_name', 'l_name', 'checked_in', 'reg_date')
    readonly_fields = ('reg_date',)


class AccessCardAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Registration', {'fields': ['member', 'rfid', 'reg_date']}),
        # TODO: the dropdown menu to chose member should list f_name,l_name in addition to student_id
        # TODO: the student numbers should be sorted numerically/alphabetically for easier search
    ]
    list_display = ('rfid', 'get_member_id', 'get_f_name', 'get_l_name', 'reg_date')
    readonly_fields = ('reg_date',)

    def get_f_name(self, obj):
        return obj.member.f_name

    get_f_name.short_description = 'First name'

    def get_l_name(self, obj):
        return obj.member.l_name

    get_l_name.short_description = 'Last name'

    def get_member_id(self, obj):
        return obj.member.student_id

    get_member_id.short_description = 'Student ID'


class LoggingEventAdmin(admin.ModelAdmin):
    # formfield_overrides = {
    # models.: {'widget': TextInput(attrs={'size':'8'})},
    # models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    # }
    fieldsets = [
        ('Check-in', {'fields': ['check_in', 'rfid']}),
        ('Check-out', {'fields': ['check_out']}),
    ]
    list_display = ('rfid', 'get_f_name', 'get_l_name', 'check_in', 'check_out')

    def get_f_name(self, obj):
        return AccessCard.objects.get(pk=obj.rfid).member.f_name

    get_f_name.short_description = 'First name'

    def get_l_name(self, obj):
        return AccessCard.objects.get(pk=obj.rfid).member.l_name

    get_l_name.short_description = 'Last name'


# Register models
admin.site.register(Member, MemberAdmin)
admin.site.register(AccessCard, AccessCardAdmin)
admin.site.register(LoggingEvent, LoggingEventAdmin)

members__name__startswith = 'Paul'