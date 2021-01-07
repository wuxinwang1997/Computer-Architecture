import re

class inst:
    def __init__(self,op,rd,rs1,rs2,imm=0,RS=None):
        self.op = op
        self.rd = rd
        self.rs1 = rs1
        self.rs2 = rs2
        self.imm = imm
        self.reservation_station = RS
        self.status = "UN_ISSUED"
        self.Issue_clock = 0
        self.Execute_clock = 0
        self.WB_clock = 0

    def _get_op(self):
        return self.op
    def _get_rd(self):
        return self.rd
    def _get_rs1(self):
        return self.rs1
    def _get_rs2(self):
        return self.rs2
    def _get_imm(self):
        return self.imm
    def _get_inst_status(self):
        return self.status
    def _get_issue_clock(self):
        return self.Issue_clock
    def _get_exe_clock(self):
        return self.Execute_clock
    def _get_wb_clock(self):
        return self.WB_clock

    def _set_status(self,status,clock):
        self.status = status
        if(status == "Issue"):
            self.Issue_clock = clock
        elif(status == "Execute"):
            self.Execute_clock = clock
        elif(status == "WB"):
            self.WB_clock = clock
        else:
            print("error:the wrong status occurred!",status)

    def _print(self):
        print("op: ",self.op," ,rd: ",self.rd," imm:",self.imm," ,status: ",self.status," ,issued at: ",self.Issue_clock,\
              " ,ex at: ",self.Execute_clock," ,WB at: ",self.WB_clock)


class reservation_station:
    def __init__(self,name):
        self.name = name
        self.busy = False
        self.op = None
        self.Vj = " "
        self.Vk = " "
        self.Qj = "None"
        self.Qk = "None"
        self.Addr = 0
        self.ALC = 1
        self.index = 0

    def _get_unit_name(self):
        return self.name
    def _get_status(self):
        return bool(self.busy)
    def _get_op(self):
        return self.op
    def _get_Vj(self):
        return self.Vj
    def _get_Vk(self):
        return self.Vk
    def _get_Qj(self):
        return self.Qj
    def _get_Qk(self):
        return self.Qk
    def _get_addr(self):
        return int(self.Addr)
    def _get_ALC(self):
        return int(self.ALC)
    def _get_index(self):
        return int(self.index)

    def _set_status(self,flag):
        self.busy = flag
    def _set_op(self,op):
        self.op = op
    def _set_Vj(self,reg):
        self.Vj = reg
    def _set_Vk(self,reg):
        self.Vk = reg
    def _set_Qj(self,fun_unit):
        self.Qj = fun_unit
    def _set_Qk(self,fun_unit):
        self.Qk = fun_unit
    def _set_addr(self,addr):
        self.Addr = addr
    def _set_ALC(self,clock):
        self.ALC = clock
    def _ALC_DEC(self):
        self.ALC -= 1
    def _set_index(self,index):
        self.index = index
    def _reset(self):
        # self.time = 0
        # self.name = " "
        self.busy = False
        self.op = "  "
        self.Vj = "  "
        self.Vk = "  "
        self.Qj = "None"
        self.Qk = "None"
        self.Addr = 0
        self.ALC = 1  # additional local controler
        self.index = 0

    def _set(self,inst):
        pass
    def _print(self):
        print("ALC:",self.ALC," RS ",self.name,": ",self.busy,"op:",self.op," Vj:",self.Vj," Vk:",self.Vk," Qj:",self.Qj," Qk:",self.Qk)

