import re
import warnings
from enum import Enum

import pt_core_news_md
from unidecode import unidecode

from assets.AutomTestException import AutomTestException

nlp = pt_core_news_md.load()

class TestCase:
    def __init__(self, className, method, parameters):
        self.className = className
        self.method = method
        self.parameters = parameters

class DescriptionStory:
    def __init__(self, role,feature,reason):
        self.role = role
        self.feature = feature
        self.reason = reason

class Acceptance:
    def __init__(self, premiss,parameters):
        self.premiss = premiss
        self.parameters = parameters


class AcceptanceCriteria:
    def __init__(self, given, when, then):
        self.given = given
        self.when = when
        self.then = then

class TagsAcceptance(Enum):
    GIVEN = 1
    WHEN = 2
    THEN = 3

def getAcceptanceCriterias(story):
    try:
        acceptanceCriterias = []
        given,when,then = None, None,None
        for itr, line in enumerate(story):
            if re.match(r"dado que",line.lower()):
                given = definePremise(story,itr)
            elif re.match(r"quando",line.lower()):
                when = defineAction(story,itr)
            elif re.match(r"então",line.lower()):
                then = defineOutcome(story,itr)
                acceptanceCriterias.append(AcceptanceCriteria(given, when, then))
                given,when,then = None, None,None
        return acceptanceCriterias
    except Exception as e:
        raise AutomTestException(e, "Unable to get acceptance criteria in user story")

def validateContent(returnedStory):
    if(len(returnedStory) >=1 and returnedStory[0] != ''):
        return True
    return False

def defineTestsFromStories(returnedStory):#TODO: este método, ao invés de levantar uma exception, trata a exception e retorna uma mensagem
    testCases = []
    warningsFromAccCriteria = []
    if validateContent(returnedStory):
        descriptionStory, acceptanceCriterias = definePartsStory(createArrayStory(returnedStory[0]))
        if acceptanceCriterias:
            testCases, warningsFromAccCriteria = defineTestsFromAcceptanceCritereas(testCases, acceptanceCriterias)
        if descriptionStory:
            testCases = defineClassForTests(testCases, descriptionStory.feature)
        for test in testCases:
            print(test.className, test.method, test.parameters)
    else:
        raise AutomTestException(message="Please insert the user story first")
    return testCases, warningsFromAccCriteria


def defineClassForTests(testCases, feature):
    try:
        feature = treatFeature(feature)
        for itr,test in enumerate(testCases):
            if test.className is None:
                testCases[itr].className = feature
        return testCases
    except Exception as e:
        raise AutomTestException(e, "Error when defining class for tests")

def treatFeature(feature):
    if feature is None or feature == '': return None
    return ''.join([str(p) for p in unidecode(feature.title()) if p.isalpha() or p.isalnum()])

def createArrayStory(story):
    return str.split(story,"\n")

def defineTestsFromAcceptanceCritereas(testCases, acceptanceCriterias):
    successTestCases = []#TODO: implementar e testar substituir o param
    errorAccCriteria = []
    for a in acceptanceCriterias:
        try:
            if a.given:
                testCases = addPremissToTest(testCases, a.given.premiss)
                testCases = addParameterToTest(testCases, a.given.parameters,a.given.premiss)
            if a.when:
                testCases = addPremissToTest(testCases, a.when.premiss)
                if a.when.parameters:
                    for parameter in a.when.parameters:
                        testCases = addParameterToTest(testCases, parameter,a.given.premiss if a.when.premiss is None else a.when.premiss)
            if a.then:
                testCases = addPremissToTest(testCases, a.then.premiss)
                if a.then.parameters:
                    for parameter in a.then.parameters:
                        testCases = addParameterToTest(testCases, parameter,a.then.premiss if a.then.premiss != None else a.when.premiss if a.when.premiss != None else a.given.premiss)
        except Exception as e:
            error_message = "Error when extracting data from the following acceptance criterion: " + a
            warnings.warn(error_message + e)
            errorAccCriteria.append(error_message)
    return testCases, errorAccCriteria


def addPremissToTest(testCases, premiss):
    if premiss is None:
        return testCases
    for t in testCases:
        if t.method == premiss:
            return testCases
    testCases.append(TestCase(None,premiss,None))
    return testCases

