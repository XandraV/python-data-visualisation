from periodic_table import periodic
from search import Search
import itertools
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__' :
    def read_from_csv(filename):
        with open(filename,newline='', encoding='utf-8') as myfile:
            reader = csv.reader(myfile)
            next(reader)
            results = dict(reader)
        return results

    m = read_from_csv('minerals_mindat.csv')
    elements_mass = periodic.molar_mass
    table = periodic.table
    unique = periodic().element_with_unique_starting()
    not_unique = periodic().element_with_not_unique_starting()

    matrix = np.zeros((118, 2))
    for k, v in elements_mass.items():
        row = list(elements_mass.keys()).index(k)
        if k in unique:
            freq = len(Search().search(k, m))
        elif k in not_unique:
            freq = len(Search().search_spec(k, not_unique[k], m))
        matrix[row][0] = v
        matrix[row][1] = freq

    df = pd.DataFrame(matrix, index=range(0,118), columns=["mass", "occurence"])
    df = df.astype(int)
    df.drop_duplicates(inplace=True)
    df2 = pd.DataFrame(table, index=range(0,118), columns=["element"])
    new = df.join(df2)
    
    new = new.replace(0, np.nan)
    num = new._get_numeric_data()
    num[num < 10] = np.nan
    with open("names.txt", 'w', newline='', encoding='utf-8') as txtfile:
        for item in new.element:
            txtfile.write(str(item)+", ")
    plt.title("Atomic number vs Occurence in minerals")
    plt.xlabel("Atomic number")
    plt.ylabel("Occurence")
    plt.scatter(new.mass, new.occurence, s = new.occurence, c=new.mass, cmap="rainbow", alpha=0.6, edgecolors="grey")
    for i, point in new.iterrows():
        plt.text(point['mass'], point['occurence'], str(point['element']), fontsize = 6, horizontalalignment='center', verticalalignment='center')
    plt.show()