# Two-Pass Assembler Implementation

## Pass 1 Execution Steps

1. **Initialization**

   - Open input and output files (Input.txt, IntermediateCode.txt, SymTable.txt, LitTable.txt, PoolTable.txt)
   - Initialize counters (SymCount, LitCount, N1Count, PCount, LineCount)

2. **For each input line:**

   - Split line into tokens (Label, OPcode, OP1, OP2)
   - Process based on operation code:

   a. **START**

   - Set initial LineCount to specified address (600)
   - Generate IC: (AD,01) (C,600) NAN

   b. **Regular Instructions (MOVER, ADD, SUB, etc.)**

   - Add label to Symbol Table if present
   - Convert to intermediate code format
   - Handle registers and operands
   - Example: MOVER AREG Y → (IS,01) (1) (S,1)

   c. **LTORG**

   - Process pending literals
   - Assign addresses to literals
   - Update Pool Table
   - Generate IC for each literal

   d. **EQU**

   - Add label to Symbol Table with referenced address
   - Example: LABEL EQU LOOP → Assign LOOP's address to LABEL

   e. **DS/DC**

   - Add label to Symbol Table
   - Generate appropriate IC
   - Update LineCount accordingly

3. **Final Steps**
   - Write Symbol Table
   - Write Literal Table
   - Write Pool Table

## Pass 2 Execution Steps

1. **Initialization**

   - Read Symbol Table and Literal Table into memory
   - Open IntermediateCode.txt and MachineCode.txt

2. **For each intermediate code line:**

   - Parse the IC components

3. **Generate Machine Code based on IC type:**

   a. **Assembler Directives (AD)**

   - START, END, LTORG, EQU, ORIGIN
   - No machine code generated

   b. **Declarative Statements (DL)**

   - DS: Generate 00 0 size
   - DC: Generate 00 0 constant

   c. **Imperative Statements (IS)**

   - Format: opcode register address
   - Replace symbolic references with actual addresses
   - Example: (IS,01) (1) (S,1) → 01 1 600

4. **Write machine code to output file**

## Example Processing

Input line:
