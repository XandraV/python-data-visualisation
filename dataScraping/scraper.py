import requests
from requests import get
import shutil
import re
import json
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def simple_get(url):
    # Attempts to get the content at `url` by making an HTTP GET request.
    # If the content-type of response is some kind of HTML/XML, return the
    # text content, otherwise return None.
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    #Returns True if the response seems to be HTML, False otherwise.
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

def log_error(e):
    print(e)

def validate_group(group_string):
    result = []
    main_result = []
    sub_result = []
    maingroups = ["Elements","Sulfides","Sulfosalts", "Halides","Oxides", "Carbonates", "Nitrates", "Borates", "Sulfates","Phosphates", "Arsenates", "Vanadates", "Silicates", "Organic Compounds"]
    subgroups = ["Metals","Metalloids", "Nonmetals", "Carbides", "Silicides","Nitrides", "Phosphides", "Selenides", "Tellurides", "Arsenides", "Antimonides", "Bismuthides", "Sulfarsenites", "Sulfantimonites","Sulfbismuthies", "Oxysulfosalts","Complex Halides", "Oxyhalides", "Hydroxyhalides", "Iodates", "Nitrates", "Monoborates", "Diborates", "Triborates", "Tetraborates", "Pentaborates", "Hexaborates", "Heptaborates", "Chromates", "Uranyl sulfates", "Molybdates", "Wolframates", "Niobates","Nesosilicates", "Sorosilicates", "Cyclosilicates","Inosilicates", "Phyllosilicates", "Tektosilicates", "Germanates", "Unclassified"]
    for mg in maingroups:
        if mg.lower() in group_string:
            main_result.append(mg)
            #break????
    for sg in subgroups:
        if sg.lower() in group_string:
            sub_result.append(sg)
            #break????
    result.append(main_result)
    result.append(sub_result)
    return result

def validate_color(color_string):
    color_result = []
    colorgroups = ["Yellow","Orange", "Green", "Blue", "Brown","Pink", "Purple", "Violet", "Black", "Red", "Grey", "White", "Blue-green", "Pale brown","Brownish", "Yellow-orange", "Colourless", "Greenish", "Greenish-blue", "Gray", "Yellowish", "Bluish", "Red-brown", "Cream", "Reddish"]
    for clr in colorgroups:
        if clr.lower() in color_string:
            color_result.append(clr)
    return color_result

def create_elements_list(formula_string):
    splitted = re.findall(r'\d*\D+', formula_string)
    newsplitted = []
    for e in splitted:
        newsplitted.append(re.findall('[A-Z][^A-Z]*', e))
    newsplitted = [item for items in newsplitted for item in items]
    newsplitted = [w.replace(')', '').replace('(', '').replace('?', '').replace('·','').replace('□', '')
    .replace('\n', '').replace('+', '').replace('-','').replace('[', '').replace(']', '').replace('₂', '')
    .replace('ₓ', '').replace('}', '').replace('{','').replace('☐','') for w in newsplitted]
    newsplitted = list(dict.fromkeys(newsplitted)) #remove duplicates
    return newsplitted

if __name__ == "__main__" :
    links_list = [('https://www.mindat.org/min-'+ str(i) +'.html') for i in range(28, 5400)]
    result = list()
    for link in links_list:
        newdict = dict()
        soup = BeautifulSoup(simple_get(link), 'html.parser')
        try:
            newdict["name"] = soup.find("h1", {"class", "mineralheading"}).text
        except:
            newdict["name"] = "error occured"
        try:
            #need clean up function from jsonclass.py
            newdict["formula"] = create_elements_list(str(soup(text=re.compile(r'Formula'))[0].parent.parent.contents[1].text))
            newdict["formulaWeb"] = str(soup(text=re.compile(r'Formula'))[0].parent.parent.contents[1].find("span"))
        except:
            newdict["formula-plain-text"] = "no data"
            newdict["formulaWeb"] = "no data"
        try:
            group_data_string = soup.find_all(text=re.compile('Nickel-Strunz 10th'))[0].parent.parent.parent.find("div", {"class", "mindatam2"}).text.lower() 
            validated_group_data = validate_group(group_data_string)
            newdict["mainGroup"] = validated_group_data[0]
            if len(validated_group_data[1]) == 0:
                newdict["subGroup"] = "no subgroups"
            else:
                newdict["subGroup"] = validated_group_data[1]
        except:
            newdict["mainGroup"] = "no data"
            newdict["subGroup"] = "no data"
        try:
            newdict["system"] = soup(text=re.compile(r'Crystal System'))[0].parent.parent.contents[1].text
        except:
            newdict["system"] = "no data"
        try:
            col = validate_color(str(soup(text=re.compile(r'Colour'))[0].parent.parent.contents[1].text))
            if(len(col) > 0):
                newdict["color"] = col
            else:
                newdict["color"] = "no data"
        except:
            newdict["color"] = "no data"
        try: 
            newdict["hardness"] = soup(text=re.compile(r'Hardness'))[0].parent.parent.contents[1].text
        except:
            newdict["hardness"] = "no data"    
        try:
            newdict["mindatLink"] = l
        except:
            newdict["mindatLink"] = "no data"
        try:    
            newdict["specificGravity"] = soup(text=re.compile(r'Specific Gravity'))[0].parent.parent.contents[1].text
        except:
            newdict["specificGravity"] = "no data"    
        try:
            newdict["lustre"] = soup(text=re.compile(r'Lustre'))[0].parent.parent.contents[1].text
        except:
            newdict["lustre"] = "no data"

        #Save image of the mineral
        #try:
        #    referer_url = 'https://www.mindat.org'+str(soup.find("div", {"class", "minpagephotobox hidephone hidepc"}).find("div", {"class", "userbigpicture noborder"}).find("a")['href'])
        #    soup = BeautifulSoup(simple_get(referer_url), 'html.parser')
        #    request_url = 'https://www.mindat.org/' + str(soup.findAll('img')[9]['src'])
        #    r = requests.get(request_url, stream=True, headers={'Referer':referer_url, 'User-agent':'hello'})
        #    if r.status_code == 200:
        #        with open(newdict["name"] + '.jpg', 'wb') as f:
        #            r.raw.decode_content = True
        #            shutil.copyfileobj(r.raw, f)
        #except:
        #    pass
        
        count = 0
        for w in newdict:
            if 'no data' in newdict[w]:
                count+=1
        if count < 1:
            result.append(newdict)
            print(newdict['name'])
        continue
       
    with open('newmineralsdata.txt', 'w', encoding='utf-8') as txtfile:
            txtfile.write(str(result))
