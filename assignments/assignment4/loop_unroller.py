import re


class instruction:
    def __init__(self,op,type,rs1,rs2,rd,imm=0,scope = 0):

        #base -->rs1 loop_label-->missing
        self.op = op
        self.type = type
        self.rs1 = rs1
        self.rs2 = rs2
        self.rd = rd
        self.imm = imm
        self.scope = scope
        self.is_issued = False
    
    def _get_op(self):
        return self.op

    def _get_type(self):
        return self.type
    def _get_rs1(self):
        return self.rs1

    def _get_rs2(self):
        return self.rs2
    def _get_rd(self):
        return self.rd    
    def _get_imm(self):
        return self.imm

    def _get_issued_state(self):
        return self.is_issued

    def _get_scope(self):
        return self.scope

    def _set_issued_state(self,state):
        self.is_issued = state

    def _is_float_op(self):
        return self.type == "float"
    def _is_int_op(self):
        return self.type == "int"

    def _print(self):
        if(self.op == "fld" or self.op == "fsd"):
            print("scope:",self.scope,self.op ,"f",self.rd,",",self.imm,"(x",self.rs1,")")
        elif(self.op == "fadd.d"):
            print("scope:",self.scope,self.op," f",self.rd,",f",self.rs1,",f",self.rs2)
        elif(self.op == "addi"):
            print("scope:",self.scope,self.op," x",self.rd,"x",self.rs1,",",self.imm)
        elif(self.op == "bne"):
            print("scope:",self.scope,self.op," x",self.rs1,",x",self.rs2,",loop_label")
        elif(self.op == "stall"):
            print("scope:",self.scope," stall")

    @classmethod
    def _pick_an_unissued_inst(self,all_inst_set,zero_map,zero_map_index):
        # for i in range(len(bitmap)):
        #    if(bitmap[i]):
        #        continue
        #    else:
        #        return all_inst_set[i]

        return all_inst_set[zero_map[zero_map_index]]
    @classmethod
    def _check(self,issued_set,cur_inst):
        for i in range(len(issued_set)):
            if(cur_inst == issued_set[i]):
                return False

        # r = max(sum(self._count_register()[0]),sum(self._count_register()[1]))
        # print("the number of register used:",r)
        cur_scope = cur_inst._get_scope()
        cur_op = cur_inst._get_op()

        if(cur_op == "fld"):
            for i in range(len(issued_set)):
                if (issued_set[i]._get_scope() != cur_scope):
                    continue
                else:
                    if (issued_set[i]._get_op() == "fsd"):
                        return False
                    if (issued_set[i]._get_op() == "fadd.d"):
                        return False
        elif(cur_op == "fadd.d"):
            if(len(issued_set) <= 1):
                return False
            else:
                # print(issued_set)
                for i in range (len(issued_set)):
                    if(issued_set[i]._get_scope() != cur_scope):
                        continue
                    else:
                        if(issued_set[i]._get_op() == "fsd"):
                            return False
                        if(issued_set[i]._get_op() == "fld"):
                            if(i >= (len(issued_set) - 1)):
                                return False
                            else:
                                return True
        elif(cur_op == "fsd"):
            if(len(issued_set) <= 5):
                return False
            else:
                for i in range(len(issued_set)):
                    if(issued_set[i]._get_scope() != cur_scope):
                        continue
                    else:
                        if(issued_set[i]._get_op() == "fadd.d"):
                            if(i  >= (len(issued_set) - 2)):
                                return False
                            else:
                                return True            
        return True

    
        

