from django.db import models
from django.utils.translation import gettext_lazy as _
import datetime

class Shp(models.Model):
    name = models.CharField(_("Nama Peta"), max_length=50)
    description = models.CharField(_("Deskripsi"), max_length=1000, blank=True)
    file = models.FileField(_("Unggah Berkas"), upload_to='%Y/%m/%d')
    uploaded_date = models.DateField(_("Tanngal Unggah"), default=datetime.date.today, blank=True)

    def __str__(self) -> str:
        return self.name