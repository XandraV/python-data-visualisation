from periodic_table import periodic
from search import Search
import itertools
import csv
import numpy as np
import seaborn as sns
import pandas as pd
import plotly.plotly as py
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
np.set_printoptions(threshold=np.nan)

class creatematrix():
    def __init__(self):
        super().__init__()

    def get_numbers_array():
        element_numbers = dict()
        for element in periodic.table:
            element_numbers[element] = periodic.table.index(element)
        return element_numbers

    def get_number(self, el, to_be_paired_elements):
        number = to_be_paired_elements.index(el)
        return number
    # Returns how many minerals conatain an element with unique starting letter
    def occurence_unique(self, element, mineral_dict):
        return len(Search.search(element, mineral_dict))

    # Returns how many minerals conatain an element with non-unique starting letter
    def occurence_not_unique(self, element, mineral_dict):
        return len(Search.search_spec(element, eval(periodic.element_with_not_unique_starting().get(element)), mineral_dict))

    # Returns an array of elements with unique starting letters that occur more than 0 times in minerals
    def unique_to_be_paired(self, unique_array, mineral_dict):
        to_be_paired = []
        for i in range(len(unique_array)):
            frequency = self.occurence_unique(unique_array[i], mineral_dict)
            if frequency != 0:
                #print(str(unique_array[i])+': '+str(frequency))
                to_be_paired.append(unique_array[i])
        return to_be_paired

    # Returns an array of elements with non-unique starting letters that occur more than 0 times in minerals
    def non_unique_to_be_paired(self, non_unique_array, mineral_dict):
        to_be_paired = []
        for key in non_unique_array.keys():
            frequency = self.occurence_not_unique(key, mineral_dict)
            if frequency != 0:
                #print(str(key)+': '+str(frequency))
                to_be_paired.append(key)
        return to_be_paired

    def get_links_dict_with_indexes(self, elements_with_not_searched_array, pairs_array, mineral_dict):
        links = dict()
        for i in range(len(pairs_array)):
            not_searched_elements = []
            for j in range(0,2):
                el = pairs_array[i][j]
                try:
                    not_searched_elements += not_one[el]
                except:
                    pass
            link_num = len(Search.search_spec_two_element(pairs_array[i][0], pairs_array[i][1], not_searched_elements, mineral_dict))
            element1 = self.get_number(str(pairs_array[i][0]), to_be_paired)
            element2 = self.get_number(str(pairs_array[i][1]), to_be_paired)
            key = (element1, element2)
            value = str(link_num)
            links[key] = value
        return links

    def replace_values_with_ones(mineral_matrix):
        for i in range(len(mineral_matrix)):
            for j in range(len(mineral_matrix[i])):
                if mineral_matrix[i][j] != 0:
                    mineral_matrix[i][j] = 1

    def fill_matrix(mineral_matrix, link_dict):
        for i in range(len(link_dict)):
            index_i = list(link_dict.keys())[i][0]
            index_j = list(link_dict.keys())[i][1]
            mineral_matrix[index_i][index_j] = link_dict[list(link_dict.keys())[i]]
    
    def calculate_pairs(to_be_paired_list):
        return list(itertools.combinations(to_be_paired_list, 2))

    def get_data_for_react_heatmap(self, data_stack):
        result = []
        for index, data in data_stack.iteritems():
            result.append('{'+('x:"{}1", y:"{}2", cellValue:{}, color:{}').format(index[0], index[1], data, data)+'}')
        return result
    
    def read_from_csv(self, filename):
        with open(filename,newline='', encoding='utf-8') as myfile:
            reader = csv.reader(myfile)
            next(reader)
            results = dict(reader)
        return results

if __name__ == '__main__' :
    my_data = creatematrix().read_from_csv('minerals_mindat.csv')

    unique_element = periodic.element_with_unique_starting()
    not_unique_element = periodic.element_with_not_unique_starting()

    to_be_paired = creatematrix().non_unique_to_be_paired(not_unique_element, my_data) + creatematrix().unique_to_be_paired(unique_element, my_data)
    
    pairs = creatematrix.calculate_pairs(to_be_paired)
    links = creatematrix().get_links_dict_with_indexes(not_unique_element, pairs, my_data)

    matrix = np.zeros((74,74))
    creatematrix.fill_matrix(matrix, links)
    df = pd.DataFrame(matrix, index=to_be_paired, columns=to_be_paired)
    df = df.astype(int)
    df.drop_duplicates(inplace=True)
    print(to_be_paired)
    
    data_stack = df.stack()
    heatmap_data_for_react = creatematrix().get_data_for_react_heatmap(data_stack)

    # heatmapdata.text is the same as heatmap_data_for_react array above
    #with open('heatmapdata.txt', 'w', encoding='utf-8') as txtfile:
            #txtfile.write(str(result))
    sns.heatmap(df, fmt='g', xticklabels=True, yticklabels=True)
    plt.show()



    
    