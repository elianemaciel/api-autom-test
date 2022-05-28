from assets.actionScreen import filltestsMUT, MethodInformation, setMethodInformation

def removeUnselectedMethods(testCases, vals3):
    selectedTests = [key for key,value in vals3.items() if value == True]
    return [test for test in testCases if test.method in selectedTests]

def generateTest(test,home):
    return filltestsMUT(MethodInformation(test.className, '', test.method, test.parameters,''))