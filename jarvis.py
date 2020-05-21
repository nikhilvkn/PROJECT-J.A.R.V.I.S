import speech_recognition as sr
import sys, time, subprocess, os, time
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

def speak(text):
	# This calls subprocess module with argument 'say', to make the
	# system respond back
	subprocess.call(['say', text])

def search_es(query):
	# This function does the search part in elasticsearch. We are
	# passing our audio to this fuction to search for the key and 
	# to return the sys_command
	try:
		res = es.search(index="voice_assistant", doc_type="text", body={
		"query" :{
        	"match": {
            	"voice_command": {
                	"query": query,
                	"fuzziness": 2
            	}
            	}
        	},
        })
		return res['hits']['hits'][0]['_source']['sys_command']
	except Exception as error:
		return False

def recognize_speech_from_mic(recognizer, microphone):
	# Here we are checking whether the recogonizer and microphone
	# are instances of Recogonizer and Microphone object
	if not isinstance(recognizer, sr.Recognizer):
		raise TypeError("`recognizer` must be `Recognizer` instance")
	if not isinstance(microphone, sr.Microphone):
		raise TypeError("`microphone` must be `Microphone` instance")
	# Below code accepts the input from microphone and pass it to
	# google recogonizer to recogonize audio. Then the recogonized
	# audio is then returned
	# Also handles the exception for the input audio
	with microphone as source:
		recognizer.adjust_for_ambient_noise(source)
		print('Listening to you...')
		audio = recognizer.listen(source)
		try:
			response = recognizer.recognize_google(audio)
			print(response)
			# return a value 1 which is used to signoff assistant
			if response == 'bye bye':
				speak('Signing off for the day, ...bye Nikhil')
				return 1
			else:
				return response
		except sr.UnknownValueError:
			speak('where you saying something..')
		except sr.RequestError as reqerror:
			print("Couldn't request results from Google Speech Recognition service.. please check your connection")

def activate(phrase='hello Jarvis'):
	# This function helps me activate jarvis from sleep
	with mic as source:
		recognizer.adjust_for_ambient_noise(source)
		audio = recognizer.listen(source)
		transcript = recognizer.recognize_google(audio)
		print("listening to you..")
		print(transcript)
		if transcript.lower() == phrase:
			return True
		else:
			return False

def sleep():
	try:
		speak('sleeping till you wake me up')
		time.sleep(3600)
	except KeyboardInterrupt:
		pass

def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper

@run_once
def create_index(es_object,record_list):
	# function helps to create elasticsearch index and handle exception
	bulk(es_object, record_list, index='voice_assistant', doc_type='text', raise_on_error=True)

if __name__ == "__main__":
	# create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # these steps will help populate the appications in /Application
    # directory for me to search through
    d = '/Applications'
    records = []
    apps = os.listdir(d)
    for app in apps:
    	record = {}
    	record['voice_command'] = 'jarvis open ' + app.split('.app')[0]
    	record['sys_command'] = 'open ' + d +'/%s' %app.replace(' ','\ ')
    	records.append(record)
    try:
    	es = Elasticsearch(['localhost:9200'])
    	create_index(es,records)
    	while True:
    		response = recognize_speech_from_mic(recognizer,microphone)
    		if response == 1:
    			break
    		elif response == 'Stay Down':
    			sleep()
    		sys_command = search_es(response)
    		if sys_command is False:
    			continue
    		else:	
    			os.system(sys_command)
    			speak("it's done")
    except KeyboardInterrupt:
    	pass		
    #except Exception as exception:
    	#print('waiting for your request..')
