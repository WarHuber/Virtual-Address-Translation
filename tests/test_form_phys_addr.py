import pytest
from src.address import form_phys_addr, segments_descriptors_table, segment_pages_table
from src.exceptions import InvalidMemoryAddressError, PageNotExistsInRAMError, SegmentNotExistsInDescriptorTableError, PageNotExistsInROMError

# Example segment and pages tables
@pytest.fixture(autouse=True)
def setup_environment(monkeypatch):
    # Setup segment descriptor table
    segments_descriptors_table.clear()
    segments_descriptors_table.extend([
        ['0', 'segment_0', '2'],  # segment_number, csv_file, pages_count
        ['1', 'segment_1', '3'],
        ['2', 'segment_2', '1']   # Added another segment for additional test cases
    ])

    # Mock segment_pages_table based on segment number provided
    def mock_load_pages_table(segment_number):
        segment_pages_table.clear()
        if segment_number == 0:
            segment_pages_table.extend([
                ['0', '1', '000000000000000000001'],
                ['1', '1', '000000000000000000010'],
                ['2', '0', '000000000000000000011'],
                ['3', '1', '000000000000000000100'],
                ['4', '0', '000000000000000000101']
            ])
        elif segment_number == 1:
            segment_pages_table.extend([
                ['0', '1', '000000000000000000011'],  # This page is in RAM
                ['1', '0', '000000000000000000100'],  # This page is not in RAM
                ['2', '1', '000000000000000000101']  # Page is in RAM
            ])
        elif segment_number == 2:
            segment_pages_table.extend([
                ['0', '1', '000000000000000000110']  # Single page, in RAM
            ])
        else:
            raise SegmentNotExistsInDescriptorTableError(segment_number)

    # Replace the actual load_pages_table function with the mock
    monkeypatch.setattr('src.address.load_pages_table', mock_load_pages_table)
    
# Test cases
def test_valid_conversion():
    expected_frame = '000000000000000000001'  # 21 bits
    expected_page_offset = '00000000000'      # 11 bits
    expected_physical_address = f'{int(expected_frame + expected_page_offset, 2):04X}'  # Hexadecimal format
    assert form_phys_addr('00000000') == expected_physical_address

def test_short_address_error():
    with pytest.raises(InvalidMemoryAddressError):
        form_phys_addr('0000000')  # 7 hex digits, not enough for 32 bits

def test_long_address_error():
    with pytest.raises(InvalidMemoryAddressError):
        form_phys_addr('000000000')  # 9 hex digits, too many for 32 bits

def test_non_hexadecimal_address():
    with pytest.raises(InvalidMemoryAddressError):
        form_phys_addr('ZZZZZZZZ')

def test_boundary_segment_number_low():
    # Assuming segment 0 is at the lowest permissible segment number that is valid
    expected_frame = '000000000000000000001'  # 21 bits
    expected_page_offset = '00000000000'      # 11 bits
    expected_physical_address = f'{int(expected_frame + expected_page_offset, 2):04X}'  # Hexadecimal format
    assert form_phys_addr('00000000') == expected_physical_address
    
def test_boundary_segment_number_high():
    # Testing the highest valid segment number
    with pytest.raises(SegmentNotExistsInDescriptorTableError):
        form_phys_addr('FFFFFF00')  # Last 11 bits as '1's will be beyond the segment range set up

def test_page_not_in_ram():
    # Tests handling of a page not loaded into RAM
    with pytest.raises(PageNotExistsInRAMError):
        form_phys_addr('00802000')  # Page number 2 in segment 1, which is not in RAM

def test_invalid_page_number():
    # Tests accessing a page number that does not exist in the segment's page table
    with pytest.raises(PageNotExistsInROMError):
        form_phys_addr('001FF000')  # Page number 511 in segment 1, which only has 3 pages

