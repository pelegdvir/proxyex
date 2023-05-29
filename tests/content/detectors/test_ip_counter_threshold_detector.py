
from time import sleep

from classification.definitions.detector_action import DetectorAction
from classification.definitions.packet import ClassifiedPacket
from content.detectors.ip_counter_threshold_detector import \
    IPCounterThresholdDetector


def test_drop_after_threshold_ip_counter_threshold_detector():
    detector = IPCounterThresholdDetector(
        ttl=1,
        threshold=3,
        weight=2,
    )
    packet1 = ClassifiedPacket.create_simple(
        src_addr="127.0.0.2",
    )
    packet2 = ClassifiedPacket.create_simple(
        src_addr="127.0.0.2",
    )
    packet3 = ClassifiedPacket.create_simple(
        src_addr="127.0.0.2",
    )
    result = detector.detect(packet1)
    assert result.action == DetectorAction.Continue
    result = detector.detect(packet2)
    assert result.action == DetectorAction.Continue
    result = detector.detect(packet3)
    assert result.action == DetectorAction.Warn
    assert result.danger_grade == 3 * 2


def test_continue_because_of_ttl_ip_counter_threshold_detector():
    detector = IPCounterThresholdDetector(
        ttl=1,
        threshold=3,
        weight=2,
    )
    packet1 = ClassifiedPacket.create_simple(
        src_addr="127.0.0.2",
    )
    packet2 = ClassifiedPacket.create_simple(
        src_addr="127.0.0.2",
    )
    packet3 = ClassifiedPacket.create_simple(
        src_addr="127.0.0.2",
    )
    result = detector.detect(packet1)
    assert result.action == DetectorAction.Continue
    result = detector.detect(packet2)
    assert result.action == DetectorAction.Continue
    sleep(1)
    result = detector.detect(packet3)
    assert result.action == DetectorAction.Continue


def test_continue_for_different_ips_ip_counter_threshold_detector():
    detector = IPCounterThresholdDetector(
        ttl=1,
        threshold=3,
        weight=2,
    )
    packet1 = ClassifiedPacket.create_simple(
        src_addr="127.0.0.2",
    )
    packet2 = ClassifiedPacket.create_simple(
        src_addr="127.0.0.2",
    )
    packet3 = ClassifiedPacket.create_simple(
        src_addr="127.0.0.1",
    )
    result = detector.detect(packet1)
    assert result.action == DetectorAction.Continue
    result = detector.detect(packet2)
    assert result.action == DetectorAction.Continue
    result = detector.detect(packet3)
    assert result.action == DetectorAction.Continue
