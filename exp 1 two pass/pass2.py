def read_table(filename):
    table = {}
    with open(filename, 'r') as f:
        for line in f:
            tokens = line.strip().split()
            if len(tokens) >= 3:
                table[tokens[0]] = tokens[2]
    return table

def main_pass2():
    with open("IntermediateCode.txt", "r") as IntCode, \
         open("MachineCode.txt", "w") as MacCode:

        # Read symbol and literal tables
        symtab = read_table("SymTable.txt")
        littab = read_table("LitTable.txt")

        print("\n -- ASSEMBLER PASS 2 OUTPUT --")
        print("\n LC\tINTERMEDIATE CODE\t\tLC\tMACHINE CODE")

        for line in IntCode:
            tokens = line.strip().split('\t')
            if len(tokens) < 2:
                continue

            lc = tokens[0]
            int_code = tokens[1]

            # Skip assembler directives
            if "(AD," in int_code or "(DL,02)" in int_code:
                print(f" {lc}\t{int_code}\t\t{lc}\t-No Machine Code-")
                continue

            # Handle DS instruction
            if "(DL,01)" in int_code:
                value = int_code.split("(C,")[1].split(")")[0]
                machine_code = f"00\t0\t{value:03}"
                print(f" {lc}\t{int_code}\t\t{lc}\t{machine_code}")
                MacCode.write(f"{lc}\t{machine_code}\n")
                continue

            # Process IS instructions
            parts = int_code.split(')')
            machine_code = []
            
            for part in parts:
                if not part.strip():
                    continue
                
                part = part.strip(' (')
                if ',' not in part:
                    continue
                
                code_type, value = part.split(',')
                
                if code_type == "IS":
                    machine_code.append(value)
                elif code_type in ["1", "2", "3", "4"]:  # Register codes
                    machine_code.append(value)
                elif code_type == "S":
                    addr = symtab.get(value, "000")
                    machine_code.append(addr)
                elif code_type == "L":
                    addr = littab.get(value, "000")
                    machine_code.append(addr)

            if machine_code:
                while len(machine_code) < 3:
                    machine_code.append("000")
                print(f" {lc}\t{int_code}\t\t{lc}\t{'\t'.join(machine_code)}")
                MacCode.write(f"{lc}\t{'\t'.join(machine_code)}\n")

if __name__ == "__main__":
    main_pass2()