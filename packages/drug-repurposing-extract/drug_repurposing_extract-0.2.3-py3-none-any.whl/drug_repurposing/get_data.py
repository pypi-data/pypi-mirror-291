import requests
import csv
from padelpy import from_smiles
import pandas as pd
import pkgutil
import pickle

model_data = pkgutil.get_data(__name__, 'rf_model.pkl')

def generate_data_from_list(cids=[]):
    results = []
    fails = []
    for cid in cids:
        try:
            resp = requests.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/" + str(cid) + "/property/MolecularWeight,MolecularFormula,IsomericSMILES,IUPACName/JSON")
            content = resp.json()
            desc_fp = from_smiles(content['PropertyTable']['Properties'][0]['IsomericSMILES'], fingerprints=True)
            desc_fp['cid'] = cid
            results.append(desc_fp)
        except Exception as e:
            print(e)
            # print(content)
            fails.append(cid)
    if(len(fails)>0):
        print("Fails CIDS: ", fails)

    if(len(results)>0):
        csv_file = 'complete_data.csv'
        field_names = results[0].keys()
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            for row in results:
                writer.writerow(row)

import pandas as pd
import pickle

import pickle
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def predict_data(df):
    loaded_rf_model = pickle.loads(model_data)
    
    cids = df['cid']    
    selected_columns = df.filter(like="Pubchem", axis=1)
    additional_columns = df[["ALogp2", "ALogP"]]
    df_filtered = pd.concat([selected_columns, additional_columns], axis=1)
    
    df_filtered.fillna(df_filtered.mean(), inplace=True)

    scaler = MinMaxScaler()
    df_normalized = scaler.fit_transform(df_filtered)
    df_normalized = pd.DataFrame(df_normalized, columns=df_filtered.columns, index=df_filtered.index)
    
    y_probabilities = loaded_rf_model.predict_proba(df_normalized)
    
    result_df = pd.DataFrame({'cid': cids, 
                              'predicted_output': loaded_rf_model.predict(df_normalized),
                              '0_class_probability': y_probabilities[:, 0],
                              '1_class_probability': y_probabilities[:, 1]})
    
    result_df.to_csv('predictions.csv', index=False)




# generate_data([942])
# generate_data_from_upload()