import tensorflow as tf
import pandas as pd                                         # data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np                                          # linear algebra
from tensorflow.keras.models import Sequential              # model type
from tensorflow.keras.layers import Dense, Dropout          # dense layer, dropout layer
from tensorflow.keras.activations import relu, sigmoid      # activation functions
from tensorflow.keras.optimizers import SGD                 # stochastic gradient descent
from tensorflow.keras.losses import binary_crossentropy     # cost function

df = pd.read_csv('dataset\Fraud_Detection_Dataset.csv')     # read csv file

cat_columns = df.select_dtypes(include='object').columns    # categorical columns
num_columns = df.select_dtypes(include=np.number).columns   # numerical columns

from sklearn.preprocessing import OneHotEncoder             # one hot encoder
from sklearn.compose import ColumnTransformer               # column transformer
from sklearn.preprocessing import StandardScaler            # standard scaler
from sklearn.model_selection import train_test_split        # train test split
from sklearn.metrics import confusion_matrix, classification_report # confusion matrix, classification report
from sklearn.pipeline import Pipeline                       # pipeline
from imblearn.over_sampling import SMOTE                    # SMOTE

X = df.drop(columns=['isFraud', 'isFlaggedFraud'])        # features
y = df['isFraud']                                       # target
smote = SMOTE()                                        # SMOTE

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(drop='first'), ['type']),
        ('num', StandardScaler(), num_columns[:-2])
    ])  # preprocessor, drop first to avoid dummy variable trap, standard scaler to scale numerical columns, drop last two columns because they are not needed, i.e. isFraud and isFlaggedFraud

p = Pipeline(steps=[('preprocessor', preprocessor)])    # pipeline

Xp = p.fit_transform(X)                                # fit and transform X
Xp, y = smote.fit_resample(Xp, y)                   # fit and transform X and y

# Creating Neural Network Model

model_vgg8 = Sequential()   # sequential model
model_vgg8.add(Dense(units=256, activation=relu, input_shape=(Xp.shape[1],)))   # input layer
model_vgg8.add(Dropout(0.2))    # dropout layer, 20% of neurons will be dropped
model_vgg8.add(Dense(units=128, activation=relu))   # hidden layer, relu activation function, 128 neurons
model_vgg8.add(Dropout(0.2))
model_vgg8.add(Dense(units=64, activation=relu))    # hidden layer, relu activation function, 64 neurons
model_vgg8.add(Dropout(0.2))
model_vgg8.add(Dense(units=32, activation=relu))    # hidden layer, relu activation function, 32 neurons
model_vgg8.add(Dropout(0.2))
model_vgg8.add(Dense(units=16, activation=relu))    # hidden layer, relu activation function, 16 neurons
model_vgg8.add(Dropout(0.2))
model_vgg8.add(Dense(units=8, activation=relu))    # hidden layer, relu activation function, 8 neurons
model_vgg8.add(Dropout(0.2))
model_vgg8.add(Dense(units=4, activation=relu))   # hidden layer, relu activation function, 4 neurons
model_vgg8.add(Dropout(0.2))
model_vgg8.add(Dense(units=2, activation=relu))   # hidden layer, relu activation function, 2 neurons
model_vgg8.add(Dropout(0.2))
model_vgg8.add(Dense(units=1, activation=sigmoid))  # output layer, sigmoid activation function, 1 neuron

# optimizer is stochastic gradient descent, which is a good default optimizer, for more info see https://keras.io/api/optimizers/sgd/
model_vgg8.compile(
    optimizer=SGD(),
    loss=binary_crossentropy,
    metrics=['accuracy', 'Precision', 'Recall']
)   # compile model, loss function is binary crossentropy, metrics are accuracy, precision and recall

model_vgg8.summary()    # summary of the model, i.e. layers, neurons, parameters, etc.

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(Xp, y, test_size=0.2, random_state=42)

# Training the model
history = model_vgg8.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2)

# Evaluating the model
model_vgg8.evaluate(X_test, y_test)

# Predicting the test set results
y_pred = model_vgg8.predict(X_test)
y_pred = (y_pred > 0.5)

# save model 
model_vgg8.save('model_vgg8.h5')
