import config

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
    with open(config.SEGMENTS_TABLE_FILE, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            segments_descriptors_table.append(row)
            
def load_pages_table(segment_number):
    with open(segments_descriptors_table[segment_number][1], "r") as f:
        reader = csv.reader(f)
        for row in reader:
            segment_pages_table.append(row)

# virtual address consists of 4 bytes, representing 32 bits
# 0-10 bits  - page offset     11 bits
# 11-20 bits - page number     10 bits
# 21-31 bits - segment number  11 bits
# to get the physical address we need to:
# 1. get the segment descriptor from the segment number
# 2. get the page table from the segment descriptor
# 3. get the frame number from the page table
# 4. concatenate the frame number with the page offset
# 5. return the physical address
def form_phys_addr(virtual_addr: str) -> str:
    page_offset = int(virtual_addr[:11], 2)
    page_number = int(virtual_addr[11:21], 2)
    segment_number = int(virtual_addr[21:], 2)
    
    load_segments_table()
    load_pages_table(segment_number)
    
    # check if the page exists
    if segment_pages_table[page_number][1] == '0':
        raise Exception(f'Page {page_number} does not exist in segment {segment_number}')
    
    frame_number = int(segment_pages_table[page_number][2], 2)
    
    return f'{frame_number:08b}{page_offset:011b}'