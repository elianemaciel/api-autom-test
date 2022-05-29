from assets.components import Method
import assets.layout as layout, assets.procedures as p
import PySimpleGUI as sg

class MethodInformation:

    def __init__(self, className='', packageName='', method='', parameters='', outputType=''):
        self.className = className
        self.packageName = packageName
        self.method = method
        self.parameters = parameters
        self.outputType = outputType

def filltestsMUT(t):
    MUT = Method()
    MUT.name = t.method
    MUT.class_name = t.className
    MUT.package_name = t.packageName
    MUT.output_type = t.outputType
    if t.parameters:
        for param in t.parameters:
            MUT.add_param_by_arg(param)
    return MUT

def viewInputDataScreen(MUT,home):
	desactivateFristScreen(home)
	win2 = sg.Window('Input data', layout.newLayoutVisualizarDados(MUT), finalize=True, element_justification='center')
	while (True):
		ev2, vals2 = win2.Read()
		if (ev2 is None or ev2 == 'Back'):
			activateFirstScreen(win2,home)
			break

def desactivateFristScreen(home):
	win2_active = True
	home.Hide()

def activateFirstScreen(win,home):
	win.Close()
	home.UnHide()

def validateMethodInformation(vals2):
	if (vals2['className'] !="" and vals2['methodName'] !="" and vals2['parameters'] !="" and vals2['Tipo']!=""):
		if (p.confere_entrada_params(vals2['parameters'])):
			return True
		else:
			sg.popup_quick_message('Parameters incorrectly filled in.')
			return False
	else:
		sg.popup_quick_message('Please fill in all required fields.')
		return False

def setMethodInformation(MUT, home):
	win2 = sg.Window('Set method information', layout.newLayoutInfoMetodo(MUT), finalize=True, element_justification='center')
	win2['Tipo'].update(set_to_index=p.get_tipoSaida_index(MUT))
	while (True):
		ev2, vals2 = win2.Read()
		if (ev2 is None or ev2 == 'Cancel'):
			activateFirstScreen(win2,home)
			break
		if (ev2 == 'Next'):
			if validateMethodInformation(vals2):
				MUT = filltestsMUT(MethodInformation(vals2['className'],vals2['packageName'],vals2['methodName'],vals2['parameters'].replace(" ", "").split(','),vals2['Tipo']))
				win2.close()
				MUT = InformTypesOfParameters(MUT,home)
				home['B1'].update(disabled=False)
				home['B3'].update(disabled=False)
				home['B2'].update('Method information defined ✓')
	return MUT 

def InformTypesOfParameters(MUT,home):
	win2 = sg.Window('Inform types of parameters', layout.newLayoutTiposParams(MUT), finalize=True, element_justification='center')
	while (True):
		ev2, vals2 = win2.Read()
		if (ev2 is None or ev2 == 'Back'):
			activateFirstScreen(win2,home)
			break

		if (ev2 == 'Next'):
			valida = True
			for x in range(0,len(vals2)):
				if (vals2[x] == ''):
					valida = False
					break
			if (valida):
				for x in range(0,len(MUT.params)):
					MUT.params[x].type_name = vals2[x]
				activateFirstScreen(win2,home)
				break
			else:
				sg.popup_quick_message('Please fill out all fields.')
			break
	return MUT