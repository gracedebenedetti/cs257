'''
    olympics-api.py
    Quoc Nguyen and Grace de Benedetti, 2 February 2021

    A program using Flask to implement HTTP-based APIs in Python.
'''
import sys
import argparse
import flask
import json
import psycopg2
from config import user
from config import password
from config import database

app = flask.Flask(__name__)

def connect_to_database():
 try:
     connection = psycopg2.connect(database=database, user=user, password=password)
     return connection
 except Exception as e:
     print(e)
     exit()

@app.route('/help')
def get_help():
    return 'Help: possible endpoints include /games, /nocs, and /medalists/games/<games_id>[noc=noc_abbreviation].'

def get_game_from_database():
  '''Returns a list of dictionaries of all games from database with id, year, season, and city'''
  connection = connect_to_database()
  cursor = connection.cursor()
  query = "SELECT * FROM games ORDER BY year"
  cursor.execute(query)
  games_list = []
  for row in cursor:
      one_game = {}
      one_game['id'] = int(row[0])
      one_game['year'] = int(row[1])
      one_game['season'] = row[2]
      one_game['city'] = row[3]
      games_list.append(one_game)
  return games_list

@app.route('/games')
def get_games():
    ''' Returns JSON list of dictionaries of games with their id, year, season, and city.'''
    games_list = get_game_from_database()
    return json.dumps(games_list)

def get_noc_from_database():
  '''Returns a list of dictionaries of NOCs with abbreviation and name.'''
  connection = connect_to_database()
  cursor = connection.cursor()
  query = "SELECT * FROM teams ORDER BY noc"
  cursor.execute(query)
  nocs_list = []
  for row in cursor:
      one_noc = {}
      one_noc['abbreviation'] = row[1]
      one_noc['name'] = row[2]
      nocs_list.append(one_noc)
  return nocs_list

@app.route('/nocs')
def get_nocs():
    ''' Returns a JSON list of dictionaries of NOCs with their abbreviation and name.'''
    nocs_list = get_noc_from_database()
    return json.dumps(nocs_list)

def get_medalists_from_database(games_id, noc_abbreviation):
  '''Returns a list of dictionaries of medalist with athlete id, athlete's name, sex, sport, event, and medal.'''
  connection = connect_to_database()
  cursor = connection.cursor()
  query = "SELECT athletes.id, athletes.name, athletes.sex, sports.sport, "
  query += "sports.event, athlete_sports_events.medal "
  query += "FROM athletes, athlete_sports_events, sports "
  query += f"WHERE athlete_sports_events.games_id={games_id} "
  query += "AND athletes.id=athlete_sports_events.athletes_id "
  query += "AND athlete_sports_events.sports_id=sports.id"
  if noc_abbreviation:
      query += f" AND noc='{noc_abbreviation}' "
  cursor.execute(query)
  medalists_list = []
  for row in cursor:
      one_medalist = {}
      one_medalist['athlete_id'] = row[0]
      one_medalist['athlete_name'] = row[1]
      one_medalist['athlete_sex'] = row[2]
      one_medalist['sport'] = row[3]
      one_medalist['event'] = row[4]
      one_medalist['medal'] = row[5]
      medalists_list.append(one_medalist)
  return medalists_list

@app.route('/medalists/games/<games_id>')
def get_medalists(games_id):
    ''' Returns a JSON list of dictionaries of medalists with the athlete's id, name, sex, sport, event, and medal.'''
    noc_abbreviation = flask.request.args.get('noc')
    medalists_list = get_medalists_from_database(games_id, noc_abbreviation)
    return json.dumps(medalists_list)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A program using Flask to implement HTTP-based APIs in Python.')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
