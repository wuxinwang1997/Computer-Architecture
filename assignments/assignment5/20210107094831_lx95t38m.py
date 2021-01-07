from prettytable import PrettyTable # used to print tables
class instruction_status:
    def __init__(self):
        self.issue=self.read_operands=self.execution_complete=self.write_result=False
        self.ins=instruction()
        self.fu=-1
        self.complete=False
        self.cando=False
    def check(self): # check which step the instruction is executing
        if self.write_result: return 4
        elif self.execution_complete: return 3
        elif self.read_operands: return 2
        elif self.issue: return 1
        else: return 0
    def change(self): #change the status of the instruction to the next step
        if self.execution_complete:
            self.write_result=True
            self.complete=True
        elif self.read_operands: self.execution_complete=True
        elif self.issue: self.read_operands=True
        else: self.issue=True
    def add(self,ins):
        self.ins=ins
class functional_unit_status:
    def __init__(self):
        self.busy=False
        self.op=""
        self.fi=self.fj=self.fk=-1
        self.qj=self.qk=-1
        self.rj=self.rk=False
        self.remain=0  # the ramaining cycles of the execution
class register_result_status:
    def __init__(self): # -1 stands for the current register is not being used
        self.f=[-1 for i in range(32)]
class instruction: # to change an instruction from a string to each part
    def __init__(self):
        self.fi=self.fj=self.fk=self.imm=0
        self.op=""
    def add(self,ins):
        i,j=ins.split()
        self.op=i
        if i=="L.D":
            k,l=j.split(',')
            self.fi=int(k[1])
            m,n=l.split('(')
            self.imm=int(m)
            self.fk=int(n[1])
        else:
            k,l,m=j.split(',')
            self.fi=int(k[1:])
            self.fj=int(l[1:])
            self.fk=int(m[1:])
ins_num=6   # total number of instrcutions
rrs=register_result_status()
fus=[]
for i in range(5):
    fus.append(functional_unit_status())
ist=[]
for i in range(10):
    ist.append(instruction_status())
dir = {0: "Integer", 1: "Mult1", 2: "Mult2", 3: "Add", 4: "Divide", 5:""}
def can_add_fun(ins):  # to judge whether an instruction can be issued
    fu=-1
    if ins.ins.op=="L.D":
        if fus[0].busy==False:
            fu=0
    elif ins.ins.op=="MUL.D":
        if fus[1].busy==False:
            fu=1
        elif fus[2].busy==False:
            fu=2
    elif ins.ins.op=="SUB.D" or ins.ins.op=="ADD.D":
        if fus[3].busy==False:
            fu=3
    elif ins.ins.op=="DIV.D":
        if fus[4].busy==False:
            fu=4
    if fu<0:
        return False
    else:
        return True
def add_fun(ins): # add the instrcution to the functional unit status
    fu=-1
    if ins.ins.op=="L.D":
        if fus[0].busy==False:
            fu=0
    elif ins.ins.op=="MUL.D":
        if fus[1].busy==False:
            fu=1
        elif fus[2].busy==False:
            fu=2
    elif ins.ins.op=="SUB.D" or ins.ins.op=="ADD.D":
        if fus[3].busy==False:
            fu=3
    elif ins.ins.op=="DIV.D":
        if fus[4].busy==False:
            fu=4
    if fu<0:
        return False
    else:
        fus[fu].busy=True
        fus[fu].op=ins.ins.op
        fus[fu].fi=ins.ins.fi
        fus[fu].fj=ins.ins.fj
        fus[fu].fk=ins.ins.fk
        for i in range(5):
            if i!=fu and fus[i].fi==fus[fu].fj and fus[i].busy:
                fus[fu].qj=i
            elif i!=fu and fus[i].fi==fus[fu].fk and fus[i].busy:
                fus[fu].qk=i
        if fus[fu].qj<0:
            fus[fu].rj=True
        else:
            fus[fu].rj=False
        if fus[fu].qk<0:
            fus[fu].rk=True
        else:
            fus[fu].rk=False
    ins.fu=fu
    rrs.f[ins.ins.fi]=fu
    return True
def check(ins,pc):  # to check whether the instruction can be executed to next step
    if ins.check()==0:
        if rrs.f[ins.ins.fi]<0:
            if can_add_fun(ins):
                ins.cando=True
                return True
    elif ins.check()==1:
        if fus[ins.fu].rj and fus[ins.fu].rk:
            ins.cando=True
    elif ins.check()==2:
        ins.cando=True
    elif ins.check()==3:
        o=True
        for i in range(ins_num):
            if i!=pc:
                if (fus[ist[i].fu].fj==fus[ins.fu].fi and fus[ist[i].fu].rj) or (fus[ist[i].fu].fk==fus[ins.fu].fi and fus[ist[i].fu].rk):
                    o=False
                    break
        if o:
            ins.cando=True
    return False
