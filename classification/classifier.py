import logging
from uuid import uuid4

from classification.definitions.detector_action import DetectorAction
from classification.definitions.detectors_results import DetectorResult
from classification.definitions.packet import ClassifiedPacket
from classification.reporter import Reporter
from classification.suites.base_suite import BaseSuite


class Classifier:
    """The component that passes a packet in a suite
    Responsible to decide what to do, call the reporter.
    """
    def __init__(self, suite: BaseSuite):
        self.suite = suite
        self.reporter = Reporter()

    def decide_if_pass(self, src_addr: str, raw: bytes) -> bool:
        classified_packet = ClassifiedPacket(
            internal_id=uuid4(),
            src_addr=src_addr,
            raw=raw,
            detectors_results=dict(),
        )
        return self._handle_classified_packet(classified_packet)

    def _handle_classified_packet(self, classified_packet: ClassifiedPacket) -> bool:
        detectors_for_packet = self.suite.initial_detectors[:]
        should_pass_packet = True

        # Future optimization: can make this section async
        # after changing detector.detect to async
        for detector in detectors_for_packet:
            detector_result = detector.detect(classified_packet)
            classified_packet.detectors_results[detector.identifier] = detector_result
            bool_action = self._handle_detector_result(classified_packet, detector_result)
            if bool_action is not None:
                should_pass_packet = bool_action
                break

        self.reporter.report(should_pass_packet, classified_packet)
        return should_pass_packet

    def _handle_detector_result(
        self,
        classified_packet: ClassifiedPacket,
        detector_result: DetectorResult,
    ) -> bool | None:
        if detector_result.action == DetectorAction.Drop:
            logging.debug(f"{classified_packet.internal_id}: drop packet")
            return False
        if detector_result.action == DetectorAction.PassAll:
            logging.debug(f"{classified_packet.internal_id}: packet super safe")
            return True
        if detector_result.action == DetectorAction.Warn:
            self._handle_warn(classified_packet, detector_result)
        elif detector_result.action != DetectorAction.Continue:
            raise NotImplementedError("New state!")

        if classified_packet.danger_grade > self.suite.danger_grade_threshold:
            logging.debug(f"{classified_packet.internal_id}: too dangerous packet!")
            return False
        return None

    def _handle_warn(self, classified_packet: ClassifiedPacket, detector_result: DetectorResult):
        logging.debug(f"{classified_packet.internal_id}: not so sure about packet")
        logging.warning(f"{classified_packet.internal_id}: Warning about: '{detector_result.longest_description}'")  # noqa: E501
