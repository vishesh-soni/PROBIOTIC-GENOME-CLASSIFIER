from django.shortcuts import render
from .forms import *
from .models import *
import pandas as pd
import pickle
from sklearn import preprocessing
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os
# import zipfile
from kmer_single_gen import *
from model_training import *
from classify import *

from django.http import HttpResponse
from django.views import View
import csv

def home(request):
    return render(request,'home.html')

def kmer(request):
    kmer_call = KmerForm()
    param = {"kmer_file_input":kmer_call}

    return render(request, 'Kmer.html',param)
    

def download(request):
    if request.method == "POST":
        # print('out')
        kmer_call = KmerForm(request.POST,request.FILES)
        entered_text = request.POST.get('my_text_field')
        print(request.POST,request.FILES)
        # kmer_path = request.FILES['kmer_files']

        if kmer_call.is_valid():
            kmer_instance = kmer_call.save()

######
        #  Create the directory if it doesn't exist
        upload_directory = os.path.join("media\kmer_files", str(kmer_instance.id))
        os.makedirs(upload_directory, exist_ok=True)

        # Handle each uploaded file
        for uploaded_file in request.FILES.getlist('kmer_files'):
            # Customize this function to define the upload path for each file
            upload_path = os.path.join(upload_directory, uploaded_file.name)

            with open(upload_path, "wb+") as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

        fasta_files = []
        for uploaded_file in request.FILES.getlist('kmer_files'):
                # Customize this function to define the upload path for each file
                upload_path = os.path.join(upload_directory, uploaded_file.name)
                fasta_files.append(upload_path)

        # Example usage:
        random_string = generate_random_string(10)
        destination_directory_1 = 'media\Temp'
        destination_directory = 'media\Temp'+'\\'+str(random_string)+'.csv'
        os.makedirs(destination_directory_1, exist_ok=True)
        alphabet = "ACGT"

        k = 8
        k_values = []
        if (upto == 1):
            start_i_k = 1
        else:
            start_i_k = k
        k_values = range(start_i_k, k+1)
        print(k_values)

        # # If numeric binning is turned on, compute quantile boundaries for various
        # # values of k.
        kmer_list = make_upto_kmer_list(k_values, alphabet)
        print(len(kmer_list))
        # fasta_files = ['sequence.fasta', 'sequence1.fasta' ,'sequence2.fasta' ,'sequence3.fasta' ]
        df = process_multiple_sequences(fasta_files, kmer_list) 
        df['Category'] = entered_text
        column_to_move = 'Category'
        columns = df.columns.tolist()
        columns = [column_to_move] + [col for col in columns if col != column_to_move]
        df = df[columns]
        file_path = destination_directory
        df.to_csv(file_path, index=False)
        df_subset = df.iloc[:, :5]

    # Convert the DataFrame to HTML
        table_html = df_subset.to_html(classes='table table-striped', index=True)

        print(df.shape)
        print(file_path)
        context = {'file_path':file_path,'table_html': table_html}
######


    return render(request,'download.html',context)

def train(request):
    pro_call = ProForm()
    pat_call = PatForm()
    param = {"pro_file_input":pro_call,'pat_file_input':pat_call}
    return render(request,'train.html',param)
    

def result(request):
    if request.method == "POST":
        print('training result')

        ## Django Model Call
        pro_call = ProForm(request.POST,request.FILES)
        pat_call = PatForm(request.POST,request.FILES)
        
        ## Save model
        if pro_call.is_valid():
            pro_call.save()
        if pat_call.is_valid():
            pat_call.save()

        ## Fetching File Path
        pro_path = request.FILES['pro_seq']
        pat_path = request.FILES['pat_seq']
        print(pro_path,pat_path)
        model_type =  request.POST.get('selected_option')

        

        pred,assembly_accession,pat_score,pro_score = training(pro_path,pat_path,model_type)
        # print(pred)
        print(len(pred),len(assembly_accession))
        df = pd.DataFrame(assembly_accession,columns=['Assembly_Accession'])
        df['Predicted Category'] = pred
        df['Probability of Category 1(Pro)'] = pro_score
        df['Probability of Category 2(Pat)'] = pat_score
        df['Probability of Category 2(Pat)'] = pat_score
        elements = df.to_html(classes='table table-striped', index=False)
        # elements = list(zip(assembly_accession,pred,pat_score,pro_score))
        param = {"elements":elements}
    return render(request,'result.html',param)

def classify(request):
    seq_call = SeqForm()
    model_call = MLfileForm()
    param = {"sequence_file_input":seq_call,'model_file_input':model_call}
    return render(request,'classify.html',param)


def predict(request):
    if request.method == "POST":
        print("Classifiy")

        ## Django Model Call
        seq_call = SeqForm(request.POST,request.FILES)
        model_call = MLfileForm(request.POST,request.FILES)

        ## Fetch Files path
        seq_path = request.FILES['sequence']
        model_path = request.FILES['ml_file']
        model_type =  request.POST.get('selected_option')

        ## Save the model
        if seq_call.is_valid():
            seq_call.save()
        if model_call.is_valid():
            model_call.save()

        y_pred,assembly_accession,pat_score,pro_score = preprocess(seq_path,model_type)
        pred = output_1(y_pred)
        print(assembly_accession)
        print(y_pred)
        df = pd.DataFrame(assembly_accession,columns=['Assembly_Accession'])
        df['Predicted Category'] = pred
        df['Probability of Category 1(Pro)'] = pro_score
        df['Probability of Category 2(Pat)'] = pat_score
        elements = df.to_html(classes='table table-striped', index=False)
        # elements = list(zip(assembly_accession,pred,pat_score,pro_score))
        param = {"sequence_file_input":seq_call,'elements':elements}

    return render(request,'predict.html',param)