def exec(ins,pc): # to execute the instruction that can be executed and change the status of flags
    if ins.cando:
        if ins.check()==0:
            add_fun(ins)
            ins.change()
        elif ins.check()==1:
            fus[ins.fu].rj=fus[ins.fu].rk=False
            fus[ins.fu].qj=fus[ins.fu].qk=-1
            if ins.fu==0:
                fus[ins.fu].remain=1
            elif ins.fu==1 or ins.fu==2:
                fus[ins.fu].remain=10
            elif ins.fu==3:
                fus[ins.fu].remain=2
            elif ins.fu==4:
                fus[ins.fu].remain=40
            ins.change()
        elif ins.check()==2:
            fus[ins.fu].remain=fus[ins.fu].remain-1
            if fus[ins.fu].remain==0:
                ins.change()
        elif ins.check()==3:
            for i in range(5):
                if fus[i].qj==ins.fu:
                    fus[i].rj=True
                if fus[i].qk==ins.fu:
                    fus[i].rk=True
            rrs.f[fus[ins.fu].fi]=-1
            fus[ins.fu].busy=False
            ins.complete=True
            ins.change()
def tickle(i):
    if i:
        return "√"
    else:
        return " "
def fuc(i):
    if i<0:
        return ""
    else:
        return dir[i]
def init():# initialize the status of the instruction status
    for i in range(ins_num):
        ist[i].cando=False
def prin(cycle,fp): # print the result of three tables of each cycle
    print("Cycle".center(5),cycle,file=fp)
    print("Instruction status:",file=fp)
    ins_sta=PrettyTable(["Instruction","i","j","k","Issue","Readop","Execcom","WriteR"])
    for i in range(ins_num):
        if ist[i].ins.op=="L.D":
            ins_sta.add_row([ist[i].ins.op,"F"+str(ist[i].ins.fi),str(ist[i].ins.imm)+"+","R"+str(ist[i].ins.fk),
                             tickle(ist[i].issue),tickle(ist[i].read_operands),tickle(ist[i].execution_complete),tickle(ist[i].write_result)])
        else:
            ins_sta.add_row(
                [ist[i].ins.op, "F"+str(ist[i].ins.fi), "F"+str(ist[i].ins.fj), "F"+str(ist[i].ins.fk), tickle(ist[i].issue), tickle(ist[i].read_operands),
                 tickle(ist[i].execution_complete), tickle(ist[i].write_result)])
    print(ins_sta,file=fp)
    print("",file=fp)
    print("Functional unit status:",file=fp)
    fun_sta=PrettyTable(["Name","Busy","Op","Fi","Fj","Fk","Qj","Qk","Rj","Rk","remain"])
    for i in range(5):
        if fus[i].busy:
            m,n=fus[i].qj,fus[i].qk
            if m<0:
                m=5
            if n<0:
                n=5
            # print(dir[m],dir[n],tickle(fus[i].rj),tickle(fus[i].rk),str(fus[i].remain))
            fun_sta.add_row([dir[i],tickle(fus[i].busy),fus[i].op,str(fus[i].fi),str(fus[i].fj),str(fus[i].fk),
                              dir[m],dir[n],tickle(fus[i].rj),tickle(fus[i].rk),str(fus[i].remain)])
        else:
            fun_sta.add_row(["","","","","","","","","","",""])
    print(fun_sta,file=fp)
    print("",file=fp)
    print("Register result status:",file=fp)
    reg_sta=PrettyTable(["F0","F2","F4","F6","F8","F10","F12","F14","F16","F18","F20","F22","F24","F26","F28","F30"])
    reg_sta.add_row([fuc(rrs.f[0]),fuc(rrs.f[2]),fuc(rrs.f[4]),fuc(rrs.f[6]),fuc(rrs.f[8]),fuc(rrs.f[10]),fuc(rrs.f[12]),
                     fuc(rrs.f[14]),fuc(rrs.f[16]),fuc(rrs.f[18]),fuc(rrs.f[20]),fuc(rrs.f[22]),fuc(rrs.f[24]),fuc(rrs.f[26]),fuc(rrs.f[28]),fuc(rrs.f[30])])
    print(reg_sta,file=fp)
    for i in range(5):
        print("",file=fp)
def main():
    fp=open("ins.in","r")
    i=0
    for line in fp:
        # ins.add(line)
        ist[i].ins.add(line)
        i=i+1
    fp.close()
    pc=1
    ins_num=i
    cycle=0
    fp=open("result.out","w")
    while True:
        cycle=cycle+1
        flag=True# judge if the codes are done already
        o=False# judge if a new instruction is issued
        init()
        for i in range(min(pc,ins_num)):
            if ist[i].complete==False:
                flag=False
                if check(ist[i],i):
                    o=True
        if o:
            pc=pc+1
        for i in range(pc):
            exec(ist[i],i)
        prin(cycle,fp)
        if flag:
            break
    fp.close()
main()