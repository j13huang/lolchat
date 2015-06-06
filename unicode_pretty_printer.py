# coding=utf8

import pprint

class UnicodePrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        #print object, object.encode('utf-8') if isinstance(object, unicode) else ''
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)

