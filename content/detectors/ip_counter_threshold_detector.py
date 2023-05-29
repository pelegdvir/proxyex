from classification.definitions.detector_action import DetectorAction
from classification.definitions.detectors_results import DetectorInternalResult
from classification.definitions.packet import ClassifiedPacket
from classification.detectors.base_detector import BaseDetector
from classification.memory.simple_shared_timed_dictionary import \
    SimpleSharedTimedDictionary


class IPCounterThresholdDetector(BaseDetector):
    """Protect against DOS from the same IP"""

    def __init__(
        self,
        maxsize: int | None = None,
        ttl: int = 1,
        threshold: int = 10,
        weight: int = 1,
    ) -> None:
        super().__init__()
        self.ips_counter = SimpleSharedTimedDictionary(maxsize, ttl)
        self.threshold = threshold
        self.weight = weight

    @property
    def name(self):
        return "ip_counter_threshold_detector"

    def _detect(self, packet: ClassifiedPacket) -> DetectorInternalResult:
        counter = int(self.ips_counter.data.get(packet.src_addr, 0)) + 1
        self.ips_counter.data[packet.src_addr] = counter
        if counter >= self.threshold:
            return DetectorInternalResult(
                danger_grade=counter * self.weight,
                action=DetectorAction.Warn,
                description="Count Many IP calls in short period",
                long_description=f"The addr {packet.src_addr} called many {counter} times",
            )
        return DetectorInternalResult()
