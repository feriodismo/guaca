import pyaudio
import speech_recognition as sr
from guaca import syntax_text
from notes.applications_gua import data
r = sr.Recognizer()
WIT_AI_KEY = data["wit_proy"] 

def milagro():
	with sr.Microphone() as source:
		print("Say something!")
		audio = r.listen(source)
	try:
		fraseo = r.recognize_wit(audio, key=WIT_AI_KEY)
		print(fraseo);
		syntax_text(fraseo);
		return fraseo
	except sr.UnknownValueError:
		print("Wit.ai could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Wit.ai service; {0}".format(e))

milagro()