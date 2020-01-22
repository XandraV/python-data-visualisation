class periodic(object):

    table = ["H", "He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr","Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe","Cs","Ba","La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn","Fr","Ra","Ac","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr","Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Cn","Nh","Fl","Mc","Lv","Ts","Og"]
    molar_mass = {"H": "1", "He": "4", "Li": "7", "Be": "9", "B": "10.81", "C": "12.01", "N": "14.00", "O": "15.99", "F": "18.99", "Ne": "20.17", "Na": "22.98", "Mg": "24.30", "Al": "26.98", "Si": "28.08", "P": "30.97", "S": "32.06", "Cl": "35.45", "Ar": "39.94", "K": "39.09", "Ca": "40.07", "Sc": "44.95", "Ti": "47.86", "V": "50.94", "Cr": "51.99", "Mn": "54.93", "Fe": "55.84", "Co": "58.93", "Ni": "58.69", "Cu": "63.54", "Zn": "65.38", "Ga": "69.72", "Ge": "72.64", "As": "74.92", "Se": "78.96", "Br": "79.90", "Kr": "83.79", "Rb": "85.46", "Sr": "87.62", "Y": "88.90", "Zr": "91.22", "Nb": "92.90", "Mo": "95.96", "Tc": "98", "Ru": "101.07", "Rh": "102.90", "Pd": "106.42", "Ag": "107.86", "Cd": "112.41", "In": "114.81", "Sn": "118.71", "Sb": "121.76", "Te": "127.60", "I": "126.90", "Xe": "131.29", "Cs": "132.90", "Ba": "137.32", "La": "138.90", "Ce": "140.11", "Pr": "140.90", "Nd": "144.24", "Pm": "145", "Sm": "150.36", "Eu": "151.96", "Gd": "157.25", "Tb": "158.92", "Dy": "162.50", "Ho": "164.93", "Er": "167.25", "Tm": "168.93", "Yb": "173.05", "Lu": "174.96", "Hf": "178.49", "Ta": "180.94", "W": "183.84", "Re": "186.20", "Os": "190.23", "Ir": "192.21", "Pt": "195.08", "Au": "196.96", "Hg": "200.59", "Tl": "204.38", "Pb": "207.2", "Bi": "208.9", "Po": "209", "At": "210", "Rn": "222", "Fr": "223", "Ra": "226", "Ac": "227", "Th": "232.03", "Pa": "231.03", "U": "238.02", "Np": "237", "Pu": "244", "Am": "243", "Cm": "247", "Bk": "247", "Cf": "251", "Es": "252", "Fm": "257", "Md": "258", "No": "259", "Lr": "262", "Rf": "267", "Db": "268", "Sg": "271", "Bh": "272", "Hs": "270", "Mt": "276", "Ds": "281", "Rg": "280", "Cn": "285", "Nh": "284", "Fl": "289", "Mc": "288", "Lv": "293", "Ts": "294", "Og": "294"} 

    def search(self, element):
        result = []
        for i in range(len(periodic.table)):
            if element in periodic.table[i] and element != periodic.table[i]:
                result.append(periodic.table[i])
        return result

    # returns array of elements that doesn't need an array of elements to exclude when searching for it in minerals
    def element_with_unique_starting(self):
        only_one = []
        for i in range(len(periodic.table)):
            kimarad = self.search(periodic.table[i])
            # not returns true if the expression after it is false ie empty or zero
            if not kimarad:
                only_one.append(str(periodic.table[i]))
        return only_one

    # returns array of elements along with the elements with same starting letter, that needs to be excluded when searching for it in minerals
    def element_with_not_unique_starting(self):
        not_one = dict()
        for i in range(len(periodic.table)):
            kimarad = self.search(periodic.table[i])
            if (len(kimarad) != 0):
                not_one[str(periodic.table[i])]= str(kimarad)
        return not_one

if __name__ == '__main__' :

    print(periodic().element_with_unique_starting())
    
    print(periodic().element_with_not_unique_starting())