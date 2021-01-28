'''List all the NOCs (National Olympic Committees), in alphabetical order by abbreviation. '''
SELECT DISTINCT noc FROM teams
ORDER BY noc;

'''List the names of all the athletes from Kenya. If your database design allows it, sort the athletes by last name.'''
SELECT athletes.name
FROM athletes, athletes_games
WHERE athletes.id = athletes_games.athletes_id
AND athletes_games.team = 'Kenya';


'''List all the medals won by Greg Louganis, sorted by year. Include whatever fields in this output that you think appropriate.'''
SELECT athlete_sports_events.medal, sports.event, games.year
FROM athlete_sports_events, sports, athletes, games
WHERE athletes.id = athlete_sports_events.athletes_id
AND athletes.name = 'Gregory Efthimios "Greg" Louganis'
AND athlete_sports_events.medal IS NOT NULL
AND sports.id = athlete_sports_events.sports_id
AND games.id = athlete_sports_events.games_id
ORDER BY games.year;


'''List all the NOCs and the number of gold medals they have won, in decreasing order of the number of gold medals.'''
SELECT teams.noc, COUNT(athlete_sports_events.medal)
FROM athlete_sports_events, teams
WHERE athlete_sports_events.medal = 'Gold'
AND athlete_sports_events.NOC = teams.NOC
GROUP BY teams.noc
ORDER BY COUNT(athlete_sports_events.medal) DESC;
