### Python Programming for Software Engineers
### Assignment 7
### 'Lambda De Parser'


# [Amir Gimaev and Vladimir Solovyev]

# Task 1
# ----------------------------------------------
# Given the following:
f = lambda x, y: x * y

# 1. Rewrite to its logical equivalence using ordinary funcion definition(s)
# [code]
def f(x, y):
    return x * y

# Task 2
# ----------------------------------------------
# Given the following:
f = lambda x: (lambda y: (lambda z: x + y + z))

# 1. How would you call it to get the result of `x + y + z`?
# [code]
f(x)(y)(z)

# 2. Rewrite it using only one lambda expression and show how to call it
# [code]
f = lambda x, y, z: x + y + z
f(x, y, z)

# Task 3
# ----------------------------------------------
# Given the following:
(lambda b = (lambda *c: print(c)): b("a", "b"))()

# 1. What happens here? Rewrite it so that the code can be 
# understood by a normal or your mate who has no idea what the lambda is! 
# Provide comments, neat formatting and a bit more meaningful var names.
# [multiline code interlaced with comments]

# First, we define the function that takes a tuple "c" as its parameter and prints it
def print_given(*given):
    '''Print a given variable number of arguments as a tuple'''
    return print(given)

# Second, we define a new function with a default parameter of print_given
def fixed_print_given(default_func=print_given):
    '''Call a passed function with "a" and "b" as its parameters'''
    # In our case "a" and "b" are two given arguments
    # that are packed into a tuple and printed to standard output
    return default_func("a", "b")

# Call the function without passed parameters, thus call it with the default argument
fixed_print_given()

# Task 4 (soft)
# ----------------------------------------------
# What are the main restrictions on the lambda?
# Provide "If yes, why? If not, why not?" for each of the following:
# 1. Does lambda restrict side effects?
# 2. Does lambda restrict number of allowed statements?
# 3. Does lambda restrict assignments? 
# 4. Does lambda restrict number of return values?
# 5. Does lambda restrict the use of default arguments values? 
# 6. Does lambda restrict possible function signatures?

# [your enumerated answers; if possible, code is welcomed]
# 1. What is a "side effect" here?
# 2. Yes because it is syntactically restricted to a single expression.
# 3. Yes, regular assignments are restricted inside lambda expressions because an assignment is 
#    a statement and statements are restricted in lambdas.
        # >>> lambda x: y = x
        #   File "<stdin>", line 1
        # SyntaxError: can't assign to lambda
        # >>> lambda x: (y = x)
        #   File "<stdin>", line 1
        #     lambda x: (y = x)
        # SyntaxError: invalid syntax
# 4. No, it'll be anything that expression inside lambda is evaluated to.
# 5. No, default argument values are accepted (as in the examples you provided in tasks 3 and 5).
# 6. Yes, just like in regular functions. E.g., keyword arguments have to come only after positional ones.

# Task 5
# ----------------------------------------------
# Given the following:
(lambda f = (lambda a: (lambda b: print(list(map(lambda x: x+x, a+b))))): 
f((1,2,3))((4,5,6)))()

# 1. What happens here? Do the same as in Task 3 and
# enumerate order of execution using (1,2,3...) in comments
# [multiline code interlaced with comments]
# lambda a: (lambda b: print(list(map(lambda x: x+x, a+b)))
def in1(a):
    def in2(b):
        print(list(map(lambda x: x+x, a+b)))
    return in2

def outer(f=in1):
    return f((1,2,3))((4,5,6))

outer()

# 1.    First function is created with a default parameter because it is called without parameters
# 2.    The default parameter is an expression that was obtained by calling a second function that creates and returns a third function
# 3.    Second function takes one parameter "a" and returns a third function
# 4.    Third function also takes one parameter "b" and uses second function's "a" inside of it.
#       Third function prints a list that was created by applying a "sum with itself" (multiply by 2) function
#       to each element of an iterable that was created by joining "a" and "b" tuples 
#       or lists or whatever that supports joining by "+".
#     
# All in all, tuples (1,2,3) and (4,5,6) are joined into a single tuple which elements are doubled. It is returned as list and printed out.


# 2. Why does map() requires list() call?
# [written answer]
# map() creates an iterator that returns elements one by one. We use list() to generate all the elements and return them as a sequence.
# Without list() we will try to print an iterator but not the elements it yields.
