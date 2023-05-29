from classification.definitions.detector_action import DetectorAction
from classification.definitions.detectors_results import DetectorInternalResult
from classification.definitions.packet import ClassifiedPacket
from classification.detectors.base_detector import BaseDetector
from classification.memory.simple_shared_set import SimpleSharedSet


class IPDenyListDetector(BaseDetector):
    """Classic IP deny list detector"""

    def __init__(self, blocked_ips: SimpleSharedSet) -> None:
        super().__init__()
        self.blocked_ips = blocked_ips

    @property
    def name(self):
        return "ip_deny_list_detector"

    def _detect(self, packet: ClassifiedPacket) -> DetectorInternalResult:
        if packet.src_addr in self.blocked_ips.data:
            return DetectorInternalResult(
                danger_grade=100,
                action=DetectorAction.Drop,
                description="Denied IP address",
                long_description=f"The addr {packet.src_addr} is blocked",
            )
        return DetectorInternalResult()
