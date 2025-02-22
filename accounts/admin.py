from django.contrib import admin
from .models import Relation,User, UserInfo
from django.contrib.auth.admin import UserAdmin

admin.site.register(Relation)


class InfoInline(admin.TabularInline):
    model=UserInfo


class ExtendedUserAdmin(UserAdmin):
    inlines=(InfoInline,)



admin.site.unregister(User)
admin.site.register(User,ExtendedUserAdmin)
