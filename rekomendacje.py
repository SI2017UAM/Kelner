#WERSJA III
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
class NeuralRecomendation:
    def __init__(self):
        self.seed = 7
        np.random.seed(self.seed)
        dataframe = pd.read_csv("workfile.csv", header=0)
        dataset = dataframe.values
        self.X = dataset[:,0:15].astype(float)
        Y = dataset[:,15]
        self.encoder = LabelEncoder()
        self.encoder.fit(Y)
        self.encoded_Y = self.encoder.transform(Y)
        self.dummy_y = np_utils.to_categorical(self.encoded_Y)
        self.out_dim=len(self.dummy_y[0])
    def createEstimator(self):
        self.estimator = KerasClassifier(build_fn=self.baseline_model, epochs=5, batch_size=5, verbose=0)
        #kfold = KFold(n_splits=10, shuffle=True, random_state=self.seed)
        #results = cross_val_score(self.estimator, self.X, self.dummy_y, cv=kfold)
        #print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
        self.estimator.fit(self.X,self.dummy_y)
    def baseline_model(self):
        # create model
        model = Sequential()
        model.add(Dense(15, input_dim=15, kernel_initializer='normal', activation='relu'))
        model.add(Dense(self.out_dim, kernel_initializer='normal', activation='softmax'))
        # Compile model
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        return model
    def predict(self,X):
        X=np.array(X)
        X=X.reshape(1,15)
        predictions = self.estimator.predict(X)
        return self.encoder.inverse_transform(predictions)[0]
