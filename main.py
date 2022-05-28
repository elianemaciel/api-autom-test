import PySimpleGUI as sg
from assets.components import Method, TestSet, Parameter, ParamRange
from assets.generator import *
import assets.layout as layout, assets.procedures as p
from assets.convertStories import *
from assets.fillMethodsAndEquivalenceClass import *
from assets.actionScreen import *

sg.theme('SystemDefault1')

# MUT = Method Under Test
MUT = Method()

testeAtual = 1 
totalTestes = 1 

home = sg.Window('AutomTest', layout.home, finalize=True, element_justification='center')
home['B1'].update(disabled=True)
home['B3'].update(disabled=True)
home['B4'].update(disabled=True)
win2_active=False

def defineTestsFromExtractedStories(testCases,home):
    win3 = sg.Window('Select Tests From Extrated Methods', layout.newConvertedStory(testCases), finalize=True, element_justification='center')
    while (True):
        ev3, vals3 = win3.Read()
        if (ev3 is None or ev3 == 'Back'):
            activateFirstScreen(win3,home)
            break
        elif(ev3 == 'Confirm'):
            if vals3:
                testCases = removeUnselectedMethods(testCases, vals3)
                win3.close()
                MUT, testCases = iterateMethods(testCases,home)
    return MUT, testCases

def iterateMethods(testCases,home):
    global testeAtual, totalTestes

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

    return MUT, testCases

while (True):
    ev1, vals1 = home.Read()
    if ev1 is None:
        break

    # Botão 1 - View Input data
    if (ev1 == 'B1' and not(win2_active)):
        viewInputDataScreen(MUT,home)
    # Botão 2 - Definir Informações do Método
    elif (ev1 == 'B2' and not(win2_active)):
        desactivateFristScreen(home)
        MUT = setMethodInformation(MUT, home)

    # Botão 3 - Especificar Conjuntos de Teste
    if (ev1 == 'B3' and not(win2_active)):
        win2_active = True
        home.Hide()
        win2 = sg.Window('Specification of test suites', layout.newLayoutConjuntosTeste(MUT), finalize=True, element_justification='center')
        #disable_minimize=True,#disable_close=True,
        while (True):
            ev2, vals2 = win2.Read()

            if (ev2 is None or ev2 == 'Back'):
                win2.Close()
                win2_active = False
                home.UnHide()
                break

            elif (ev2 == 'Remove'):
                if (len(vals2[0]) > 0):
                    MUT.remove_from_test_set_list( vals2[0][0] )
                    win2.Close()
                    home.Hide()
                    if (len(MUT.testsets)==0):
                        home['B4'].update(disabled=True)
                        home['B3'].update('Specification of test suites')
                    win2 = sg.Window('Specification of test suites', layout.newLayoutConjuntosTeste(MUT), finalize=True, element_justification='center')

            elif (ev2 == 'Params'): # Vai para janela de Especificar Parâmetros
                par = Parameter("expected_output", MUT.params[0].type_name)
                if (MUT.output_type == 'boolean' or MUT.output_type == 'char'):
                    ppp = ParamRange(par,vals2[4])
                    vals2[5] = ''
                    vals2[6] = ''
                elif (MUT.output_type == 'String'):
                    ppp = ParamRange(par,vals2[4],vals2[5])
                    vals2[6] = ''
                else: # int / double / float / Date
                    ppp = ParamRange(par,vals2[3],vals2[4],vals2[5])

                if (p.telaInicialConjTesteCorreta(vals2[2],vals2[3]) and p.entradaTipoCorreta(MUT.output_type,vals2[4],vals2[5],'')):
                    test = TestSet(vals2[2], int(vals2[3]),ppp)
                    win3_active = True
                    win2.Hide()
                    win3 = sg.Window('Parameters of the new test suite', layout.newLayoutEspecificarParam(MUT, vals2[2]),
                        finalize=True, element_justification='center')
                    while (True):
                        ev3, vals3 = win3.Read()

                        if (ev3 is None or ev3 == 'Cancelar'):
                            if ( len(MUT.testsets) > 0 ):
                                MUT.testsets.pop()
                            win3.Close()
                            win2.UnHide()
                            win3_active = False
                            break

                        elif (ev3 == 'Confirmar'):
                            cont = 0
                            valida = True
                            for x in range(0,len(MUT.params)):
                                if (MUT.params[x].type_name == 'boolean' or MUT.params[x].type_name == 'char'):
                                    if( p.entradaTipoCorreta(MUT.params[x], vals3[cont]) ):
                                        par = Parameter(MUT.params[x].name, MUT.params[x].type_name)
                                        pr = ParamRange(par, vals3[cont])
                                        test.add_param_range(pr)
                                        cont += 1
                                    else:
                                        test.clear_params()
                                        valida = False
                                        break
                                elif (MUT.params[x].type_name == 'String'):
                                    if( p.entradaTipoCorreta(MUT.params[x], vals3[cont], vals3[cont+1]) ):
                                        par = Parameter(MUT.params[x].name, MUT.params[x].type_name)
                                        pr = ParamRange(par, vals3[cont], vals3[cont+1])
                                        test.add_param_range(pr)
                                        cont += 2
                                    else:
                                        test.clear_params()
                                        valida = False
                                        break
                                else: # int / float / double / Date
                                    if( p.entradaTipoCorreta(MUT.params[x], vals3[cont], vals3[cont+1], vals3[cont+2]) ):
                                        par = Parameter(MUT.params[x].name, MUT.params[x].type_name)
                                        pr = ParamRange(par, vals3[cont], vals3[cont+1], vals3[cont+2])
                                        test.add_param_range(pr)
                                        cont += 3
                                    else:
                                        test.clear_params()
                                        valida = False
                                        break

                            if (valida):
                                MUT.add_testset(test)
                                win3.Close()
                                win3_active = False
                                win2.Close()
                                home.Hide()
                                home['B4'].update(disabled=False)
                                home['B4'].update(button_color=('white','#006400'))
                                home['B3'].update('Specified test suites ✓')
                                win2 = sg.Window('Specification of test suites', layout.newLayoutConjuntosTeste(MUT), finalize=True, element_justification='center')
                                break

    # Botão 4 - GERAR TESTES
    if (ev1 == 'B4' and not(win2_active)):
        generate_tests( MUT )
        if (testCases):
            MUT, testCases = iterateMethods(testCases,home)

    # Botão 5 - Sobre AutomTest
    if (ev1 == 'B5' and not(win2_active)):
        win2_active = True
        home.Hide()
        win2 = sg.Window('About AutomTest', layout.newLayoutSobre(), finalize=True, element_justification='center')
        #disable_minimize=True,#disable_close=True,
        while (True):
            ev2, vals2 = win2.Read()
            if (ev2 is None or ev2 == 'Back'):
                win2.Close()
                win2_active = False
                home.UnHide()
                break
    
    # Botão 6 - Adicionar histórias de usuário
    if (ev1 == 'B6' and not(win2_active)):
        home.Hide()
        win2 = sg.Window('Upload User stories', layout.newUserStory(), finalize=True, element_justification='center')
        while (True):
            ev2, vals2 = win2.Read()
            if (ev2 is None or ev2 == 'Cancel'):
                activateFirstScreen(win2,home)
                break
            elif(ev2 == 'Next'):
                testCases = defineTestsFromStories(vals2)
                totalTestes = len(testCases)
                win2.close()
                MUT, testCases = defineTestsFromExtractedStories(testCases,home)
                activateFirstScreen(win2,home)
                home['B6'].update(disabled=True)

print('\n******************** Data ********************\n')
print(MUT)
