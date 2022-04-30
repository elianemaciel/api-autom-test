from cmath import log
from enum import Enum
from itertools import chain, islice, tee
import spacy
import pt_core_news_sm
import re

nlp = pt_core_news_sm.load()

testCases = []

class classTestCase:
    def __init__(self, classMethod, method, parameters):
        self.classMethod = classMethod
        self.method = method
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

def validateContent(vals):
    if(len(vals) >=1 and vals[0] != ''):
        return True
    return False

def defineTestsFromStories(vals):
    if(validateContent(vals)):
        storie = createArrayStorie(vals[0])
        return definePartsStorie(storie)


def createArrayStorie(storie):
    return str.split(storie,"\n")

def defineTestsFromAcceptanceCritereas(acceptanceCriterias):
    for a in acceptanceCriterias:
        if re.match("Deve",a.given):
            addPremissToTest(a)


def addPremissToTest(a):
    for t in testCases:
        if t.method == a:
            return None
    


def definePartsStorie(storie):
    descriptionStorie = getRoleFeatureReason(storie)
    storie = getStorieWithoutDescription(storie)
    acceptanceCriterias = getAcceptanceCriterias(storie)
    return defineTestsFromAcceptanceCritereas(acceptanceCriterias)


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
        if "dado que" in line.lower() or (tag == TagsAcceptance.GIVEN and re.match("e\s", line.lower())):
            tag = TagsAcceptance.GIVEN
            given = definePremise(storie,itr)
        elif "quando" in line.lower() or (tag == TagsAcceptance.WHEN and re.match("e\s", line.lower())):
            tag = TagsAcceptance.WHEN
            when = defineAction(storie,itr)
        elif "então" in line.lower():
            tag = TagsAcceptance.THEN
            then = defineOutcome(storie,itr)
            acceptanceCriterias.append(AcceptanceCriteria(given, when, then))    
    return acceptanceCriterias

def definePremise(storie,itr):
    phrase = searchKeyGiven(storie[itr])
    doc = nlp(phrase)
    for word in doc:
        if word.pos_ == 'VERB':
            phrase = createImperative(word.lemma_, word.text,phrase)
            break
        elif word.text.lower() == "logado":
            phrase = createImperative("logar",word.text,phrase)
            break
    return createTestTitle(phrase)


def createImperative(lemma,text,phrase):
    return "{} {}".format(lemma,re.search("(?<={}\s).*".format(text),phrase).group())

def defineAction(storie,itr):
    doc = nlp(storie[itr])
    if (validateRegisterScenario(doc)): 
        return treatWhen(storie[itr], doc)


def defineOutcome(storie,itr):
    fields = []
    phrase = searchKeyThen(storie[itr])
    doc = nlp(storie[itr])
    if(verifyFields(doc)):
        return getLinesField(storie[(itr+1):])

def verifyFields(doc):
     if 'campo' in [word.lemma_ for word in doc]:
        return True


def getLinesField(storie):
    fields = []
    for x in storie:
        if x.lower() in ['','cenário','scenario','dado']:
            break
        fields.append(x)
    return [treatField(field) for field in fields]

def treatField(field):
    if re.match("\"",field):
        return re.search("(?<=\")[A-z|\s|\-]+(?=\(([^)]+)\)|\")",field).group().strip().title()
    elif re.search("(?<=campo\s\").*",field):
        word = re.search("campo.*",field).group()
        return re.search("(?<=\")[A-z|\s|\-]+(?=\(([^)]+)\)|\")",word).group().strip().title()
    elif re.search("(?<=campo\s).*",field):
        doc = nlp(field)
        for word in doc:
           print(word.text,word.lemma)
    return None

def searchKeyGiven(phrase):
    return re.search("(?<=dado que\s).*|(?<=e\s).*",phrase.lower()).group().strip()


def searchKeyWhen(phrase):
    return re.search("(?<=quando\s).*|(?<=e\s).*",phrase.lower()).group().strip()

def searchKeyThen(phrase):
    return re.search("(?<=então\s).*|(?<=e\s).*",phrase.lower()).group().strip()


def treatWhen(phrase, doc):
    phrase = searchKeyWhen(phrase)
    for word in doc:
        if word.pos_ == 'VERB':
            if word.lemma_ in ['desejar','estiver']:
                phrase = re.search("(?<=desejar\s).*|(?<=estiver\s).*",phrase.lower()).group().strip()
            else:
                phrase = phrase.replace(word.text,word.lemma_,1).title()
    return createTestTitle(phrase)


def createTestTitle(phrase):
    return 'Deve{}'.format(''.join([str(p) for p in phrase.title() if p.isalpha() or p.isalnum()]))


def searchKeyAuxWhen(phrase):
    return re.search("(?<=desejar\s).*|(?<=estiver\s).*",phrase.lower()).group().strip()


def validateRegisterScenario(doc):
    for word in doc:
        if word.pos_ == "VERB":
            if word.lemma_  in ['cadastrar','inserir']:
                return True
    return False


def getRoleFeatureReason(storie):
    role = defineRole(storie)
    feature = defineFeature(storie)
    reason = defineReason(storie)

    print(role, feature, reason)
    return {'role': role, 'feature': feature, 'reason': reason}

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
    return re.match("(como\s)|(enquanto\s)",line.lower())
        

def defineFeature(description):
    for des in description:
        phrase = removeKeysFeature(des)
        if (phrase):
            return nlpFeature(phrase)
    return None


def removeKeysFeature(line):
    if searchKeysFeature(line):
        return re.search("(?<=quero\s).*|(?<=preciso\s).*",line.lower()).group()


def searchKeysFeature(line):
    return re.match("(quero\s)|(preciso\s)",line.lower())


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
