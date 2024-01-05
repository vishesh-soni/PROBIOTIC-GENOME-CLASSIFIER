from django import forms
from multiupload.fields import MultiFileField 
from .models import *


class KmerForm(forms.ModelForm):
    class Meta:
        model = Kmer
        fields = ['kmer_files']

    kmer_files = MultiFileField(max_file_size=1024 * 1024 * 1024, required=False)

class ProForm(forms.ModelForm):
    class Meta:
        model = Pro_file
        fields = '__all__'
        labels = {
            'pro_seq': 'Path to labelled k-mer set 1:',
        }

class PatForm(forms.ModelForm):
    class Meta:
        model = Pat_file
        fields = '__all__'
        labels = {
            'pat_seq': 'Path to labelled k-mer set 2:',
        }


class SeqForm(forms.ModelForm):
    class Meta:
        model = Seq
        fields = '__all__'
        labels = {
            'sequence': 'Path to the directory containing genomes:',
        }


class MLfileForm(forms.ModelForm):
    class Meta:
        model = MLmodel
        fields = '__all__'
        labels = {
            'ml_file': 'Path to directory containing models:',
        }