from enum import Enum
import typing


class Events(Enum):
    ADD_FOLDER = 1
    REMOVE_FOLDER =2 
    UPDATED_FOLDER =3

class Event(object): 

	def __init__(self): 
		self.__eventhandlers= []

	def __iadd__(self, handler): 
		self.__eventhandlers.append(handler) 
		return self
	def __isub__(self, handler): 
		self.__eventhandlers.remove(handler) 
		return self
	def __call__(self, event:Events, payload:typing.Any): 
		for eventhandler in self.__eventhandlers: 
			eventhandler(event,payload) 
    
FolderEvents = Event()
FileEvents = Event()