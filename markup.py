#!/usr/bin/env python
import sys
import re
from handlers import *
from util import *
from rules import *

__metaclass__ = type
class Parser:
    def __init__(self, handler):
        self.handler = handler
	self.rules = []
	self.filters = []
    def addRule(self, rule):
        self.rules.append(rule)
    def addFilter(self, pattern, name):
        def filter(block, handler):
	    return re.sub(pattern, handler.sub(name), block)
	self.filters.append(filter)
    def parse(self, file):
        body = []
    	for block in blocks(file):
    	    for filter in self.filters:
    	        block = filter(block, self.handler)
    	    for rule in self.rules:
    	        if rule.condition(block):
    		    last = rule.action(block, self.handler)
    		    if last:
                        if last is not True: body.append(last)
                        if last is True or last[:4] != '<ul>': break

        return self.handler.document(''.join(body))
class BasicTextParser(Parser):
    def __init__(self, handler):
        Parser.__init__(self, handler)
        self.addRule(ListRule())
        self.addRule(HeadingRule())
        self.addRule(ParagraghRule())

        self.addFilter(r'\*(.+?)\*', 'emphasis')
        self.addFilter(r'(http://[\.a-zA-Z/]+)', 'url')
        self.addFilter(r'([\.a-zA-Z]+@[\.a-zA-Z]+[a-zA-Z]+)', 'mail')

handler = HTMLRenderer()
parser = BasicTextParser(handler)

print parser.parse(sys.stdin)
