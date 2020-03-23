import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow_docs as tfdocs
import tensorflow_docs.plots
import tensorflow_docs.modeling
import os
import numpy as np

from sklearn import preprocessing
print(tf.__version__)
os.listdir()

raw_dataset = pd.read_csv("RealFlorianopolisDistancia")
# raw_dataset = pd.read_csv("FloriapEstimator II/RealFlorianopolisDistancia")

del raw_dataset["Endereco"]
del raw_dataset["AreaServico"]
del raw_dataset["Varanda"]
del raw_dataset["Lavanderia"]
del raw_dataset["Playground"]
del raw_dataset["SalaoFestas"]
del raw_dataset["ArCondicionado"]

dataset = pd.get_dummies(raw_dataset, columns=['Bairro'])
del dataset['Bairro_0']


dataset.tail()
dataset.isna().sum()
dataset = dataset.dropna()

train_dataset = dataset.sample(frac=0.7,random_state=0)
test_dataset = dataset.drop(train_dataset.index)

sns.pairplot(train_dataset[["Tamanho", "Quartos","Garagem","Banheiros"]], diag_kind="kde")
plt.show()

train_stats = train_dataset.describe()
train_stats.pop("Prices")
train_stats = train_stats.transpose()
train_stats

train_labels = train_dataset.pop('Prices')
test_labels = test_dataset.pop('Prices')

train_labels = np.asarray(train_labels)
test_labels = np.asarray(test_labels)
normed_train_data = np.asarray(train_dataset)
normed_test_data = asarray(test_dataset)

def build_model():
  model = keras.Sequential([
    layers.Dense(128, activation='relu', input_shape=[len(train_dataset.keys())]),
    layers.Dense(128, activation='relu'),
    layers.Dense(128, activation='relu'),
    layers.Dense(128, activation='relu'),
    layers.Dense(128, activation='relu'),
    layers.Dense(128, activation='relu'),
    layers.Dense(128, activation='relu'),
    layers.Dense(128, activation='relu'),
    layers.Dense(128, activation='relu'),
    layers.Dense(1),
  ])

  optimizer = tf.keras.optimizers.RMSprop(0.001)

  model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['mae', 'mse'])
  return model

model = build_model()
model.summary()


example_batch = normed_train_data[:10]
example_result = model.predict(example_batch)
example_result

EPOCHS = 10000

history = model.fit(
  normed_train_data, train_labels,
  epochs=EPOCHS, validation_split = 0.3, verbose=0,
  callbacks=[tfdocs.modeling.EpochDots()])

hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch
hist.tail()

plotter = tfdocs.plots.HistoryPlotter(smoothing_std=2)

plotter.plot({'Basic': history}, metric = "mean_absolute_error")
plt.ylim([0, 10])
plt.ylabel('MAE [Prices]')
plt.show()

plotter.plot({'Basic': history}, metric = "mean_squared_error")
plt.ylim([0, 20])
plt.ylabel('MSE [Prices^2]')
plt.show()

model.save('ModeloRealImoveis')
