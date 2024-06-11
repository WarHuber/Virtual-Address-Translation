import pytest
from src.analyzer import form_addr
from src.exceptions import InvalidMemoryAddressError, PageNotExistsInRAMError, SegmentNotExistsInDescriptorTableError

@pytest.fixture
def mock_form_phys_addr(mocker):
    return mocker.patch('src.address.form_phys_addr')

def test_form_addr_empty():
    with pytest.raises(InvalidMemoryAddressError):
        form_addr([])

def test_form_addr_single_token():
    with pytest.raises(InvalidMemoryAddressError):
        form_addr(['AB'])

def test_form_addr_two_tokens():
    with pytest.raises(InvalidMemoryAddressError):
        form_addr(['AB', 'CD'])
