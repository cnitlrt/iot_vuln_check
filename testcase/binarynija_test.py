from binaryninja import *

if __name__ == "__main__":

    bv = BinaryViewType.get_view_of_file("./command_inject")
    bv.update_analysis()
    for func in bv.functions:
        print(func.symbol.name)