def addParameterToTest(testCases, parameter, premiss):
    if premiss is None or len(parameter) == 0:
        return testCases
    for itr,x in enumerate(testCases):
        if x.method == premiss:
            if testCases[itr].parameters is None:
                testCases[itr].parameters = [parameter]
            else:
                if parameter not in testCases[itr].parameters:
                    testCases[itr].parameters.append(parameter)
            return testCases
    return testCases


def definePartsStory(story):
    descriptionStory = getRoleFeatureReason(story)
    story = getStoryWithoutDescription(story)
    acceptanceCriterias = getAcceptanceCriterias(story)
    return descriptionStory,acceptanceCriterias


def getStoryWithoutDescription(story):
    try:
        linesToRemove = []
        for line in story:
            if searchKeysRole(line) or searchKeysFeature(line) or searchKeysReason(line):
                linesToRemove.append(line)
        return [s for s in story if s not in linesToRemove]
    except Exception as e:
        raise AutomTestException(e, "Unable to get user story after removing description")


def definePremise(story,itr):
    return Acceptance(getPremiseFromPhrase(story[itr]), getLinesField(story[itr:]))


def getPremiseFromPhrase(phrase):
    doc = nlp(phrase)
    if validateValidatorScenario(doc):
        return createMethodValidateScenario(doc)
    return createTestTitle(verifyImperative(phrase))

def verifyImperative(phrase):
    phrase = searchKeyGiven(phrase)
    doc = nlp(phrase)
    for itr,word in enumerate(doc):
        if word.pos_ == 'AUX':
            if doc[itr+1].pos_ != 'VERB':
                phrase = createImperative(word.lemma_, word.text,phrase)
                break
        elif word.pos_ in ['VERB']:
            phrase = createImperative(word.lemma_, word.text,phrase)
            break
        elif word.text.lower() == "logado":
            phrase = createImperative("logar",word.text,phrase)
            break
        elif word.text.lower() == "selecione":
            phrase = createImperative("selecionar",word.text,phrase)
            break
    return phrase

def createImperative(lemma,text,phrase):
    return "{} {}".format(lemma,re.search(r"(?<={}\s).*".format(text),phrase).group())

def defineAction(story,itr):
    return Acceptance(treatWhen(story[itr]), getLinesField(story[itr:]))


def defineOutcome(story,itr):
    return Acceptance(None,getLinesField(story[(itr):]))

def verifyFields(field):
    doc = nlp(field)
    if getVerbAndTagsFields(doc) or verifyTagField(doc) or validateRegisterScenario(doc):
        return True

def verifyTagField(doc):
    for word in doc:
        if word.lemma_ == 'campo':
            return True
    return None


def getLinesField(story):
    fields = []
    for iter,x in enumerate(story):
        if (not verifyFields(x) and not re.match("e",x.lower())):
            continue
        TratedFields = getArrayFields(x)
        if TratedFields:
            fields.extend(TratedFields)
        if len(story) > iter+1 and validateEndOfBlock(story[iter+1]):
            break
    return treatFields(fields)

def validateEndOfBlock(line):
    if line.strip() == '':
        return True
    startBlocks = ['cenário','scenario','dado que',"então","quando"]
    for s in startBlocks:
        if re.match(s,line.lower()):
            return True
    return None

def treatFields(fields):
    fields = [unidecode(''.join([str(p) for p in field.title() if p.isalpha() or p.isalnum()])) for field in fields]
    return [field[0].lower() + field[1:] for field in fields if field.strip() != '']


def getArrayFields(field):
    if field == '': return None
    if re.match(r"\"",field):
        return [unidecode(re.search(r"(?<=\")[A-z|\s|\-]+(?=\(([^)]+)\)|\")",field).group().strip())]
    if re.search(r"(?<=campo\s\").*",field):
        word = re.search(r"campo.*",field).group()
        return [unidecode(re.search(r"(?<=\")[A-z|\s|\-]+(?=\(([^)]+)\)|\")",word).group().strip())]
    return getFieldWidthoutTags(field)

