import sys,PySimpleGUI as sg
sys.path.append('../automtest/assets')
import layout, random, procedures as p
from components import TestSet

home = [      
	[sg.Button('View input data', size=(40, 3), font='Default 12 bold', key='B1')],
	[sg.Button('Set method information', size=(40, 3), font='Default 12 bold', key='B2')],
	[sg.Button('Specify equivalence classes', size=(40, 3), font='Default 12 bold', key='B3')],
	[sg.Button('Generate tests', size=(40, 3), font='Default 12 bold', key='B4')],
	[sg.Button('Convert User Storie to Test Case', size=(40, 3), font='Default 12 bold', key='B6')],
	[sg.Button('About AutomTest', size=(40, 3), font='Default 12 bold', key='B5')]
]

def newLayoutInfoMetodo(MUT):
	all_params = ''
	for x in range(0,len(MUT.params)):
		if (x == 0):
			all_params += MUT.params[x].name
		else:
			all_params += ','+MUT.params[x].name

	content = [
		[sg.Text('Classe name *', size=(16, 1)), sg.InputText(MUT.class_name, size=(30, 1))],
		[sg.Text('Package name', size=(16, 1)), sg.InputText(MUT.package_name, size=(30, 1))],
		[sg.Text('Method name *', size=(16, 1)), sg.InputText(MUT.name, size=(30, 1))],
		[sg.Text('Parameters *', size=(16, 1)), sg.InputText(all_params, size=(30, 1))],
		[sg.Text('Output type *', size=(16, 1)),
			sg.InputCombo(['int', 'String', 'float', 'double', 'char', 'boolean', 'Date'], size=(28, 1), key='Tipo', enable_events=True, readonly='True')],
		[sg.Text('')], #quebra de linha
		[sg.Button("Next", key='Next'), sg.Button("Cancel")]
	]
	return content

def newUserStorie():

	content = [
		[sg.Text('User Storie', size=(16, 1)), sg.Multiline("""Descrição da história
Como um desenvolvedor
Quero utilizar o código base de cadastro de usuários 
Para que eu possa utilizar o mesmo a partir de adequações de acordo a necessidade do sistema

Critérios de aceitação
A funcionalidade de cadastro de usuário deverá se implementada seguindo as regras abaixo: 

Dado que o usuário esteja logado no sistema 
Quando desejar cadastrar um usuário no sistema
Então o sistema disponibilizará que sejam preenchidos os campos abaixo:
"Nome completo (obrigatório)"
"E-mail (obrigatório)"
"CPF (obrigatório)"
"Telefone (obrigatório)" 
E selecione dentre as opções de perfis já cadastrados, exibidas no campo "Perfil"
E selecione dentre as opções "Controle pelo LDAP", "Controle pela aplicação" para o campo "Forma de acesso".

Dado que o usuário esteja cadastrando um usuário para o sistema 
E adicionar ao campo "Nome completo" símbolos (exceto apóstrofo) ou números
Então o sistema deverá destacar o campo em vermelho 
E exibirá a mensagem: Este Nome está inválido 

Dado que o usuário esteja cadastrando um usuário no sistema
Quando adicionar um dado em formato inválido para os campos de E-mail, CPF ou Telefone
Então o sistema deverá destacar o campo em vermelho
E exibirá a mensagem: "Este [nome do campo] está inválido"

Dado que o usuário esteja alterando uma informação inválida
Quando corrigi-la
Então o sistema deverá remover o destaque do campo
E removerá a mensagem referente a esta.

Dado que o usuário esteja cadastrando um usuário no sistema
Quando adicionar um E-mail, CPF ou Telefone já cadastrado no sistema 
Então o sistema deverá destacar o campo em vermelho
E exibirá a mensagem: "Este [nome do campo] já está sendo utilizado por outro usuário "

# Formas de acesso 

Dado que o usuário selecione a forma de acesso "Controle pelo LDAP"
Quando salvar o cadastro do usuário com sucesso
Então o sistema deverá enviar um e-mail para o usuário cadastrado confirmando o cadastro.

Dado que o usuário selecione a forma de acesso "Controle pela aplicação"
Quando salvar o cadastro do usuário com sucesso
Então o sistema deverá enviar um e-mail para o usuário cadastrado confirmando o cadastro
E enviará um link para a definição de senha

# Auditoria
Dado que o usuário esteja cadastrando um usuário 
Quando a operação ocorrer com sucesso
Então o sistema deverá salvar a data, hora e informação do usuário que realizou a operação 
""",size=(40, 16))],
		[sg.Text('')], #quebra de linha
		[sg.Button("Next", key='Next'), sg.Button("Cancel")]
	]
	return content

def newLayoutTiposParams(MUT):
	content = [[sg.Text('Type of '+MUT.params[x].name, size=(16, 1)),
				sg.InputCombo(['int', 'String', 'float', 'double', 'char', 'boolean', 'Date'],
					size=(28, 1), enable_events=True, readonly='True')] for x in range(len(MUT.params))]
	content += [[sg.Button("Next", key='Next'),sg.Button("Back",tooltip='Back to Home Screen')]]
	return content