class register_result_status:
    def __init__(self):
        self.F0 = "Invalid"
        self.F1 = "Invalid"
        self.F2 = "Invalid"
        self.F3 = "Invalid"
        self.F4 = "Invalid"
        self.F5 = "Invalid"
        self.F6 = "Invalid"
        self.F7 = "Invalid"
        self.F8 = "Invalid"
        self.F9 = "Invalid"
        self.F10 = "Invalid"
        self.F11 = "Invalid"
        self.F12 = "Invalid"
        self.F13 = "Invalid"
        self.F14 = "Invalid"
        self.F15 = "Invalid"

    def _get_all_registers(self):
        result = []
        if (self.F0 == "Invalid"):
            result.append(" ")
        else:
            result.append((self.F0))
        if (self.F1 == "Invalid"):
            result.append(" ")
        else:
            result.append((self.F1))
        if (self.F2 == "Invalid"):
            result.append(" ")
        else:
            result.append((self.F2))
        if (self.F3 == "Invalid"):
            result.append(" ")
        else:
            result.append((self.F3))
        if (self.F4 == "Invalid"):
            result.append(" ")
        else:
            result.append((self.F4))
        if (self.F5 == "Invalid"):
            result.append(" ")
        else:
            result.append((self.F5))
        if (self.F6 == "Invalid"):
            result.append(" ")
        else:
            result.append((self.F6))
        if (self.F7 == "Invalid"):
            result.append(" ")
        else:
            result.append((self.F7))
        if (self.F8 == "Invalid"):
            result.append(" ")
        else:
            result.append((self.F8))
        if (self.F9 == "Invalid"):
            result.append(" ")
        else:
            result.append((self.F9))
        if (self.F10 == "Invalid"):
            result.append(" ")
        else:
            result.append((self.F10))
        if (self.F11 == "Invalid"):
            result.append(" ")
        else:
            result.append((self.F11))
        if (self.F12 == "Invalid"):
            result.append(" ")
        else:
            result.append((self.F12))
        if (self.F13 == "Invalid"):
            result.append(" ")
        else:
            result.append((self.F13))
        if (self.F14 == "Invalid"):
            result.append(" ")
        else:
            result.append((self.F14))
        if (self.F14 == "Invalid"):
            result.append(" ")
        else:
            result.append((self.F14))
        return result
    
    def _get_function_unit(self,source_reg):
        if(source_reg == "F0"):
            return self.F0
        elif(source_reg == "F1"):
            return self.F1
        elif(source_reg == "F2"):
            return self.F2
        elif(source_reg == "F3"):
            return self.F3
        elif(source_reg == "F4"):
            return self.F4
        elif(source_reg == "F5"):
            return self.F5
        elif(source_reg == "F6"):
            return self.F6
        elif(source_reg == "F7"):
            return self.F7
        elif(source_reg == "F8"):
            return self.F8
        elif(source_reg == "F9"):
            return self.F9
        elif(source_reg == "F10"):
            return self.F10
        elif(source_reg == "F11"):
            return self.F11
        elif(source_reg == "F12"):
            return self.F12
        elif(source_reg == "F13"):
            return self.F13
        elif(source_reg == "F14"):
            return self.F14
        elif(source_reg == "F15"):
            return self.F15
        else:
            print("")
        
        
    def _set_function_unit(self,reg,function_unit):
        if(reg == "F0"):
            self.F0 = function_unit
        elif(reg == "F1"):
            self.F1 = function_unit
        elif(reg == "F2"):
            self.F2 = function_unit
        elif(reg == "F3"):
            self.F3 = function_unit
        elif(reg == "F4"):
            self.F4 = function_unit
        elif(reg == "F5"):
            self.F5 = function_unit
        elif(reg == "F6"):
            self.F6 = function_unit
        elif(reg == "F7"):
            self.F7 = function_unit
        elif(reg == "F8"):
            self.F8 = function_unit
        elif(reg == "F9"):
            self.F9 = function_unit
        elif(reg == "F10"):
            self.F10 = function_unit
        elif(reg == "F11"):
            self.F11 = function_unit
        elif(reg == "F12"):
            self.F12 = function_unit
        elif(reg == "F13"):
            self.F13 = function_unit
        elif(reg == "F14"):
            self.F14 = function_unit
        elif(reg == "F15"):
            self.F15 = function_unit
        else:
            print("error:the register is not defined!")
    def _reset_function_unit(self,fun_unit):
        if(self.F0 == fun_unit):
            self.F0 = "Invalid"
        if(self.F1 == fun_unit):
            self.F1 = "Invalid"
        if(self.F2 == fun_unit):
            self.F2 = "Invalid"
        if(self.F3 == fun_unit):
            self.F3 = "Invalid"
        if(self.F4 == fun_unit):
            self.F4 = "Invalid"
        if(self.F5 == fun_unit):
            self.F5 = "Invalid"
        if(self.F6 == fun_unit):
            self.F6 = "Invalid"
        if(self.F7 == fun_unit):
            self.F7 = "Invalid"
        if(self.F8 == fun_unit):
            self.F8 = "Invalid"
        if(self.F9 == fun_unit):
            self.F9 = "Invalid"
        if(self.F10 == fun_unit):
            self.F10 = "Invalid"
        if(self.F11 == fun_unit):
            self.F11 = "Invalid"
        if(self.F12 == fun_unit):
            self.F12 = "Invalid"
        if(self.F13 == fun_unit):
            self.F13 = "Invalid"
        if(self.F14 == fun_unit):
            self.F14 = "Invalid"
        if(self.F15 == fun_unit):
            self.F15 = "Invalid"

    def _print(self):
        if(self.F0 != "Invalid"):
            print("F0:",self.F0)
        if (self.F1 != "Invalid"):
            print("F1:", self.F1)
        if (self.F2 != "Invalid"):
            print("F2:", self.F2)
        if (self.F3 != "Invalid"):
            print("F3:", self.F3)
        if (self.F4 != "Invalid"):
            print("F4:", self.F4)
        if (self.F5 != "Invalid"):
            print("F5:", self.F5)
        if (self.F6 != "Invalid"):
            print("F6:", self.F6)
        if (self.F7 != "Invalid"):
            print("F7:", self.F7)
        if (self.F8 != "Invalid"):
            print("F8:", self.F8)
        if (self.F9 != "Invalid"):
            print("F9:", self.F9)
        if (self.F10 != "Invalid"):
            print("F10:", self.F10)
        if (self.F11 != "Invalid"):
            print("F11:", self.F11)
        if (self.F12 != "Invalid"):
            print("F12:", self.F12)
        if (self.F13 != "Invalid"):
            print("F13:", self.F13)
        if (self.F14 != "Invalid"):
            print("F14:", self.F14)
        if (self.F15 != "Invalid"):
            print("F15:", self.F15)

