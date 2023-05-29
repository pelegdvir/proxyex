from classification.detectors.base_detector import BaseDetector


class BaseSuite:
    """Base suite, most of the time we would like to implement only initial_detectors"""

    @property
    def danger_grade_threshold(self) -> int:
        return 100

    @property
    def initial_detectors(self) -> list[BaseDetector]:
        raise NotImplementedError()
