# -*- coding: utf-8 -*-
"""
Copyright(C) 2023 baidu, Inc. All Rights Reserved

# @Time : 2024/7/25 15:15
# @Author : yangtingyu01
# @Email: yangtingyu01@baidu.com
# @File : precision_recall_accuracy.py
# @Software: PyCharm
"""
from typing import List, Union, Optional, Sequence, Tuple, Any
import numpy as np

from gaea_operator.utils import paddle, torch, Tensor, PTensor, TTensor
from gaea_operator.utils import METRIC
from ..metric import MetricOperator
from ..check import check_input_dim, check_input_type


@METRIC.register_module('precision_recall_accuracy')
class PrecisionRecallAccuracy(MetricOperator):
    """
    PrecisionRecallAccuracy is a operator transform character to confusion matrix.
    """
    metric_name = 'precision_recall_accuracy'

    def __init__(self,
                 labels: Optional[List],
                 **kwargs):
        super(PrecisionRecallAccuracy, self).__init__(num_classes=kwargs.get('num_classes', 2))
        self.labels = labels
        self.add_state("tp_sum", default=0)
        self.add_state("pred_sum", default=0)
        self.add_state("gt_sum", default=0)

    def update(self, predictions: Union[List, Tensor], references: Union[List, Tensor]) -> None:
        """
        Accumulates the references and predictions.
        """
        check_input_type(predictions=predictions, references=references)
        for ref, pred in zip(references, predictions):
            # 增加 ground truth 计数
            self.gt_sum += 1

            # 判断是否是负样本（没有任何标注）
            is_negative_sample = ref == ""  # 假设 ref 为空字符串或 None 代表负样本

            # 判断是否没有预测值
            is_empty_prediction = pred == ""  # 假设 pred 为空字符串或 None 代表没有预测值

            # 增加 prediction 计数
            if not is_empty_prediction:
                self.pred_sum += 1

            # 增加 true positive 计数
            if ref == pred and not is_negative_sample:
                self.tp_sum += 1

    def compute(self) -> Any:
        """
        Computes Precision, Recall, and Accuracy.
        """
        precision = self.tp_sum / self.pred_sum if self.pred_sum != 0 else -1.0
        # 计算 Recall
        recall = self.tp_sum / self.gt_sum if self.gt_sum != 0 else -1.0
        # 计算 Accuracy
        accuracy = self.tp_sum / (self.pred_sum + self.gt_sum - self.tp_sum) \
            if (self.pred_sum + self.gt_sum - self.tp_sum) != 0 else -1.0

        return precision, recall, accuracy
