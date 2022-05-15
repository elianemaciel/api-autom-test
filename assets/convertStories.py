from cmath import log
from enum import Enum
from itertools import tee
from sre_constants import FAILURE, SUCCESS
from unidecode import unidecode
from turtle import xcor
import pt_core_news_sm
import re

nlp = pt_core_news_sm.load()

testCases = []

class TestCase:
    def __init__(self, classMethod, method, parameters):
        self.classMethod = classMethod
        self.method = method
        self.parameters = parameters

class DescriptionStorie:
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

def validateContent(returnedStorie):
    if(len(returnedStorie) >=1 and returnedStorie[0] != ''):
        return True
    return False

def defineTestsFromStories(returnedStorie):
    if(validateContent(returnedStorie)):
        descriptionStorie,acceptanceCriterias = definePartsStorie(createArrayStorie(returnedStorie[0]))
        if acceptanceCriterias:
            defineTestsFromAcceptanceCritereas(acceptanceCriterias)
        if descriptionStorie:
            defineClassForTests(descriptionStorie.feature)
        for test in testCases:
            print(test.classMethod, test.method, test.parameters)
    return testCases


def defineClassForTests(feature):
    feature = treatFeature(feature)
    for itr,test in enumerate(testCases):
        if test.classMethod is None:
            testCases[itr].classMethod = feature
    return testCases

def treatFeature(feature):
    return createTestTitle(feature)

def createArrayStorie(storie):
    return str.split(storie,"\n")

def defineTestsFromAcceptanceCritereas(acceptanceCriterias):
    for a in acceptanceCriterias:
        if a.given:
            addPremissToTest(a.given.premiss) 
            addParameterToTest(a.given.premiss,a.given.parameters)
        if a.when:
            addPremissToTest(a.when.premiss)
            if a.when.parameters:
                for x in a.when.parameters:
                    addParameterToTest(x,a.given.premiss if a.when.premiss == None else a.when.premiss)
        if a.then:
                addPremissToTest(a.then.premiss)
                if a.then.parameters:
                    for x in a.then.parameters:
                        addParameterToTest(x,a.then.premiss if a.then.premiss != None else a.when.premiss if a.when.premiss != None else a.given.premiss)
    return None


def addPremissToTest(a):
    if a == None: return 
    for t in testCases:
        if t.method == a:
            return None
    testCases.append(TestCase(None,a,None))

def addParameterToTest(parameter, premiss):
    if premiss is None: return SUCCESS
    for itr,x in enumerate(testCases):
        if x.method == premiss:
            if testCases[itr].parameters == None:
                testCases[itr].parameters = [parameter]
            else:
                if parameter not in testCases[itr].parameters:
                    testCases[itr].parameters.append(parameter)
            return SUCCESS
    return FAILURE


def definePartsStorie(storie):
    descriptionStorie = getRoleFeatureReason(storie)
    storie = getStorieWithoutDescription(storie)
    acceptanceCriterias = getAcceptanceCriterias(storie)
    return descriptionStorie,acceptanceCriterias


def getStorieWithoutDescription(storie):
    linesToRemove = []
    for line in storie:
        if searchKeysRole(line) or searchKeysFeature(line) or searchKeysReason(line):
            linesToRemove.append(line)    
    return [s for s in storie if s not in linesToRemove]

def getAcceptanceCriterias(storie):
    acceptanceCriterias = []
    tag = TagsAcceptance.GIVEN
    given,when,then = "","",""
    for itr, line in enumerate(storie):
        if re.match("dado que",line.lower()):
            tag = TagsAcceptance.GIVEN
            given = definePremise(storie,itr)
        elif re.match("quando",line.lower()):
            tag = TagsAcceptance.WHEN
            when = defineAction(storie,itr)
        elif re.match("então",line.lower()):
            tag = TagsAcceptance.THEN
            then = defineOutcome(storie,itr)
            acceptanceCriterias.append(AcceptanceCriteria(given, when, then))    
    return acceptanceCriterias

def definePremise(storie,itr):
    return Acceptance(createTestTitle(verifyImperative(storie[itr])), getLinesField(storie[itr:]))

def verifyImperative(phrase):
    phrase = searchKeyGiven(phrase)
    doc = nlp(phrase)
    for itr,word in enumerate(doc):
        if word.pos_ == 'AUX':
            if doc[itr+1].pos_ != 'VERB':
                phrase = createImperative(word.lemma_, word.text,phrase)
                break
        if word.pos_ in ['VERB']:
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
    return "{} {}".format(lemma,re.search("(?<={}\s).*".format(text),phrase).group())

def defineAction(storie,itr):
    doc = nlp(storie[itr])
    return Acceptance(treatWhen(storie[itr], doc) if validateRegisterScenario(doc) else None, getLinesField(storie[itr:]))


def defineOutcome(storie,itr):
    return Acceptance(None,getLinesField(storie[(itr):]))

def verifyFields(field):
    doc = nlp(field)
    if getVerbAndTagsFields(doc) or verifyTagField(doc) or validateRegisterScenario(doc):
        return True

def verifyTagField(doc):
    for word in doc:
        if word.lemma_ == 'campo':
            return True


def getLinesField(storie):
    fields = []
    for iter,x in enumerate(storie):
        if not verifyFields(x) and not re.match("e",x.lower()): continue
        TratedFields = treatField(x)
        if TratedFields:
            fields.extend(TratedFields)
        if len(storie) > iter+1 and validateEndOfBlock(storie[iter+1]):
            break
    return fields

def validateEndOfBlock(line):
    if line.strip() == '':
        return True 
    startBlocks = ['cenário','scenario','dado que',"então","quando"] 
    for s in startBlocks:
        if(re.match(s,line.lower())):
            return True
    return None

