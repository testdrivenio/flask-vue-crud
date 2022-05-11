import pickle

def setVarFromFile(varName,varValue):
    file = open(varName, 'wb')
    pickle.dump(varValue, file)
    file.close()

def getVarFromFile(varName):
    file = open(varName, 'rb')
    varName = pickle.load(file)
    file.close()
    return varName