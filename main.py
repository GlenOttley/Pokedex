from flask import Flask, render_template, url_for, request, jsonify, make_response, redirect
import json
import requests
from unitconvert import lengthunits, massunits
import math
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pokemon.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Cry(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	filepath = db.Column(db.String(20), unique=False, nullable=False)

# with sqlite3.connect('pokemon.db') as db:
# 	cursor = db.cursor()

# for num in range(1, 152):
# 	if num < 10:
# 		file = f'00{str(num)}.wav'
# 	elif num < 100:
# 		file = f'0{str(num)}.wav'
# 	else:
# 		file = f'{str(num)}.wav'
# 	cursor.execute('''INSERT INTO Cry(filepath)
# 	VALUES(?)''', (file,))
# db.commit()

def getPokeList():
	url = f'https://pokeapi.co/api/v2/pokemon?limit=151'
	response = requests.get(url)
	pokeList = response.json()
	return pokeList['results']

def getPokemon(pokeName):
	url = f'https://pokeapi.co/api/v2/pokemon/{pokeName}'
	response = requests.get(url)
	pokemon = response.json()
	return pokemon

def getPokemonId(pokemon):
	if pokemon['id'] < 10:
		pokeId = 'No. 00' + str(pokemon['id'])
	elif pokemon['id'] < 100:
		pokeId = 'No. 0' + str(pokemon['id'])
	else:
		pokeId = 'No. ' + str(pokemon['id'])
	return pokeId

def getPokemonDescription(pokemon):
	pokeUrl = pokemon['species']['url']
	response = requests.get(pokeUrl)
	pokeUrl = response.json()
	pokeDescription = pokeUrl['flavor_text_entries'][2]['flavor_text'].split('\f')
	pokeDescriptionP1 = pokeDescription[0]
	if len(pokeDescription) == 2:
		pokeDescriptionP2 = pokeDescription[1]
	else:
		pokeDescriptionP2 = ''
	return pokeDescriptionP1, pokeDescriptionP2

def getPokemonGenus(pokemon):
	pokeUrl = pokemon['species']['url']
	response = requests.get(pokeUrl)
	pokeUrl = response.json()
	pokeGenus = pokeUrl['genera'][7]['genus'].split('Pokémon')[0]
	return pokeGenus

def getPokemonHeight(pokemon):
	pokeHeight = pokemon['height'] / 10
	fraction, feet = math.modf(lengthunits.LengthUnit(pokeHeight, 'm', 'ft').doconvert())
	inches = round(lengthunits.LengthUnit(fraction, 'ft', 'in').doconvert())
	if inches == 12:
		feet += 1
		inches = 0
	inches /= 100
	pokeHeight = feet + inches
	pokeHeight = str(pokeHeight)
	if len(pokeHeight) == 4:
		pokeHeight = f"{pokeHeight[0]}' {pokeHeight[2]}{pokeHeight[3]}'"
	else:
		pokeHeight = f"{pokeHeight[0]}' {pokeHeight[2]}0'"
	return pokeHeight

def getPokemonWeight(pokemon):
	pokeWeight = pokemon['weight'] / 10
	if pokeWeight > 1:
		pokeWeight = str(round((massunits.MassUnit(pokeWeight, 'kg', 'lb').doconvert())))
		pokeWeight = f'{pokeWeight}.0 l b'
	else:
		pokeWeight = str(round((massunits.MassUnit(pokeWeight, 'kg', 'lb').doconvert()), 1))
		pokeWeight = f'{pokeWeight} l b'
	return pokeWeight

@app.route('/pokemon', methods=['POST'])
def returnPokemon():
	req = request.get_json()
	pokemon = getPokemon(req['data'])
	pokeDescriptionP1, pokeDescriptionP2 = getPokemonDescription(pokemon)
	pokeCry = Cry.query.get(pokemon['id']).filepath
	res = make_response(jsonify({
		'poke-cry': f'static/audio/cry/{pokeCry}',
		'image': pokemon['sprites']['versions']['generation-i']['red-blue']['front_gray'],
		'poke-id': getPokemonId(pokemon),
		'name': pokemon['name'],
		'poke-genus': getPokemonGenus(pokemon),
		'poke-height': getPokemonHeight(pokemon),
		'poke-weight': getPokemonWeight(pokemon),
		'poke-description-p1': pokeDescriptionP1,
		'poke-description-p2': pokeDescriptionP2
		}), 200)
	return res

@app.route('/')
def pokedex():
	pokeIdList = []
	pokeNameList = []
	pokeList = getPokeList()
	counter = 1
	for pokemon in pokeList:
		if counter < 10:
			pokeIdList.append(f'00' + str(counter))
		elif counter < 100:
			pokeIdList.append(f'0' + str(counter))
		else:
			pokeIdList.append(str(counter))
		counter += 1
		pokeNameList.append(pokemon['name'])
	return render_template('pokedex.html', pokeIdList=pokeIdList, pokeNameList=pokeNameList, zip=zip)

# if __name__ == '__main__':
# 	app.run(debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
