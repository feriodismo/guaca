# setup
import os
import json
import sys
sys.path.insert(0, './notes')
from applications_gua import data
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = data["go_proy"]
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM', 'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')
pos_number = ('UNKNOWN', 'SINGULAR', 'PLURAL', 'DUAL')
pos_gender = ('UNKNOWN', 'FEMININE', 'MASCULINE', 'NEUTER')
pos_tense = ('UNKNOWN', 'CONDITIONAL_TENSE', 'FUTURE', 'PAST', 'PRESENT', 'IMPERFECT', 'PLUPERFECT')
# pos_mood = ('UNKNOWN', 'CONDITIONAL_MOOD', 'IMPERATIVE', 'INDICATIVE', 'INTERROGATIVE', 'JUSSIVE', 'SUBJUNCTIVE')
# pos_aspect = ('UNKNOWN', 'PERFECTIVE', ' IMPERFECTIVE', 'PROGRESSIVE')
pos_person = ('PERSONAL_UNKNOWN', 'FIRST', ' SECOND', 'THIRD', 'REFLEXIVE_PERSON')
pos_dependency = ('UNKNOWN', 'ABBREV', 'ACOMP', 'ADVCL', 'ADVMOD', 'AMOD', 'APPOS', 'ATTR', 'AUX', 'AUXPASS', 'CC', 'CCOMP', 'CONJ', 'CSUBJ', 'CSUBJPASS', 'DEP', 'DET', 'DISCOURSE', 'DOBJ', 'EXPL', 'GOESWITH', 'IOBJ', 'MARK', 'MWE', 'MWV', 'NEG', 'NN', 'NPADVMOD', 'NSUBJ', 'NSUBJPASS', 'NUM', 'NUMBER', 'P', 'PARATAXIS', 'PARTMOD', 'PCOMP', 'POBJ', 'POSS', 'POSTNEG', 'PRECOMP', 'PRECONJ', 'PREDET', 'PREF', 'PREP', 'PRONL', 'PRT', 'PS', 'QUANTMOD', 'RCMOD', 'RCMODREL', 'RDROP', 'REF', 'REMNANT', 'REPARANDUM', 'ROOT', 'SNUM', 'SUFF', 'TMOD', 'TOPIC', 'VMOD', 'VOCATIVE', 'XCOMP', 'SUFFIX', 'TITLE', 'ADVPHMOD', 'AUXCAUS', 'AUXVV', 'DTMOD', 'FOREIGN', 'KW', 'LIST', 'NOMC', 'NOMCSUBJ', 'NOMCSUBJPASS', 'NUMC', 'COP', 'DISLOCATED', 'ASP', 'GMOD', 'GOBJ', 'INFMOD', 'MES', 'NCOMP')

# data update
def jsonUpdate(word, tag, gender, tense, person, number, lemma, sentence_used):
	with open('./data.json', 'r') as readjson:
		feeds = json.load(readjson)
	with open('./data.json', 'w') as writejson:
		index = len(feeds['words'])

		feeds['words'][index] = {
				"word": word,
				"tag": tag,
				"gender": gender,
				"tense": tense,
				"person": person,
				"number": number,
				"lemma": lemma,
				"used sentece": sentence_used
		}
		json.dump(feeds, writejson, indent=4)


def syntax_text(text):
    """Detects syntax in the text."""
    client = language.LanguageServiceClient()

 

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        language='es',
        #label='DISCOURSE',
        type=enums.Document.Type.PLAIN_TEXT)


    tokens = client.analyze_syntax(document).tokens
    
 
    # part-of-speech tags from enums.PartOfSpeech.Tag
    
    sentence_used = document.content
    for token in tokens:
    	
    	edge = token.dependency_edge.label
    	print(edge)
    	#print(token.part_of_speech)
    	word = token.text.content
    	tag = pos_tag[token.part_of_speech.tag]
    	gender = pos_gender[token.part_of_speech.gender]
    	tense = pos_tense[token.part_of_speech.tense]
    	person = pos_person[token.part_of_speech.person]
    	number = pos_number[token.part_of_speech.number]
    	lemma = token.lemma
    	print(word + ': ' + tag + ', ' + gender + ', ' + tense +', '+ person +', '+ number)
    	jsonUpdate(word, tag, gender, tense, person, number, lemma, sentence_used)
    print('')

# syntax_text('yo muerdo suave')

def getLemma(response):
	if response != False:
		with open('./data.json', 'r') as readjson:
			feeds = json.load(readjson)
		for index in feeds['words']:
			# print(feeds['words'][index]['word'])
			if (feeds['words'][index]['word'] == response):
				theLemma = feeds['words'][index]['lemma']
				return theLemma
	else:
		return False

def searchWord(tag, gender, tense, person, number, response):
	with open('./data.json', 'r') as readjson:
		feeds = json.load(readjson)
	# print(tag)
	if tag == pos_tag[11]:
		for index in feeds['words']:
			# print(feeds['words'][index]['word'])
			if (person in (feeds['words'][index]['person'], False)) and (getLemma(response) in (feeds['words'][index]['lemma'], False)) and (feeds['words'][index]['tag'] == tag):
				print(feeds['words'][index]['word'])

searchWord(pos_tag[11], 'none', pos_tense[4], False, 'none', False)

# mala noticia: los tiempos en google language en espaniol estan malos!

