from binaryninja import *
from fast_trans.functions import *
from fast_trans.more_types import *
from fast_trans.base import *
from fast_trans.method import *
from rprint import *

if __name__ == "__main__":
    
    bv = open_view("./testcase/framework/httpd.bndb")
    bv.update_analysis()
    system_c = System(prog_bv=bv, func="system")
    popen_c = System(prog_bv=bv, func="popen")
    dosystem_c = Dosystem(prog_bv=bv, func="dosystem")
    snprintf_c = Snprintf(prog_bv=bv, func="snprintf")

    search = CommandInject([system_c, popen_c, dosystem_c])
    try:
        search.get_result(system_c.arg_xrefs, snprintf_c.arg_xrefs)
    except:
        pass
    search.burptal_search()