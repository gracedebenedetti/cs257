'''
olympics.py
author: Grace de Benedetti for CS257 Software Design, Professor Jeff Ondich

Command-line program that can print NOCs and the number of gold medals they have
won, all athletes competing for a specified NOC, or athletes and the number of
gold medals they have won.
'''

import psycopg2
import argparse
import sys

from config import password
from config import database
from config import user

def get_parsed_arguments():
    parser = argparse.ArgumentParser(description='prints out data from olympics database according to queries and user input.')
    parser.add_argument('-n', '--NOC', metavar='NOC', nargs= 1, help='NOC in which you are searching for athletes (three letter acronym for any national olympic committee)')
    parser.add_argument('-m', '--gold_medals', metavar='gold_medals', nargs= '*', default = 'go', help='prints NOCs and their number of gold medals won, type ""-m go""')
    parser.add_argument('-a', '--athlete_medals', metavar='athlete_medals', nargs= '*', default = 'go', help='prints athlete names and their number of medals won, type ""-a go""')
    parsed_arguments = parser.parse_args()
    return parsed_arguments

try:
    connection = psycopg2.connect(database=database, user=user, password=password)
except Exception as e:
    print(e)
    exit()

cursor = connection.cursor()
arguments = get_parsed_arguments()

#for athletes competing for specified NOC
if arguments.NOC:
    search_string = arguments.NOC[0]
    query = '''SELECT athletes.name
                FROM athletes, athlete_sports_events
                WHERE athletes.id = athlete_sports_events.athletes_id
                AND athlete_sports_events.NOC = %s'''
    try:
        cursor.execute(query, (search_string,))
    except Exception as e:
        print(e)
        exit()

    print('===== Athletes competing for team {0} ====='.format(search_string))
    for row in cursor:
        print(row[0])
    print()

#for gold medals won by each NOC
if arguments.athlete_medals and not arguments.gold_medals and not arguments.NOC:
    query = '''SELECT teams.noc, COUNT(athlete_sports_events.medal)
                FROM athlete_sports_events, teams
                WHERE athlete_sports_events.medal = 'Gold'
                AND athlete_sports_events.NOC = teams.NOC
                GROUP BY teams.noc
                ORDER BY COUNT(athlete_sports_events.medal) DESC;'''
    try:
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    print('===== NOCs and their number of gold medals won =====')
    for row in cursor:
        print(row[0], row[1])
    print()

#for number of medals won by each athlete
if arguments.gold_medals and not arguments.athlete_medals and not arguments.NOC:
    query = '''SELECT athletes.name, COUNT(athlete_sports_events.medal)
                FROM athletes, athlete_sports_events
                WHERE athletes.id = athlete_sports_events.athletes_id
                GROUP BY athletes.name
                ORDER BY COUNT(athlete_sports_events.medal);''' #Ascending because higher medals will show at the bottom of terminal
    try:
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    print('===== Athletes and their number of medals won =====')
    for row in cursor:
        print(row[0], row[1])
    print()

connection.close()