class pre_loop_unroller:
    def __init__(self):
        self.instruction_set = []
  
        

    def _read_file(self,file):
        fileobj = open(file,"r")
        self.__read_and_parsing(fileobj)
        fileobj.close()

                
    def __read_and_parsing(self,fileobj):
        for line in fileobj:
            segs = line.strip().split(' ')
            temp = segs[0]
            if (re.match(temp,"loop")):
                pass 
            elif (re.match(temp,"fld")):
                l = segs[-1]
                l = l.strip().split(',')
                rd = l[0][1:]
                l = l[1]
                l = l.strip().split('(')
                imm = l[0]
                l = l[1]
                l = l.strip().split(')')
                base = l[0][1:]
                self.instruction_set.append(instruction("fld","float",base,None,rd,imm))
            elif (re.match(temp,"fadd.d")):
                l = segs[-1]
                l = l.strip().split(',')
                rd = l[0][1:]
                rs1 = l[1][1:]
                rs2 = l[2][1:]
                # print(rd,rs2)
                self.instruction_set.append(instruction("fadd.d","float",rs1,rs2,rd))
            elif (re.match(temp,"fsd")):
                l = segs[-1]
                l = l.strip().split(',')
                rd = l[0][1:]
                l = l[1]
                l = l.strip().split('(')
                imm = l[0]
                l = l[1]
                l = l.strip().split(')')
                base = l[0][1:]
                self.instruction_set.append(instruction("fsd","float",base,None,rd,imm))
            elif(re.match(temp,"addi")):
                l = segs[-1]
                l = l.strip().split(',')
                rd = l[0][1:]
                rs1 = l[1][1:]
                sham = l[2]
                # print(rd,rs2)
                self.instruction_set.append(instruction("addi","int",rs1,None,rd,8))
            elif(re.match(temp,"bne")):
                l = segs[-1]
                l = l.strip().split(',')
                rs1 = l[0][1:]
                rs2 = l[1][1:]
                label = l[2]
                # print("bne:",rs1,rs2)
                self.instruction_set.append(instruction("bne","int",rs1,rs2,None))
                

    def _count_register(self):
        fmap,imap = [0 for i in range(32)],[0 for i in range(32)]
        for i in range(len(self.instruction_set)):
            if(self.instruction_set[i]._get_op() == "fld" or self.instruction_set[i]._get_op() == "fsd"):
                rs1 = self.instruction_set[i]._get_rs1()
                r_NO = int(rs1[1:])
                if(imap[r_NO] == 0):
                    imap[r_NO] = 1
                rd = self.instruction_set[i]._get_rd()
                r_NO = int(rd[1:])
                if(fmap[r_NO] == 0):
                    fmap[r_NO] = 1

            elif(self.instruction_set[i]._get_op() == "fadd.d"):
                rs1 = self.instruction_set[i]._get_rs1()
                r_NO = int(rs1[1:])
                if(fmap[r_NO] == 0):
                    fmap[r_NO] = 1
                rs2 = self.instruction_set[i]._get_rs2()
                r_NO = int(rs2[1:])
                if(fmap[r_NO] == 0):
                    fmap[r_NO] = 1
                rd = self.instruction_set[i]._get_rd()
                r_NO = int(rd[1:])
                if(fmap[r_NO] == 0):
                    fmap[r_NO] = 1

            elif(self.instruction_set[i]._get_op() == "addi"):
                rs1 = self.instruction_set[i]._get_rs1()
                r_NO = int(rs1[1:])
                if(imap[r_NO] == 0):
                    imap[r_NO] = 1
                rd = self.instruction_set[i]._get_rd()
                r_NO = int(rd[1:])
                if(imap[r_NO] == 0):
                    imap[r_NO] = 1

            elif(self.instruction_set[i]._get_op() == "bne"):
                rs1 = self.instruction_set[i]._get_rs1()
                r_NO = int(rs1[1:])
                if(imap[r_NO] == 0):
                    imap[r_NO] = 1
                rs2 = self.instruction_set[i]._get_rs2()
                r_NO = int(rs2[1:])
                if(imap[r_NO] == 0):
                    imap[r_NO] = 1

            i += 1
        
        print(fmap)
        print(imap)

        return fmap,imap

    def _pre_unroll(self,n):
        self.fmap = {'0':0,
                    '2':1,
                    '4':2}
        self.imap = {'1':0,
                    '2':1}
        self.pre_unroll_inst_set = []
        # for i in range(len(self.instruction_set)):
        #    self.instruction_set[i]._print()
        # fmap,imap = self._count_register()
        scope = 0
        for i in range(n * 3):
            inst =self.instruction_set[i % 3]
            op = inst._get_op()
            itype = inst._get_type()
            rs1 = inst._get_rs1()
            rs2 = inst._get_rs2()
            rd = inst._get_rd()
            imm = inst._get_imm()
            if(op == "fld" or op == "fsd"):
                rs1 = self.imap[rs1]
                rd = self.fmap[rd]
                self.pre_unroll_inst_set.append(instruction(op,itype,rs1,rs2,rd,scope*8,scope))
            elif(op == "fadd.d"):
                rs1 = self.fmap[rs1]
                rs2 = self.fmap[rs2]
                rd = self.fmap[rd]
                self.pre_unroll_inst_set.append(instruction(op,itype,rs1,rs2,rd,scope=scope))
            
            if(i % 3 == 2):  
                scope += 1
                self.fmap = {'0':4*scope,
                        '2':1,
                        '4':4*scope + 2
                        }
                self.imap = {'1':0,
                         '2':1
                        }
            i += 1

        inst =self.instruction_set[3]
        op = inst._get_op()
        itype = inst._get_type()
        rs1 = inst._get_rs1()
        rs2 = inst._get_rs2()
        rd = inst._get_rd()
        imm = inst._get_imm()
        if(op == "addi"):
                    rs1 = self.imap[rs1]
                    rd = self.imap[rd]
                    self.pre_unroll_inst_set.append(instruction(op,itype,rs1,None,rd,scope*8))
        inst =self.instruction_set[4]
        op = inst._get_op()
        itype = inst._get_type()
        rs1 = inst._get_rs1()
        rs2 = inst._get_rs2()
        rd = inst._get_rd()
        imm = inst._get_imm()
        if(op == "bne"):
                    rs1 = self.imap[rs1]
                    rs2 = self.imap[rs2]
                    self.pre_unroll_inst_set.append(instruction(op,itype,rs1,rs2,None))
        for i in range(14):
            self.pre_unroll_inst_set[i]._print()

