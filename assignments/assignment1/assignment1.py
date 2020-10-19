"""
Memory

32-bit address
8-bit cell

Register

32 32-bit

Program

Add the number in memory address 0 and 1 to address 3
    Load r1, #0
    Load r2, #1
    Add r3, r1, r2
    Store r3, #3
"""
# use pandas to show our data
import pandas as pd

def dec2bin(data):
    """
    An integer data takes up 4 bytes of 32-bits
    param data : a number showed in decimal
    return res : a number showed in binary, each value of the array is coming from [0, 1]
    """
    res = [0 for i in range(32)]
    index = 31
    while data:
        res[index] = data % 2
        data //= 2
        index -= 1
    return ''.join('%s' %id for id in res)

def bin2dec(data):
    """
    An integer data takes up 4 bytes of 32-bits
    param data : a number showed in binary, each value of the array is coming from [0, 1]
    return res : a number showed in decimal
    """
    res = 0
    index = 31
    while index >= 0:
        res += int(data[index]) * pow(2, 31-index)
        index -= 1
    return res

def binadd(x, y):
    return dec2bin(bin2dec(x) + bin2dec(y))

# Define the class of cell
# In my machine, I use Big-endian to save values
class Cell():
    def __init__(self):
        self.value = ''.join('%s' %id for id in [0 for i in range(8)])

    def save(self, data):
        """
        data is a 8-bit binary number
        param data : an array which contains 8 numbers coming from [0,1] in it
        """
        self.value = data

    def get(self):
        return self.value

    
# Difine a memory class
# 32-bit address
class Memory():
    def __init__(self):
        """
        Memory:
        32-bit address
        8-bit cell
        """
        # init 4 address 0*4, 1*4, 2*4, 3*4
        # because one memory cantains 4 cells
        # so the addresses are multiples of 4
        self.address = []
        for i in range(4):
            self.address.append(dec2bin(i*4))
        
        # init cells to save value
        mems = []
        for i in range(4):
            mem = []
            for i in range(4):
                mem.append(Cell())
            mems.append(mem)
        
        # init memory which contains 4 value at their address
        self.memory = {self.address[0]: mems[0], self.address[1]: mems[1], self.address[2]:mems[2], self.address[3]: mems[3]}

    def save(self, address, data):
        """
        when save a value to a memory, it changes the 4 cells' values
        """
        for i in range(4):
            self.memory[dec2bin(address*4)][i].save(dec2bin(data)[i*8:(i+1)*8])

    def get(self, loc):
        """
        get the whole value of a memory
        """
        res = dict()
        for k in range(4):
            res[self.address[k]] = ''.join([i.get() for i in self.memory[self.address[k]]])
        return res[dec2bin(loc)]

    def show(self):
        """
        show the whole value of a memory
        """
        res = list()
        for k in range(4):
            res.append({'address':self.address[k], 'value':''.join([i.get() for i in self.memory[self.address[k]]])})
        df = pd.DataFrame(res, columns=['address', 'value'])
        return print("The state of the memory is:\n", df)

# Difine a register class
# 32-bit address
class Register():
    def __init__(self):
        """
        Register:
        32 32-bit
        Program
        """
        self.reg = dict()
        for i in range(32):
            self.reg[str(i)] = ''.join('%s' %id for id in [0 for i in range(32)])

    def save(self, data, loc):
        self.reg[str(loc)] = data

    def get(self, loc):
        """
        when get the value of a register, it will return to init situation
        """
        res = self.reg[str(loc)]
        # self.reg[str(loc)] = ''.join('%s' %id for id in [0 for i in range(32)])
        return res

    def show(self):
        """
        show the whole value of a memory
        """
        res = list()
        for k in range(32):
            res.append({'id':k, 'value':self.reg[str(k)]})
        df = pd.DataFrame(res, columns=['id', 'value'])
        return print("The state of the register is:\n", df)

# Define the machine class
class Machine():
    def __init__(self,memory, register):
        self.memory = memory
        self.register = register

    def Load(self, loc_r, loc_m):
        data = self.memory.get(loc_m*4)
        self.register.save(data, loc_r)
        print("Load data from Memory%d to Register%d the value is %d\n"%(loc_m, loc_r, bin2dec(data)))

    def Add(self, loc3, loc1, loc2):
        data1 = self.register.get(loc1)
        data2 = self.register.get(loc2)
        data3 = binadd(data1, data2)
        self.register.save(data3, loc3)
        print("Add data %d from Register%d and %d from Register%d to %d to be saved in Register%d\n"%(bin2dec(data1), loc1, bin2dec(data2), loc2, bin2dec(data3), loc3))

    def Store(self, loc_r, loc_m):
        data = self.register.get(loc_r)
        self.memory.save(loc_m, bin2dec(data))
        print("Store data from Register%d to Memory%d the value is %d\n"%(loc_r, loc_m, bin2dec(data)))

    def Show(self):
        self.memory.show()
        self.register.show()

# This function is defined to do unit testing
def test():
    print(dec2bin(155))
    print(bin2dec('00000000000000000000000010011011'))
    memory = Memory()
    print(memory.get(0))
    memory.save(0, 1)
    print(memory.get(0))
    register = Register()
    register.save(memory.get(0), 0)
    print(register.get(0))

# The main function to do the data-flows
def main():
    """
    Program

    Add the number in memory address 0 and 1 to address 3
        Load r1, #0
        Load r2, #1
        Add r3, r1, r2
        Store r3, #3
    """
    print("----------------------------- Init Machine ---------------------------------\n")
    memory = Memory()
    memory.save(0, 1)
    memory.save(1, 2)
    register = Register()
    machine = Machine(memory, register)
    machine.Show()
    print("----------------------------- Load ---------------------------------\n")
    machine.Load(1, 0)
    machine.Show()
    machine.Load(2, 1)
    machine.Show()
    print("------------------------------ Add ---------------------------------\n")
    machine.Add(3, 1, 2)
    machine.Show()
    print("----------------------------- Store --------------------------------\n")
    machine.Store(3, 3)
    machine.Show()

if __name__ == '__main__':
    main()