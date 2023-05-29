import logging
from uuid import UUID, uuid4

from classification.definitions.detectors_results import (
    DetectorInternalResult, DetectorResult)
from classification.definitions.packet import ClassifiedPacket


class BaseDetector:
    """Base structure for a detector.
    Most of the time we want to implement only 2 functions"""

    @property
    def name(self) -> str:
        raise NotImplementedError()

    def _detect(self, packet: ClassifiedPacket) -> DetectorInternalResult:
        raise NotImplementedError()

    def __init__(self):
        self._identifier = uuid4()

    @property
    def identifier(self) -> UUID:
        return self._identifier

    def detect(self, packet: ClassifiedPacket) -> DetectorResult:
        logging.debug(f"{packet.internal_id}: running detector {self.name}")
        result = self._detect(packet)
        return DetectorResult(
            detector_id=self.identifier,
            detector_name=self.name,
            danger_grade=result.danger_grade,
            action=result.action,
            description=result.description or "All good",
            long_description=result.long_description,
        )