def getFieldWidthoutTags(field):
    doc = nlp(field)
    verbAndtag = getVerbAndTagsFields(doc)
    if verbAndtag:
        textAfterVerbAndTag = re.search(r"(?<=\s{}).*".format(verbAndtag),field.lower()).group().strip()
        if existsMultipleFieldsBetweenComma(textAfterVerbAndTag):
            return getMultipleFieldsBetweenComma(textAfterVerbAndTag)
        else:
            field = getNounAfterVerbFeature(nlp(textAfterVerbAndTag))
            if field is None or field == '':
                return [s.strip() for s in re.findall(r"(?<={}\s)[A-zÀ-ú-\/]+".format(verbAndtag),unidecode(field.lower()))]
            else:
                return [field]
    elif re.match(r"e\s",field.lower()):
        return getFieldWithoutVerb(doc)
    return None

def getFieldWithoutVerb(doc):
    if doc[0].pos_ == "CCONJ" and doc[1].pos_ in["DET","NUM"]:
        return [unidecode(re.search(r"(?<={}\s)[\w\/]+\s?[\w\/ ]+".format(doc[1].text),doc.text.lower()).group().strip())]
    return None

def existsMultipleFieldsBetweenComma(field):
    if "," in field or re.search(r"\se\s",field):
        return True

def getVerbAndTagsFields(doc):
    for itr,word in enumerate(doc):
        #é necessário colocar o selecione po uma limitação do spacy
        if word.lemma_ in ["enviar","preencher","salvar", "selecionar", "selecione", "informar","digitar","guardar","inserir"]:
            if len(doc) > itr+1 and doc[itr+1].pos_ in ["NOUN","PRON","DET","NUM"]:
                return "{} {}".format(word.text,doc[itr+1].text)
    return None

def getMultipleFieldsBetweenComma(field):
    return removeConnectives([''.join(s) for s in re.findall(r"([\w\/]+\s?[\w\/ ]+(?=\,|\se\s))|(?:((?<=e\s)[\w\/]+\s?[\w\/\s]+)|((?<=\,\s)[\w\/]+\s?[\w\/\s]+))",unidecode(field))])

def removeConnectives(fields):
    newFields = []
    for field in fields:
        doc = nlp(field)
        newField = ''
        for word in doc:
            if word.pos_ != "DET":
                newField += " " + word.text
        newFields.append(newField.strip())
    return newFields

def searchKeyGiven(phrase):
    return re.search(r"(?<=dado que\s).*|(?<=e\s).*",phrase.lower()).group().strip()


def searchKeyWhen(phrase):
    return re.search(r"(?<=quando\s).*|(?<=e\s).*",phrase.lower()).group().strip()

def searchKeyThen(phrase):
    return re.search(r"(?<=então\s).*|(?<=e\s).*",phrase.lower()).group().strip()


def treatWhen(phrase):
    doc = nlp(phrase)
    if validateValidatorScenario(doc):
        return createMethodValidateScenario(doc)
    if validateUniquenessScenario(doc):
        return createMethodUniquenessScenario(doc)
    if validateRegisterScenario(doc):
        return createMethodRegisterScenario(doc)
    return None

def validateValidatorScenario(doc):
    return len([word.lemma_ for word in doc if word.lemma_ in ["válido","inválido","incorreto","vazio"]]) > 0

def createMethodUniquenessScenario(doc):
    verbAndTag = getVerbAndTagsFields(doc)
    if verbAndTag:
        field = [s.strip() for s in re.findall(r"(?<={}\s)[A-zÀ-ú-\/]+".format(verbAndTag),unidecode(doc.text.lower()))]
        return createTestTitle("Validar {}".format(field[0]))
    return None

def validateUniquenessScenario(doc):
    expressions = ["já associado","previamente associado","duplicado","já cadastrado","previamente cadastrado","já existente","já informado"]
    return len([s for s in expressions if s in doc.text]) > 0

def hasNegativeValidation(doc):
    verbAndTag = getVerbAndTagsFields(doc)
    if verbAndTag:
        return "não" in re.search(r".*(?=\s{})".format(verbAndTag),doc.text).group().lower()

def createMethodValidateScenario(doc):
    verbAndTag = getVerbAndTagsFields(doc)
    if verbAndTag:
        field = [s.strip() for s in re.findall(r"(?<={}\s)[A-zÀ-ú-\/]+".format(verbAndTag),unidecode(doc.text.lower()))]
        return createTestTitle("Validar {}".format(field[0]))
    return None

