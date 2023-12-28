from binaryninja import *
from fast_trans.functions import *
from rprint import *

def get_cross(dictA: dict, dictB: dict):

    keys = []
    for va in dictA:
        for vb in dictB:
            if dictA[va] == dictB[vb]:
                keys.append({va:dictA[va], vb:dictB[vb]})
    return keys

if __name__ == "__main__":

    bv = open_view("./testcase/command_inject")
    # bv = open_view("./testcase/httpd")
    bv.update_analysis()
    system_c = System(prog_bv=bv, func="system")
    snprintf_c = Snprintf(prog_bv=bv, func="snprintf",args=3)
    sprintf_c = Sprintf(prog_bv=bv, func="sprintf",args=1)

    for key,value in system_c.all_args.items():
        info(hex(key), "-> ", hex(value))
    for key,value in snprintf_c.all_args.items():
        info(hex(key), "-> ", [hex(i.value) for i in value])
    for key,value in sprintf_c.all_args.items():
        info(hex(key), "-> ", [hex(i.value) for i in value])
    # print(snprintf_c.all_args[1]  ,system_c.all_args[1])
    # Searcher("./testcase/command_inject",snprintf_c.all_args[1]  ,system_c.all_args[1])
    Searcher("./testcase/command_inject",0x7d0  ,0x79F)
            # for i in range(self.args):
            #     temp_arg.append(func.get_parameter_at(ref.address,None,i))
            #     if (i==0) and((self.is_constant(temp_arg[i]) ) or (temp_arg[i].type==0)):
            #         break
            #     elif(i==3) and("%s"not in self.bv.get_ascii_string_at(temp_arg[2].value,min_length = 2)):
            #         break