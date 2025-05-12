"""
DWL: This file demonstrates a trivial function "intadd" returning
the sum of two integer numbers.
(see llvm_define.py)
"""

from llvmlite import ir

# Create some useful types
int_type = ir.IntType(64)
func_type = ir.FunctionType(int_type, (int_type, int_type))

# Create an empty module...
module = ir.Module(name=__file__)
# and declare a function named "intadd" inside it
func = ir.Function(module, func_type, name="intadd")

# Now implement the function
block = func.append_basic_block(name="entry")
builder = ir.IRBuilder(block)
a, b = func.args
result = builder.add(a, b, name="res")
builder.ret(result)

# Print the module IR
print(module)
