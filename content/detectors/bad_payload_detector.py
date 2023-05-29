from classification.definitions.detector_action import DetectorAction
from classification.definitions.detectors_results import DetectorInternalResult
from classification.definitions.packet import ClassifiedPacket
from classification.detectors.base_detector import BaseDetector
from classification.memory.simple_shared_set import SimpleSharedSet


class BadPayloadDenyDetector(BaseDetector):
    """Detector that finds if a specific payload is in the package"""

    def __init__(self, bad_payloads: SimpleSharedSet) -> None:
        super().__init__()
        self.bad_payloads = bad_payloads

    @property
    def name(self):
        return "bad_payload_detector"

    def _detect(self, packet: ClassifiedPacket) -> DetectorInternalResult:
        if not packet.raw:
            return DetectorInternalResult()
        something_bad = next(
            (
                bad_paylod
                for bad_paylod
                in self.bad_payloads.data
                if bad_paylod in packet.raw
            ),
            None,
        )
        if something_bad:
            return DetectorInternalResult(
                danger_grade=100,
                action=DetectorAction.Drop,
                description="Bad payload detected",
                long_description=f"The payload {something_bad} is blocked",
            )
        return DetectorInternalResult()
