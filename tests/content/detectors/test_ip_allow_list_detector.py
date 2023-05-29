
from classification.definitions.detector_action import DetectorAction
from classification.definitions.packet import ClassifiedPacket
from classification.memory.simple_shared_set import SimpleSharedSet
from content.detectors.ip_allow_list_detector import IPAllowListDetector


def test_continue_ip_allow_list_detector():
    detector = IPAllowListDetector(
        allowed_ips=SimpleSharedSet(data={"127.0.0.1"}),
    )
    packet = ClassifiedPacket.create_simple(
        src_addr="127.0.0.2",
        raw=b"",
    )
    result = detector.detect(packet)
    assert result.action == DetectorAction.Continue


def test_pass_ip_allow_list_detector():
    detector = IPAllowListDetector(
        allowed_ips=SimpleSharedSet(data={"127.0.0.3"}),
    )
    packet = ClassifiedPacket.create_simple(
        src_addr="127.0.0.3",
        raw=b"",
    )
    result = detector.detect(packet)
    assert result.action == DetectorAction.PassAll
