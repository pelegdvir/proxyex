

from dataclasses import dataclass
from uuid import UUID

from classification.definitions.detector_action import DetectorAction


@dataclass
class DetectorInternalResult:
    """Same as `DetectorResult`, but with less fields. For content writers"""
    danger_grade: int = 0
    action: DetectorAction = DetectorAction.Continue
    description: str | None = None
    long_description: str | None = None


@dataclass
class DetectorResult:
    """The result of a detector"""
    # Random id, useful for logs, also great for future references
    detector_id: UUID
    # Detector name, useful for logs
    detector_name: str
    # The actual result, read more in `DetectorAction`
    action: DetectorAction = DetectorAction.Continue
    # How bad the packet is (most of the time 0-100 is the scale)
    danger_grade: int = 0
    # Short description, for logs / UI
    description: str | None = None
    # Long description, for logs / UI
    long_description: str | None = None
    # Future: support calling other sub detectors based on this result
    # call_detectors: list[UUID] | None = None

    @property
    def longest_description(self) -> str:
        if self.long_description:
            return self.long_description
        if self.description:
            return self.description
        return "No description"
