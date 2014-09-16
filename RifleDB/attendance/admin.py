from django.contrib import admin

from attendance.models import Member, AccessCard


# Customised model admin objects
class MemberAdmin(admin.ModelAdmin):
    # formfield_overrides = {
    # models.: {'widget': TextInput(attrs={'size':'8'})},
    #     models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    # }
    fieldsets = [
        ('Registration', {'fields': ['student_id', 'reg_date']}),
        ('Identity', {'fields': ['f_name', 'l_name']}),
        ('Contact details', {'fields': []}),
        # TODO: admin should also see and update address, phone, card, ... in the same form
    ]
    list_display = ('student_id', 'reg_date', 'f_name', 'l_name')
    readonly_fields = ('reg_date',)

# Register models
admin.site.register(Member, MemberAdmin)
admin.site.register(AccessCard)