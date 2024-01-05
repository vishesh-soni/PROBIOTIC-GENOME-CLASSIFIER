from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Kmer)
class KmerAdmin(admin.ModelAdmin):
    list_display = ['id','kmer_file']


@admin.register(Pro_file)
class ProAdmin(admin.ModelAdmin):
    list_display = ['id','pro_seq']

@admin.register(Pat_file)
class PatAdmin(admin.ModelAdmin):
    list_display = ['id','pat_seq']

@admin.register(Seq)
class SeqAdmin(admin.ModelAdmin):
    list_display = ['id','sequence']


@admin.register(MLmodel)
class MLfileAdmin(admin.ModelAdmin):
    list_display = ['id','ml_file']





