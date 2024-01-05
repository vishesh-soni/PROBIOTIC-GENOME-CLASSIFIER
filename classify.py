import pandas as pd
import pickle
from sklearn import preprocessing
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier #Random Forest
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from model_training import *

def preprocess(dataset_path,model_type):

    if int(model_type) == 1:
        classifier = pickle.load(open('media\ml_model\model.pkl', 'rb'))
        print(model_type)
    
    dataset = pd.read_csv('media\seq'+'\\'+str(dataset_path),index_col = 'Assembly Accession')
    print(dataset.shape)

    dataset = dataset.drop(['Category'],axis=1)
    assembly_accession = list(dataset.index)

    feature_names = ['TCTACA', 'TGGTCCAG', 'ATCCTTGC', 'TGAGGCGG', 'GTTCCTG', 'ACCGATA', 'CTATCTGG', 'TCCTTCAG', 'GTCGATT', 'CTACACTA', 'GATAGGGA', 'CATGTGAA', 'AAGGACG', 'CGGATATT', 'AACTTGA', 'ACGAGG', 'ATAGGGCG', 'GTTTACT', 'AAGCCTA', 'GCCCGT', 'CCACCGT', 'ACAT', 'GTCTATGG', 'GACATGG', 'GAATTGAA', 'TCGCAATG', 'ACTCGTG', 'AGTTCCTG', 'TCTCACGG', 'AAAGCGA', 'CCATAGAT', 'GATCATTC', 'GACTAGTC', 'GACCCTG', 'CTGCATG', 'TGAGCTT', 'GTCTCAGG', 'AATTC', 'CGGTCAAT', 'ACCAAAG', 'CTATCGA', 'GACAGTA', 'CTAGCA', 'CCATAGA', 'GGAGATTT', 'TAACCTTC', 'ACATGGT', 'GAATTGTA', 'AGGTGC', 'CTGAGACA', 'AATGCAAC', 'CTATCGGT', 'GCTCTTGA', 'TGAGACCC', 'AAGCTCAC', 'AATCCCT', 'CTAA', 'ACTTACTT', 'AAGTTCCA', 'TACACACT', 'ACACTCC', 'TCTACAAT', 'TCACTTCA', 'TTCTCACA', 'TTTGGAG', 'CACACGAC', 'GGTCACCG', 'GAACCGTG', 'GCTTGCTA', 'GAGGCGT', 'CATACCTC', 'TTGGACCA', 'CAATTGTA', 'GTACTACG', 'CCAGGAA']
    dataset_filtered = dataset.loc[:, feature_names]
    print(dataset_filtered.shape)
    x = dataset_filtered.values
    Standard_Scaler = preprocessing.StandardScaler()
    x_scaled = Standard_Scaler.fit_transform(x)
    x_scaled_df = pd.DataFrame(x_scaled, columns=dataset_filtered.columns)
    x_scaled_df.index = dataset_filtered.index
    y_pred = classifier.predict(x_scaled_df)
    prob = classifier.predict_proba(x_scaled_df)
    pat_score,pro_score = round_off(prob)
    return y_pred,assembly_accession,pat_score,pro_score