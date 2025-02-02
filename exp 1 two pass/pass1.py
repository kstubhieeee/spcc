class OPtab:
    def __init__(self, OPcode, Mclass, mNemonic):
        self.OPcode = OPcode
        self.Mclass = Mclass
        self.mNemonic = mNemonic

optab = [
    OPtab("MOVER", "IS", "01"),
    OPtab("MOVEM", "IS", "02"),
    OPtab("ADD", "IS", "03"),
    OPtab("SUB", "IS", "04"),
    OPtab("MULT", "IS", "05"),
    OPtab("DIV", "IS", "06"),
    OPtab("BC", "IS", "07"),
    OPtab("COMP", "IS", "08"),
    OPtab("PRINT", "IS", "09"),
    OPtab("READ", "IS", "10"),
    OPtab("START", "AD", "01"),
    OPtab("END", "AD", "02"),
    OPtab("EQU", "AD", "03"),
    OPtab("ORIGIN", "AD", "04"),
    OPtab("LTORG", "AD", "05"),
    OPtab("DS", "DL", "01"),
    OPtab("DC", "DL", "02")
]

def getOP(s):
    for i, entry in enumerate(optab):
        if entry.OPcode == s:
            return i
    return -1

def getRegID(s):
    regs = {"AREG": "1", "BREG": "2", "CREG": "3", "DREG": "4"}
    return regs.get(s, "0")

class SymTable:
    def __init__(self, No, SymbolName, Address):
        self.No = No
        self.SymbolName = SymbolName
        self.Address = Address

ST = [SymTable(0, "", "") for _ in range(50)]  # Increased size to 50

def presentST(s):
    for entry in ST:
        if entry.SymbolName == s:
            return True
    return False

def getSymID(s):
    for i, entry in enumerate(ST):
        if entry.SymbolName == s:
            return i
    return -1

class LitTable:
    def __init__(self, No, LiteralName, Address):
        self.No = No
        self.LiteralName = LiteralName
        self.Address = Address

LT = [LitTable(0, "", "") for _ in range(50)]  # Increased size to 50

def presentLT(s):
    for entry in LT:
        if entry.LiteralName == s:
            return True
    return False

def getLitID(s):
    for i, entry in enumerate(LT):
        if entry.LiteralName == s:
            return i
    return -1

class PoolTable:
    def __init__(self, no, L_No):
        self.no = no
        self.L_No = L_No

PT = [PoolTable(0, "") for _ in range(50)]  # Increased size to 50

def main_pass1():
    with open("Input.txt", "r") as fin, \
         open("IntermediateCode.txt", "w") as Inp, \
         open("SymTable.txt", "w") as SymTab, \
         open("LitTable.txt", "w") as LitTab, \
         open("PoolTable.txt", "w") as PoolTab:

        SymCount = 0
        LitCount = 0
        N1Count = 0
        PCount = 0
        LineCount = 0
        LineCount2 = "---"

        print("\n -- ASSEMBLER PASS 1 OUTPUT --")
        print("\n <LABEL\tOPCODE\tOP1\tOP2\tLine Count\tINTERMEDIATE CODE>")

        for line in fin:
            tokens = line.strip().split()
            if len(tokens) < 4:
                tokens.extend(["NAN"] * (4 - len(tokens)))
            Label, OPcode, OP1, OP2 = tokens[:4]

            id = getOP(OPcode)
            if id == -1:
                continue
            IntCode = f"({optab[id].Mclass},{optab[id].mNemonic})"

            if OPcode == "START":
                LineCount = int(OP1) if OP1 != "NAN" else 0
                IntCode += f" (C,{OP1}) NAN"
                LineCount2 = "---"

            elif OPcode == "EQU":
                LineCount2 = "---"
                if presentST(OP1):
                    if not presentST(Label):
                        ST[SymCount] = SymTable(SymCount + 1, Label, ST[getSymID(OP1)].Address)
                        SymCount += 1
                    else:
                        ST[getSymID(Label)].Address = ST[getSymID(OP1)].Address
                IntCode += " NAN NAN"

            elif Label != "NAN":
                if not presentST(Label):
                    ST[SymCount] = SymTable(SymCount + 1, Label, str(LineCount))
                    SymCount += 1
                else:
                    ST[getSymID(Label)].Address = str(LineCount)

            if OPcode == "LTORG":
                for i in range(LitCount - N1Count, LitCount):
                    LineCount2 = str(LineCount)
                    lit_code = "(DL,01) (C,"
                    c = LT[i].LiteralName[2]
                    lit_code += c + ") NAN"
                    LT[i].Address = str(LineCount)
                    LineCount += 1
                    Inp.write(f"{LineCount2}\t{lit_code}\n")
                
                if N1Count > 0:
                    PT[PCount] = PoolTable(PCount + 1, f"#{LT[LitCount - N1Count].No}")
                    PCount += 1
                N1Count = 0
                continue

            elif OPcode == "DC":
                LineCount2 = str(LineCount)
                IntCode += f" (C,{OP2}) NAN"
                LineCount += 1

            elif OPcode == "DS":
                LineCount2 = str(LineCount)
                IntCode += f" (C,{OP1}) NAN"
                LineCount += int(OP1)

            elif OPcode == "END":
                LineCount2 = "---"
                IntCode += " NAN NAN"
                if N1Count > 0:
                    for i in range(LitCount - N1Count, LitCount):
                        lit_lc = str(LineCount)
                        lit_code = "(DL,01) (C,"
                        c = LT[i].LiteralName[2]
                        lit_code += c + ") NAN"
                        LT[i].Address = str(LineCount)
                        LineCount += 1
                        Inp.write(f"{lit_lc}\t{lit_code}\n")
                    PT[PCount] = PoolTable(PCount + 1, f"#{LT[LitCount - N1Count].No}")
                    PCount += 1

            elif OPcode not in ["START", "EQU", "LTORG", "DC", "DS", "END"]:
                LineCount2 = str(LineCount)
                if OP1 != "NAN":
                    IntCode += f" ({getRegID(OP1)})"
                
                if OP2.startswith("='"):
                    LT[LitCount] = LitTable(LitCount + 1, OP2, "?")
                    LitCount += 1
                    N1Count += 1
                    IntCode += f" (L,{LitCount})"
                elif OP2 != "NAN":
                    if not presentST(OP2):
                        ST[SymCount] = SymTable(SymCount + 1, OP2, "?")
                        SymCount += 1
                    IntCode += f" (S,{getSymID(OP2) + 1})"
                else:
                    IntCode += " NAN"
                LineCount += 1

            print(f" {Label}\t{OPcode}\t{OP1}\t{OP2}\t{LineCount2}\t{IntCode}")
            Inp.write(f"{LineCount2}\t{IntCode}\n")

        # Write tables
        for i in range(SymCount):
            SymTab.write(f"{ST[i].No}\t{ST[i].SymbolName}\t{ST[i].Address}\n")
        
        for i in range(LitCount):
            LitTab.write(f"{LT[i].No}\t{LT[i].LiteralName}\t{LT[i].Address}\n")
        
        for i in range(PCount):
            PoolTab.write(f"{PT[i].no}\t{PT[i].L_No}\n")

if __name__ == "__main__":
    main_pass1()