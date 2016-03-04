__metaclass__ = type
class Rule:
    def action(self, block, handler):
        return handler.tag(self.type, block)
class HeadingRule(Rule):
    type = 'heading'
    def condition(self, block):
        return not '\n' in block and len(block) <= 70 and not block[-1] == ':'
class TitleRule(HeadingRule):
    type = 'title'
    first = True
    def condition(self, block):
        if not self.first: return False
        self.first = False
        return HeadingRule.condition(self, block)
class ListitemRule(Rule):
    type = 'listitem'
    def condition(self, block):
        return block[0] == '-'
    def action(self, block, handler):
        return handler.tag(self.type, block[1:].strip())
class ListRule(ListitemRule):
    type = 'list'
    listTable = []
    inside = False
    def condition(self, block):
        return True
    def action(self, block, handler):
        listItemCondition = ListitemRule.condition(self, block)
        
        if not self.inside and listItemCondition:
            self.listTable = []
            self.inside = True
        elif self.inside and not listItemCondition:
            self.inside = False
            return handler.tag(self.type, ''.join(self.listTable))
            
        if self.inside:
            self.listTable.append(handler.tag(ListitemRule.type, block[1:].strip()))
        else:
            return False

        return True
class ParagraghRule(Rule):
    type = 'paragragh'
    def condition(self, block):
        return True

