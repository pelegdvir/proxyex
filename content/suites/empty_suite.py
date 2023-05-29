from classification.detectors.base_detector import BaseDetector
from classification.suites.base_suite import BaseSuite


class EmptySuite(BaseSuite):
    """Example a suite that passes everything."""

    @property
    def initial_detectors(self) -> list[BaseDetector]:
        return []
