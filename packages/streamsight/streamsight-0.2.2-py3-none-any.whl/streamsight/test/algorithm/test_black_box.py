import pytest
from streamsight.datasets import TestDataset
from streamsight.settings import SlidingWindowSetting, SingleTimePointSetting
from streamsight.evaluators import EvaluatorBuilder

@pytest.fixture()
def sliding_window():
    dataset = TestDataset()
    data = dataset.load()
    setting = SlidingWindowSetting(
        4,
        3
    )
    setting.split(data)
    return setting

@pytest.fixture()
def single_time_point():
    dataset = TestDataset()
    data = dataset.load()
    setting = SingleTimePointSetting(
        4,
    )
    setting.split(data)
    return setting

# TODO test when there is repeated users in unlabeled data as seq data