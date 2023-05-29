class SimpleSharedSet:
    """Very simple set - for const data (IP allow list)"""
    def __init__(self, data: set) -> None:
        self.data = data
