import sgf
with open("../trainingData/extracted/kgs-19-2007/2007-01-01-1.sgf") as f:
    collection = sgf.parse(f.read())
    for child in collection.children:
        for node in child.nodes:
            print(node.properties)