class tomasulo:
    def __init__(self):
        self.clock = 0

        self.show_ptr = 0
        self.queue_ptr = 0
        self.all_inst_queue = []

        self.finish_tag = False

        self.RS_load1 = reservation_station("Load1")
        self.RS_load2 = reservation_station("Load2")
        self.RS_load3 = reservation_station("Load3")
        self.RS_Add1 = reservation_station("Add1")
        self.RS_Add2 = reservation_station("Add2")
        self.RS_Add3 = reservation_station("Add3")

        self.RS_Mult1 = reservation_station("Mult1")
        self.RS_Mult2 = reservation_station("Mult2")

        self.RS_Store1 = reservation_station("Store1")
        self.RS_Store2 = reservation_station("Store2")
        self.RS_Store3 = reservation_station("Store3")

        self.result_register_status = register_result_status()

        self.all_exec_state = []

    def _run(self):
        while(self.finish_tag == False):
            self._issue()
            self._exex()
            self._write()
            self._set_finish_tag()

            # self.all_exec_state.append()
            self._print()
            self._snap_shot()
            if(self.clock >= 60):
                break


    def _issue(self):
        self.clock += 1
        if(self.queue_ptr >= len(self.all_inst_queue)):
            return
        if(len(self.all_inst_queue) == 0):
            print("error,no instruction initialized in the queue.")
            return 
        temp_inst = self.all_inst_queue[self.queue_ptr]
        issue_tag,rs = self._structure_hazard_check(temp_inst)
        if(issue_tag == False):
            print("structure hazard detected")
            return
        elif(issue_tag == True):
            if(rs == None):
                print("this clock is for scalar:",temp_inst._get_op())
                self.all_inst_queue[self.queue_ptr]._set_status("Issue",self.clock)
                self.all_inst_queue[self.queue_ptr]._set_status("Execute", self.clock)
                self.all_inst_queue[self.queue_ptr]._set_status("WB", self.clock)
                self.queue_ptr += 1
                return
            else:
                rs._reset()
                self.all_inst_queue[self.queue_ptr]._set_status("Issue",self.clock)
                rs._set_index(self.queue_ptr)
                self._set_reservation_station(rs,temp_inst)
                self.queue_ptr += 1
            
    def _set_reservation_station(self,rs,inst):
        rs._set_status(True)
        rs._set_op(inst._get_op())
        if(inst._get_op() == "L.D"):
            rs._set_addr(inst._get_imm())
            self.result_register_status._set_function_unit(inst._get_rd(),rs._get_unit_name())
            rs._set_ALC(100)

        elif(inst._get_op() == "S.D"):
            # rs._set_ALC(100)
            rs._set_addr(inst._get_imm())
            if(self.result_register_status._get_function_unit(inst._get_rs2()) == "Invalid"):
                rs._set_Vk(inst._get_rs2())
            else:
                rs._set_Qk(self.result_register_status._get_function_unit(inst._get_rs2()))
        elif(inst._get_op() == "MUL.D"):
            rs._set_ALC(10)
            self.result_register_status._set_function_unit(inst._get_rd(),rs._get_unit_name())
            if(self.result_register_status._get_function_unit(inst._get_rs1()) == "Invalid"):
                rs._set_Vj(inst._get_rs1())
            else:
                rs._set_Qj(self.result_register_status._get_function_unit(inst._get_rs1()))
            
            if(self.result_register_status._get_function_unit(inst._get_rs2()) == "Invalid"):
                rs._set_Vk(inst._get_rs2())
            else:
                rs._set_Qk(self.result_register_status._get_function_unit(inst._get_rs2()))
        elif (inst._get_op() == "DIV.D"):
            rs._set_ALC(40)
            self.result_register_status._set_function_unit(inst._get_rd(), rs._get_unit_name())
            if (self.result_register_status._get_function_unit(inst._get_rs1()) == "Invalid"):
                rs._set_Vj(inst._get_rs1())
            else:
                rs._set_Qj(self.result_register_status._get_function_unit(inst._get_rs1()))

            if (self.result_register_status._get_function_unit(inst._get_rs2()) == "Invalid"):
                rs._set_Vk(inst._get_rs2())
            else:
                rs._set_Qk(self.result_register_status._get_function_unit(inst._get_rs2()))
        elif (inst._get_op() == "ADD.D" or inst._get_op() == "SUB.D"):
            rs._set_ALC(2)
            self.result_register_status._set_function_unit(inst._get_rd(), rs._get_unit_name())
            if (self.result_register_status._get_function_unit(inst._get_rs1()) == "Invalid"):
                rs._set_Vj(inst._get_rs1())
            else:
                rs._set_Qj(self.result_register_status._get_function_unit(inst._get_rs1()))

            if (self.result_register_status._get_function_unit(inst._get_rs2()) == "Invalid"):
                rs._set_Vk(inst._get_rs2())
            else:
                rs._set_Qk(self.result_register_status._get_function_unit(inst._get_rs2()))
        else:
            print("this clock the reservation stations are not changed!")
        

    def _structure_hazard_check(self,temp_inst):
        if(temp_inst._get_op() == "L.D"):
            if(self.RS_load1._get_status() == True and self.RS_load2._get_status() == True \
                and self.RS_load3._get_status() == True):
                return False,None
            else:
                if(self.RS_load1._get_status() == False):
                    return True,self.RS_load1
                elif(self.RS_load2._get_status() == False):
                    return True,self.RS_load2
                else:
                    return True,self.RS_load3
        elif(temp_inst._get_op() == "MUL.D" or temp_inst._get_op() == "DIV.D"):
            if(self.RS_Mult1._get_status() == True and self.RS_Mult2._get_status() == True):
                return False,None
            else:
                if(self.RS_Mult1._get_status() == False):
                    return True,self.RS_Mult1
                else:
                    return True,self.RS_Mult2
        elif(temp_inst._get_op() == "S.D"):
            if(self.RS_Store1._get_status() == True and self.RS_Store2._get_status() == True \
                and self.RS_Store3._get_status() == True):
                return False,None
            else:
                if(self.RS_Store1._get_status() == False):
                    return True,self.RS_Store1
                elif(self.RS_Store2._get_status() == False):
                    return True,self.RS_Store2
                else:
                    return True,self.RS_Store3
        elif(temp_inst._get_op() == "SUB.D" or temp_inst._get_op() == "ADD.D"):
            if(self.RS_Add1._get_status() == True and self.RS_Add2._get_status() == True \
                and self.RS_Add3._get_status() == True):
                return False,None
            else:
                if(self.RS_Add1._get_status() == False):
                    return True,self.RS_Add1
                elif(self.RS_Add2._get_status() == False):
                    return True,self.RS_Add2
                else:
                    return True,self.RS_Add3
        elif(temp_inst._get_op() == "DADDUI" or temp_inst._get_op() == "BNE"):
            return True,None
        else:
            print("error,this instruction is not defined!")    

            

    def _exex(self):
        if(self.RS_Add1._get_status() == True):
            if(self.RS_Add1._get_Qj() == "None" and self.RS_Add1._get_Qk() == "None"):

                self.RS_Add1._ALC_DEC()
                if(self.RS_Add1._get_ALC() == 0):
                    index = self.RS_Add1._get_index()
                    self.all_inst_queue[index]._set_status("Execute",self.clock)
        if(self.RS_Add2._get_status() == True):
            if(self.RS_Add2._get_Qj() == "None" and self.RS_Add2._get_Qk() == "None"):
                self.RS_Add2._ALC_DEC()
                if(self.RS_Add2._get_ALC() == 0):
                    index = self.RS_Add2._get_index()
                    self.all_inst_queue[index]._set_status("Execute",self.clock)
        if(self.RS_Add3._get_status() == True):
            if(self.RS_Add3._get_Qj() == "None" and self.RS_Add3._get_Qk() == "None"):
                self.RS_Add3._ALC_DEC()
                if(self.RS_Add3._get_ALC() == 0):
                    index = self.RS_Add3._get_index()
                    self.all_inst_queue[index]._set_status("Execute",self.clock)
        if(self.RS_Mult1._get_status() == True):
            if(self.RS_Mult1._get_Qj() == "None" and self.RS_Mult1._get_Qk() == "None"):
                self.RS_Mult1._ALC_DEC()
                if(self.RS_Mult1._get_ALC() == 0):
                    index = self.RS_Mult1._get_index()
                    self.all_inst_queue[index]._set_status("Execute",self.clock)
        if(self.RS_Mult2._get_status() == True):
            if(self.RS_Mult2._get_Qj() == "None" and self.RS_Mult2._get_Qk() == "None"):
                self.RS_Mult2._ALC_DEC()
                if(self.RS_Mult2._get_ALC() == 0):
                    index = self.RS_Mult2._get_index()
                    self.all_inst_queue[index]._set_status("Execute",self.clock)

        if(self.RS_load1._get_status() == True):
            if (self.RS_load1._get_ALC() == 100):
                self.RS_load1._set_ALC(2)
            else:
                self.RS_load1._ALC_DEC()
                if(self.RS_load1._get_ALC() == 0):
                    index = self.RS_load1._get_index()
                    self.all_inst_queue[index]._set_status("Execute",self.clock)
        if(self.RS_load2._get_status() == True):
            if (self.RS_load2._get_ALC() == 100):
                self.RS_load2._set_ALC(2)
            else:
                self.RS_load2._ALC_DEC()
                if(self.RS_load2._get_ALC() == 0):
                    index = self.RS_load2._get_index()
                    self.all_inst_queue[index]._set_status("Execute",self.clock)
        if(self.RS_load3._get_status() == True):
            if (self.RS_load3._get_ALC() == 100):
                self.RS_loadd3._set_ALC(2)
            else:
                self.RS_load3._ALC_DEC()
                if(self.RS_load3._get_ALC() == 0):
                    index = self.RS_load3._get_index()
                    self.all_inst_queue[index]._set_status("Execute",self.clock)

        if(self.RS_Store1._get_status() == True):
            if(self.RS_Store1._get_Qk() == "None"):
                if(self.RS_Store1._get_ALC() == 100):
                    self.RS_Store1._set_ALC(2)
                else:
                    self.RS_Store1._ALC_DEC()
                    if(self.RS_Store1._get_ALC() == 0):
                        index = self.RS_Store1._get_index()
                        self.all_inst_queue[index]._set_status("Execute",self.clock)
        if(self.RS_Store2._get_status() == True):
            if(self.RS_Store2._get_Qk() == "None"):
                if(self.RS_Store2._get_ALC() == 100):
                    self.RS_Store2._set_ALC(2)
                else:
                    self.RS_Store2._ALC_DEC()
                    if(self.RS_Store2._get_ALC() == 0):
                        index = self.RS_Store2._get_index()
                        self.all_inst_queue[index]._set_status("Execute",self.clock)
        if (self.RS_Store3._get_status() == True):
            if (self.RS_Store3._get_Qk() == "None"):
                if (self.RS_Store3._get_ALC() == 100):
                    self.RS_Store3._set_ALC(2)
                else:
                    self.RS_Store3._ALC_DEC()
                    if (self.RS_Store3._get_ALC() == 0):
                        index = self.RS_Store3._get_index()
                        self.all_inst_queue[index]._set_status("Execute", self.clock)

    def _write(self):
        if(self.RS_load1._get_status() == True):
            if(self.RS_load1._get_ALC() == 0):
                self.RS_load1._set_ALC(1000)
            if(self.RS_load1._get_ALC() == 999):
                index = self.RS_load1._get_index()
                self.all_inst_queue[index]._set_status("WB",self.clock)
                self.result_register_status._reset_function_unit("Load1")
                self._RAW_and_WAW("Load1",self.all_inst_queue[index]._get_imm())
                self.RS_load1._reset()
        if(self.RS_load2._get_status() == True):
            if(self.RS_load2._get_ALC() == 0):
                self.RS_load2._set_ALC(1000)
            if(self.RS_load2._get_ALC() == 999):
                index = self.RS_load2._get_index()
                self.all_inst_queue[index]._set_status("WB",self.clock)
                self.result_register_status._reset_function_unit("Load2")
                self._RAW_and_WAW("Load2",self.all_inst_queue[index]._get_imm())
                self.RS_load2._reset()
        if(self.RS_load3._get_status() == True):
            if(self.RS_load3._get_ALC() == 0):
                self.RS_load3._set_ALC(1000)
            if(self.RS_load3._get_ALC() == 999):
                index = self.RS_load3._get_index()
                self.all_inst_queue[index]._set_status("WB",self.clock)
                self.result_register_status._reset_function_unit("Load3")
                self._RAW_and_WAW("Load3",self.all_inst_queue[index]._get_imm())
                self.RS_load3._reset()

        if(self.RS_Store1._get_status() == True):
            if(self.RS_Store1._get_Qk() == "None"):
                if(self.RS_Store1._get_ALC() == 0):
                    self.RS_Store1._set_ALC(1000)
                if(self.RS_Store1._get_ALC() == 999):
                    index = self.RS_Store1._get_index()
                    self.all_inst_queue[index]._set_status("WB",self.clock)
                # self.result_register_status._reset_function_unit("Store1")
                # self._RAW_and_WAW("Store1",self.all_inst_queue[index]._get_imm())
                    self.RS_Store1._reset()
        if(self.RS_Store2._get_status() == True):
            if(self.RS_Store2._get_Qk() == "None"):
                if (self.RS_Store2._get_ALC() == 0):
                    self.RS_Store2._set_ALC(1000)
                if (self.RS_Store2._get_ALC() == 999):
                    index = self.RS_Store2._get_index()
                    self.all_inst_queue[index]._set_status("WB",self.clock)
                # self.result_register_status._reset_function_unit("Store2")
                # self._RAW_and_WAW("Store2",self.all_inst_queue[index]._get_imm())
                    self.RS_Store2._reset()
        if(self.RS_Store3._get_status() == True):
            if(self.RS_Store3._get_Qk() == "None"):
                if (self.RS_Store3._get_ALC() == 0):
                    self.RS_Store3._set_ALC(1000)
                if (self.RS_Store3._get_ALC() == 999):
                    index = self.RS_Store3._get_index()
                    self.all_inst_queue[index]._set_status("WB",self.clock)
                # self.result_register_status._reset_function_unit("Store3")
                # self._RAW_and_WAW("Store3",self.all_inst_queue[index]._get_imm())
                    self.RS_Store3._reset()

        if(self.RS_Mult1._get_status() == True):
            if(self.RS_Mult1._get_ALC() == 0):
                self.RS_Mult1._set_ALC(1000)
            if(self.RS_Mult1._get_ALC() == 999):
                index = self.RS_Mult1._get_index()
                self.all_inst_queue[index]._set_status("WB",self.clock)
                self.result_register_status._reset_function_unit("Mult1")
                self._RAW_and_WAW("Mult1","the mul value")
                self.RS_Mult1._reset()
        if(self.RS_Mult2._get_status() == True):
            if(self.RS_Mult2._get_ALC() == 0):
                self.RS_Mult2._set_ALC(1000)
            if(self.RS_Mult2._get_ALC() == 999):
                index = self.RS_Mult2._get_index()
                self.all_inst_queue[index]._set_status("WB",self.clock)
                self.result_register_status._reset_function_unit("Mult2")
                self._RAW_and_WAW("Mult2","mul value")
                self.RS_Mult2._reset()

        if(self.RS_Add1._get_status() == True):
            if(self.RS_Add1._get_ALC() == 0):
                self.RS_Add1._set_ALC(1000)
            if(self.RS_Add1._get_ALC() == 999):
                index = self.RS_Add1._get_index()
                self.all_inst_queue[index]._set_status("WB",self.clock)
                self.result_register_status._reset_function_unit("Add1")
                self._RAW_and_WAW("Add1","add value")
                self.RS_Add1._reset()
        if(self.RS_Add2._get_status() == True):
            if(self.RS_Add2._get_ALC() == 0):
                self.RS_Add2._set_ALC(1000)
            if(self.RS_Add2._get_ALC() == 999):
                index = self.RS_Add2._get_index()
                self.all_inst_queue[index]._set_status("WB",self.clock)
                self.result_register_status._reset_function_unit("Add2")
                self._RAW_and_WAW("Add2","add value")
                self.RS_Add2._reset()
        if(self.RS_Add3._get_status() == True):
            if(self.RS_Add3._get_ALC() == 0):
                self.RS_Add3._set_ALC(1000)
            if(self.RS_Add3._get_ALC() == 999):
                index = self.RS_Add3._get_index()
                self.all_inst_queue[index]._set_status("WB",self.clock)
                self.result_register_status._reset_function_unit("Add3")
                self._RAW_and_WAW("Add3","add value")
                self.RS_Add3._reset()
                    
    def _RAW_and_WAW(self,fun_unit_name,value):
        if(self.RS_Add1._get_Qj() == fun_unit_name):
            self.RS_Add1._set_Qj("None")
            self.RS_Add1._set_Vj(value)
        if(self.RS_Add1._get_Qk() == fun_unit_name):
            self.RS_Add1._set_Qk("None")
            self.RS_Add1._set_Vk(value)
        if(self.RS_Add2._get_Qj() == fun_unit_name):
            self.RS_Add2._set_Qj("None")
            self.RS_Add2._set_Vj(value)
        if(self.RS_Add2._get_Qk() == fun_unit_name):
            self.RS_Add2._set_Qk("None")
            self.RS_Add2._set_Vk(value)
        if(self.RS_Add3._get_Qj() == fun_unit_name):
            self.RS_Add3._set_Qj("None")
            self.RS_Add3._set_Vj(value)
        if(self.RS_Add3._get_Qk() == fun_unit_name):
            self.RS_Add3._set_Qk("None")
            self.RS_Add3._set_Vk(value)

        if(self.RS_Mult1._get_Qj() == fun_unit_name):
            self.RS_Mult1._set_Qj("None")
            self.RS_Mult1._set_Vj(value)
        if(self.RS_Mult1._get_Qk() == fun_unit_name):
            self.RS_Mult1._set_Qk("None")
            self.RS_Mult1._set_Vk(value)
        if(self.RS_Mult2._get_Qj() == fun_unit_name):
            self.RS_Mult2._set_Qj("None")
            self.RS_Mult2._set_Vj(value)
        if(self.RS_Mult2._get_Qk() == fun_unit_name):
            self.RS_Mult2._set_Qk("None")
            self.RS_Mult2._set_Vk(value)

        if(self.RS_Store1._get_Qk() == fun_unit_name):
            self.RS_Store1._set_Qk("None")
            self.RS_Store1._set_Vk(value)
        if(self.RS_Store2._get_Qk() == fun_unit_name):
            self.RS_Store2._set_Qk("None")
            self.RS_Store2._set_Vk(value)    

    def _set_finish_tag(self):
        for i in range(len(self.all_inst_queue)):
            if (self.all_inst_queue[i]._get_inst_status() != "WB"):
                self.finish_tag = False
                return
        self.finish_tag = True

    def _print(self):
        print("---------------------------------------------------")
        print("current clock:",self.clock)
        for i in range(len(self.all_inst_queue)):
            self.all_inst_queue[i]._print()
        print("------------reserved stations---------")
        self.RS_Add1._print()
        self.RS_Add2._print()
        self.RS_Add3._print()
        self.RS_load1._print()
        self.RS_load2._print()
        self.RS_load3._print()
        self.RS_Mult1._print()
        self.RS_Mult2._print()
        self.RS_Store1._print()
        self.RS_Store2._print()
        self.RS_Store3._print()
        print("--------------register state------------")
        self.result_register_status._print()

    def _run_step(self):
        self._run()
        # showr = shower(self.all_exec_state)
        # showr.update_tree_view(0)




    def _snap_shot(self):
        inst_state = []
        for i in range(len(self.all_inst_queue)):
            state = []
            state.append(self.all_inst_queue[i]._get_op())
            state.append(self.all_inst_queue[i]._get_issue_clock())
            state.append(self.all_inst_queue[i]._get_exe_clock())
            state.append(self.all_inst_queue[i]._get_wb_clock())
            inst_state.append(state)

        register_state = self.result_register_status._get_all_registers()

        RS_state = []
        state = []
        state.append(self.RS_Add1._get_ALC())
        state.append("RS_Add1")
        state.append(self.RS_Add1._get_status())
        state.append(self.RS_Add1._get_op())
        state.append(self.RS_Add1._get_Vj())
        state.append(self.RS_Add1._get_Vk())
        state.append(self.RS_Add1._get_Qj())
        state.append(self.RS_Add1._get_Qk())
        RS_state.append(state)

        state = []
        state.append(self.RS_Add2._get_ALC())
        state.append("RS_Add2")
        state.append(self.RS_Add2._get_status())
        state.append(self.RS_Add2._get_op())
        state.append(self.RS_Add2._get_Vj())
        state.append(self.RS_Add2._get_Vk())
        state.append(self.RS_Add2._get_Qj())
        state.append(self.RS_Add2._get_Qk())
        RS_state.append(state)

        state = []
        state.append(self.RS_Add3._get_ALC())
        state.append("RS_Add3")
        state.append(self.RS_Add3._get_status())
        state.append(self.RS_Add3._get_op())
        state.append(self.RS_Add3._get_Vj())
        state.append(self.RS_Add3._get_Vk())
        state.append(self.RS_Add3._get_Qj())
        state.append(self.RS_Add3._get_Qk())
        RS_state.append(state)

        state = []
        state.append(self.RS_load1._get_ALC())
        state.append("RS_Load1")
        state.append(self.RS_load1._get_status())
        state.append(self.RS_load1._get_op())
        state.append(self.RS_load1._get_Vj())
        state.append(self.RS_load1._get_Vk())
        state.append(self.RS_load1._get_Qj())
        state.append(self.RS_load1._get_Qk())
        RS_state.append(state)

        state = []
        state.append(self.RS_load2._get_ALC())
        state.append("RS_Load2")
        state.append(self.RS_load2._get_status())
        state.append(self.RS_load2._get_op())
        state.append(self.RS_load2._get_Vj())
        state.append(self.RS_load2._get_Vk())
        state.append(self.RS_load2._get_Qj())
        state.append(self.RS_load2._get_Qk())
        RS_state.append(state)

        state = []
        state.append(self.RS_load3._get_ALC())
        state.append("RS_Load3")
        state.append(self.RS_load3._get_status())
        state.append(self.RS_load3._get_op())
        state.append(self.RS_load3._get_Vj())
        state.append(self.RS_load3._get_Vk())
        state.append(self.RS_load3._get_Qj())
        state.append(self.RS_load3._get_Qk())
        RS_state.append(state)

        state = []
        state.append(self.RS_Mult1._get_ALC())
        state.append("RS_Mult1")
        state.append(self.RS_Mult1._get_status())
        state.append(self.RS_Mult1._get_op())
        state.append(self.RS_Mult1._get_Vj())
        state.append(self.RS_Mult1._get_Vk())
        state.append(self.RS_Mult1._get_Qj())
        state.append(self.RS_Mult1._get_Qk())
        RS_state.append(state)

        state = []
        state.append(self.RS_Mult2._get_ALC())
        state.append("RS_Mult2")
        state.append(self.RS_Mult2._get_status())
        state.append(self.RS_Mult2._get_op())
        state.append(self.RS_Mult2._get_Vj())
        state.append(self.RS_Mult2._get_Vk())
        state.append(self.RS_Mult2._get_Qj())
        state.append(self.RS_Mult2._get_Qk())
        RS_state.append(state)
        state = []
        state.append(self.RS_Store1._get_ALC())
        state.append("RS_Store1")
        state.append(self.RS_Store1._get_status())
        state.append(self.RS_Store1._get_op())
        state.append(self.RS_Store1._get_Vj())
        state.append(self.RS_Store1._get_Vk())
        state.append(self.RS_Store1._get_Qj())
        state.append(self.RS_Store1._get_Qk())
        RS_state.append(state)
        state = []
        state.append(self.RS_Store2._get_ALC())
        state.append("RS_Store2")
        state.append(self.RS_Store2._get_status())
        state.append(self.RS_Store2._get_op())
        state.append(self.RS_Store2._get_Vj())
        state.append(self.RS_Store2._get_Vk())
        state.append(self.RS_Store2._get_Qj())
        state.append(self.RS_Store2._get_Qk())
        RS_state.append(state)
        state = []
        state.append(self.RS_Store3._get_ALC())
        state.append("RS_Store3")
        state.append(self.RS_Store3._get_status())
        state.append(self.RS_Store3._get_op())
        state.append(self.RS_Store3._get_Vj())
        state.append(self.RS_Store3._get_Vk())
        state.append(self.RS_Store3._get_Qj())
        state.append(self.RS_Store3._get_Qk())
        RS_state.append(state)

        temp = []
        temp.append(inst_state)
        temp.append(RS_state)
        temp.append(register_state)
        self.all_exec_state.append(temp)




    def _read_insts(self,filename):
        inst_list = []
        fileobj = open(filename,"r")
        for line in fileobj:
            temp_inst = None
            segs = line.strip().split(' ')
            # print(segs)
            op = segs[0]
            if(re.match(op,"L.D")):
                regs = segs[1]
                regs = regs.strip().split(',')
                rd = regs[0]
                rss = regs[1].split('(')
                imm = rss[0]
                rs2 = rss[1].split(')')[0]
                temp_inst = inst(op,rd,None,rs2,imm,RS="Load")
            elif(re.match(op,"MUL.D")):
                regs = segs[1].strip().split(',')
                rd = regs[0]
                rs1 = regs[1]
                rs2 = regs[2]
                temp_inst = inst(op,rd,rs1,rs2,RS="Mult")
            elif(re.match(op,"DIV.D")):
                regs = segs[1].strip().split(',')
                rd = regs[0]
                rs1 = regs[1]
                rs2 = regs[2]
                temp_inst = inst(op,rd,rs1,rs2,RS="Mult")
            elif (re.match(op, "ADD.D")):
                regs = segs[1].strip().split(',')
                rd = regs[0]
                rs1 = regs[1]
                rs2 = regs[2]
                temp_inst = inst(op, rd, rs1, rs2, RS="Add")
            elif (re.match(op, "SUB.D")):
                regs = segs[1].strip().split(',')
                rd = regs[0]
                rs1 = regs[1]
                rs2 = regs[2]
                temp_inst = inst(op, rd, rs1, rs2, RS="Add")
            elif(re.match(op,"S.D")):
                regs = segs[1]
                regs = regs.strip().split(',')
                rs2 = regs[1]
                rss = regs[0].split('(')
                imm = rss[0]
                rs1 = rss[1].split(')')[0]
                rd = None
                temp_inst = inst(op,rd,rs1,rs2,imm,RS="Store")
            elif(re.match(op,"DADDUI")):
                regs = segs[1].strip().split(',')
                rd = regs[0]
                rs1 = regs[1]
                imm = regs[2][1:]
                temp_inst = inst(op,rd,rs1,None,imm=imm,RS="Stall")
            elif(re.match(op,"BNE")):
                regs = segs[1].strip().split(',')
                rd = regs[0]
                rs1 = regs[1]
                rs2 = regs[2]
                temp_inst = inst(op,rd,rs1,rs2,RS="Stall")
            else:
                print("error:Instructions unidentified!")
            inst_list.append(temp_inst)
        fileobj.close()
        return inst_list

    def _initial_inst_queue(self,filename):
        # inst_queue = self._read_insts("source1.S")
        inst_queue = self._read_insts(filename)
        self.all_inst_queue.clear()
        self.all_inst_queue = inst_queue


