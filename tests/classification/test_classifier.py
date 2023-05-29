
from classification.classifier import Classifier
from content.suites.mock_suite import MockSuite


def test_continue_if_all_normal():
    classifier = Classifier(suite=MockSuite())
    result = classifier.decide_if_pass(
        src_addr="127.0.0.10",
        raw=b"safe",
    )
    assert result is True


def test_drop_bad_payload():
    classifier = Classifier(suite=MockSuite())
    result = classifier.decide_if_pass(
        src_addr="127.0.0.10",
        raw=b"worse",
    )
    assert result is False


def test_continue_bad_payload_with_allowed_ip():
    classifier = Classifier(suite=MockSuite())
    result = classifier.decide_if_pass(
        src_addr="127.0.0.3",
        raw=b"worse",
    )
    assert result is True


def test_drop_good_payload_with_denied_ip():
    classifier = Classifier(suite=MockSuite())
    result = classifier.decide_if_pass(
        src_addr="127.0.0.2",
        raw=b"safe",
    )
    assert result is False


def test_drop_after_flood():
    classifier = Classifier(suite=MockSuite())
    # Note: 20 = 100 / (2 + 3)
    # Note: safe packet = total grade /
    # (IPCounterThresholdDetector1.weight + IPCounterThresholdDetector2.weight)
    for _ in range(20):
        result = classifier.decide_if_pass(
            src_addr="127.0.0.10",
            raw=b"safe",
        )
        assert result is True
    result = classifier.decide_if_pass(
        src_addr="127.0.0.10",
        raw=b"safe",
    )
    assert result is False
