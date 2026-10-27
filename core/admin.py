from django.contrib import admin
from .models import PageView

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ('path', 'user', 'ip_address', 'timestamp')
    list_filter = ('timestamp', 'path')
    search_fields = ('path', 'user__username', 'ip_address', 'user_agent')
    date_hierarchy = 'timestamp'
    readonly_fields = ('path', 'user', 'ip_address', 'user_agent', 'referer', 'session_key', 'timestamp')

    def has_add_permission(self, request):
        return False
