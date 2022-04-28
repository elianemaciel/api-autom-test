from cmath import log
from enum import Enum
from itertools import chain, islice, tee
import spacy
import pt_core_news_sm
import re

nlp = pt_core_news_sm.load()

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
        return definePartsStorie(vals[0])

def definePartsStorie(storie):
    descriptionStorie = getRoleFeatureReason(storie)
    acceptanceCriterias = getAcceptanceCriterias(storie)
    print(descriptionStorie)

def getAcceptanceCriterias(storie):
    acceptanceCriterias = []
    storie = str.split(storie,"\n")
    tag = TagsAcceptance.GIVEN
    given,when,then = "","",""
    for itr, line in enumerate(storie):
        if "dado que" in line.lower() or (tag == TagsAcceptance.GIVEN and re.search("^e ", line.lower())):
            tag = TagsAcceptance.GIVEN
            given = definePremise(given,line)
        elif "quando" in line.lower():
            tag = TagsAcceptance.WHEN
            when = defineAction(when, line)
        elif "então" in line.lower():
            tag = TagsAcceptance.WHEN
            then = defineOutcome(then,line)
            if(re.search("^dado que|^cenário|scenario", storie[itr])):
                acceptanceCriterias.append(AcceptanceCriteria(given, when, then))    
    return acceptanceCriterias

def definePremise(given,line):
    phrase = searchKeyGiven(line)
    doc = nlp(phrase)
    persona = ''
    for word in doc:
        if word.pos_ == 'DET' or word.pos_ == "NOUN":
            persona = "{} {}".format(persona, word.text)
        elif word.pos_ == 'VERB':
            phrase = "{} {}".format(word.lemma_,re.search("(?<={}\s).*".format(word.text),phrase).group())
        elif word.text.lower() == "logado":
            phrase = "logar " + re.search("(?<={}\s).*".format(word.text),phrase).group()
    given = "{} {}".format(given,phrase)
    return {'persona': persona, 'given': given}

def defineAction(given,line):
    phrase = searchKeyGiven(line)
    doc = nlp(phrase)
    persona = ''
    for word in doc:
        if word.pos_ == 'DET' or word.pos_ == "NOUN":
            persona = "{} {}".format(persona, word.text)
        elif word.pos_ == 'VERB':
            phrase = "{} {}".format(word.lemma_,re.search("(?<={}\s).*".format(word.text),phrase).group())
        elif word.text.lower() == "logado":
            phrase = "logar " + re.search("(?<={}\s).*".format(word.text),phrase).group()
    given = "{} {}".format(given,phrase)
    return {'persona': persona, 'given': given}

def searchKeyGiven(phrase):
    return re.search("(?<=dado que\s).*|(?<=e\s).*",phrase.lower()).group()


def searchKeyWhen(phrase):
    return re.search("(?<=quando\s).*|(?<=e\s).*",phrase.lower()).group()


def defineOutcome(then,line):
    pass


def getRoleFeatureReason(storie):
    description = str.split(storie,"\n")
    role = defineRole(description)
    feature = defineFeature(description)
    reason = defineReason(description)

    print(role, feature, reason)
    return {'role': role, 'feature': feature, 'reason': reason}

def defineRole(description):
    for des in description:
        phrase = searchKeysRole(des)
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


def searchKeysRole(line):
    if "Como" in line or "Enquanto" in line:
        return re.search("(?<=Como\s).*|(?<=Enquanto\s).*",line).group()

def defineFeature(description):
    for des in description:
        phrase = searchKeysFeature(des)
        if (phrase):
            return nlpFeature(phrase)
    return None

def searchKeysFeature(line):
    if "Quero" in line or "Preciso" in line:
        return re.search("(?<=Quero\s).*|(?<=Preciso\s).*",line).group()

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
        phrase = searchKeysReason(des)
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


def searchKeysReason(line):
    if "Para que" in line or "Porque" in line or "Então" in line:
        return re.search("(?<=Para que\s).*|(?<=Porque\s).*|(?<=Então\s).*",line).group()
