'''
csv creator program convert.py
created by Grace de Benedetti at Carleton College
Prof Jeff Ondich: CS 257, Winter 2020

This program will read the Kaggle CSV files and write one CSV file for each of the tables
in the database design.
'''

import csv

def create_data(reader, noc_regions_reader):
    athletes = {} # maps ID --> info like name, etc.
    games = {} # maps (year, season) --> {‘id’:#, ‘city’:..}
    sports = {}
    teams = {}
    athlete_sports_events = {}
    athlete_games = {} #maps (athletes_id, games_id) --> age, height, weight, team
    noc_regions = {}
    for row in noc_regions_reader:
        if len(row) > 1:
            #teams
            teams_id = row[0]
            if teams_id not in teams:
                one_team = {}
                one_team['id'] = len(teams) + 1
                one_team['region'] = row[1]
                teams[teams_id] = one_team
    for row in reader:
        if len(row) > 1:
            # athlete
            athletes_id = int(row[0])
            if athletes_id not in athletes:
                one_athlete = {}
                one_athlete['name'] = row[1]
                one_athlete['sex'] = row[2]
                athletes[athletes_id] = one_athlete
            # games
            year = row[9]
            season = row[10]
            games_key = (year, season)
            if games_key not in games:
                one_games = {}
                one_games['id'] = len(games) + 1
                one_games['city'] = row[11]
                games[games_key] = one_games
            games_id = games[games_key]['id']
            #sports
            sports_key = row[13]
            if sports_key not in sports:
                one_sport = {}
                one_sport['id'] = len(sports) + 1
                one_sport['sport'] = row[12]
                sports[sports_key] = one_sport
            sports_id = sports[sports_key]['id']
            #athlete_sports_events
            athlete_sports_events_key = (athletes_id, games_id, sports_id)
            if athlete_sports_events_key not in athlete_sports_events:
                one_athlete_event = {}
                if row[14] == "NA":
                    medal = "NULL"
                else:
                    medal = row[14]
                one_athlete_event['medal'] = medal
                athlete_sports_events[athlete_sports_events_key] = one_athlete_event
            # athletes_games
            athlete_games_key = (athletes_id, games_id)
            if athlete_games_key not in athlete_games:
                if row[3] == "NA":
                    age = "NULL"
                else:
                    age = int(row[3])
                if row[4] == "NA":
                    height = "NULL"
                else:
                    height = float(row[4])
                if row[5] == "NA":
                    weight = "NULL"
                else:
                    weight = float(row[5])
                year = int(row[9])
                one_athlete_game = {}
                one_athlete_game['age'] = age
                one_athlete_game['height'] = height
                one_athlete_game['weight'] = weight
                one_athlete_game['team'] = row[6]
                athlete_games[athlete_games_key] = one_athlete_game
    return (athletes, games, sports, teams, athlete_sports_events, athlete_games)

def write_csv(data_dictionary, title, fields_list):
    with open(title, "w") as file:
        writer = csv.DictWriter(file, fields_list)
        for item in data_dictionary:
            #print(key)
            writer.writerow({field: data_dictionary[item].get(field) or item for field in fields_list})

def write_games_csv(data_dictionary):
    with open('games.csv', 'w') as f:
        writer = csv.writer(f)
        for (year, season) in data_dictionary:
            id = data_dictionary[(year, season)]['id']
            city = data_dictionary[(year, season)]['city']
            writer.writerow([id, year, season, city])

def write_athlete_sports_events_csv(data_dictionary):
    with open("athlete_sports_events.csv", 'w') as f:
        writer = csv.writer(f)
        for (athletes_id, games_id, sports_id) in data_dictionary:
            medal = data_dictionary[(athletes_id, games_id, sports_id)]['medal']
            writer.writerow([athletes_id, games_id, sports_id, medal])

def write_athlete_games_csv(data_dictionary):
    with open("athlete_games.csv", 'w') as f:
        writer = csv.writer(f)
        for (athletes_id, games_id) in data_dictionary:
            age = data_dictionary[(athletes_id, games_id)]['age']
            height = data_dictionary[(athletes_id, games_id)]['height']
            weight = data_dictionary[(athletes_id, games_id)]['weight']
            team = data_dictionary[(athletes_id, games_id)]['team']
            writer.writerow([athletes_id, games_id, age, height, weight, team])

'''def write_athletes_csv(data_dictionary):
    file = open("athletes.csv", 'w')
    with file:
        writer = csv.DictWriter(file, data_dictionary.keys())
        for id in data_dictionary:
            data = data_dictionary[id]
            writer.writerow([id, data])'''

def create_reader(csv_name):
    with open(csv_name) as file:
        next(file)
        reader = (list(csv.reader(file, skipinitialspace=True)))
    return reader

def main():
    athlete_events_reader = create_reader('athlete_events.csv')
    noc_regions_reader = create_reader('noc_regions.csv')
    #create data to write into csv
    athletes, games, sports, teams, athlete_sports_events, athlete_games = create_data(athlete_events_reader, noc_regions_reader)
    #write the csv
    write_csv(athletes, "athletes.csv", ['id', 'name', 'sex'])
    write_games_csv(games)
    write_csv(sports, "sports.csv", ['id', 'sport', 'event'])
    write_csv(teams, "teams.csv", ['id', 'NOC', 'region'])
    #create linking tables
    write_athlete_sports_events_csv(athlete_sports_events)
    write_athlete_games_csv(athlete_games)

if __name__ == '__main__':
    main()
