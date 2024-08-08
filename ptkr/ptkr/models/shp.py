from django.db import models
from django.utils.translation import gettext_lazy as _
import datetime
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Shp(models.Model):
    name = models.CharField(_("Nama Peta"), max_length=50)
    description = models.CharField(_("Deskripsi"), max_length=1000, blank=True)
    file = models.FileField(_("Unggah Berkas"), upload_to='%Y/%m/%d')
    uploaded_date = models.DateField(_("Tanggal Unggah"), default=datetime.date.today, blank=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = 'Shape Files'


@receiver(post_save, sender=Shp)
def publish_date(sender, instance, created, **kwargs):
    pass

@receiver(post_delete, sender=Shp)
def delete_date(sender, instance, created, **kwargs):
    pass