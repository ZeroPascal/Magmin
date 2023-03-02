from enum import Enum
import typing





class Event(object): 

	def __init__(self): 
		self.__eventhandlers= []

	def __iadd__(self, handler): 
		self.__eventhandlers.append(handler) 
		return self
	def __isub__(self, handler): 
		self.__eventhandlers.remove(handler) 
		return self
	def __call__(self, event:typing.Any, payload:typing.Any): 
		for eventhandler in self.__eventhandlers: 
			eventhandler(event,payload) 

AnyEvent= Event()

class FolderEvents(Enum):
    ADD_FOLDER = 1
    REMOVE_FOLDER =2 
    UPDATED_FOLDER =3

class FolderEventHandler(Event):
	def __init__(self):
		super().__init__()
	def __iadd__(self,handler):
		super().__iadd__(handler)
	def __call__(self,event:FolderEvents,payload:typing.Any):
		super().__call__(event,payload)
		AnyEvent(event,payload)


class FileEvents(Enum):
    ADD_FOLDER = 1
    REMOVE_FOLDER =2 
    UPDATED_FOLDER =3
			
class FileEventHandler(Event):
	def __init__(self):
		super().__init__()
	def __iadd__(self,handler):
		super().__iadd__(handler)
	def __call__(self,event:FolderEvents,payload:typing.Any):
		super().__call__(event,payload)
		AnyEvent(event,payload)

