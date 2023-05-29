from classification.definitions.packet import ClassifiedPacket


class Reporter:
    """Very simple logger. Currently logs only dropped packets"""
    def report(
        self,
        action: bool,
        classified_packet: ClassifiedPacket,
    ):
        if not self._should_store_log(action, classified_packet):
            return
        log = self._create_log(action, classified_packet)
        self._store_log(log)

    def _store_log(self, log: str):
        # Replace with storage to db/...
        # notice its now python logging lib
        print(log)

    def _should_store_log(
        self,
        action: bool,
        classified_packet: ClassifiedPacket,
    ) -> bool:
        return action is False or classified_packet.danger_grade > 0

    def _create_log(
        self,
        action: bool,
        classified_packet: ClassifiedPacket,
    ) -> str:
        log = "Dropped packet" if not action else "Check this packet"
        log += f"\ngrade: {str(classified_packet.danger_grade)}"
        log += f"\ndata: {str(classified_packet.raw)}"
        if classified_packet.detectors_results:
            for detector_result in classified_packet.detectors_results.values():
                log += f"\n {detector_result.detector_name}: {detector_result.longest_description}"
        return log