def test_maximum_page_offset():
    # Testing the highest permissible page offset which is all bits as '1's in the offset region
    expected_frame = '000000000000000000011'  # 21 bits
    expected_page_offset = '11111111111'      # 11 bits (2047)
    page_offset = f'{int(expected_page_offset, 2):011b}'
    page_number = f'{0:010b}'
    segment_number = f'{1:011b}'
    virtual_address = page_offset + page_number + segment_number
    virtual_address_hex = f'{int(virtual_address, 2):08X}'
    expected_physical_address = f'{int(expected_frame + expected_page_offset, 2):04X}'
    assert form_phys_addr(virtual_address_hex) == expected_physical_address  # High offset in page 0, segment 1

def test_minimum_page_offset():
    # Testing the lowest permissible page offset which is all bits as '0's
    expected_frame = '000000000000000000011'  # 21 bits
    expected_page_offset = '00000000000'      # 11 bits (0)
    page_offset = f'{int(expected_page_offset, 2):011b}'
    page_number = f'{0:010b}'
    segment_number = f'{1:011b}'
    virtual_address = page_offset + page_number + segment_number
    virtual_address_hex = f'{int(virtual_address, 2):08X}'
    expected_physical_address = f'{int(expected_frame + expected_page_offset, 2):04X}'
    assert form_phys_addr(virtual_address_hex) == expected_physical_address  # Low offset in page 0, segment 1

def test_segment_switching():
    # Ensure the correct segment is being accessed when switching segments
    expected_frame = '000000000000000000101'  # 21 bits from segment 1, page 2
    expected_page_offset = '00000000000'      # 11 bits
    page_offset = f'{int(expected_page_offset, 2):011b}'
    page_number = f'{2:010b}'
    segment_number = f'{1:011b}'
    virtual_address = page_offset + page_number + segment_number
    virtual_address_hex = f'{int(virtual_address, 2):08X}'
    expected_physical_address = f'{int(expected_frame + expected_page_offset, 2):04X}'
    assert form_phys_addr(virtual_address_hex) == expected_physical_address  # Page 2, segment 1

def test_invalid_segment_number_high():
    # Invalid segment number beyond the highest defined
    with pytest.raises(SegmentNotExistsInDescriptorTableError):
        page_offset = f'{0:011b}'
        page_number = f'{0:010b}'
        segment_number = f'{3:011b}'
        virtual_address = page_offset + page_number + segment_number
        virtual_address_hex = f'{int(virtual_address, 2):08X}'
        form_phys_addr(virtual_address_hex)

def test_full_address_range():
    # Test conversion for full address range (segment, page number, and offset)
    expected_frame = '000000000000000000101'  # 21 bits from segment 1, page 2
    expected_page_offset = '11111111111'      # 11 bits (2047)
    page_offset = f'{int(expected_page_offset, 2):011b}'
    page_number = f'{2:010b}'
    segment_number = f'{1:011b}'
    virtual_address = page_offset + page_number + segment_number
    virtual_address_hex = f'{int(virtual_address, 2):08X}'
    expected_physical_address = f'{int(expected_frame + expected_page_offset, 2):04X}'
    assert form_phys_addr(virtual_address_hex) == expected_physical_address  # High offset in page 2, segment 1

def test_edge_case_segment_boundary():
    # Test conversion at the boundary of a segment
    expected_frame = '000000000000000000101'  # 21 bits from segment 1, page 2
    expected_page_offset = '00000000000'      # 11 bits (0)
    page_offset = f'{int(expected_page_offset, 2):011b}'
    page_number = f'{2:010b}'
    segment_number = f'{1:011b}'
    virtual_address = page_offset + page_number + segment_number
    virtual_address_hex = f'{int(virtual_address, 2):08X}'
    expected_physical_address = f'{int(expected_frame + expected_page_offset, 2):04X}'
    assert form_phys_addr(virtual_address_hex) == expected_physical_address  # Low offset in page 2, segment 1
