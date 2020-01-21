import re
import itertools
from periodic_table import periodic

class Search(object):

    def __init__(self):
        super().__init__()

    def search(phrase, mydict):
        a = []
        for key, value in mydict.items():
            if str(phrase) in str(value):
                a.append(key)
        return a

    def search_molecule(molecule, mydict):
        a = []
        for key, value in mydict.items():
            clean_value = re.sub('\d', '', value)
            if molecule in clean_value:
                a.append(key)
        return a
    
    def search_spec(searched_element, not_searched, mydict):
        result = []
        ok = False
        for key, value in mydict.items():
            if str(searched_element) in str(value):
                splitted = re.findall('\d*\D+', value)
                newsplitted = []
                for e in splitted:
                    newsplitted.append(re.findall('[A-Z][^A-Z]*', e))
                newsplitted = [item for items in newsplitted for item in items]
                newsplitted = [w.replace(')', '').replace('(', '').replace('?', '').replace('·','').replace('□', '')
                .replace('\n', '').replace('+', '').replace('-','').replace('[', '').replace(']', '').replace('₂', '')
                .replace('ₓ', '').replace('Σ', '') for w in newsplitted]
                two_character_list = []
                for i in range(len(newsplitted)):
                    line = newsplitted[i]
                    n = 2
                    newelement = [line[i:i+n] for i in range(0, len(line), n)][0]
                    two_character_list.append(newelement)
                #print(two_character_list)

                if all(x in two_character_list for x in [searched_element]):
                    result.append(value)

                #if searched_element in two_character_list:
                #    if searched_element not in not_searched:
                 #       result.append(value)
        #print(result)
        return result
        

    def search_spec_two_element(searched_element, searched_element2, not_searched, mydict):
        result = []
        ok = False
        for key, value in mydict.items():
            if searched_element in value:
                splitted = re.findall('\d*\D+', value)
                newsplitted = []
                for e in splitted:
                    newsplitted.append(re.findall('[A-Z][^A-Z]*', e))
                newsplitted = [item for items in newsplitted for item in items]
                newsplitted = [w.replace(')', '').replace('(', '').replace('?', '').replace('·','').replace('□', '')
                .replace('\n', '').replace('+', '').replace('-','').replace('[', '').replace(']', '').replace('₂', '')
                .replace('ₓ', '').replace('}','').replace('{','') for w in newsplitted]
                two_character_list = []
                for i in range(len(newsplitted)):
                    line = newsplitted[i]
                    n = 2
                    newelement = [line[i:i+n] for i in range(0, len(line), n)][0]
                    two_character_list.append(newelement)
                #print(two_character_list)
                if all(x in two_character_list for x in [searched_element, searched_element2]):
                    result.append(value)

        #print(result)
        return result