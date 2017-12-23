#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CAVEAT UTILITOR
#
# This file was automatically generated by Grako.
#
#    https://pypi.python.org/pypi/grako/
#
# Any changes you make to it will be overwritten the next time
# the file is generated.


from __future__ import print_function, division, absolute_import, unicode_literals

from grako.buffering import Buffer
from grako.parsing import graken, Parser
from grako.util import re, RE_FLAGS, generic_main  # noqa


KEYWORDS = {}


class CspBuffer(Buffer):
    def __init__(
        self,
        text,
        whitespace=None,
        nameguard=None,
        comments_re=None,
        eol_comments_re=None,
        ignorecase=None,
        namechars='',
        **kwargs
    ):
        super(CspBuffer, self).__init__(
            text,
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            namechars=namechars,
            **kwargs
        )


class CspParser(Parser):
    def __init__(
        self,
        whitespace=None,
        nameguard=None,
        comments_re=None,
        eol_comments_re=None,
        ignorecase=None,
        left_recursion=False,
        parseinfo=True,
        keywords=None,
        namechars='',
        buffer_class=CspBuffer,
        **kwargs
    ):
        if keywords is None:
            keywords = KEYWORDS
        super(CspParser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            left_recursion=left_recursion,
            parseinfo=parseinfo,
            keywords=keywords,
            namechars=namechars,
            buffer_class=buffer_class,
            **kwargs
        )

    @graken()
    def _start_(self):
        self._token('Variables')
        self._variables_()
        self.name_last_node('vs')
        self._token('Constraints')
        self._constraints_()
        self.name_last_node('cs')
        self._token('end')
        self._check_eof()
        self.ast._define(
            ['cs', 'vs'],
            []
        )

    @graken()
    def _variables_(self):
        with self._choice():
            with self._option():
                self._ident_()
                self.name_last_node('id')
                self._token('in')
                self._token('[')
                self._signed_float_()
                self.name_last_node('inf')
                self._token(',')
                self._signed_float_()
                self.name_last_node('sup')
                self._token(']')
                self._token(';')
                self._variables_()
                self.name_last_node('rest')
            with self._option():
                self._void()
            self._error('no available options')
        self.ast._define(
            ['id', 'inf', 'rest', 'sup'],
            []
        )

    @graken()
    def _constraints_(self):
        with self._choice():
            with self._option():
                self._inequality_()
                self.name_last_node('head')
                self._token(';')
                self._constraints_()
                self.name_last_node('rest')
            with self._option():
                self._void()
            self._error('no available options')
        self.ast._define(
            ['head', 'rest'],
            []
        )

    @graken()
    def _inequality_(self):
        with self._choice():
            with self._option():
                self._expression_()
                self.name_last_node('left')
                self._token('==')
                self.name_last_node('op')
                self._expression_()
                self.name_last_node('right')
            with self._option():
                self._expression_()
                self.name_last_node('left')
                self._token('<')
                self.name_last_node('op')
                self._expression_()
                self.name_last_node('right')
            with self._option():
                self._expression_()
                self.name_last_node('left')
                self._token('<=')
                self.name_last_node('op')
                self._expression_()
                self.name_last_node('right')
            with self._option():
                self._expression_()
                self.name_last_node('left')
                self._token('>')
                self.name_last_node('op')
                self._expression_()
                self.name_last_node('right')
            with self._option():
                self._expression_()
                self.name_last_node('left')
                self._token('>=')
                self.name_last_node('op')
                self._expression_()
                self.name_last_node('right')
            self._error('no available options')
        self.ast._define(
            ['left', 'op', 'right'],
            []
        )

    @graken()
    def _expression_(self):
        self._term_()
        self.name_last_node('head')
        self._expr_rest_()
        self.name_last_node('rest')
        self.ast._define(
            ['head', 'rest'],
            []
        )

    @graken()
    def _expr_rest_(self):
        with self._choice():
            with self._option():
                self._token('+')
                self.name_last_node('op')
                self._cut()
                self._term_()
                self.name_last_node('arg')
                self._expr_rest_()
                self.name_last_node('rest')
            with self._option():
                self._token('-')
                self.name_last_node('op')
                self._cut()
                self._term_()
                self.name_last_node('arg')
                self._expr_rest_()
                self.name_last_node('rest')
            with self._option():
                self._void()
            self._error('no available options')
        self.ast._define(
            ['arg', 'op', 'rest'],
            []
        )

    @graken()
    def _term_(self):
        self._min_expr_()
        self.name_last_node('head')
        self._term_rest_()
        self.name_last_node('rest')
        self.ast._define(
            ['head', 'rest'],
            []
        )

    @graken()
    def _term_rest_(self):
        with self._choice():
            with self._option():
                self._token('*')
                self.name_last_node('op')
                self._cut()
                self._min_expr_()
                self.name_last_node('arg')
                self._term_rest_()
                self.name_last_node('rest')
            with self._option():
                self._token('/')
                self.name_last_node('op')
                self._cut()
                self._min_expr_()
                self.name_last_node('arg')
                self._term_rest_()
                self.name_last_node('rest')
            with self._option():
                self._void()
            self._error('no available options')
        self.ast._define(
            ['arg', 'op', 'rest'],
            []
        )

    @graken()
    def _min_expr_(self):
        with self._choice():
            with self._option():
                self._token('-')
                self.name_last_node('op')
                self._cut()
                self._min_expr_()
                self.name_last_node('arg')
            with self._option():
                self._pow_expr_()
                self.name_last_node('@')
            self._error('no available options')
        self.ast._define(
            ['arg', 'op'],
            []
        )

    @graken()
    def _pow_expr_(self):
        self._factor_()
        self.name_last_node('base')
        self._pow_expr_rest_()
        self.name_last_node('rest')
        self.ast._define(
            ['base', 'rest'],
            []
        )

    @graken()
    def _pow_expr_rest_(self):
        with self._choice():
            with self._option():
                self._token('^')
                self.name_last_node('op')
                self._cut()
                self._integer_()
                self.name_last_node('arg')
                self._pow_expr_rest_()
                self.name_last_node('rest')
            with self._option():
                self._void()
            self._error('no available options')
        self.ast._define(
            ['arg', 'op', 'rest'],
            []
        )

    @graken()
    def _factor_(self):
        with self._choice():
            with self._option():
                self._subexpression_()
            with self._option():
                self._float_()
            with self._option():
                self._integer_()
            with self._option():
                self._infinity_()
            with self._option():
                self._interval_()
            with self._option():
                self._ident_()
            self._error('no available options')

    @graken()
    def _subexpression_(self):
        self._token('(')
        self._cut()
        self._expression_()
        self.name_last_node('@')
        self._token(')')

    @graken()
    def _integer_(self):
        self._pattern(r'\d+')

    @graken()
    def _signed_float_(self):
        with self._choice():
            with self._option():
                self._float_()
                self.name_last_node('value')
            with self._option():
                self._token('-')
                self.name_last_node('minus')
                self._float_()
                self.name_last_node('value')
            self._error('no available options')
        self.ast._define(
            ['minus', 'value'],
            []
        )

    @graken()
    def _float_(self):
        self._pattern(r'((\d*\.\d+)|(\d+\.?))([eE][+-]?\d+)?')

    @graken()
    def _infinity_(self):
        self._token('inf')

    @graken()
    def _interval_(self):
        self._token('[')
        self._expression_()
        self.name_last_node('inf')
        self._token(',')
        self._expression_()
        self.name_last_node('sup')
        self._token(']')
        self.ast._define(
            ['inf', 'sup'],
            []
        )

    @graken()
    def _ident_(self):
        self._pattern(r'[a-zA-Z][a-zA-Z0-9]*')


class CspSemantics(object):
    def start(self, ast):
        return ast

    def variables(self, ast):
        return ast

    def constraints(self, ast):
        return ast

    def inequality(self, ast):
        return ast

    def expression(self, ast):
        return ast

    def expr_rest(self, ast):
        return ast

    def term(self, ast):
        return ast

    def term_rest(self, ast):
        return ast

    def min_expr(self, ast):
        return ast

    def pow_expr(self, ast):
        return ast

    def pow_expr_rest(self, ast):
        return ast

    def factor(self, ast):
        return ast

    def subexpression(self, ast):
        return ast

    def integer(self, ast):
        return ast

    def signed_float(self, ast):
        return ast

    def float(self, ast):
        return ast

    def infinity(self, ast):
        return ast

    def interval(self, ast):
        return ast

    def ident(self, ast):
        return ast


def main(filename, startrule, **kwargs):
    with open(filename) as f:
        text = f.read()
    parser = CspParser()
    return parser.parse(text, startrule, filename=filename, **kwargs)


if __name__ == '__main__':
    import json
    from grako.util import asjson

    ast = generic_main(main, CspParser, name='Csp')
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(asjson(ast), indent=2))
    print()
