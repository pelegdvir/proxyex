
from classification.definitions.detector_action import DetectorAction
from classification.definitions.packet import ClassifiedPacket
from classification.memory.simple_shared_set import SimpleSharedSet
from content.detectors.bad_payload_detector import BadPayloadDenyDetector


def test_continue_bad_payload_detector():
    detector = BadPayloadDenyDetector(
        bad_payloads=SimpleSharedSet(data={b"of", b"doom"}),
    )
    packet = ClassifiedPacket.create_simple(
        src_addr="127.0.0.1",
        raw=b"good vibes",
    )
    result = detector.detect(packet)
    assert result.action == DetectorAction.Continue


def test_drop_bad_payload_detector():
    detector = BadPayloadDenyDetector(
        bad_payloads=SimpleSharedSet(data={b"of", b"doom"}),
    )
    packet = ClassifiedPacket.create_simple(
        src_addr="127.0.0.1",
        raw=b"doom upon us",
    )
    result = detector.detect(packet)
    assert result.action == DetectorAction.Drop
