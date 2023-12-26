from fast_trans.base import *
#snprintf函数检查
class Snprintf(Checker):
    def __init__(self, prog_bv: BinaryView, func: str, args=1) -> None:
        super().__init__(prog_bv, func, args)


    '''
    snprintf(dest, length, pattern, arg1, arg2 ...)
    Snprintf return addr:[dest] ("%s" must in pattern)
    '''
    def get_dict(self):
        for ref in self.ref:
            func = ref.function
            temp_arg = []
            temp_arg.append(func.get_parameter_at(ref.address,None,0))
            pattern = self.bv.get_ascii_string_at(func.get_parameter_at(ref.address,None,2).value, min_length = 2).value
            if ("%s" in pattern):
                self.all_args.update({ref.address:temp_arg})
            else:
                continue

#sprintf函数检查
class Sprintf(Checker):
    def __init__(self, prog_bv: BinaryView, func: str, args=1) -> None:
        super().__init__(prog_bv, func, args)

    '''
    sprintf(dest, pattern, arg1, arg2 ...)
    Sprintf return addr:[dest] ("%s" must in pattern)
    '''
    def get_dict(self):
        if self.ref == None:
            return
            
        for ref in self.ref:
            func = ref.function
            temp_arg = []
            temp_arg.append(func.get_parameter_at(ref.address,None,0))
            pattern = self.bv.get_ascii_string_at(func.get_parameter_at(ref.address,None,1).value, min_length = 2).value
            if ("%s" in pattern):
                self.all_args.update({ref.address:temp_arg})
            else:
                continue

#system函数检查
class System(Checker):
    def __init__(self, prog_bv: BinaryView, func: str, args=1) -> None:
        super().__init__(prog_bv, func, args)

    def get_dict(self):
        if self.ref == None:
            return
            
        for ref in self.ref:
            func = ref.function
            temp_arg = func.get_parameter_at(ref.address,None,0)
            if not self.is_constant(temp_arg):
                self.all_args.update({ref.address:temp_arg.value})

# #dosystem检查 <-继承System
# class Dosystem(System):
#     def __init__(self, prog_bv: BinaryView, func: str, args=1) -> None:
#         super().__init__(prog_bv, func, args)

#popen检查 <-继承System
class Popen(System):
    def __init__(self, prog_bv: BinaryView, func: str, args=1) -> None:
        super().__init__(prog_bv, func, args)

#execve检查 <-继承System
class Popen(System):
    def __init__(self, prog_bv: BinaryView, func: str, args=1) -> None:
        super().__init__(prog_bv, func, args)