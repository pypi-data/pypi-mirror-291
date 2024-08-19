# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2024/7/23 21:53
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : ratio_statistic.py
# @Software: PyCharm
"""
from typing import List, Union, Any, Dict
import numpy as np
from collections import defaultdict
from ..metric import MetricOperator
from gaea_operator.utils import METRIC
from ..check import check_input_num_classes
from gaea_operator.utils import list2ndarray


@METRIC.register_module('ratio_statistic')
class RatioStatistic(MetricOperator):
    """
    Count statistics.
    """
    metric_name = 'ratio_statistic'

    def __init__(self, **kwargs):
        super(RatioStatistic, self).__init__(num_classes=kwargs.get('num_classes', 2))

        self.add_state("annotated_images", default=np.zeros(self.num_classes))
        self.add_state("images", default=np.zeros(self.num_classes))

    def update(self, annotated_images: Union[List[Dict], np.ndarray], images: Union[List[Dict], np.ndarray]) -> None:
        """
        Computes and returns the middle states, such as sum etc.
        """

        sum_annotated_images = np.sum(annotated_images, axis=0)
        sum_images = np.sum(images, axis=0)
        self.annotated_images += sum_annotated_images
        self.images += sum_images

    def compute(self) -> Any:
        """
        Computes the metric by middle states.
        """
        if self.images == 0:
            results = -1
        else:
            results = self.annotated_images / self.images
        return self.annotated_images.tolist(), self.images.tolist(), results.tolist()
