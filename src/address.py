import src.config as cfg
from src.exceptions import PageNotExistsInROMError, PageNotExistsInRAMError, SegmentNotExistsInDescriptorTableError, InvalidMemoryAddressError

import csv

# segments descriptors table contains the following fields:
# 1. segment number
# 2. segment pages table path
# 3. pages count
segments_descriptors_table = []

# segment pages table contains the following fields:
# 1. page number
# 2. existence bit
# 3. frame number
segment_pages_table = []

def load_segments_table():
    with open(cfg.SEGMENTS_TABLE_FILE, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            segments_descriptors_table.append(row)
            
def load_pages_table(segment_number):
    try:
        with open(cfg.DATA_DIR + segments_descriptors_table[segment_number][1] + ".csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                segment_pages_table.append(row)
    except IndexError:
        raise SegmentNotExistsInDescriptorTableError(segment_number)

def form_phys_addr(virtual_addr: str) -> str:
    """
    Translates a virtual address to a physical address.

    The virtual address is a 32-bit value, divided into three parts:
    - The first 11 bits (0-10) represent the page offset.
    - The next 10 bits (11-20) represent the page number.
    - The final 11 bits (21-31) represent the segment number.

    The translation process is as follows:
    1. Retrieve the segment descriptor using the segment number.
    2. Retrieve the page table from the segment descriptor.
    3. Retrieve the frame number from the page table.
    4. Concatenate the frame number with the page offset to form the physical address.
    5. Return the physical address.

    Args:
        virtual_address (int): The virtual address to be translated.

    Returns:
        int: The translated physical address.
    """
    
    # check if the address is valid
    if len(virtual_addr) != 8:
        raise InvalidMemoryAddressError(virtual_addr)
    
    try:
        binary = f'{int(virtual_addr, 16):032b}'
    except ValueError:
        raise InvalidMemoryAddressError(virtual_addr)
    
    page_offset = int(binary[:11], 2)
    page_number = int(binary[11:21], 2)
    segment_number = int(binary[21:], 2)
    
    load_segments_table()
    
    load_pages_table(segment_number)
    
    # check if the page is loaded
    try:
        if segment_pages_table[page_number][1] == '0':
            raise PageNotExistsInRAMError(virtual_addr)
    except IndexError:
        raise PageNotExistsInROMError(virtual_addr)
    
    frame_number = int(segment_pages_table[page_number][2], 2)
    
    return f'{int(f"{frame_number:021b}{page_offset:011b}", 2):04X}'
