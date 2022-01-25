"""
This file defines the functions to call the APIs of MAKES.
https://docs.microsoft.com/en-us/azure/cognitive-services/KES/evaluatemethod
https://docs.microsoft.com/en-us/azure/cognitive-services/KES/calchistogrammethod
https://docs.microsoft.com/en-us/azure/cognitive-services/KES/interpretmethod
"""

import requests as rq
import json
import time

entity_engine_host = 'http://makes-isi-entity-engine.cloudapp.net/'
semantic_interpretation_engine_host = 'http://makes-isi-entity-engine.cloudapp.net/'
step = 1000

# def composite(a, b):
#     if type(b) == 'string':
#         return "Composite({}=='{}')".format(a, b)
#     else:
#         return "Composite({}=={})".format(a, b)
#
# def And(a, b):
#
#
#
#
# def expr_generate(**kwargs):
#     result = ""
#     for each in kwargs:
#         if '.' in each:
#             result += 'Composite'
#


def request_url(url, retry_interval=2, retry_times=5):
    connection_error_retry = retry_times
    json_error_retry = retry_times
    while connection_error_retry != 0 and json_error_retry != 0:
        try:
            r = rq.get(url)
            if r.status_code != 200:
                print('invalid status code')
                return {}
            result = r.json()
            return result
        except (OSError, ConnectionError, TimeoutError):
            time.sleep(retry_interval)
            print('successfully dealt with connection error')
            connection_error_retry -= 1
        except json.decoder.JSONDecodeError:
            time.sleep(retry_interval)
            print('successfully dealt with json decode error')
            json_error_retry -= 1

    # exceeded retry_times
    return {'entities': [], 'num_entities': -1}


def calcHistogram(field, year):
    # This function returns the number of papers in the specific field in the given year.

    expr = "And(Composite(F.FN=='{}'),Y={})".format(field, year)
    url = entity_engine_host + "calchistogram?expr={}&timeout=100000000".format(expr)
    result = request_url(url)
    if not result['num_entities']:
        return False
    num = result['num_entities']
    return num


# def evaluate(field, year, count):
#     # This function returns all the paper entities of a given filed in a given year
#     papers = []
#     for i in range(0, count, step):
#         method = 'evaluate?'
#         expr = "expr=And(Composite(F.FN=='{}'),Y={})".format(field, year)
#         attributes = "&attributes=Id,Ti,CC,RId,Y,D,AA.AfId,AA.DAfN,AA.AuId,AA.DAuN,AA.S,F.FN,C.CId,C.CN,J.JId,J.JN"
#         options = "&count={}&offset={}&timeout=100000000".format(step, i)
#         url = entity_engine_host + method + expr + attributes + options
#         result = request_url(url)
#         entities = result['entities']
#         papers.extend(entities)
#         print(year, len(papers), '/', count, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
#     return papers


def evaluate(field, year, count, offset):
    method = 'evaluate?'
    expr = "expr=And(Composite(F.FN=='{}'),Y={})".format(field, year)
    attributes = "&attributes=Id,Ti,CC,RId,Y,D,AA.AfId,AA.DAfN,AA.AuId,AA.DAuN,AA.S,F.FN,C.CId,C.CN,J.JId,J.JN"
    options = "&count={}&offset={}&timeout=100000000".format(step, offset)
    url = entity_engine_host + method + expr + attributes + options
    result = request_url(url)
    entities = result['entities']
    print(year, offset, '/', count, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    return entities


def conference_display_name(conference_id):
    url = entity_engine_host + "evaluate?expr=" \
          + "Id=%s" % conference_id \
          + "&attributes=Id,DCN"
    while 1:
        try:
            r = rq.get(url)
            break
        except (OSError, ConnectionError, TimeoutError):
            time.sleep(2)
            print('**********************successfully dealt with error******************')
    result = r.json()
    return result['entities'][0]['DCN']


def journal_display_name(journal_id):
    url = entity_engine_host + "evaluate?expr=" \
          + "Id=%s" % journal_id \
          + "&attributes=Id,DJN"
    while 1:
        try:
            r = rq.get(url)
            break
        except (OSError, ConnectionError, TimeoutError):
            time.sleep(2)
            print('**********************successfully dealt with error******************')
    result = r.json()
    return result['entities'][0]['DJN']


def interpret(title):
    url = semantic_interpretation_engine_host + "interpret?query=%s" % title
    while 1:
        try:
            r = rq.get(url)
            break
        except (OSError, ConnectionError, TimeoutError):
            time.sleep(2)
            print('**********************successfully dealt with error******************')

    if r.status_code != 200:
        return False
    result = r.json()
    if not result['interpretations']:
        return False
    interpretation = result['interpretations'][0]
    rule = interpretation['rules'][0]
    output = rule['output']
    value = output['value']
    return value


def get_paper_data(title):
    interpretation = interpret(title)
    if not interpretation:
        return False
    paper_data = evaluate(interpretation)
    if not paper_data:
        return False

    return paper_data


if __name__ == '__main__':
    print(conference_display_name(1158167855))
