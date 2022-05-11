from flask import Flask
from flask_restful import Resource, Api
from flask import request, redirect
from werkzeug.utils import secure_filename
import json
from flask_restful import Resource, Api
from flask import request, redirect
from flask_restful import reqparse
from werkzeug.utils import secure_filename
import os
import datetime
from models.playlist import PlaylistModel
from variable_store import *
from checktype import *
from models.accounts import g, AccountsModel
from models.accounts import auth
import random

def getNext():
	mode = getVarFromFile('mode')
	if mode == 'seq':
		try:
			if getVarFromFile('first'):
				setVarFromFile('first', False)
				
			else:
				first=PlaylistModel.top_by_priority().json()
				PlaylistModel.delete_by_priority()
				playlist_entry=PlaylistModel(name=first['name'], duration=first['duration'], type=first['type'])
				playlist_entry.save_to_db()
				PlaylistModel.update_priority()

			PlaylistModel.update_id_as_priority()
			return PlaylistModel.top_by_priority().json()
		except:
			#llista buida, reprodueix, el contingut per defecte
			return {'path': "./static/default.mp4", 'duration': 0, 'type': 'video'}

	elif mode == 'inter':
		try:
			if getVarFromFile('defaultTurn'):
				setVarFromFile('defaultTurn', False)
				first=PlaylistModel.top_by_priority().json()
				PlaylistModel.delete_by_priority()
				playlist_entry=PlaylistModel(name=first['name'], duration=first['duration'], type=first['type'])
				playlist_entry.save_to_db()
				PlaylistModel.update_priority()
				PlaylistModel.update_id_as_priority()
				return PlaylistModel.top_by_priority().json()
				
			else:
				setVarFromFile('defaultTurn', True)
				forced_next_metadata = getVarFromFile('intercalated_metadata')
				return json.loads(json.dumps(forced_next_metadata))
		except:
			#llista buida, reprodueix, el contingut per defecte
			return {'path': "./static/default.mp4", 'duration': 0, 'type': 'video'}

	elif mode == 'rndm':
		try:
			unplayed_entries = PlaylistModel.retrieveByUnplayed()
			if not unplayed_entries:
				PlaylistModel.makeAllUnplayed()
				#When it finishes, triggers the default.mp4 to know it has finished
				#if not, do inside this if:
				#unplayed_entries = PlaylistModel.retrieveByUnplayed()
			container_ids = []
			for e in unplayed_entries:
				print(e.json()['id'])
				id=e.json()['id']
				container_ids.append(id)
			"""
			try:
				random_element = PlaylistModel.find_by_id(random.choice(container_ids)).json()
				setVarFromFile('random_element', {'name': random_element['name'], 'type': random_element['type'],'priority':random_element['priority'], 'duration': random_element['duration']})
				PlaylistModel.delete_by_name(random_element['name'])
				#playlist_entry.save_to_db()
			except:
				return {'path': "./static/bloc1.mp4", 'duration': 0, 'type': 'video'}

			try:
				random_element = getVarFromFile('random_element')
				firstToUpdate=PlaylistModel.top_by_priority()
				#setVarFromFile('firstBackUp', firstToUpdate)
				setVarFromFile('firstBackUp', {'name': firstToUpdate['name'], 'type': firstToUpdate['type'],'priority':firstToUpdate['priority'], 'duration': firstToUpdate['duration']})
				firstToUpdate.updateData(name=random_element['name'],type=random_element['type'],duration=random_element['duration'])
				firstToUpdate.save_to_db()
			except:
				return {'path': "./static/bloc2.mp4", 'duration': 0, 'type': 'video'}

			try:
				firstBackUp = getVarFromFile('firstBackUp')
				playlist_entry=PlaylistModel(name=firstBackUp['name'], duration=7, type='Image')
				playlist_entry.save_to_db()
				PlaylistModel.update_priority()
				return PlaylistModel.top_by_priority().json()
			except:
				return {'path': "./static/bloc3.mp4", 'duration': 0, 'type': 'video'}
			"""
			random_element = PlaylistModel.find_by_id(random.choice(container_ids))
			#auxRandomName = random_element.name 
			#firstToUpdate=PlaylistModel.top_by_priority()
			#auxFirstToUpdate = firstToUpdate.name
			setVarFromFile('random_element_id',random_element.id) 
			random_element.id = 1984
			random_element.save_to_db()

			firstToUpdate=PlaylistModel.top_by_priority() 
			setVarFromFile('firstToUpdate_id',firstToUpdate.id) 
			firstToUpdate.id = getVarFromFile('random_element_id')
			firstToUpdate.save_to_db()

			random_element = PlaylistModel.find_by_id(1984)
			random_element.id = getVarFromFile('firstToUpdate_id')
			random_element.played = 1
			random_element.save_to_db()
			PlaylistModel.update_id_as_priority()
			return PlaylistModel.top_by_priority().json()
		except:
			#llista buida, reprodueix, el contingut per defecte
			return {'path': "./static/default.mp4", 'duration': 0, 'type': 'video'}


	elif mode == 'rndm-inter':
		try:
			if getVarFromFile('defaultTurn') or PlaylistModel.top_by_priority().json()['path'] == getVarFromFile('intercalated_metadata')['path']:
				setVarFromFile('defaultTurn', False)
				unplayed_entries = PlaylistModel.retrieveByUnplayed()
				if not unplayed_entries:
					PlaylistModel.makeAllUnplayed()
					#When it finishes, triggers the default.mp4 to know it has finished
					#if not, do inside this if:
					#unplayed_entries = PlaylistModel.retrieveByUnplayed()
				container_ids = []
				for e in unplayed_entries:
					id=e.json()['id']
					container_ids.append(id)
				random_element = PlaylistModel.find_by_id(random.choice(container_ids))
				#auxRandomName = random_element.name 
				#firstToUpdate=PlaylistModel.top_by_priority()
				#auxFirstToUpdate = firstToUpdate.name
				setVarFromFile('random_element_id',random_element.id) 
				random_element.id = 1984
				random_element.save_to_db()

				firstToUpdate=PlaylistModel.top_by_priority() 
				setVarFromFile('firstToUpdate_id',firstToUpdate.id) 
				firstToUpdate.id = getVarFromFile('random_element_id')
				firstToUpdate.save_to_db()

				random_element = PlaylistModel.find_by_id(1984)
				random_element.id = getVarFromFile('firstToUpdate_id')
				random_element.played = 1
				random_element.save_to_db()
				PlaylistModel.update_id_as_priority()
				return PlaylistModel.top_by_priority().json()
				
			else:
				setVarFromFile('defaultTurn', True)
				forced_next_metadata = getVarFromFile('intercalated_metadata')
				return json.loads(json.dumps(forced_next_metadata))
		except:
			#llista buida, reprodueix, el contingut per defecte
			return {'path': "./static/default.mp4", 'duration': 0, 'type': 'video'}

	else:
		try:
			entries = PlaylistModel.retrieveAllEntries()
			container_entries = []
			for e in entries:
				container_entries.append(e.json()['id'])
			return PlaylistModel.find_by_id(random.choice(container_entries))
		except:
			#llista buida, reprodueix, el contingut per defecte
			return {'path': "./static/default.mp4", 'duration': 0, 'type': 'video'}