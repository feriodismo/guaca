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


# data update
def jsonUpdate(forma, genero, tiempo, palabra):
	with open('./data.json', 'r') as readjson:
		feeds = json.load(readjson)
	with open('./data.json', 'w') as writejson:
		
		feeds[palabra] = {
			"tag": forma,
			"gender": genero,
			"tiempo": tiempo,
			"frase": "none"
		}
		json.dump(feeds, writejson, indent=4)


def syntax_text(text):

    client = language.LanguageServiceClient()
    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        language='es',
        #label='DISCOURSE',
        type=enums.Document.Type.PLAIN_TEXT)

    tokens = client.analyze_syntax(document).tokens

    # part-of-speech tags from enums.PartOfSpeech.Tag
    pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM', 'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')
    pos_number = ('UNKNOWN', 'SINGULAR', 'PLURAL', 'DUAL')
    pos_gender = ('UNKNOWN', 'FEMININE', 'MASCULINE', 'NEUTER')
    pos_tense = ('UNKNOWN', 'CONDITIONAL_TENSE', 'FUTURE', 'PAST', 'PRESENT', 'IMPERFECT', 'PLUPERFECT')
    pos_mood = ('UNKNOWN', 'CONDITIONAL_MOOD', 'IMPERATIVE', 'INDICATIVE', 'INTERROGATIVE', 'JUSSIVE', 'SUBJUNCTIVE')
    pos_aspect = ('UNKNOWN', 'PERFECTIVE', ' IMPERFECTIVE', 'PROGRESSIVE')
    
    for token in tokens:
    	palabra = token.text.content
    	forma = pos_tag[token.part_of_speech.tag]
    	genero = pos_gender[token.part_of_speech.gender]
    	tiempo = pos_tense[token.part_of_speech.tense]
    	print(token.text.content + ': ' + pos_tag[token.part_of_speech.tag] + ', ' + pos_gender[token.part_of_speech.gender] + ', ' + pos_tense[token.part_of_speech.tense] )
    	jsonUpdate(forma, genero, tiempo, palabra)
    


