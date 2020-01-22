import re
import csv
import json
class jsonclass(object):
    def __init__(self):
        super().__init__()

    def create_clean_dict(self, mydict):
        result = list()
        for key, value in mydict.items():
            newdict = dict()
            splitted = re.findall('\d*\D+', value)
            newsplitted = []
            for e in splitted:
                newsplitted.append(re.findall('[A-Z][^A-Z]*', e))
            newsplitted = [item for items in newsplitted for item in items]
            newsplitted = [w.replace(')', '').replace('(', '').replace('?', '').replace('·','').replace('□', '')
            .replace('\n', '').replace('+', '').replace('-','').replace('[', '').replace(']', '').replace('₂', '')
            .replace('ₓ', '').replace('}', '').replace('{','').replace('☐','') for w in newsplitted]
            newsplitted = list(dict.fromkeys(newsplitted))
            if('u00' not in key):
                if('u00' not in newsplitted):
                    newdict["name"] = key
                    newdict["formula"] = newsplitted
                    result.append(newdict)
                else:
                    pass
            else:
                pass
        return result

    def read_from_csv(self, filename):
        with open(filename,newline='', encoding='utf-8') as myfile:
            reader = csv.reader(myfile)
            next(reader)
            results = dict(reader)
        return results

if __name__ == '__main__' :
    m = jsonclass().read_from_csv('minerals_mindat.csv')
    c = jsonclass().create_clean_dict(m)
    print(c)
    with open('jsondata.txt', 'w', encoding='utf-8') as outfile:  
        json.dump(c, outfile, ensure_ascii=False)