def count_NOT_zero_with_strping(map,last_index):
    counter = 0
    zero_map = []
    for i in range(len(map)):
        if(map[i] == False and i != last_index):
            counter += 1
            zero_map.append(i)
        else:
            continue
    return zero_map,counter

def count_NOT_zero(map):
    counter = 0
    zero_map = []
    for i in range(len(map)):
        if(map[i] == False):
            counter += 1
            zero_map.append(i)
    return zero_map,counter

class loop_unroller:

    def __init__(self):
        self.best_choice = []
        self.total_clock = 10000
        self.counter = 0
        # self.temp_clock = 0
        # self.temp_inst = []
        self.counter_time = 0
        # self.last_index = 0


    def _reset_state(self):
        # self.temp_inst.clear()
        # self.temp_clock = 0
        # self.last_index = last_index
        self.best_choice.clear()
        # print("temp best choice:",self.best_choice)

    def _unroll(self,all_inst_set,bit_map,temp_inst,temp_clock):
        self.counter_time += 1
        # print(self.counter_time)
        zero_map, counter = count_NOT_zero(bit_map)
        # try_bit = [False] * counter
        if(counter == 0):
            print("temp clock:",self.total_clock)
            if(temp_clock <= self.total_clock):
                print(bit_map)
                print(temp_clock)
                self.total_clock = temp_clock
                self.best_choice = []
                print("After clear, the length of best choice is:",len(self.best_choice))
                self.best_choice = temp_inst
                print("temp best choice:")
                # for i in range(len(self.best_choice)):
                #     self.best_choice[i]._print()
                return
        if(temp_clock > self.total_clock):
            print("cutting down:")
            return
        else:
            tag = False
            for i in range(counter):
                # try_bit[i] = True
                cur_inst = instruction._pick_an_unissued_inst(all_inst_set,zero_map,i)
                if(instruction._check(temp_inst,cur_inst)):
                    tag = True
                    temp_clock += 1
                    temp_inst.append(cur_inst)
                    bit_map[zero_map[i]] = True
                    # bit_map
                    # print("before the bit map:",bit_map,len(temp_inst))
                    self._unroll(all_inst_set,bit_map,temp_inst,temp_clock)
                    # print("after the bit map:",bit_map,len(temp_inst))
                    bit_map[zero_map[i]] = False
                    temp_clock -= 1
                    temp_inst.pop(-1)
                    # print(bit_map)
                    print("the solution length now:", len(temp_inst))

            if(tag == False):
                temp_clock += 1
                print("add a nop instruction,",temp_clock)
                nop_inst = instruction("stall","stall",None,None,None)
                temp_inst.append(nop_inst)
                self._unroll(all_inst_set,bit_map,temp_inst,len(temp_inst))




        # if(temp_clock >= self.total_clock):
        #     # if(last_index[-1] == 128):
        #     #     pass
        #     # else:
        #     #     bit_map[last_index[-1]] = False
        #     # print("pop:")
        #     # temp_inst[-1]._print()
        #     # temp_inst.pop(-1)
        #     # temp_clock -= 1
        #     # last_index.pop(-1)
        #     # self._unroll(all_inst_set,bit_map,temp_inst,temp_clock,last_index)
        #     return
        # elif(last_index == 128):
        #     zero_map,counter = count_NOT_zero(bit_map)
        #     try_bit = [False] * counter
        #     for i in range(counter):
        #         if(try_bit[i] == True):
        #             continue
        #         try_bit[i] = True
        #         cur_inst = instruction._pick_an_unissued_inst(all_inst_set,zero_map,i)
        #         if(instruction._check(temp_inst,cur_inst)):
        #             if (i == counter - 1):
        #                 temp_clock += 1
        #                 last_index = 128
        #                 temp_inst.append(instruction("stall", "stall", None, None, None))
        #                 # print("push stall inst")
        #                 self._unroll(all_inst_set, bit_map, temp_inst, temp_clock, last_index)
        #                 # print(bit_map)
        #
        #             else:
        #                 temp_clock += 1
        #                 # print("push:")
        #                 # cur_inst._print()
        #                 temp_inst.append(cur_inst)
        #                 bit_map[zero_map[i]] = True
        #                 # print("cur_bit_map:",bit_map)
        #                 last_index = zero_map[i]
        #                 self._unroll(all_inst_set,bit_map,temp_inst,temp_clock,last_index)
        #                 bit_map[zero_map[i]] = False
        # else:
        #     if(bit_map == [True]* len(bit_map)):
        #         if(temp_clock < self.total_clock):
        #             self.best_choice.clear()
        #             self.best_choice = temp_inst
        #             self.total_clock = temp_clock
        #             print("get one solution")
        #             print("current total clock:",self.total_clock)
        #             return
        #     else:
        #         zero_map,counter = count_NOT_zero(bit_map)
        #         try_bit = [False] * counter
        #         for i in range(counter):
        #             if(try_bit[i] == True):
        #                 continue
        #             cur_inst = instruction._pick_an_unissued_inst(all_inst_set,zero_map,i)
        #             # if(cur_inst == all_inst_set[last_index]):
        #             #     print(last_index)
        #             #     continue
        #             # print("the choice we have:",counter)
        #             try_bit[i] = True
        #             if(cur_inst == all_inst_set[last_index]):
        #                 continue
        #             if(instruction._check(temp_inst,cur_inst)):
        #                 temp_clock += 1
        #                 # print("pushll:",i)
        #                 # cur_inst._print()
        #                 temp_inst.append(cur_inst)
        #                 bit_map[zero_map[i]] = True
        #                 # print("cur_bit_map:",bit_map)
        #                 last_index = zero_map[i]
        #                 # print("enter next res:")
        #                 self._unroll(all_inst_set,bit_map,temp_inst,temp_clock,last_index)
        #                 bit_map[zero_map[i]] = False
        #             else:
        #                 if(i == counter - 1):
        #                     temp_clock += 1
        #                     last_index = 128
        #                     temp_inst.append(instruction("stall","stall",None,None,None))
        #                     # print("push stall inst")
        #                     self._unroll(all_inst_set,bit_map,temp_inst,temp_clock,last_index)
        #                     # print(bit_map)
        #                 continue
        #         return



                
