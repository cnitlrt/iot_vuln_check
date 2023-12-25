from enum import Enum, auto
import os
import argparse
from binaryninja import *
class Success(Enum):
    FORMAT_UNCONSTANT = auto()
    FORMAT_OVERFLOW = auto()
    STACKOVERFLOW = auto()
    COMMANDINJECT = auto()
    COMMANDUNCONSTANT = auto()
    BUFOVERFLOW = auto()
#check command injection
def check_commend(symbol):
    addr = get_function_addr(symbol)
    if addr == None:
        return []
    refs = bv.get_code_refs(addr)
    for ref in refs:
        func = ref.function
        cmd = func.get_parameter_at(ref.address,None,0)
        if is_constant(cmd):
            continue
        callees = func.callees        
        if 'sprintf' in [callee.symbol.name for callee in callees]:        
            ret.append((symbol,func.name,ref.address,Success.COMMANDINJECT))

def check_doSystem(symbol):
    addr = get_function_addr(symbol)
    if addr == None:
        return []
    refs = bv.get_code_refs(addr)
    for ref in refs:
        func = ref.function
        fmt = func.get_parameter_at(ref.address,None,0)
        if not is_constant(fmt):
            ret.append((symbol,func.name,ref.address,Success.COMMANDUNCONSTANT))
            continue
        asc = bv.get_ascii_string_at(fmt.value,min_length = 2)
        if asc == None:
            continue
        fmt_value = asc.value
        cidx = 0
        arg_idx = 0
        while True:
            idx = fmt_value.find("%",cidx)
            if idx < 0:
                break
            arg_idx += 1
            cidx = idx + 1
            if fmt_value[idx:].startswith("%s"):
                arg = func.get_parameter_at(ref.address,None,arg_idx)
                if not is_constant(arg):
                    ret.append((symbol,func.name,ref.address,Success.COMMANDINJECT))
                    break
            

def check_execv(symbol = "execv"):
    addr = get_function_addr(symbol)
    if addr == None:
        return []
    refs = bv.get_code_refs(addr)
    for ref in refs:
        func = ref.function
        cmd = func.get_parameter_at(ref.address,None,1)
        if is_constant(cmd):
            continue    
        ret.append((symbol,func.name,ref.address,Success.COMMANDINJECT))

def check_sprintf(symbol = "sprintf"):
    addr = get_function_addr(symbol)
    if addr == None:
        return []
    refs = bv.get_code_refs(addr)
    for ref in refs:
        func = ref.function
        fmt = func.get_parameter_at(ref.address,None,1)
        if not is_constant(fmt):
            ret.append((symbol,func.name,ref.address,Success.FORMAT_UNCONSTANT))
            continue
        asc = bv.get_ascii_string_at(fmt.value,min_length = 2)
        if asc == None:
            continue
        fmt_value = asc.value
        cidx = 0
        arg_idx = 1
        while True:
            idx = fmt_value.find("%",cidx)
            if idx < 0:
                break
            arg_idx += 1
            cidx = idx + 1
            if fmt_value[idx:].startswith("%s"):
                arg = func.get_parameter_at(ref.address,None,arg_idx)
                if not is_constant(arg):
                    ret.append((symbol,func.name,ref.address,Success.FORMAT_OVERFLOW))
                    break

def check_printf(symbol = "printf"):
    addr = get_function_addr(symbol)
    if addr == None:
        return []
    refs = bv.get_code_refs(addr)
    for ref in refs:
        func = ref.function
        fmt = func.get_parameter_at(ref.address,None,0)
        if not is_constant(fmt):
            ret.append((symbol,func.name,ref.address,Success.FORMAT_UNCONSTANT))
            continue
def check_syslog(symbol = "syslog"):
    addr = get_function_addr(symbol)
    if addr == None:
        return []
    refs = bv.get_code_refs(addr)
    for ref in refs:
        func = ref.function
        fmt = func.get_parameter_at(ref.address,None,1)
        if not is_constant(fmt):
            ret.append((symbol,func.name,ref.address,Success.FORMAT_UNCONSTANT))
            continue

