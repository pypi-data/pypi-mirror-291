from django.db import models
import json
import gzip
from io import BytesIO
from django.utils.html import format_html
from django.conf import settings

class userLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    time = models.DateTimeField(max_length=9999,null=True,blank=True)
    url = models.CharField(max_length=255,null=True, blank=True)
    metaData = models.BinaryField(null=True, blank=True)
    postData = models.BinaryField(null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    status_code = models.IntegerField(default=0)
    status_type = models.CharField(max_length=9999,null=True,blank=True)
    def __str__(self):
        user_display = self.user.username if self.user else "Anonymous"
        return (
            f"{user_display}"
        )
    
    @staticmethod
    def decompress_json(compressed_data):
        buf = BytesIO(compressed_data)
        with gzip.GzipFile(fileobj=buf, mode='rb') as f:
            return f.read().decode('utf-8')
        
    def get_metadata(self):
        return userLog.decompress_json(self.metaData) if self.metaData else ""

    def get_postdata(self):
        return userLog.decompress_json(self.postData) if self.postData else ""

    def format_json_as_html(self, json_data):
        if not json_data:
            return ""
        try:
            data = json.loads(json_data)
            return format_html('<pre>{}</pre>', json.dumps(data, indent=2))
        except json.JSONDecodeError:
            return format_html('<pre>{}</pre>', json_data)
        
    def get_time(self):
        return self.time.strftime('%d.%m.%y %H:%m:%S') if self.time else ""
    
    def get_status_code(self):
        status_colors = {
            200: 'green',
            400: 'orange',
            404: 'red',
            500: 'purple',
        }

        status_code = self.status_code 

        color = status_colors.get(status_code, 'black')

        return format_html(
            '<span style="color: {};font-weight:800;">{}</span>',
            color,
            status_code
        )
