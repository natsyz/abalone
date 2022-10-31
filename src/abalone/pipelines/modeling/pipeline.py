"""
This is a boilerplate pipeline 'modeling'
generated using Kedro 0.18.3
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import preparation, modeling


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=preparation,
            inputs=["preprocessed_dataset", "params:label"],
            outputs=["data_train", "data_test", "label_train", "label_test"],
            name="preparation_node"
        ),
        node(
            func=modeling,
            inputs=["data_train", "data_test", "label_train", "label_test", "params:max_depth"],
            outputs="metrics_eval",
            name="modeling_node"
        )
    ])
