from collections import namedtuple

#import llvm_compile

token_stream = []

word_dict = {}

user_dict = {}

int_stack = []

is_compile_mode = False

compiled_words = ""

UserFuncData = namedtuple('UserFuncData', ['pc_in', 'pc_out'])

def add_func():
    a_1 = int_stack.pop(-1)
    a_2 = int_stack.pop(-1)
    # TODO verify types
    s = a_1 + a_2
    int_stack.append(s)
    return UserFuncData(None, None)

def sub_func():
    a_1 = int_stack.pop(-1)
    a_2 = int_stack.pop(-1)
    # TODO verify types
    s = a_2 - a_1
    int_stack.append(s)
    return UserFuncData(None, None)

def mul_func():
    a_1 = int_stack.pop(-1)
    a_2 = int_stack.pop(-1)
    # TODO verify types
    s = a_1 * a_2
    int_stack.append(s)
    return UserFuncData(None, None)

def div_func():
    a_1 = int_stack.pop(-1)
    a_2 = int_stack.pop(-1)
    # TODO verify types
    s = a_2 // a_1
    int_stack.append(s)
    return UserFuncData(None, None)

def mod_func():
    op_1 = int_stack.pop(-1)
    op_2 = int_stack.pop(-1)
    result = op_2 % op_1
    int_stack.append(result)
    return UserFuncData(None, None)

def divmod_func():
    op_1 = int_stack.pop(-1)
    op_2 = int_stack.pop(-1)
    div_result = op_2 // op_1
    mod_result = op_2 % op_1
    int_stack.append(mod_result)
    int_stack.append(div_result)
    return UserFuncData(None, None)

def pow_func():
    op_1 = int_stack.pop(-1)
    op_2 = int_stack.pop(-1)
    # TODO verify types
    result = op_2 ** op_1
    int_stack.append(result)
    return UserFuncData(None, None)

def negate_func():
    v = int_stack.pop(-1)
    int_stack.append(-v)
    return UserFuncData(None, None)

def sign_func():
    v = int_stack.pop(-1)
    if v < 0:
        int_stack.append(-1)
    elif v > 0:
        int_stack.append(1)
    else:
        int_stack.append(0)
    return UserFuncData(None, None)

def min_func():
    op_1 = int_stack.pop(-1)
    op_2 = int_stack.pop(-1)
    # TODO verify types
    result = min(op_1, op_2)
    int_stack.append(result)
    return UserFuncData(None, None)

def max_func():
    op_1 = int_stack.pop(-1)
    op_2 = int_stack.pop(-1)
    # TODO verify types
    result = max(op_1, op_2)
    int_stack.append(result)
    return UserFuncData(None, None)

def dup_func():
    op = int_stack[-1]
    int_stack.append(op)
    return UserFuncData(None, None)

def drop_func():
    int_stack.pop(-1)
    return UserFuncData(None, None)

def swap_func():
    op_1 = int_stack.pop(-1)
    op_2 = int_stack.pop(-1)
    int_stack.append(op_1)
    int_stack.append(op_2)
    return UserFuncData(None, None)






def print_func():
    v = int_stack.pop(-1)
    print(v)
    return UserFuncData(None, None)

def set_compile_func():
    global is_compile_mode
    is_compile_mode = True
    global compiled_words
    compiled_words = ""

def end_compile_func():
    global is_compile_mode
    is_compile_mode = False
    print("compiled words:", compiled_words)
    compiled_toks = compiled_words.split()

    if len(compiled_toks) == 0:
        print("empty body? doing nothing")
        return

    # TODO take compiled words and put it into a dynamic dictionary of words
    first_word = compiled_toks.pop(0)

    is_num = False
    try:
        n = int(first_word)
        is_num = True
    except ValueError:
        is_num = False

    if is_num:
        print("trying to bind a word to a number, skipping")
        return
    if first_word in word_dict:
        print("trying to overwrite a reserved word, skipping")
        return
    if first_word in user_dict:
        print("trying to overwrite a user word, skipping")
        return
    definition = ' '.join(compiled_toks)
    print("binding %s to %s" % (first_word, definition))
    user_dict[first_word] = definition


