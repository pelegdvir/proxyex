from classification.definitions.detector_action import DetectorAction
from classification.definitions.detectors_results import DetectorInternalResult
from classification.definitions.packet import ClassifiedPacket
from classification.detectors.base_detector import BaseDetector
from classification.memory.simple_shared_set import SimpleSharedSet


class IPAllowListDetector(BaseDetector):
    """Detector to avoid all other checks"""

    def __init__(self, allowed_ips: SimpleSharedSet) -> None:
        super().__init__()
        self.allowed_ips = allowed_ips

    @property
    def name(self):
        return "ip_allow_list_detector"

    def _detect(self, packet: ClassifiedPacket) -> DetectorInternalResult:
        if packet.src_addr in self.allowed_ips.data:
            return DetectorInternalResult(
                danger_grade=0,
                action=DetectorAction.PassAll,
                description="Allow IP address",
                long_description=f"The addr {packet.src_addr} is allowed",
            )
        return DetectorInternalResult()
