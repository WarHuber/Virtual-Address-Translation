class CustomError(Exception):
    """Base class for other exceptions"""
    pass

# MEMORY ERRORS

class PageNotExistsInRAMError(CustomError):
    """Raised when the page does not exist in RAM"""
    def __init__(self, virtual_address: str , message="Page does not exist in RAM"):
        self.message = message + f" for address {virtual_address}"
        super().__init__(self.message)

class PageNotExistsInROMError(CustomError):
    """Raised when the page does not exist in memory"""
    def __init__(self, page_number: int, message="Page does not exist in memory"):
        self.message = message + f" for page number {page_number}"
        super().__init__(self.message)

class SegmentNotExistsInDescriptorTableError(CustomError):
    """Raised when the segment does not exist in the descriptor table"""
    def __init__(self, segment_number: int, message="Segment does not exist in the descriptor table"):
        self.message = message + f" for segment number {segment_number}"
        super().__init__(self.message)

class InvalidMemoryAddressError(CustomError):
    """Raised when the memory address is invalid"""
    def __init__(self, virtual_address: str, message="Invalid memory address"):
        self.message = message + f" for address {virtual_address}"
        super().__init__(self.message)