import pandas as pd
import pickle
from sklearn import preprocessing
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier #Random Forest
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import numpy as np

def output(pred,class_1,class_2):
    out =[]
    for i in pred:
        if i==0:
            out.append(class_1)
        else:
            out.append(class_2)
    return out

def output_1(pred):
    out =[]
    for i in pred:
        if i==0:
            out.append('pro')
        else:
            out.append('pat')
    return out

def round_off(prob):
    pat_score=[]
    pro_score =[]
    for i in prob:
        pat_score.append(round(i[0], 3))
        pro_score.append(round(i[1], 3))
    return pat_score,pro_score

def training(pro_path,pat_path,model_type):

    ## File path for pat and pro
    pro_i_mer = pd.read_csv('media\pro_file'+'\\'+str(pro_path), index_col = 'Assembly Accession')
    pat_i_mer = pd.read_csv('media\pat_file'+'\\'+str(pat_path), index_col = 'Assembly Accession')

    class_1 = pro_i_mer['Category'][0]
    class_2 = pat_i_mer['Category'][1]
    print(str(class_1),str(class_2))
    
    ## Concat the pat and pro dataframe
    pat_pro_i_mer = pd.concat([pro_i_mer, pat_i_mer])
    pat_pro_i_mer['Category'] = pat_pro_i_mer['Category'].replace({str(class_1): 1})
    pat_pro_i_mer['Category'] = pat_pro_i_mer['Category'].replace({str(class_2): 0})
    datasets=pat_pro_i_mer

    ## Feature Engineering
    feature_names = ['TCTACA','Category', 'TGGTCCAG', 'ATCCTTGC', 'TGAGGCGG', 'GTTCCTG', 'ACCGATA', 'CTATCTGG', 'TCCTTCAG', 'GTCGATT', 'CTACACTA', 'GATAGGGA', 'CATGTGAA', 'AAGGACG', 'CGGATATT', 'AACTTGA', 'ACGAGG', 'ATAGGGCG', 'GTTTACT', 'AAGCCTA', 'GCCCGT', 'CCACCGT', 'ACAT', 'GTCTATGG', 'GACATGG', 'GAATTGAA', 'TCGCAATG', 'ACTCGTG', 'AGTTCCTG', 'TCTCACGG', 'AAAGCGA', 'CCATAGAT', 'GATCATTC', 'GACTAGTC', 'GACCCTG', 'CTGCATG', 'TGAGCTT', 'GTCTCAGG', 'AATTC', 'CGGTCAAT', 'ACCAAAG', 'CTATCGA', 'GACAGTA', 'CTAGCA', 'CCATAGA', 'GGAGATTT', 'TAACCTTC', 'ACATGGT', 'GAATTGTA', 'AGGTGC', 'CTGAGACA', 'AATGCAAC', 'CTATCGGT', 'GCTCTTGA', 'TGAGACCC', 'AAGCTCAC', 'AATCCCT', 'CTAA', 'ACTTACTT', 'AAGTTCCA', 'TACACACT', 'ACACTCC', 'TCTACAAT', 'TCACTTCA', 'TTCTCACA', 'TTTGGAG', 'CACACGAC', 'GGTCACCG', 'GAACCGTG', 'GCTTGCTA', 'GAGGCGT', 'CATACCTC', 'TTGGACCA', 'CAATTGTA', 'GTACTACG', 'CCAGGAA']
    dataset_filtered = datasets.loc[:, feature_names]
    y = dataset_filtered["Category"]
    # print(y)
    dataset_filtered = dataset_filtered.drop(["Category"], axis=1)

    #First scale the whole data in a standard distribution
    x = dataset_filtered.values
    Standard_Scaler = preprocessing.StandardScaler()
    x_scaled = Standard_Scaler.fit_transform(x)
    x_scaled_df = pd.DataFrame(x_scaled, columns=dataset_filtered.columns)
    x_scaled_df.index = dataset_filtered.index

    ## Train Test Split
    X_train, X_test, y_train, y_test = train_test_split(x_scaled_df, y, test_size = 0.1, random_state=0)
    assembly_accession = np.array(x_scaled_df.index)
    assembly_accession = np.reshape(assembly_accession,[-1])
    print(y_train)
    print(model_type)
    ## Model 1
    if int(model_type) == 1:
        classifier = XGBClassifier()
        classifier_name = "XG Boost"
        print(classifier_name)
        classifier.fit(X_train, y_train.astype('int'))


    ## Model 2 
    elif int(model_type) == 2:
        classifier = RandomForestClassifier()
        classifier.fit(X_train, y_train.astype('int'))


    ## Model 3 
    elif int(model_type) == 3:
        classifier = DecisionTreeClassifier()
        classifier.fit(X_train, y_train.astype('int'))

    
    
    ## Fit the model
    

    print("Testing")
    y_pred = classifier.predict(x)
    prob = classifier.predict_proba(x)
    print(prob.shape)
    y_pred = output(y_pred,class_1,class_2)
    pat_score,pro_score = round_off(prob)
    return y_pred,assembly_accession,pat_score,pro_score