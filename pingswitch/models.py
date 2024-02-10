from django.db import models

class PingData(models.Model):
    switch_label = models.CharField(max_length=3)
    t1 = models.IntegerField()
    t2 = models.IntegerField()
    t3 = models.IntegerField()
    t4 = models.IntegerField()
    t5 = models.IntegerField()
    ping_status = models.IntegerField()
    ping_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.switch_label} - {self.ping_time}"
