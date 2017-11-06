# sgfParser.py
# parses sgf files, need to get posistions + next move
# from an sgf game

import sgf

class ParseSGF:
    def __init__(self, filename):
        self.file = open(filename)
        self.collection = sgf.parse(self.file.read())
        
    def printNodes(self):
        for child in self.collection.children:
            for node in child.nodes:
                print(node.properties)
def testParseSGF():
    filename = "../trainingData/extracted/kgs-19-2007/2007-01-01-1.sgf"
    test = ParseSGF(filename)
    test.printNodes()

if __name__ == '__main__':
    testParseSGF()
