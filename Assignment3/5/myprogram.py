from reflect import reflect

@reflect
def foo(bar1, bar2=""):
    """This function does nothing useful
    :param bar1: description
    :param bar2: description
    """
    print("some\nmultiline\noutput") # some comment with 'print'

foo(None, bar2="snickers")
reflect = reflect(reflect)  # Decorate reflect with reflect
reflect(reflect)            # Call the reflect function on itself