def newLayoutVisualizarDados(MUT):
	headings1 = ['Class','Package','Method','Type of Output']
	data1 = [[MUT.class_name, MUT.package_name, MUT.name, MUT.output_type ]]
	
	headings2 = ['Method parameter','Type']
	data2 = []
	for x in range(0,len(MUT.params)):
		data2 += [[[MUT.params[x].name]] +  [[MUT.params[x].type_name]]]
	
	content = [
		[sg.Text('')], #quebra de linha
		[sg.Table(values=data1,headings=headings1,justification='center',auto_size_columns=True,
			key='table1',hide_vertical_scroll=True,num_rows=1)],
		[sg.Text('')], #quebra de linha
		[sg.Table(values=data2,headings=headings2,justification='center',auto_size_columns=True,
			key='table2',hide_vertical_scroll=True,num_rows=len(MUT.params))],
		[sg.Text('')], #quebra de linha
		[sg.Button("Back")]
	]
	return content

def newLayoutTipo( tipo ):
	content = []
	if (tipo == 'String'):
		content += [
			[sg.Text('Substrings'),sg.InputText('', size=(30, 1))],
			[sg.Text('Substrings sizes'),sg.InputText('', size=(30, 1))]
		]
	elif (tipo == 'char'):
		content += [[sg.Text('Include:'),sg.InputText('', size=(30, 1))]]
	elif (tipo == 'boolean'):
		content += [[sg.InputCombo(['True', 'False'], size=(28, 1), enable_events=True, readonly='True')]]
	elif (tipo == 'Date'):
		content += [
			[sg.Text('From'),sg.InputText('', size=(10, 1)),sg.Text('to'),sg.InputText('', size=(10, 1))],
			[sg.Text('Include:'),sg.InputText('', size=(10, 1))],
		]
	else: # int / float / double
		content += [
			[sg.Text('From'),sg.InputText('', size=(10, 1)),sg.Text('to'),sg.InputText('', size=(10, 1))],
			[sg.Text('Include:'),sg.InputText('', size=(10, 1))],
		]
	return content

def newLayoutConjuntosTeste(MUT):
	#lists = ['Listbox 1', 'Listbox 2', 'Listbox 3', 'Listbox 4']
	lists = []
	for x in range(0,len(MUT.testsets)):
		lists += [MUT.testsets[x].name]

	col = [
		[sg.Text('Equivalence classes:')],
		[sg.Listbox(values=(lists), size=(18,7), no_scrollbar=True, enable_events=True)],
		[sg.Button("Remove")]
	]
	col2 = [
		[sg.Text('New equivalence class',font='Default 10 bold underline')],
		[sg.Text('Equivalence class name:'), sg.InputText('', size=(20,1))],
		[sg.Text('Number of test cases to generate: '), sg.InputText('', size=(5, 1))],
		[sg.Text('')], #quebra de linha
		[sg.Text('Expected output ('+MUT.output_type+'):', size=(25, 1),font='Default 12',justification='center')]
	]
	
	col2 += newLayoutTipo(MUT.output_type)
	col2 += [sg.Text(' ')],[sg.Button("Specify parameters", key='Params'),sg.Button("Back")]

	return [[sg.Column(col),sg.VerticalSeparator(pad=None),sg.Column(col2)]] #divisor vertical

def newLayoutEspecificarParam(MUT,nome_conj_teste):

	tab_layout = []
	all_tabs = []

	for x in range(0,len(MUT.params)):
		tab_layout.append( [sg.Tab('Range of '+MUT.params[x].name+' ('+MUT.params[x].type_name+')', newLayoutTipo(MUT.params[x].type_name ))] )

	for x in range(0,len(MUT.params)):
		all_tabs += tab_layout[x]

	return [
		[sg.Text('Equivalence class: '+nome_conj_teste, font='Default 11 bold')],
		[sg.TabGroup( [all_tabs])],
		[sg.Button("Confirm", key='Confirmar'),sg.Button("Cancel")]
	]

def newLayoutSobre():
	content = [
		[sg.Image(data=p.get_img_data('../automtest/assets/img/logo.jpg', first=True))],
		[sg.Text('AutomTest', font='Default 12 bold')],
		[sg.Text('')], #quebra de linha
		[sg.Text('Test case generator for JUnit based on\nfunctional requirements specifications.', font='Default 12')],
		[sg.Text('')], #quebra de linha
		#[sg.Text('Desenvolvido por',font='Default 12'),sg.Button('Daniel David Fernandes',border_width=0, font='Default 12', key='aboutme', button_color=('white',sg.theme_background_color()))],
		[sg.Text('2019 - 2020', font='Default 12')],
		[sg.Text('')], #quebra de linha
		[sg.Button("Back")]
	]
	return content

#horizontal line: sg.Text('_'*30)
#justification='center', size=(10, 1)