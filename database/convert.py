'''
csv creator program convert.py
created by Grace de Benedetti at Carleton College
Prof Jeff Ondich: CS 257, Winter 2020

This program will read the Kaggle CSV files and write one CSV file for each of the tables
in the database design.
'''

import csv


'''\copy [athlete_events] to '[athlete_events.csv]' csv header'''

'''def convert_text_to_numbers(reader):
    for row in reader:
        age = int(row[3])
        height_centimeters = float(row[4])
        weight_kilos = int(row[5])
        year = int(row[9])
    return reader'''

def create_athletes_data(reader):
    athletes = []
    for row in reader:
        if len(row) > 1:
            one_athlete = []
            one_athlete.append(row[0])
            #row[1].split( )
            #print(row[1])
            one_athlete.append(row[1])
            #one_athlete.append(row[1][-1])
            one_athlete.append(row[2])
            one_athlete.append(row[7])
        athletes.append(one_athlete)
    return athletes

def create_games_data(reader):
    games = []
    id = 1
    for row in reader:
        if len(row) > 1 and row[8] not in games:
            one_game = []
            one_game.append(id)
            one_game.append(row[8])
            one_game.append(row[9])
            one_game.append(row[10])
            one_game.append(row[11])
            id += 1
        games.append(one_game)
    return games

def create_sports_data(reader):
    sports = []
    id = 1
    for row in reader:
        if len(row) > 1:
            one_sport = []
            one_sport.append(id)
            one_sport.append(row[12])
            one_sport.append(row[13])
            id += 1
        sports.append(one_sport)
    return sports

def create_teams_data(noc_regions_reader):
    teams = []
    id = 1
    for row in noc_regions_reader:
        if len(row) > 1:
            one_team = []
            one_team.append(id)
            one_team.append(row[0])
            one_team.append(row[1])
            one_team.append(row[2])
            id += 1
        teams.append(one_team)
    return teams

'''def create_athlete_events_data(athletes_reader, games_reader, sports_reader, athlete_events_reader):
    #need to read from newly created csvs
    #one line is made up of appending from athletes, games, then athlete_events
    athlete_events = []
    for row in athelete_events_reader:
        if len(row) > 1:
            one_athlete_event = [athlete_id, games_id, age, height, weight, team]
            one_athlete_event.insert(2, row[3])
            one_athlete_event.insert(3, row[4])
            one_athlete_event.insert(4, row[5])
            one_athlete_event.insert(5, row[6])
    for row in athletes_reader
        athlete_events.append(one_athlete_event)
    return athlete_events

def create_athlete_games_data(athletes_reader, games_reader, athlete_events_reader):
    athlete_games = {}
    for row in athelete_events_reader:
        athlete_games[athletes_id] = row[3], row[4], row[5], row[6];
        if len(row) > 1:
            one_athlete_event = [athlete_id, games_id, age, height, weight, team]
            one_athlete_event.insert(2, row[3])
            one_athlete_event.insert(3, row[4])
            one_athlete_event.insert(4, row[5])
            one_athlete_event.insert(5, row[6])

            one_athlete
        athlete_events.append(one_athlete_event)
    return athlete_events'''

def write_csv(data, title):
    myData = data
    myFile = open(title, "w")
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(myData)

def write_dictcsv(data, title):
    fields = ['id', 'games', 'year', 'season', 'city']
    dict_data = [data]
    myFile = open(title, 'w')
    with myFile:
        writer = csv.DictWriter(myFile, fieldnames = fields)
        for [(games, year, season, city)] in dict_data:
            id = games_dictionary[(games, year, season, city)]
            writer.writerow([id, games, year, season, city])

def create_reader(csv_name):
    with open(csv_name) as file:
        if csv_name == "athlete_events" or "noc_regions":
            next(file)
        reader = (list(csv.reader(file, skipinitialspace=True)))
    return reader

def main():
    athlete_events_reader = create_reader('athlete_events.csv')
    #convert_text_to_numbers(athlete_events_reader)
    #create readers for each csv
    noc_regions_reader = create_reader('noc_regions.csv')
    #create data to write into csv
    athletes = create_athletes_data(athlete_events_reader)
    games = create_games_data(athlete_events_reader)
    sports = create_sports_data(athlete_events_reader)
    teams = create_teams_data(noc_regions_reader)
    #write the csv
    write_csv(athletes, "athletes.csv")
    write_csv(games, "games.csv")
    write_csv(sports, "sports.csv")
    write_csv(teams, "teams.csv")
    #create linking tables
    #athlete_events = create_athlete_events_data(athletes_reader, games_reader, sports_reader, athlete_events_reader)
    #athlete_games = create_athlete_games_data(athletes_reader, games_reader, athlete_events_reader)
    athletes_reader = create_reader('athletes.csv')
    sports_reader = create_reader('sports.csv')
    games_reader = create_reader('games.csv')
    #write_csv(athlete_events, "athlete_events.csv")
    #write_csv(athelete_games, "athlete_games.csv")

if __name__ == '__main__':
    main()
