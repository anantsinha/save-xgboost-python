# -*- coding: utf-8 -*-
"""Porting XGBoost Models to Java.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Pe2aGu-v6ZtjouzioEmZ1AHNxVmaneRa

### Mount drive & import statements
"""

from google.colab import drive
drive.mount('/content/drive')

from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd
# to dump dataframe into LIBSVM file
from sklearn.datasets import dump_svmlight_file

"""###Data pre-processing for model"""

boston = load_boston()

# convert to pandas df

data = pd.DataFrame(boston.data)
data.columns = boston.feature_names
# target variable is available in a sep attribute - boston.target
data['PRICE'] = boston.target

#separate target var
X, y = data.iloc[:,:-1],data.iloc[:,-1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

"""### Convert data into a data matrix"""

# Convert data to a DMatrix
data_dmatrix = xgb.DMatrix(data=X,label=y)

"""### Convert your data to Libsvm format

> XGBoost in Java needs data to be in Libsvm format

> The model loaded in Java will make prediction on this data, hence you may chose to replace X with X_test and y with y_test


"""

dump_svmlight_file(X=X, y=y, f='libsvmData.txt', zero_based=True)

"""### Model Creation"""

xg_reg = xgb.XGBRegressor(objective ='reg:linear', colsample_bytree = 0.3, learning_rate = 0.1,
                max_depth = 5, alpha = 10, n_estimators = 10)

xg_reg.fit(X_train,y_train)

preds = xg_reg.predict(X_test)

"""### Generate predictions using test data"""

preds = xg_reg.predict(X_test)

preds

"""### Save model to load into Java"""

xg_reg.save_model('xgbModel.model')