def treatField(field):
    if field == '': return None
    if re.match("\"",field):
        return [re.search("(?<=\")[A-z|\s|\-]+(?=\(([^)]+)\)|\")",field).group().strip().title()]
    elif re.search("(?<=campo\s\").*",field):
        word = re.search("campo.*",field).group()
        return [re.search("(?<=\")[A-z|\s|\-]+(?=\(([^)]+)\)|\")",word).group().strip().title()]
    elif "operação" in field:
        return None
    else:
        return getFieldWidthoutTags(field)

def getFieldWidthoutTags(field):
    doc = nlp(field)
    verbAndtag = getVerbAndTagsFields(doc)
    if verbAndtag:
        textAfterVerbAndTag = re.search("(?<=\s{}).*".format(verbAndtag),field.lower()).group().strip()
        if existsMultipleFieldsBetweenComma(textAfterVerbAndTag):
            return getMultipleFieldsBetweenComma(textAfterVerbAndTag)
        else: 
            return [s.strip() for s in re.findall("(?<={}\s)[A-zÀ-ú-\/]+".format(verbAndtag),unidecode(field.lower()))] 
    elif re.match("e\s",field.lower()):
        return getFieldWithoutVerb(field,doc)
    return None

def getFieldWithoutVerb(field,doc):
    if doc[0].pos_ == "CCONJ" and doc[1].pos_ in["DET","NUM"]:
        return [re.search("(?<={}\s)[\w\/]+\s?[\w\/ ]+".format(doc[1].text),unidecode(field.lower())).group().strip()]
    else:
        return None

def existsMultipleFieldsBetweenComma(field):
    if "," in field or re.search("\se\s",field):
        return True

def getVerbAndTagsFields(doc):    
    for itr,word in enumerate(doc):
        #é necessário colocar o selecione po uma limitação do spacy
        if(word.lemma_) in ["enviar","preencher","salvar", "selecionar", "selecione", "informar","digitar"]:
            if len(doc) > itr+1 and doc[itr+1].pos_ in ["NOUN","PRON","DET","NUM"]:
                return "{} {}".format(word.text,doc[itr+1].text)
    return None

def getMultipleFieldsBetweenComma(field):
    return [''.join(s) for s in re.findall("([\w\/]+\s?[\w\/ ]+(?=\,|\se\s))|(((?<=e\s)[\w\/]+\s?[\w\/\s]+)|(?<=\,\s)[\w\/]+\s?[\w\/\s]+)",unidecode(field))]

def searchKeyGiven(phrase):
    return re.search("(?<=dado que\s).*|(?<=e\s).*",phrase.lower()).group().strip()


def searchKeyWhen(phrase):
    return re.search("(?<=quando\s).*|(?<=e\s).*",phrase.lower()).group().strip()

def searchKeyThen(phrase):
    return re.search("(?<=então\s).*|(?<=e\s).*",phrase.lower()).group().strip()


def treatWhen(phrase, doc):
    phrase = searchKeyWhen(phrase)
    if validateOperationAction(phrase): return None
    for word in doc:
        if word.pos_ in ['VERB','AUX']:
            if word.lemma_ in ['desejar','estar',"dever"]:
                phrase = re.search("(?<=desejar\s).*|(?<=estiver\s).*|(?<=deve\s).*",phrase.lower()).group().strip()
            else:
                phrase = phrase.replace(word.text,word.lemma_,1).title()
    return createTestTitle(phrase)


def createTestTitle(phrase):
    return unidecode('Deve{}'.format(''.join([str(p) for p in phrase.title() if p.isalpha() or p.isalnum()])))

def validateOperationAction(phrase):
    return "operação" in phrase

def searchKeyAuxWhen(phrase):
    return re.search("(?<=desejar\s).*|(?<=estiver\s).*",phrase.lower()).group().strip()


def validateRegisterScenario(doc):
    for word in doc:
        if word.pos_ in ["VERB", "NOUN"] :
            if word.lemma_  in ['cadastrar',"registrar",'inserir']:
                return True
    return False


def getRoleFeatureReason(storie):
    role = defineRole(storie)
    feature = defineFeature(storie)
    reason = defineReason(storie)
    return DescriptionStorie(role,feature,reason)

def defineRole(description):
    for des in description:
        phrase = removeKeysRole(des)
        if (phrase):
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
        return re.search("(?<=como\s).*|(?<=enquanto\s).*",line.lower()).group()


def searchKeysRole(line):
    return re.match("(como\s)|(enquanto\s|eu como\s)",line.lower())
        

def defineFeature(description):
    for des in description:
        phrase = removeKeysFeature(des)
        if (phrase):
            return nlpFeature(phrase)
    return None


def removeKeysFeature(line):
    if searchKeysFeature(line):
        return re.search("(?<=quero\s).*|(?<=preciso\s).*|(?<=desejo\s).*",line.lower()).group()


def searchKeysFeature(line):
    return re.match("(quero\s)|(preciso\s)|(desejo\s)",line.lower())


def nlpFeature(phrase):
    doc = nlp(phrase)
    for word in doc:
        if word.pos_ == 'VERB':
            return re.search("(^{}).*".format(word.text),phrase).group()
        elif word.pos_ in ['ADP','AUX','CCONJ','DET','NUM','PART','PRON','SCONJ']:
            phrase = re.sub(word.text,"",phrase,1).strip()
    return phrase.strip()


def defineReason(description):
    for des in description:
        phrase = removeKeysReason(des)
        if (phrase):
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
        return re.search("(?<=para que\s).*|(?<=porque\s).*",line.lower()).group() 

def searchKeysReason(line):
    return re.match("(para que\s)|(porque\s)",line.lower())
