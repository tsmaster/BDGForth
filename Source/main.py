#import llvm_compile

token_stream = []

word_dict = {}

user_dict = {}

int_stack = []

is_compile_mode = False

compiled_words = ""

def add_func():
    a_1 = int_stack.pop(-1)
    a_2 = int_stack.pop(-1)
    # TODO verify types
    s = a_1 + a_2
    int_stack.append(s)

def sub_func():
    a_1 = int_stack.pop(-1)
    a_2 = int_stack.pop(-1)
    # TODO verify types
    s = a_2 - a_1
    int_stack.append(s)

def mul_func():
    a_1 = int_stack.pop(-1)
    a_2 = int_stack.pop(-1)
    # TODO verify types
    s = a_1 * a_2
    int_stack.append(s)

def div_func():
    a_1 = int_stack.pop(-1)
    a_2 = int_stack.pop(-1)
    # TODO verify types
    s = a_2 // a_1
    int_stack.append(s)

def mod_func():
    op_1 = int_stack.pop(-1)
    op_2 = int_stack.pop(-1)
    result = op_2 % op_1
    int_stack.append(result)
    
def divmod_func():
    op_1 = int_stack.pop(-1)
    op_2 = int_stack.pop(-1)
    div_result = op_2 // op_1
    mod_result = op_2 % op_1
    int_stack.append(mod_result)
    int_stack.append(div_result)
    
def pow_func():
    op_1 = int_stack.pop(-1)
    op_2 = int_stack.pop(-1)
    # TODO verify types
    result = op_2 ** op_1
    int_stack.append(result)

def negate_func():
    v = int_stack.pop(-1)
    int_stack.append(-v)

def sign_func():
    v = int_stack.pop(-1)
    if v < 0:
        int_stack.append(-1)
    elif v > 0:
        int_stack.append(1)
    else:
        int_stack.append(0)
        
def min_func():
    op_1 = int_stack.pop(-1)
    op_2 = int_stack.pop(-1)
    # TODO verify types
    result = min(op_1, op_2)
    int_stack.append(result)

def max_func():
    op_1 = int_stack.pop(-1)
    op_2 = int_stack.pop(-1)
    # TODO verify types
    result = max(op_1, op_2)
    int_stack.append(result)

def dup_func():
    op = int_stack[-1]
    int_stack.append(op)

def drop_func():
    int_stack.pop(-1)

def swap_func():
    op_1 = int_stack.pop(-1)
    op_2 = int_stack.pop(-1)
    int_stack.append(op_1)
    int_stack.append(op_2)


        

    

def print_func():
    v = int_stack.pop(-1)
    print(v)

def branch_func():
    offset = stack.pop()
    # we need to change the program counter somehow?

def branch_p_func():
    offset = stack.pop()
    operator = stack.pop()
    # TODO eval operator, and if true, change program counter

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
        print("trying to bind a word to a number")
        return
    if first_word in word_dict:
        print("trying to overwrite a reserved word")
        return
    if first_word in user_dict:
        print("trying to overwrite a user word")
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

def cvt_word_to_number(w):
    # TODO parse floats
    return int(w)

def get_next():
    t = token_stream.pop(-1)
    if t in word_dict:
        return word_dict[t]
    try:
        num = cvt_word_to_number(t)
        return num
    except ValueError:
        pass
    
    print("undefined token", t)
    
    return t

def compile_token(tok):
    global compiled_words
    compiled_words += " " + tok

def run_user_word(definition):
    toks = definition.split()
    for t in toks:
        try:
            n = int(t)
            int_stack.append(n)
            continue
        except ValueError:
            pass
                    
        if t in word_dict:
            w = word_dict[t]
            r = w()
            if not (r is None):
                int_stack.append(r)
        elif t in user_dict:
            d = user_dict[t]
            run_user_word(d)
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
                    if not (r is None):
                        int_stack.append(r)
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