def bye_func():
    exit(-1)

def words_func():
    s = ' '.join(word_dict.keys())
    print(s)

def stack_func():
    for n in int_stack:
        print("[%d]" % n)

def branch_func(ufd):
    offset = int_stack.pop(-1)
    new_pc = ufd.pc_in + offset

    if new_pc < 0:
        print("error, invalid branch offset")
        new_pc = 0
    return UserFuncData(ufd.pc_in, new_pc)

def branch_cond_func(ufd):
    cond = int_stack.pop(-1)
    offset = int_stack.pop(-1)

    new_pc = None
    
    if cond != 0:
        new_pc = ufd.pc_in + offset

        if new_pc < 0:
            print("error, invalid branch offset")
            new_pc = 0
    return UserFuncData(ufd.pc_in, new_pc)

def return_func(ufd):
    return UserFuncData(ufd.pc_in, -1)




word_dict['+'] = add_func
word_dict['-'] = sub_func
word_dict['*'] = mul_func
word_dict['/'] = div_func
word_dict['%'] = mod_func
word_dict['/%'] = divmod_func
word_dict['^'] = pow_func
word_dict['.'] = print_func
word_dict['negate'] = negate_func
word_dict['sign'] = sign_func
word_dict['min'] = min_func
word_dict['max'] = max_func
word_dict['dup'] = dup_func
word_dict['drop'] = drop_func
word_dict['swap'] = swap_func
word_dict['bye'] = bye_func
word_dict[':'] = set_compile_func
word_dict[';'] = end_compile_func
word_dict['words'] = words_func
word_dict['stack'] = stack_func
word_dict['branch'] = branch_func
word_dict['branch?'] = branch_cond_func
word_dict['return'] = return_func

def cvt_word_to_number(w):
    # TODO parse floats
    return int(w)

def compile_token(tok):
    global compiled_words
    compiled_words += " " + tok

def run_user_word(definition):
    #print ('in RUW')

    # TODO don't store definitions as a string, might as well store as
    # a list of tokens

    toks = definition.split()

    pc = 0

    while pc < len(toks):
        #print("PC:", pc)
        t = toks[pc]
        #print("tok:", t)

        try:
            n = int(t)
            int_stack.append(n)
            pc += 1
            continue
        except ValueError:
            pass

        if t in word_dict:
            #print("found",t,"in word_dict")
            w = word_dict[t]

            ufd = UserFuncData(pc, None)
            ret_data = w(ufd)

            #print("got ret", ret_data)

            if not (ret_data.pc_out is None):
                pc = ret_data.pc_out
                if pc == -1:
                    return
            else:
                pc += 1
            #print("new pc", pc)

        elif t in user_dict:
            #print("found",t,"in user_dict")
            d = user_dict[t]

            run_user_word(d)

            pc += 1
            #print ("new pc", pc)

        else:
            print("unknown token", t)


def main():
    print("Hello from bdgforth!")

    while True:
        try:
            inputline = input("> ")
            toks = inputline.split()

            global token_stream
            token_stream = toks

            #print("toks:", toks)
            #print("tok_str: ", token_stream)

            for t in token_stream:
                #print("t:", t)
                #print("s:", int_stack)
                if is_compile_mode:
                    if t == ';':
                        end_compile_func()
                    else:
                        compile_token(t)
                    continue
                try:
                    n = int(t)
                    int_stack.append(n)
                    continue
                except ValueError:
                    pass

                if t in word_dict:
                    w = word_dict[t]
                    r = w()
                elif t in user_dict:
                    d = user_dict[t]
                    run_user_word(d)
                else:
                    print("unknown token", t)

        except EOFError:
            break

if __name__ == "__main__":
    # TODO take filenames as args
    main()
