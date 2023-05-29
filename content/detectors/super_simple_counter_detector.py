from classification.definitions.detector_action import DetectorAction
from classification.definitions.detectors_results import DetectorInternalResult
from classification.definitions.packet import ClassifiedPacket
from classification.detectors.base_detector import BaseDetector
from classification.memory.simple_shared_timed_dictionary import \
    SimpleSharedTimedDictionary


class SuperSimpleCounterDetector(BaseDetector):
    """Finds if the packet data is just a raw counter (support also for increase by 2 counters)"""

    def __init__(
        self,
        maxsize: int | None = None,
        ttl: int = 1,
        threshold: int = 10,
        numbers_to_check: int = 20,
    ):
        super().__init__()
        self.counter = SimpleSharedTimedDictionary(maxsize, ttl)
        self.threshold = threshold
        self.numbers_to_check = numbers_to_check

    @property
    def name(self):
        return "super_simple_counter_detector"

    def _detect(self, packet: ClassifiedPacket) -> DetectorInternalResult:
        try:
            number = int(packet.raw)
        except ValueError:
            return DetectorInternalResult()
        self.counter.data[number] = True
        found_similar = sum(
            number - i in self.counter.data
            for i
            in range(self.numbers_to_check)
        )
        if found_similar >= self.threshold:
            return DetectorInternalResult(
                danger_grade=100,
                action=DetectorAction.Drop,
                description="Seems like a counter",
                long_description=f"Counter of {found_similar} in packet",
            )
        return DetectorInternalResult()
