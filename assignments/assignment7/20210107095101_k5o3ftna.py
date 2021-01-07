

class BTB_item:
    def __init__(self,pc,valid,target_pc):
        self.pc = pc
        self.valid = valid
        self.target_pc = target_pc

    def _get_pc(self):
        return self.pc
    def _get_valid(self):
        return self.valid
    def _get_target_pc(self):
        return self.target_pc
    def _update(self,pc,valid,target):
        self.pc = pc
        self.valid = valid
        self.target_pc = target

# no tags in BHT table!
class BHT_item:
    def __init__(self , n_bit_predictor=0x00):
        self.n_bit_predictor = n_bit_predictor
    def _get_n_bit_predictor(self):
        return self.n_bit_predictor

    # shift by 1/0 bit to update the item
    def _update(self,last_real_choice):
        self.n_bit_predictor = (self.n_bit_predictor << int(last_real_choice)) % 4 


class selector_item:
    def __init__(self):
        self.two_bit_selector = 0x00
    def _get_two_bit_selector(self):
        return self.two_bit_selector
    def _update(self,value):
        self.two_bit_selector = value

class BHT:

    # init the bht table with 1024 items
    def __init__(self):
        self.bht_table = []
        for i in range(1024):
            self.bht_table.append(BHT_item())

    def _update_BHT(self,pc,last_real_choice):
        index = int(pc[-10:])
        print(index)
        self.bht_table[index]._update(last_real_choice)


class BTB:

    # init the btb table with 256 items
    def __init__(self):
        self.btb_table = []
        for i in range(256):
            self.btb_table.append(BTB_item(pc=0,valid=False,target_pc=0))

    def _update_BTB(self,pc,valid,target_pc):
        index = int(pc[-8:])
        print(index)
        self.btb_table[index]._update(pc,valid,target_pc)



class Selector:
    # init the selector with 1024 items
    def __init__(self):
        self.selector_table = []
        for i in range(1024):
            self.selector_table.append(selector_item())

    # default source from btb
    def _update(self,pc,select_from_btb):
        index = int(pc[-10:])
        selector_item = self.selector_table[index]._get_two_bit_selector()
        if(select_from_btb == True):
            if(selector_item == 3):
                pass
            else:
                self.selector_table[index]._update(selector_item + 1)
        else:
            if(selector_item == 0):
                pass
            else:
                self.selector_table[index]._update(selector_item - 1)
        
    


class predictor:
    # init the main structure:BTB table,BHT table and the Selector
    def __init__(self):
        self.BTB_predictor = BTB()
        self.BHT_predictor = BHT()
        self.Selector = Selector()

    # generate some default datas
    def _shuffle(self):
        for i in range(8):
            self.BHT_predictor.bht_table[i*4]._update(last_real_choice = i%2)
            self.BTB_predictor.btb_table[i]._update(pc = i*4,valid = True,target = i+20)

    # predict with BTB
    def _predict_with_btb(self,pc):
        print("in IF stage:")
        btb_index = int(pc[-8:])
        if(self.BTB_predictor.btb_table[btb_index]._get_pc() == pc):
            if(self.BTB_predictor.btb_table[btb_index]._get_valid() == True):
                print("BTB predict next PC is:",self.BTB_predictor.btb_table[btb_index]._get_target_pc())
                return str(self.BTB_predictor.btb_table[btb_index]._get_target_pc())
        else:
            print("this PC is not found in BTB")
            return str(int(pc) + 4)

    # predict with BHT.
    # here I don't care about the icache,so when the prediction of BHT is "True",the offset is set to constant value:8
    # (that is,there is no action to look up the icache to get the offset) and 8 is just used to show the difference between pc + 4
    def _predict_with_bht(self,pc):
        print("in ID stage:")
        bht_index = int(pc[-10:])
        if(self.BHT_predictor.bht_table[bht_index]._get_n_bit_predictor() == 3 or 
            self.BHT_predictor.bht_table[bht_index]._get_n_bit_predictor() == 1):
            print("BHT predict branch taken")
            icache_index = pc[:30]
            # offset = icache[icache_index]
            offset = 8
            target_pc = int(pc) + offset
        else:
            print("BHT predict branch no taken")
            target_pc = int(pc) + 4
        return str(target_pc)

    # use the selector to choose the prediction,if the value of selector >= 2,then the predictor will use the BHT result.
    def _predict(self,pc):
        bht_target_pc = self._predict_with_bht(pc)
        btb_target_pc = self._predict_with_btb(pc)
        selector_index = int(pc[-10:])
        selector_result = self.Selector.selector_table[selector_index]._get_two_bit_selector()
        if(selector_result >= 2):
            return False,bht_target_pc
        else:
            return True,btb_target_pc


    # here the tag is used to simulate the real execution result
    def _update(self,pc,npc,select_from_btb_tag,tag=True):
        print("after the EX stage,update the table.")
        self.BHT_predictor._update_BHT(pc,tag)
        self.BTB_predictor._update_BTB(pc,True,npc)
        self.Selector._update(pc,select_from_btb_tag)


if __name__ == "__main__":
    P = predictor()
    P._shuffle()


    select_from_btb_tag,nPC = P._predict(pc = "0000")
    print("the prediction is:",nPC)
    P._update("0000",nPC,select_from_btb_tag,nPC != str(int("0000") + 4))


