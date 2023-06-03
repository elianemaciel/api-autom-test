from assets import convertStories


def send_user_story(user_story_txt):
    try:
        #TODO: a lógica relatada a seguir, de exibir popup e mostrar a tela, não deve ser implementada aqui no Repository,
        # mas nas classes de UI
        testCases, warnings = convertStories.defineTestsFromStories(user_story_txt)
        #caso tenha ocorrido warnings, mostra a lista numa tela de warning, com opção de continuar ou de mudar o user story
        #caso tenha ocorrido warnings e o usuário optado por continuar, encaminha para tela de seleção de métodos
        #caso não tenha ocorrido erro, encaminha para tela de seleção dos métodos
    except:
        #Levanta error no popup e não muda de tela caso tenha ocorrido erro.
