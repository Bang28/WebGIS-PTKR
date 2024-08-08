from django.db import models
from django.utils.translation import gettext_lazy as _
import datetime
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import geopandas as gpd
import os
import glob
import zipfile
from sqlalchemy import *
from geo.Geoserver import Geoserver
from pg.pg import Pg 

# Initialize the library
db = Pg(dbname='ptkr', user='postgres', password='12345678', host='localhost', port='5433')
geo = Geoserver('http://127.0.0.1:8080/geoserver', username='admin', password='geoserver')

# Database connection string (postgresql://${database_user}:${databse_password}@${database_host}:${database_port}/${database_name}
conn_str = 'postgresql://postgres:12345678@localhost:5433/ptkr'

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
    file = instance.file.path
    file_format = os.path.basename(file).split('.')[-1]
    file_name = os.path.basename(file).split('.')[0]
    file_path = os.path.dirname(file)
    name = instance.name

    # extract zipfile
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(file_path)

    os.remove(file) # remove zip file

    shp = glob.glob(r'{}/**/*.shp'.format(file_path), 
                    recursive=True) # to get shp

    try:
        req_shp = shp[0]
        gdf = gpd.read_file(req_shp) #make geodataframe
        engine = create_engine(conn_str) # create the SQLAlchemy's engine to use
        gdf.to_postgis(
            con=engine,
            schema='data',
            name=name,
            if_exists='replace'
        )

        for s in shp:
            os.remove(s)

    except Exception as e:
        for s in shp:
            os.remove(s)

        instance.delete()
        print('There is problem during shp uploade: ', e)

    # publish shp to the geoserver using gerserver-rest
    try:
        geo.create_featurestore(store_name=name, workspace='ptkr', db='ptkr', host='localhost', 
                                pg_user='postgres', pg_password='12345678', schema='data', port=5433)
        geo.publish_featurestore(workspace='ptkr', store_name=name, pg_table=name)
        geo.create_outline_featurestyle('ptkr_shp', workspace='ptkr')
        geo.publish_style(layer_name=name, style_name='ptkr_shp', workspace='ptkr')
    except Exception as e:
        print(e)

@receiver(post_delete, sender=Shp)
def delete_date(sender, instance, created, **kwargs):
    pass