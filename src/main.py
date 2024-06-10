import config as cfg
from address import form_phys_addr

def form_addr(tokens: list[str]) -> str:
    virtual_addr = ''
    for token in tokens:
        virtual_addr += token
    return form_phys_addr(virtual_addr)

def clean_data(data: str) -> str:
    return "".join(data.split())

def get_tokens(data: str) -> list[str]:
    return [data[i:i+2] for i in range(0, len(data), 2)]

def print_row(tokens: list[str], mnemonic: str, operands: int, error_code:int = None, file=None):
    print(' '.join(tokens)); print()
    if error_code:
        print(f'Error: {cfg.ERRORS[error_code]}'); print()
    print(f'{mnemonic} {", ".join(operands)}'); print()

def analyze(input_file, output_dir):
    print("Analyzing file:", input_file)
    print("Output directory:", output_dir)

    # read the input file and clean the data from whitespaces
    with open(input_file, "r") as f:
        data = f.read()
        data = clean_data(data)
        
    # write cleaned data to program_cleaned.txt
    output_file = output_dir + "program_cleaned.txt"
    with open(output_file, "w") as f:
        f.write(data)
        
    # read the cleaned data assuming 2 characters as a single token - byte
    with open(output_file, "r") as f:
        data = f.read()
        tokens = get_tokens(data)
        
    # analyze the tokens
    i = 0
    current_token = ''
    operands = []
    reverse_flag = False
    reverse_opcode = False
    while i < len(tokens):
        current_token = tokens[i]
        
        if current_token in cfg.OPCODES:
            opcode = current_token
            i += 1
            
            if opcode in cfg.REVERSE_OPCODE:
                reverse_flag = bool(tokens[i][0])
                reverse_opcode = True
                
            for operand in cfg.OPCODES[opcode]['operands']:
                if operand == 'REG':
                    operands.append('R' + str(int(tokens[i][0 if not reverse_opcode else 1], 16)))
                    i += 1
                    
                elif operand == 'ADDR':
                    operands.append(form_addr(tokens[i:i+4]))
                    i += 4
                    

            
            

    print("Analysis complete")

if __name__ == "__main__":
    analyze(cfg.INPUT_FILE, cfg.OUTPUT_DIR)