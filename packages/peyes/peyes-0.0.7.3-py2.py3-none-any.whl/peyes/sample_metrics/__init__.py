from typing import Union, Optional

from peyes._DataModels.EventLabelEnum import EventLabelSequenceType
from peyes._DataModels.UnparsedEventLabel import UnparsedEventLabelType, UnparsedEventLabelSequenceType

from peyes.sample_metrics._counts_and_matrices import label_counts, transition_matrix, confusion_matrix
from peyes.sample_metrics._calculate_metrics import calculate


def accuracy(ground_truth: EventLabelSequenceType, prediction: EventLabelSequenceType,) -> float:
    return calculate(ground_truth, prediction, "accuracy")


def balanced_accuracy(ground_truth: EventLabelSequenceType, prediction: EventLabelSequenceType,) -> float:
    return calculate(ground_truth, prediction, "balanced_accuracy")


def cohen_kappa(ground_truth: EventLabelSequenceType, prediction: EventLabelSequenceType,) -> float:
    return calculate(ground_truth, prediction, "cohen's_kappa")


def mcc(ground_truth: EventLabelSequenceType, prediction: EventLabelSequenceType,) -> float:
    return calculate(ground_truth, prediction, "mcc")


def complement_nld(ground_truth: EventLabelSequenceType, prediction: EventLabelSequenceType,) -> float:
    return calculate(ground_truth, prediction, "1_nld")


def precision(
        ground_truth: EventLabelSequenceType,
        prediction: EventLabelSequenceType,
        pos_labels: Optional[Union[UnparsedEventLabelType, UnparsedEventLabelSequenceType]],
        average: str = "weighted",
) -> float:
    return calculate(ground_truth, prediction, "precision", pos_labels=pos_labels, average=average)


def recall(
        ground_truth: EventLabelSequenceType,
        prediction: EventLabelSequenceType,
        pos_labels: Optional[Union[UnparsedEventLabelType, UnparsedEventLabelSequenceType]],
        average: str = "weighted",
) -> float:
    return calculate(ground_truth, prediction, "recall", pos_labels=pos_labels, average=average)


def f1_score(
        ground_truth: EventLabelSequenceType,
        prediction: EventLabelSequenceType,
        pos_labels: Optional[Union[UnparsedEventLabelType, UnparsedEventLabelSequenceType]],
        average: str = "weighted",
) -> float:
    return calculate(ground_truth, prediction, "f1", pos_labels=pos_labels, average=average)


def d_prime(
        ground_truth: EventLabelSequenceType,
        prediction: EventLabelSequenceType,
        pos_labels: Union[UnparsedEventLabelType, UnparsedEventLabelSequenceType],
        correction: str = "loglinear",
) -> float:
    return calculate(ground_truth, prediction, "d_prime", pos_labels=pos_labels, correction=correction)


def criterion(
        ground_truth: EventLabelSequenceType,
        prediction: EventLabelSequenceType,
        pos_labels: Union[UnparsedEventLabelType, UnparsedEventLabelSequenceType],
        correction: str = "loglinear",
) -> float:
    return calculate(ground_truth, prediction, "criterion", pos_labels=pos_labels, correction=correction)
