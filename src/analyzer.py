import src.config as cfg
from src.address import form_phys_addr

def form_addr(tokens: list[str]) -> str:
    virtual_addr = ''
    for token in tokens:
        virtual_addr += token
    return f'[{form_phys_addr(virtual_addr)}]'

def clean_data(data: str) -> str:
    return "".join(data.split())

def get_tokens(data: str) -> list[str]:
    return [data[i:i+2] for i in range(0, len(data), 2)]

def print_row(tokens: list[str], mnemonic: str, operands: int, error_code:int = None, file=None):
    print(' '.join(tokens), file=file)
    if error_code:
        print(f'Error: {cfg.ERRORS[error_code]}', file=file)
    print(f'{mnemonic} {", ".join(operands)}', file=file); print(file=file)

def analyze(input_file, output_dir):
    print("Analyzing file:", input_file)
    print("Output directory:", output_dir)
    
    CLEANED_FILE = output_dir + "program_cleaned.txt"
    ANALYSIS_FILE = output_dir + "analysis.txt"

    # read the input file and clean the data from whitespaces
    with open(input_file, "r") as f:
        data = f.read()
        data = clean_data(data)
        
    # write cleaned data to program_cleaned.txt
    output_file = CLEANED_FILE
    with open(output_file, "w") as f:
        f.write(data)
        
    # read the cleaned data assuming 2 characters as a single token - byte
    with open(output_file, "r") as f:
        data = f.read()
        tokens = get_tokens(data)
        
    with open(ANALYSIS_FILE, "w") as f:
        # analyze the tokens
        i = 0
        command = []
        current_token = ''
        arguments = []
        while i < len(tokens):
            error_code = None
            current_token = tokens[i]
            
            if current_token in cfg.OPCODES:
                opcode = current_token
                i += 1
                # i: index of the first operand
                command = [opcode]
                
                reverse_flag = False
                if opcode in cfg.REVERSE_OPCODE:
                    reverse_flag = bool(tokens[i][0])
                    
                operands = cfg.OPCODES[opcode]['operands']

                if len(operands) == 1:
                    operand_size = cfg.OPERAND_SIZES[operands[0]]
                    
                    if operands[0] == 'SHIFT':
                        arguments = [f'{int(tokens[i], 16)}']
                        command.append(tokens[i])
                    elif operands[0] == 'ADDR':
                        try:
                            arguments = [form_addr(tokens[i:i+operand_size])]
                        except Exception as e:
                            error_code = 5
                            arguments = [f'[0x{"".join(tokens[i:i+operand_size])}]']
                        command.extend(tokens[i:i+operand_size])
                        
                    i += operand_size
                    
                elif len(operands) == 2:
                    operands_sizes = [cfg.OPERAND_SIZES[operand] for operand in operands]
                    
                    if operands[0] == 'REG' and operands[1] == 'REG':
                        arguments = [f'R{int(tokens[i][0], 16)}', f'R{int(tokens[i][1], 16)}']
                        command.append(tokens[i])
                        i += 1  # REG REG
                        
                    elif operands[0] == 'REG' and operands[1] == 'ADDR':
                        command.append(tokens[i])
                        try:
                            arguments = [f'R{int(tokens[i][0], 16)}', form_addr(tokens[i+1:i+operands_sizes[1]+1])]
                        except Exception as e:
                            error_code = 5
                            arguments = [f'R{int(tokens[i][0], 16)}', f'[0x{"".join(tokens[i+1:i+operands_sizes[1]+1])}]']
                        command.extend(tokens[i+1:i+operands_sizes[1]+1])
                        
                        i += 1                  # REG
                        i += operands_sizes[1]  # ADDR
                        
                    elif operands[0] == 'REG' and operands[1] == 'LIT16':
                        arguments = [f'R{int(tokens[i][1], 16)}', f'{int(tokens[i+1], 16)}']
                        command.append(tokens[i])
                        command.append(tokens[i+1])
                        i += 1 # REG
                        i += 2 # LIT16
                        
                    if reverse_flag:
                        arguments = arguments[::-1]

                print_row(command, 
                          cfg.OPCODES[opcode]['mnemonic'], 
                          arguments, 
                          error_code=error_code, 
                          file=f)
                    

    print("Analysis complete")
