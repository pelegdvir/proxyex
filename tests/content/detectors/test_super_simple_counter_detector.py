
from time import sleep

from classification.definitions.detector_action import DetectorAction
from classification.definitions.packet import ClassifiedPacket
from content.detectors.super_simple_counter_detector import \
    SuperSimpleCounterDetector


def test_continue_not_a_number_super_simple_counter_detector():
    detector = SuperSimpleCounterDetector(
        ttl=1,
        threshold=3,
        numbers_to_check=10,
    )
    packet1 = ClassifiedPacket.create_simple(
        src_addr="127.0.0.2",
        raw=b"nothing",
    )
    result = detector.detect(packet1)
    assert result.action == DetectorAction.Continue


def test_drop_after_threshold_super_simple_counter_detector():
    detector = SuperSimpleCounterDetector(
        ttl=1,
        threshold=3,
        numbers_to_check=10,
    )
    packet1 = ClassifiedPacket.create_simple(
        src_addr="127.0.0.2",
        raw=b"1",
    )
    packet2 = ClassifiedPacket.create_simple(
        src_addr="127.0.0.2",
        raw=b"2",
    )
    packet3 = ClassifiedPacket.create_simple(
        src_addr="127.0.0.2",
        raw=b"3",
    )
    result = detector.detect(packet1)
    assert result.action == DetectorAction.Continue
    result = detector.detect(packet2)
    assert result.action == DetectorAction.Continue
    result = detector.detect(packet3)
    assert result.action == DetectorAction.Drop


def test_continue_because_of_ttl_super_simple_counter_detector():
    detector = SuperSimpleCounterDetector(
        ttl=1,
        threshold=3,
        numbers_to_check=10,
    )
    packet1 = ClassifiedPacket.create_simple(
        src_addr="127.0.0.2",
        raw=b"1",
    )
    packet2 = ClassifiedPacket.create_simple(
        src_addr="127.0.0.2",
        raw=b"2",
    )
    packet3 = ClassifiedPacket.create_simple(
        src_addr="127.0.0.2",
        raw=b"3",
    )
    result = detector.detect(packet1)
    assert result.action == DetectorAction.Continue
    result = detector.detect(packet2)
    assert result.action == DetectorAction.Continue
    sleep(1)
    result = detector.detect(packet3)
    assert result.action == DetectorAction.Continue


def test_continue_for_same_call_threshold_super_simple_counter_detector():
    detector = SuperSimpleCounterDetector(
        ttl=1,
        threshold=3,
        numbers_to_check=10,
    )
    packet1 = ClassifiedPacket.create_simple(
        src_addr="127.0.0.2",
        raw=b"1",
    )
    packet2 = ClassifiedPacket.create_simple(
        src_addr="127.0.0.2",
        raw=b"1",
    )
    packet3 = ClassifiedPacket.create_simple(
        src_addr="127.0.0.2",
        raw=b"1",
    )
    result = detector.detect(packet1)
    assert result.action == DetectorAction.Continue
    result = detector.detect(packet2)
    assert result.action == DetectorAction.Continue
    result = detector.detect(packet3)
    assert result.action == DetectorAction.Continue
