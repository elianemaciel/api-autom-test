from unittest import TestCase
import PySimpleGUI as sg
from assets.actionScreen import filltestsMUT, MethodInformation, activateFirstScreen
import assets.layout as layout

def removeUnselectedMethods(testCases, vals3):
    selectedTests = [key for key,value in vals3.items() if value == True]
    return [test for test in testCases if test.method in selectedTests]

def generateTest(test,home):
    return filltestsMUT(MethodInformation(test.className, '', test.method, test.parameters,''))

def defineTestsFromExtractedStories(MUT, testCases, home, testeAtual, totalTestes ):
    win3 = sg.Window('Select Tests From Extrated Methods', layout.newConvertedStory(testCases), finalize=True, element_justification='center')
    while (True):
        ev3, vals3 = win3.Read()
        if (ev3 is None or ev3 == 'Back'):
            activateFirstScreen(win3,home)
            break
        elif(ev3 == 'Confirm'):
            if vals3:
                testCases = removeUnselectedMethods(testCases, vals3)
                totalTestes = len(testCases)
                win3.close()
                if totalTestes > 0:
                    MUT, testCases, testeAtual = iterateMethods(testCases,home, testeAtual,totalTestes)
    return MUT, testCases, testeAtual, totalTestes 

def iterateMethods(testCases, home, testeAtual, totalTestes):
    MUT = generateTest(testCases[0],home)
    del testCases[0]
    home['B4'].update('Generate tests ({}/{})'.format(testeAtual,totalTestes))
    if testeAtual < totalTestes:
        testeAtual = testeAtual + 1

    home['B1'].update(disabled=True)
    home['B2'].update('Set method information')
    home['B3'].update(disabled=True)
    home['B3'].update('Specify equivalence classes')
    home['B4'].update(disabled=True)
    home['B4'].update(button_color=('white','#283b5b'))

    return MUT, testCases, testeAtual

def updateClassOfTestCases(class_name, testCases):
    for itr,test in enumerate(testCases):
        testCases[itr].className = class_name
    return testCases