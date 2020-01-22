from jsonclass import jsonclass
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt

class count_distinct_elements(object):
    def __init__(self):
        super().__init__()

    def count(self, mylist):
        mineral_names = []
        element_count = []
        for mydict in mylist:
            name_of_mineral = mydict[list(mydict.keys())[0]]
            number_of_elements = len(mydict[list(mydict.keys())[1]])
            mineral_names.append(name_of_mineral)
            element_count.append(number_of_elements)
        df = pd.DataFrame({'count': element_count,'names': mineral_names}, columns=['count', 'names'])
        #print(df.loc[df['count'] == 7]) # Returns minerals with certain number of elements
        return df.groupby('count').count()       

if __name__ == '__main__' :
    def read_from_csv(filename):
        with open(filename,newline='', encoding='utf-8') as myfile:
            reader = csv.reader(myfile)
            next(reader)
            results = dict(reader)
        return results

    m = read_from_csv('minerals_mindat.csv')
    c = jsonclass().create_clean_dict(m)
    my_groupped_dataframe = count_distinct_elements().count(c)
    my_data_frame = pd.DataFrame(my_groupped_dataframe).reset_index()
    
    my_data_frame1 = pd.DataFrame(my_groupped_dataframe)
    my_data_frame1.plot(kind='bar', colormap = 'rainbow')
    plt.xlabel("Number of elements")
    plt.ylabel("Number of Minerals")
    plt.title("Distribution of number of elements in minerals")

    names_data_actual = my_data_frame['names']

    # generate array with 120 nan
    result = []
    for i in range(1,14):
        result.append(np.linspace(i-1,i,num=10,endpoint=False))
    result = [item for items in result for item in items]
    names_data = np.empty(len(result))
    names_data[:] = np.nan

    # substitute the corresponding counts
    j = 1
    for k in range(0, len(names_data_actual)):
        names_data[j+9] = names_data_actual[k]
        j+=10

    mynewframe = pd.DataFrame({'names': names_data})
    finalframe1 = mynewframe.interpolate(method='polynomial', order=3).plot()
    finalframe = mynewframe.interpolate(method='polynomial', order=3)
    newfinalframe = finalframe.dropna().reset_index()
    plt.scatter(finalframe.index, finalframe.names, s = 60, c = finalframe.names, cmap="PuRd", alpha=0.6)
    plt.title("Distribution of number of elements in minerals")
    plt.xlabel("Number of elements")
    plt.ylabel("Number of Minerals")
    
    plt.show()
    