from django.contrib import admin
from request_logger.models import userLog


@admin.register(userLog)
class UserLogAdmin(admin.ModelAdmin):
    list_display = ['user','ip','url','status_type','get_status_code','get_time']
    readonly_fields = ['metadata_display', 'postdata_display']
    search_fields = ['ip','user__username']
    list_filter = ['user','status_code','status_type','time']

    def metadata_display(self, obj):
        return obj.format_json_as_html(obj.get_metadata())

    def postdata_display(self, obj):
        return obj.format_json_as_html(obj.get_postdata())

    metadata_display.short_description = 'Metadata'
    postdata_display.short_description = 'Post Data'