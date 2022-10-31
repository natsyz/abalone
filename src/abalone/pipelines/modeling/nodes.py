"""
This is a boilerplate pipeline 'modeling'
generated using Kedro 0.18.3
"""
import matplotlib.pyplot as plt
import pandas as pd
from kedro.extras.datasets.matplotlib import MatplotlibWriter
from typing import Any, Tuple
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.tree import plot_tree

def preparation(dataset: pd.DataFrame, label: str) -> Tuple:
    """Membagi dataset menjadi training set dan test set.

    Keyword arguments:
    dataset -- Dataset yang akan ditransformasi
    label -- Nama kolom yang merupakan label dari data
    """
    # Label pada dataset (Untuk diprediksi pada saat klasifikasi)
    label_df = dataset[label].to_frame()
    # Menghapus label dan menyisakan hanya fitur pada dataset
    data = dataset.drop(columns=[label], axis=1)
    
    # Membagi dataset menjadi training set dan test set
    # dengan jumlah training set adalah sebanyak 80% dari data keseluruhan 
    data_train, data_test, label_train, label_test = train_test_split(
        data, label_df, train_size=0.8, random_state=42)

    return data_train, data_test, label_train, label_test

def modeling(
    data_train: pd.DataFrame,
    data_test: pd.DataFrame,
    label_train: pd.DataFrame,
    label_test: pd.DataFrame,
    max_depth: int
    ) -> str:
    """Modeling dengan model decision tree, kemudian melakukan
    evaluasi dan visualisasi dari decision tree yang dibuat.

    Keyword arguments:
    data_train  - Dataset berisi data train model
    data_test   - Dataset berisi data test model
    label_train - Dataset berisi label train model
    label_test  - Dataset berisi label test model
    max_depth   - Angka kedalaman decision tree
    """
    # Melakukan modeling dengan model decision tree
    model = _training(data_train, label_train, max_depth)
    # Memprediksi data testing
    predicted = model.predict(data_test) 
    # Menghitung metrics evaluasi berupa nilai akurasi, presisi, recall, dan F1-Score
    metrics_eval = _evaluation(label_test, predicted)
    # Menyimpan figure decission tree
    _save_figure(data_train, label_train, model)

    return metrics_eval


def _training(data_train: pd.DataFrame, label_train: pd.DataFrame, max_depth: int) -> Any:
    """Melakukan training model decision tree."""
    model = DecisionTreeClassifier(max_depth=max_depth)
    model.fit(data_train, label_train)

    return model

def _evaluation(label_test: pd.DataFrame, predicted: any) -> str:
    """Menghitung metrics evaluasi berupa nilai akurasi, presisi, recall, dan F1-Score."""
    akurasi = "Akurasi: " + str(accuracy_score(label_test, predicted)) +"\n"
    presisi = "Presisi:" + str(precision_score(label_test, predicted)) +"\n"
    recall = "Recall: "+ str(recall_score(label_test, predicted)) +"\n"
    f1 = "F1-score: " + str(f1_score(label_test, predicted))

    return akurasi + presisi + recall + f1

def _save_figure(data_train: pd.DataFrame, label_train: pd.DataFrame, model: any) -> None:
    """Melakukan visualisasi pada model decision tree yang sudah dibangun sebelumnya,
    kemudian menyimpan figure decission tree ke lokal."""
    features = list(data_train.columns)
    labels = [str(label) for label in list(label_train['Class'].unique())]

    # Menyimpan figure decission tree
    fig = plt.figure(figsize=(25,20))
    plot_tree(model, feature_names=features, class_names=labels, filled=True)
    single_plot_writer = MatplotlibWriter(
      filepath="data/08_reporting/decession_tree_plot.png"
    )
    plt.close()
    single_plot_writer.save(fig)