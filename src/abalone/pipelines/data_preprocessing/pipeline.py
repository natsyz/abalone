"""
This is a boilerplate pipeline 'data_preprocessing'
generated using Kedro 0.18.3
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import drop_dataset, preprocessing

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=drop_dataset,
            inputs=["dataset", "params:columns"],
            outputs="dropped_dataset",
            name="drop_dataset_node"
        ),
        node(
            func=preprocessing,
            inputs="dropped_dataset",
            outputs="preprocessed_dataset",
            name="preprocessing_node"
        )
    ])
