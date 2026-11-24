import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print(sns.get_dataset_names())

df = sns.load_dataset('penguins')

print(df.head(10))

print(df.shape)

print(df.tail())

print(df.isnull().sum())

print(df.describe())

print(df.dtypes)

print(df.info())

print(df.describe(include='all'))

print(df.corr(numeric_only=True))

sns.heatmap(df.corr(numeric_only=True), annot=True)
plt.show()

df.select_dtypes(include=[np.number]).hist(figsize=(12,8))
plt.show()

print(df.sex.value_counts())
print(df.island.value_counts())
print(df.species.value_counts())

sns.countplot(data=df, x='sex')
plt.show()

sns.countplot(data=df, x='island')
plt.show()

sns.countplot(data=df, x='species')
plt.show()

sns.countplot(data=df, x='sex', hue='species')
plt.show()

sns.pairplot(data=df, hue="species")
plt.show()