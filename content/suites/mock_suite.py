from classification.detectors.base_detector import BaseDetector
from classification.memory.simple_shared_set import SimpleSharedSet
from classification.suites.base_suite import BaseSuite
from content.detectors.bad_payload_detector import BadPayloadDenyDetector
from content.detectors.ip_allow_list_detector import IPAllowListDetector
from content.detectors.ip_counter_threshold_detector import \
    IPCounterThresholdDetector
from content.detectors.ip_deny_list_detector import IPDenyListDetector
from content.detectors.super_simple_counter_detector import \
    SuperSimpleCounterDetector


class MockSuite(BaseSuite):
    """Example for all detectors, notice that order matters!
    If we will run IPAllowListDetector first, we will skip other tests"""
    def __init__(self) -> None:
        # Memory that can get shared between detectors
        self.allowed_ips = SimpleSharedSet(data={
            "127.0.0.3",
        })
        self.blocked_ips = SimpleSharedSet(data={
            "127.0.0.2",
        })
        self.bad_payloads = SimpleSharedSet(data={
            b"bad",
            b"worse",
        })
        self._detectors: list[BaseDetector] = [
            IPDenyListDetector(
                blocked_ips=self.blocked_ips,
            ),
            IPAllowListDetector(
                allowed_ips=self.allowed_ips,
            ),
            BadPayloadDenyDetector(
                bad_payloads=self.bad_payloads,
            ),
            IPCounterThresholdDetector(
                ttl=1,
                threshold=10,
                weight=2,
            ),
            # Can the same detector multiple times
            IPCounterThresholdDetector(
                ttl=3,
                threshold=10,
                weight=3,
            ),
            SuperSimpleCounterDetector(
                ttl=100,
                threshold=5,
                numbers_to_check=20,
            )
        ]

    @property
    def initial_detectors(self) -> list[BaseDetector]:
        return self._detectors
