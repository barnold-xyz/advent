class Program:
    def __init__(self, data):
        self.A = int(data[0].replace('Register A: ', ''))
        self.B = int(data[1].replace('Register B: ', ''))
        self.C = int(data[2].replace('Register C: ', ''))
        self.inst = list(map(int, data[4].replace('Program: ', '').split(',')))
        self.combo_map = {1: 1, 2: 2, 3: 3, 4: self.A, 5: self.B, 6: self.C}
        self.ops = {0: self.adv, 1: self.bxl, 2: self.bst, 3: self.jnz, 4: self.bxc, 5: self.out, 6: self.bdv, 7: self.cdv}
        self.inst_pointer = 0
        self.output = []

    def get_combo(self, num):
        if num in [0, 1, 2, 3]: return num
        elif num == 4: return self.A
        elif num == 5: return self.B
        elif num == 6: return self.C
        else: raise ValueError(f"Invalid combo identifier: {num}")

    def adv(self, operand):  # opcode 0
        self.A = self.A >> self.get_combo(operand)
    def bxl(self, literal):  # opcode 1
        self.B = self.B ^ literal
    def bst(self, operand):  # opcode 2
        self.B = self.get_combo(operand) & 0b111
        print(f'in bst, operand: {operand}, B: {self.B}, combo_map: {self.get_combo(operand)}')
        print(f'combo_map: {self.combo_map}')
    def jnz(self, operand):  # opcode 3
        if self.A != 0:
            self.inst_pointer = operand - 2
    def bxc(self, operand):  # opcode 4
        self.B = self.B ^ self.C
    def out(self, operand):  # opcode 5
        self.output.append(self.get_combo(operand) & 0b111)
    def bdv(self, operand):  # opcode 6
        self.B = self.A >> self.get_combo(operand)
    def cdv(self, operand):  # opcode 7
        self.C = self.A >> self.get_combo(operand)

    def __str__(self):
        return f"A: {self.A}, B: {self.B}, C: {self.C}, IP: {self.inst_pointer}, Output: {self.output}"
    def __repr__(self):
        return self.__str__()

    def run_program(self, inst=None, A=None, B=None, C=None):
        inst = inst or self.inst  
        for reg, val in {'A': A, 'B': B, 'C': C}.items():
            if val is not None: setattr(self, reg, val)

        self.inst_pointer = 0
        self.output = []
        while self.inst_pointer < len(inst):
            opcode = inst[self.inst_pointer]
            operand = inst[self.inst_pointer + 1]

            print(f'running op {opcode} with operand {operand}')
            self.ops[opcode](operand)
            self.inst_pointer += 2
        return self.output

def test():
    '''If register C contains 9, the program 2,6 would set register B to 1.
If register A contains 10, the program 5,0,5,1,5,4 would output 0,1,2.
If register A contains 2024, the program 0,1,5,4,3,0 would output 4,2,5,6,7,7,7,7,3,1,0 and leave 0 in register A.
If register B contains 29, the program 1,7 would set register B to 26.
If register B contains 2024 and register C contains 43690, the program 4,0 would set register B to 44354.
'''
    data = open("2024/17/test.txt").read().splitlines()
    prog = Program(data)
    print(prog)
    print(prog.run_program(C=9, inst=[2,6]))
    print(prog)
    print(prog.run_program(A=10, inst=[5,0,5,1,5,4]))
    print(prog)
    print(prog.run_program(A=2024, inst=[0,1,5,4,3,0]))
    print(prog)
    print(prog.run_program(B=29, inst=[1,7]))
    print(prog)
    print(prog.run_program(B=2024, C=43690, inst=[4,0]))
    print(prog)

prog = Program(open("2024/17/input.txt").read().splitlines())
print(prog.run_program())
print(prog)
print('part 1:\n', ','.join(map(str, prog.output)))