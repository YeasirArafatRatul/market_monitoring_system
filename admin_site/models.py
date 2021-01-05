from django.db import models

# Create your models here.
NOTICE_TYPE = (
    ('warning', 'WARNING'),
    ('fine', 'FINE'),
    ('info', 'INFO'),
    ('order', 'ORDER'),
)


class Notice(models.Model):
    receiver = models.CharField(max_length=34)
    subject = models.CharField(max_length=250)
    description = models.TextField()
    notice_type = models.CharField(
        max_length=34, choices=NOTICE_TYPE, default='info')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.receiver} -> {self.subject}'
