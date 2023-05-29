
from classification.definitions.detector_action import DetectorAction
from classification.definitions.packet import ClassifiedPacket
from classification.memory.simple_shared_set import SimpleSharedSet
from content.detectors.ip_deny_list_detector import IPDenyListDetector


def test_continue_ip_deny_list_detector():
    detector = IPDenyListDetector(
        blocked_ips=SimpleSharedSet(data={"127.0.0.1"}),
    )
    packet = ClassifiedPacket.create_simple(
        src_addr="127.0.0.2",
        raw=b"",
    )
    result = detector.detect(packet)
    assert result.action == DetectorAction.Continue


def test_drop_ip_deny_list_detector():
    detector = IPDenyListDetector(
        blocked_ips=SimpleSharedSet(data={"127.0.0.1"}),
    )
    packet = ClassifiedPacket.create_simple(
        src_addr="127.0.0.1",
        raw=b"",
    )
    result = detector.detect(packet)
    assert result.action == DetectorAction.Drop
