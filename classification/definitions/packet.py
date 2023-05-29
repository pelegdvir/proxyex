from dataclasses import dataclass
from uuid import UUID, uuid4

from classification.definitions.detectors_results import DetectorResult


@dataclass
class ClassifiedPacket:
    """Packet that we've classified/ currently to classifying
    Note: should add more fields such as headers, ports, ...
    """
    # internal random id
    internal_id: UUID
    # src ip addr
    src_addr: str
    # raw http content
    raw: bytes
    # all detector results - mutable
    detectors_results: dict[UUID, DetectorResult] | None = None

    @property
    def danger_grade(self) -> int:
        """How problematic the packet, based on current `detectors_results`
        Note: Consider moving this 'logic' outside the class if it will become more"""
        if not self.detectors_results:
            return 0
        return sum(
            result.danger_grade
            for result
            in self.detectors_results.values()
        )

    @classmethod
    def create_simple(
        cls,
        src_addr: str = '127.0.0.1',
        raw: bytes = b'',
    ) -> "ClassifiedPacket":
        """Test function"""
        return cls(
            internal_id=uuid4(),
            src_addr=src_addr,
            raw=raw,
        )
