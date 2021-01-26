'''List all the NOCs (National Olympic Committees), in alphabetical order by abbreviation. '''
SELECT DISTINCT noc FROM teams
ORDER BY noc;

'''List the names of all the athletes from Kenya. If your database design allows it, sort the athletes by last name.'''
SELECT athletes.name
FROM athletes
WHERE athletes.noc = "KEN";


'''List all the medals won by Greg Louganis, sorted by year. Include whatever fields in this output that you think appropriate.'''
SELECT athlete_events.medal, sports.event
FROM athlete_events, sports, athletes, games
WHERE athletes.id = athlete_events.athletes_id
AND athletes.name = "Gregory Efthimios ""Greg"" Louganis"
AND sports.id = athlete_events.sports_id
AND games.id = athlete_events.games_id
ORDER BY games.year

'''List all the NOCs and the number of gold medals they have won, in decreasing order of the number of gold medals.'''
SELECT teams.noc, athlete_events.medals
FROM teams, athlete_events, athletes
WHERE athletes.id = athlete_events.athletes_id
AND athletes.noc = teams.NOC
AND athlete_events.medals == "Gold"
GROUP BY team.NOC
ORDER BY COUNT(athlete_events.medals) DESC;
