from django.contrib import admin
from .models import Teacher, Student, Classe, Topic, Message, Contact


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'joined_classes')
    readonly_fields = ('joined_classes',)

    def joined_classes(self, obj):
        return ", ".join(c.name for c in obj.classes.all())
    joined_classes.short_description = "Joined classes"


admin.site.register(Teacher)
admin.site.register(Student, StudentAdmin)
admin.site.register(Classe)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Contact)