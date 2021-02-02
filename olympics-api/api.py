#/usr/bin/env python3
'''
    flask_sample.py
    Jeff Ondich, 22 April 2016
    Updated 7 October 2020

    A slightly more complicated Flask sample app than the
    "hello world" app found at http://flask.pocoo.org/.
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

@app.route('/')
def hello():
    return 'Hello, Citizen of CS257.'

def get_game_from_database():
  try:
      connection = psycopg2.connect(database=database, user=user, password=password)
  except Exception as e:
      print(e)
      exit()
  cursor = connection.cursor()
  query = "SELECT * FROM games ORDER BY year"
  cursor.execute(query)
  games_list = []
  for row in cursor:
      one_game = {}
      game_id = int(row[0])
      year = int(row[1])
      season = row[2]
      city = row[3]
      one_game['id'] = game_id
      one_game['year'] = year
      one_game['season'] = season
      one_game['city'] = city
      games_list.append(one_game)
  return games_list

@app.route('/games')
def get_games():
    ''' Returns list of games with their id, year, season, and city. '''
    games_list = get_game_from_database()
    return json.dumps(games_list)


def get_noc_from_database():
  try:
      connection = psycopg2.connect(database=database, user=user, password=password)
  except Exception as e:
      print(e)
      exit()
  cursor = connection.cursor()
  query = "SELECT * FROM teams ORDER BY noc"
  cursor.execute(query)
  games_list = []
  for row in cursor:
      one_game = {}
      team_id = row[0]
      noc_abbreviation = row[1]
      noc_name = row[2]
      one_game['id'] = team_id
      one_game['abbreviation'] = noc_abbreviation
      one_game['name'] = noc_name
      games_list.append(one_game)
  return games_list

@app.route('/nocs')
def get_nocs():
    nocs_list = get_noc_from_database()
    return json.dumps(nocs_list)


def get_medalists_from_database(games_id):
  try:
      connection = psycopg2.connect(database=database, user=user, password=password)
  except Exception as e:
      print(e)
      exit()
  cursor = connection.cursor()
  query = "SELECT athletes.id, athletes.name, athletes.sex, sports.sport, "
  query += "sports.event, athlete_sports_events.medal "
  query += "FROM athletes, athlete_sports_events, sports "
  query += f"WHERE athlete_sports_events.games_id={games_id} "
  query += "AND athletes.id=athlete_sports_events.athletes_id "
  query += "AND athlete_sports_events.sports_id=sports.id"
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

def get_medalists_from_database_with_noc(games_id, noc_abbreviation):
  try:
      connection = psycopg2.connect(database=database, user=user, password=password)
  except Exception as e:
      print(e)
      exit()
  cursor = connection.cursor()
  query = "SELECT athletes.id, athletes.name, athletes.sex, sports.sport, "
  query += "sports.event, athlete_sports_events.medal "
  query += "FROM athletes, athlete_sports_events, sports "
  query += f"WHERE athlete_sports_events.games_id={games_id} "
  query += "AND athletes.id=athlete_sports_events.athletes_id "
  query += f"AND noc='{noc_abbreviation}' "
  query += "AND athlete_sports_events.sports_id=sports.id"
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
    noc_abbreviation = flask.request.args.get('noc')
    if (noc_abbreviation):
      medalists_list = get_medalists_from_database_with_noc(games_id, noc_abbreviation)
    else:
      medalists_list = get_medalists_from_database(games_id)
    return json.dumps(medalists_list)

@app.route('/help')
def get_help():
    return flask.render_template('help.html')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
