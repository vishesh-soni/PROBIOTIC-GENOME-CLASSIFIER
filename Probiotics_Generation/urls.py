from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from my_app import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('kmer',views.kmer), 
    path('download',views.download),
    path('train',views.train),
    path('result',views.result),
    path('classify',views.classify),
    path('predict',views.predict),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