if __name__ == "__main__":
    tomasulo = tomasulo()
    tomasulo._initial_inst_queue("source.S")
    # tomasulo._initial_inst_queue("source1.S")



    # for i in range(len(tomasulo.all_inst_queue)):
    #     tomasulo.all_inst_queue[i]._print()
    tomasulo._run()
    # tomasulo._run()
    inst = tomasulo.all_exec_state

    import tkinter as tk
    from tkinter import ttk
    root = tk.Tk()
    root.title("tomasulo algorithm")
    root.geometry("500x300")
    # var = tk.StringVar(root)
    index = 0
    def forward():
        global index
        global inst
        print("enter")
        if(index > len(inst)):
            index =  len(inst)
        else:
            index += 1
            # var.set(index)
        x = treeview1.get_children()
        for item in x:
            treeview1.delete(item)
        x = treeview2.get_children()
        for item in x:
            treeview2.delete(item)
        x = treeview3.get_children()
        for item in x:
            treeview3.delete(item)

        for i in range(len(inst[index-1][0])):
            treeview1.insert('', i, values=inst[index-1][0][i])
        treeview1.update()
        for i in range(len(inst[index-1][1])):
            treeview2.insert('', i, values=inst[index-1][1][i])
        treeview2.update()
        treeview3.insert('', 0, values=inst[index-1][2])
        treeview3.update()
        var.set(str(index))
        print(index)
    def backward():
        global index
        if(index <= 0 ):
            index = 1
        else:
            index -= 1
            # var.set(index)
        x = treeview1.get_children()
        for item in x:
            treeview1.delete(item)
        x = treeview2.get_children()
        for item in x:
            treeview2.delete(item)
        x = treeview3.get_children()
        for item in x:
            treeview3.delete(item)

        for i in range(len(inst[index-1][0])):
            treeview1.insert('', i, values=inst[index-1][0][i])
        treeview1.update()
        for i in range(len(inst[index-1][1])):
            treeview2.insert('', i, values=inst[index-1][1][i])
        treeview2.update()
        treeview3.insert('', 0, values=inst[index-1][2])
        treeview3.update()
        var.set(str(index))
    button_forward = tk.Button(root, text="forward", width=20, command=forward)
    button_forward.pack()
    button_backward = tk.Button(root, text="backward", width=20, command=backward)
    button_backward.pack()

    fram1 = tk.Frame(root)
    fram1.pack()
    lb = tk.Label(fram1,text="current clock:")
    lb.pack()
    var = tk.StringVar()
    l = tk.Label(root, textvariable=var, fg='red', font=('Arial', 12), width=30, height=2)
    l.pack()


    frame = tk.Frame(root)
    frame.pack()
    columns = ("inst", "issue", "exe", "wb")
    treeview1 = ttk.Treeview(frame, show="headings", columns=columns)  # 表格
    treeview1.column("inst", width=150, anchor='center')  # 表示列,不显示
    treeview1.column("issue", width=100, anchor='center')
    treeview1.column("exe", width=100, anchor='center')
    treeview1.column("wb", width=150, anchor='center')

    treeview1.heading("inst", text=" instruction")
    treeview1.heading("issue", text="issue")
    treeview1.heading("exe", text="execute")
    treeview1.heading("wb", text="write result")
    treeview1.pack()
    treeview1.heading("inst", text=" instruction")


    for i in range(len(inst[index][0])):
        treeview1.insert('', i, values=inst[index][0][i])
    treeview1.update()
    colums1 = ("ALC","reserved station", "busy", "op", "Vj", "Vk", "Qj", "Qk")
    treeview2 = ttk.Treeview(frame, columns=colums1)
    treeview2.column("ALC", width=100,anchor="center")
    treeview2.column("reserved station", width=300, anchor="center")
    treeview2.column("busy", width=80, anchor='center')
    treeview2.column("op", width=80, anchor='center')
    treeview2.column("Vj", width=80, anchor='center')
    treeview2.column("Vk", width=80, anchor='center')
    treeview2.column("Qj", width=80, anchor='center')
    treeview2.column("Qk", width=80, anchor='center')
    treeview2.heading("ALC", text="ALC")
    treeview2.heading("reserved station", text="reserved station")
    treeview2.heading("busy", text=" busy")
    treeview2.heading("op", text="op")
    treeview2.heading("Vj", text="Vj")
    treeview2.heading("Vk", text="Vk")
    treeview2.heading("Qj", text="Qj")
    treeview2.heading("Qk", text="Qk")
    treeview2.pack()
    for i in range(len(inst[index][1])):
        treeview2.insert('', i, values=inst[index][1][i])
    treeview2.update()
    treeview3 = ttk.Treeview(root, columns=(
        "F0", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "F13", "F14", "F15"))
    treeview3.column("F0", width=80, anchor='center')
    treeview3.column("F1", width=80, anchor='center')
    treeview3.column("F2", width=80, anchor='center')
    treeview3.column("F3", width=80, anchor='center')
    treeview3.column("F4", width=80, anchor='center')
    treeview3.column("F5", width=80, anchor='center')
    treeview3.column("F6", width=80, anchor='center')
    treeview3.column("F7", width=80, anchor='center')
    treeview3.column("F8", width=80, anchor='center')
    treeview3.column("F9", width=80, anchor='center')
    treeview3.column("F10", width=80, anchor='center')
    treeview3.column("F11", width=80, anchor='center')
    treeview3.column("F12", width=80, anchor='center')
    treeview3.column("F13", width=80, anchor='center')
    treeview3.column("F14", width=80, anchor='center')
    treeview3.column("F15", width=80, anchor='center')
    treeview3.heading("F0", text="F0")
    treeview3.heading("F1", text="F1")
    treeview3.heading("F2", text="F2")
    treeview3.heading("F3", text="F3")
    treeview3.heading("F4", text="F4")
    treeview3.heading("F5", text="F5")
    treeview3.heading("F6", text="F6")
    treeview3.heading("F7", text="F7")
    treeview3.heading("F8", text="F8")
    treeview3.heading("F9", text="F9")
    treeview3.heading("F10", text="F10")
    treeview3.heading("F11", text="F11")
    treeview3.heading("F12", text="F12")
    treeview3.heading("F13", text="F13")
    treeview3.heading("F14", text="F14")
    treeview3.heading("F15", text="F15")
    treeview3.pack()
    treeview3.insert('', 0, values=inst[index][2])
    treeview3.update()
    root.mainloop()
