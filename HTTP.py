#!/usr/bin/env python3
'''
    HTTP.py
    Grace de Benedetti, January 2021
    How to retrieve results
    from an HTTP-based API, parse the results (JSON in this case),
    and manage the potential errors.
'''

import sys
import argparse
import json
import urllib.request

API_BASE_URL = 'https://api.covidtracking.com'

def get_state_covid_cases(state):
    url = f'{API_BASE_URL}/v1/states/{state}/current.json'
    data_from_server = urllib.request.urlopen(url).read()
    string_from_server = data_from_server.decode('utf-8')
    covid_information_dictionary = json.loads(string_from_server)
    result_list = []
    positive = covid_information_dictionary.get('positive')
    death = covid_information_dictionary.get('death')
        #part_of_speech_category = part_of_speech.get('partofspeechcategory', '')
    result_list.append({'positive':positive, 'death':death})
    return result_list

def main(args):
    covid_cases = get_state_covid_cases(args.state)
    print(covid_cases)



if __name__ == '__main__':
    # When I use argparse to parse my command line, I usually
    # put the argparse setup here in the global code, and then
    # call a function called main to do the actual work of
    # the program.
    parser = argparse.ArgumentParser(description='Get covid case info from the COVID API')

    parser.add_argument('-state',
                        metavar='state',
                        help='state abbreviation')
                        #choices=['root', 'conjugate'])


    args = parser.parse_args()
    main(args)
