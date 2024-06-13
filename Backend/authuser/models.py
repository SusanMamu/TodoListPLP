from django.db import models

class OTP(models.Model):
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    otp = models.TextField()
    expirydate = models.TextField()
    email = models.EmailField(null=True)


    def __str__(self):
        return f"{self.id} - {self.email} "

    class Meta:
        db_table = 'otps'