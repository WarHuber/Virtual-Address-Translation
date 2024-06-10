INPUT_DIR = "input/"
OUTPUT_DIR = "output/"
DATA_DIR = "data/"

INPUT_FILE = INPUT_DIR + "program.txt"

OUTPUT_FILE = OUTPUT_DIR + "result.txt"

PAGES_TABLE_FILE = DATA_DIR + "pages.csv"
SEGMENTS_TABLE_FILE = DATA_DIR + "segments.csv"

OPERAND_SIZES = {
    'REG': 1,
    'ADDR': 4,
    'SHIFT': 1,
    'LIT16': 4
}

OPCODES = {
    '1A': {'mnemonic': 'MOV', 'operands': ['REG', 'REG']},
    '1B': {'mnemonic': 'MOV', 'operands': ['REG', 'ADDR']},
    '01': {'mnemonic': 'ADD', 'operands': ['REG', 'REG']},
    '02': {'mnemonic': 'ADD', 'operands': ['REG', 'ADDR']},
    '94': {'mnemonic': 'JG',  'operands': ['SHIFT']},
    '95': {'mnemonic': 'JG',  'operands': ['ADDR']},
    '80': {'mnemonic': 'CMP', 'operands': ['REG', 'REG']},
    '1C': {'mnemonic': 'MOV', 'operands': ['REG', 'LIT16']},
}

REVERSE_OPCODE = [
    '1B',
    '02',
    '1C'
]

ERRORS = {
    1: 'Invalid opcode',
    2: 'Invalid operand',
    3: 'Invalid addressing mode',
    4: 'Invalid register',
    5: 'Invalid memory location',
}

PAGE_SIZE = 2*2**10
DESCRIPTOR_TABLE_SIZE = 2048