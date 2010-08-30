"""Tests for the fakeout module."""
from unittest2 import TestCase, main

from fakeout import fakeout, fakeout_do

# Experimental code to enable clearer declaration of interdependent data
#   using a class as a namespace
def make_AttribIterator(filter):
    """Creates an AttribIterator metaclass with a given attribute filter.

    `filter` is passed (name, value) pairs.
    Its return is interpreted as a Boolean
      indicating whether or not a given pair should be part of the iteration.
    """
    class AttribIterator(type):
        """Metaclass which allows the class's elements to be iterated over."""
        def __iter__(self):
            from itertools import ifilter
            return ifilter(filter, self.__dict__.iteritems())
    return AttribIterator

# The interdependent data
class TestStrings(object):
    """Just contains a list of strings to be tested."""
    __metaclass__ = make_AttribIterator(
        lambda name_value: name_value[0].find('string') > -1)
    string = "the normal test string"
    string_with_newline = string + '\n'
    multiline_string = "a multiline\nstring"
    multiline_string_with_closing_newline = multiline_string + '\n'

test_strings = tuple(TestStrings)


# Test functions which take a single string parameter
def test_print_with_context_manager(test_case, string):
    from StringIO import StringIO
    fake_out = StringIO()
    with fakeout(fake_out):
        print string
    test_case.assertEqual(string + "\n", fake_out.getvalue())

def test_do_write(test_case, string):
    def write_to_stdout(string):
        from sys import stdout
        stdout.write(string)
    test_case.assertEqual(string,
                          fakeout_do(write_to_stdout, string)[1])


test_methods = (test_print_with_context_manager,
                test_do_write)

def make_test_method(testfn, string, name=None, doc=None):
    def test_method(test_case):
        return testfn(test_case, string)
    test_method.__name__ = name
    test_method.__doc__ = doc
    return test_method

def make_mixin_class(name, inputs, test_function,
                     test_method_name_fmt='test_{name}'.format,
                     test_method_doc_fmt=
                        "Test {method} with the string '{value}'".format):
    """Generates a mixin class which contains partials of `test_method`.

    `test_method_name_fmt` and `test_method_doc_fmt` will be be used
      to format the name and docstring of each test method.
    """

    ##~~  print "inputs:"
    ##~~  pprint(inputs)

    def make_class_test_method(name, value):
        format_args = {'name': name, 'value': value,
                       'method': test_function.__name__}
        return make_test_method(test_function, value,
                                name=test_method_name_fmt(**format_args),
                                doc=test_method_doc_fmt(**format_args))
    ##{{~~
    ##~~  def print_items(it):
    ##~~      for item in it:
    ##~~          print "  printed item: {0}".format(item)
    ##~~          yield item
    ##~~  inputs = print_items(inputs)
    ##}}~~

    methods = (make_class_test_method(name, value) for name, value in inputs)

    ##{{~~
    ##~~  methods = print_items(methods)
    ##}}~~

    class_dict = dict((method.__name__, method) for method in methods)
    return type(name, (TestCase,), class_dict)

TestPrintWithContextManager = make_mixin_class('TestPrintWithContextManager',
                                               test_strings,
                                               test_print_with_context_manager)

TestDoWrite = make_mixin_class('TestDoWrite', test_strings, test_do_write)



if __name__ == '__main__':
    main()
