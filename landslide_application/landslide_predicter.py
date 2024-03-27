import pickle

# Load the model from the pickle file
with open('xgb_model.pkl', 'rb') as model_file:
    loaded_xgb_model = pickle.load(model_file)


import numpy as np

def landslide_fn(features_list):
                int_features2 = np.array(features_list)

                int_features1 = int_features2.reshape(1, -1)


                tested1=loaded_xgb_model.predict(int_features1)



                print(tested1)

                return  tested1

