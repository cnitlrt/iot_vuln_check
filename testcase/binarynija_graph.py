from binaryninja import *
from fast_trans.functions import *
from fast_trans.more_types import *
from fast_trans.base import *
from rprint import *

if __name__ == "__main__":

    # bv = open_view("./testcase/framework/httpd")
    # bv = open_view("./testcase/framework/httpd.bndb")
    bv = open_view("./testcase/command_inject.exe")
    bv.update_analysis()
    system_c = System(prog_bv=bv, func="system")
    system_c.visualize_basic_block_graph()

    snprintf_c = Snprintf(prog_bv=bv, func="snprintf",args=3)
    snprintf_c.visualize_basic_block_graph()