def createMethodRegisterScenario(doc):
    phrase = searchKeyWhen(doc.text)
    for word in doc:
        if word.pos_ in ['VERB','AUX']:
            if word.lemma_ in ['desejar','estar',"dever"]:
                phrase = re.search(r"(?<=desejar\s).*|(?<=estiver\s).*|(?<=deve\s).*",phrase.lower()).group().strip()
            else:
                phrase = phrase.replace(word.text,word.lemma_,1).title()
    return createTestTitle(phrase)

def createTestTitle(phrase):
    if phrase is None or phrase == '': return None
    doc = nlp(phrase)
    for word in doc:
        if word.pos_ in ["DET","NUM", "ADP"]:
            phrase = re.sub(r"\b{}\b\s+".format(word.text),"",phrase)
    return unidecode('{}'.format(''.join([str(p) for p in phrase.title() if p.isalpha() or p.isalnum()])))

def searchKeyAuxWhen(phrase):
    return re.search(r"(?<=desejar\s).*|(?<=estiver\s).*",phrase.lower()).group().strip()


def validateRegisterScenario(doc):
    for word in doc:
        if word.pos_ in ["VERB", "NOUN"] :
            if word.lemma_  in ['cadastrar',"registrar",'inserir']:
                return True
    return False


def getRoleFeatureReason(story):
    try:
        role = defineRole(story)
    except Exception as e:
        raise AutomTestException(e, "Unable to get role defined in user story")
    try:
        feature = defineFeature(story) #TODO: esse carinha tem um espaço em branco
    except Exception as e:
        raise AutomTestException(e, "Unable to get user story feature")
    try:
        reason = defineReason(story)
    except Exception as e:
        raise AutomTestException(e, "Unable to get user story reason")
    return DescriptionStory(role, feature, reason)

def defineRole(description):
    for des in description:
        phrase = removeKeysRole(des)
        if phrase:
            return nlpRole(phrase)
    return None


def nlpRole(phrase):
    doc = nlp(phrase)
    for word in doc:
        if word.pos_ in ['ADP','AUX','CCONJ','DET','NUM','PART','PRON','SCONJ']:
            phrase = re.sub(word.text,"",phrase,1)
        else:
            break
    return phrase.strip()

def removeKeysRole(line):
    if searchKeysRole(line):
        return re.search(r"(?<=como\s).*|(?<=enquanto\s).*",line.lower()).group()


def searchKeysRole(line):
    return re.match(r"(como\s)|(como um\s)|(enquanto\s)|(enquanto um\s)|(eu como\s)|(eu como um\s)|(eu, como\s)|(eu, como um\s)",line.lower())

def defineFeature(description):
    for des in description:
        phrase = removeKeysFeature(des)
        if phrase:
            return nlpFeature(phrase)
    return None


def removeKeysFeature(line):
    if searchKeysFeature(line):
        return re.search(r"(?<=quero\s).*|(?<=preciso\s).*|(?<=desejo\s).*|(?<=gostaria de\s).*",line.lower()).group()
    return None


def searchKeysFeature(line):
    return re.match(r"(quero\s)|(preciso\s)|(desejo\s)",line.lower())


def nlpFeature(phrase):
    doc = nlp(phrase)
    for itr,word in enumerate(doc):
        if word.pos_ == 'VERB':
            return getNounAfterVerbFeature(doc[itr:])
    return phrase.strip()

def getNounAfterVerbFeature(doc):
    nouns = ''
    for word in doc:
        if word.pos_ in ['NOUN', 'ADJ']:
            if word.lemma_ not in ["válido","inválido","incorreto","vazio"]:
                nouns = nouns + ' ' + word.text
        elif word.pos_ in ["DET"]:
            continue
        elif nouns != '':
            return nouns
    return nouns.strip()

def defineReason(description):
    for des in description:
        phrase = removeKeysReason(des)
        if phrase:
            return nlpReason(phrase)
    return None


def nlpReason(phrase):
    doc = nlp(phrase)
    for word in doc:
        if word.pos_ in ['PRON','DET',]:
            phrase = re.sub(word.text,"",phrase,1)
        elif  word.pos_ == 'VERB':
            return re.sub(word.text,word.lemma_,phrase,1).strip()
    return phrase.strip()

def removeKeysReason(line):
    if searchKeysReason(line):
        return re.search(r"(?<=para que\s).*|(?<=porque\s).*",line.lower()).group()

def searchKeysReason(line):
    return re.match(r"(para que\s)|(porque\s)",line.lower())
