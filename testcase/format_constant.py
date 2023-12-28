from binaryninja import *
from fast_trans.functions import *
from fast_trans.more_types import *
from fast_trans.base import *
from fast_trans.method import *
from rprint import *

if __name__ == "__main__":
    
    bv = open_view("./testcase/format_unconstant")
    bv.update_analysis()
    printf_c = Printf(bv,"printf",1)
    search = FormatUnconstant(printf_c)
    search.burptal_search()