if __name__ == "__main__":
    pre_obj = pre_loop_unroller()
    pre_obj._read_file("source.S")
    pre_obj._pre_unroll(4)

    pre_obj.pre_unroll_inst_set.append(instruction("stall","stall",None,None,None))
    obj = loop_unroller()
    
    # print((len(pre_obj.pre_unroll_inst_set)-2) / 3)
    print(len(pre_obj.pre_unroll_inst_set[0:12]))
    # for i in range (int((len(pre_obj.pre_unroll_inst_set)-2) / 3)):
    #     obj._reset_state()
    #     bit_map = [0] * (len(pre_obj.pre_unroll_inst_set)-2)
    #     bit_map[i] = True
    #     obj.temp_inst.append(pre_obj.pre_unroll_inst_set[i])
    #     print("loop:",i*3)
    #     obj._unroll(pre_obj,bit_map,i*3)
    
    obj._reset_state()
    # bit_map = [False] * (len(pre_obj.pre_unroll_inst_set)-3)
    bit_map = [False] * 12
    bit_map[0] = True
    temp_inst = []
    temp_inst.append(pre_obj.pre_unroll_inst_set[0])
    obj._unroll(pre_obj.pre_unroll_inst_set[0:12],bit_map,temp_inst,1)


    print("-----the result---")
    print("counter time:",obj.counter_time)
    for i in range(len(obj.best_choice)):
        obj.best_choice[i]._print()
    # print(len(obj.best_choice))
    # print(obj.total_clock)
    pre_obj.pre_unroll_inst_set[13]._print()
    pre_obj.pre_unroll_inst_set[14]._print()
        # def _unroll(self,pre_unroller_obj,bit_map,temp_inst,temp_clock):
    #     self.counter_time += 1
    #     print(self.counter_time)
    #     if(self.temp_clock >= self.total_clock):
    #         if(self.last_index == 128):
    #             print("pop:")
    #             self.temp_inst[-1]._print()
    #             self.temp_inst.pop(-1)
    #             self.temp_clock -= 1
    #         else:
    #             print("pop:")
    #             self.temp_inst[-1]._print()
    #             self.temp_inst.pop(-1)
    #             bit_map[self.last_index] = False
    #             self.temp_clock -= 1
    #         return
        
    #     elif(self.last_index == 128):
    #         zero_map,counter = count_NOT_zero(bit_map)
    #         success = True
    #         for i in range(counter):
    #             cur_inst = instruction._pick_an_unissued_inst(pre_unroller_obj.pre_unroll_inst_set,zero_map,i)
    #             if(instruction._check(self.temp_inst,cur_inst)):
    #                 self.temp_clock += 1
    #                 print("push:")
    #                 cur_inst._print()
    #                 self.temp_inst.append(cur_inst)
    #                 bit_map[zero_map[i]] = True
    #                 print("cur_bit_map:",bit_map)
    #                 self.last_index = zero_map[i]
    #                 self._unroll(pre_unroller_obj,zero_map)
    #             else:
    #                 if(i == counter - 1):
    #                     success = False
    #                 continue

    #     else:
    #         if(bit_map == [1]* len(bit_map)):
    #             if(self.temp_clock < self.total_clock):
    #                 self.best_choice = self.temp_inst
    #                 self.total_clock = self.temp_clock
    #                 print("current total clock:",self.total_clock)
    #                 return
    #         else:
    #             zero_map,counter = count_NOT_zero(bit_map)
    #             success = True
    #             for i in range(counter):
    #                 cur_inst = instruction._pick_an_unissued_inst(pre_unroller_obj.pre_unroll_inst_set,zero_map,i)
    #                 print("the choice we have:",counter)
    #                 if(instruction._check(self.temp_inst,cur_inst)):
    #                     self.temp_clock += 1
    #                     print("pushll:",i)
    #                     cur_inst._print()
    #                     self.temp_inst.append(cur_inst)
    #                     bit_map[zero_map[i]] = True
    #                     print("cur_bit_map:",bit_map)
    #                     self.last_index = zero_map[i]
    #                     self._unroll(pre_unroller_obj,zero_map)
    #                     break
    #                 else:
    #                     if(i == counter - 1):
    #                         success = False
    #                     continue
    #                 break
    #             if(success == False):
    #                 self.temp_clock += 1
    #                 self.last_index = 128
    #                 self.temp_inst.append(instruction("stall","stall",None,None,None))
    #                 print("push stall inst")
    #                 self._unroll(pre_unroller_obj,bit_map)