def check_strcpy(symbol = "strcpy"):
    addr = get_function_addr("strcpy")
    # print(hex(addr))
    if addr == None:
        return []
    refs = bv.get_code_refs(addr)
    for ref in refs:
        func = ref.function
        buf = func.get_parameter_at(ref.address,None,0)
        # print(buf.type)
        if buf.type == RegisterValueType.StackFrameOffset:    
            buf = func.get_parameter_at(ref.address,None,1)
            ret.append((symbol,func.name,ref.address,Success.BUFOVERFLOW))
            continue

def check_read():
    addr = get_function_addr("read")
    if addr == None:
        return []
    refs = bv.get_code_refs(addr)
    for ref in refs:
        func = ref.function
        buf = func.get_parameter_at(ref.address,None,1)
        buf_size = -(buf.value)
        size = func.get_parameter_at(ref.address,None,2)
        size = size.value
        if size > buf_size:
            ret.append(("read",func.name,ref.address,Success.BUFOVERFLOW))
            continue

def check_memcpy():
    addr = get_function_addr("memcpy")
    if addr == None:
        return []
    refs = bv.get_code_refs(addr)
    for ref in refs:
        func = ref.function
        cmd = func.get_parameter_at(ref.address,None,1)
        size = func.get_parameter_at(ref.address,None,2)
        if is_constant(cmd):
            continue
        callees = func.callees 
        if 'strlen' in [callee.symbol.name for callee in callees]:        
            ret.append(("memcpy",func.name,ref.address,Success.BUFOVERFLOW))
            continue

def check_fmt():
    check_printf()
    check_syslog()
    check_syslog("sscanf")

def check_overflow():
    check_memcpy()
    check_sprintf()
    check_strcpy()
    check_strcpy("strcat")

def check_cmd():
    check_commend("system")
    check_doSystem("doSystem")
    check_commend("popen")
    check_commend("execve")
    check_execv()

def get_function_addr(symbol):
    syms = []
    if symbol in bv.symbols:
        syms = bv.symbols[symbol]
    for i in syms:
        if "mips32" == bv.arch.name or "mipsel32" == bv.arch.name:
            if i.type == check_type:
                return i.address
        else:
            if i.type == SymbolType.ImportedFunctionSymbol:
                return i.address
    return None

def is_constant(a):
    return a.type == RegisterValueType.ConstantPointerValue or a.type == RegisterValueType.ConstantValue

def get_checktype():
    check_type_tmp = ""
    tmp_symbols = bv.symbols["system"]
    m = 0
    for tmp_symbol in tmp_symbols:
        # print(tmp_symbol)
        xrefs = bv.get_code_refs(tmp_symbol.address)
        for _ in xrefs:
            m += 1
        if m > 3:
            check_type_tmp = tmp_symbol.type
            break
    return check_type_tmp


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--file", help="File to analyze")
    parser.add_argument("-p","--path", help="Path to analyze")
    args = parser.parse_args()
    check_type = ""
    if args.file:
        bv = open_view(args.file)

        bv.update_analysis()
        for func in bv.functions:
            print(func.symbol.name)

        if bv == None:
            pass
        if check_type == "":
            check_type = get_checktype()         
        ret = []
        check_overflow()
        check_cmd()
        check_fmt()
        for i in ret:
            print("%-20s %-15s function: %-20s addr: 0x%x %s"%(args.file,i[0],i[1],i[2],i[3]))
    elif args.path:
        path = os.listdir(args.path)
        for file in path:
            bv = open_view(args.path + file)
            if bv == None:
                continue
            if check_type == "":
                check_type = get_checktype()
            ret = []
            check_overflow()
            check_cmd()
            check_fmt()
            for i in ret:
                print("%-20s %-15s function: %-20s addr: 0x%x %s"%(args.path + file,i[0],i[1],i[2],i[3]))
    # input_file = sys.argv[1]
    # bv = open_view(input_file)
    # settings = SaveSettings()
    # ret = []
    # # check_overflow(bv)
    # check_memcpy()
    # # check_printf(bv)
    # # check_sprintf(bv)
    # # check_strcpy(bv)
    # for i in ret:
    #     print("%-15s function: %-20s addr: 0x%x %s"%(i[0],i[1],i[2],i[3]))
