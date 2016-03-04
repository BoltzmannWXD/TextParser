__metaclass__ = type
class Handler:
    def callback(self, prefix, name, *args):
        method = getattr(self, prefix+name, None)
	if callable(method): return method(*args)

    def sub(self, name):
        def substitution(match):
	    result = self.callback('sub_', name, match)
	    if result is None: result = match.group(0)
	    return result
	return substitution

class HTMLRenderer(Handler):
    documents = {'paragragh': 'p',
                 'heading': 'h2',
                 'list': 'ul',
                 'listitem': 'li',
                 'title': 'title',
                 'body': 'body',
                 'head': 'head',
                 'document': 'html'
     }
    def document(self, body, title='...'):
        return '<html><head><title>%s</title></head><body>%s</body></html>' % (title, body)
    def tag(self, type, content):
        tag = self.documents.get(type)
        if not tag: raise TypeError,'There are no %s.' % type
        return '<%(tag)s>%(content)s</%(tag)s>' % {'tag': tag, 'content': content}
    def sub_emphasis(self, match):
        return '<em>%s</em>' % match.group(1)
    def sub_url(self, match):
        return '<a href="%s">%s</a>' % (match.group(1), match.group(1))
    def sub_mail(self, match):
        return '<a href="mailto:%s">%s</a>' % (match.group(1), match.group(1))
