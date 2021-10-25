import xlrd

path = 'data.xlsx'


contents = {}
URLs = {}
inverted_index = {}

repeated = ["انتهای","پیام"]

newLineCharacter = '\n'



# set into a list
def convert(set):
    return sorted(set)


#remove character half space
def remove_newLineCharacter(token):
    return token.replace(newLineCharacter, '')


#tokenize and filter '![](https://...)' and 'انتهای پیام'
def tokenize(txt):
    t1 = [remove_newLineCharacter(x) for x in txt.split() if (not x.startswith('![]') and (not x in repeated))]
    return t1



def I_index(tokens , contents):

    for token in tokens:

        for i in contents.keys():

            if token in contents[i]:

                if token not in inverted_index:
                    inverted_index[token] = []

                if token in inverted_index:
                    inverted_index[token].append(i)

    return inverted_index



def main():
    
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_index(0)

    for i in range(1 , sheet.nrows):

        id = int(sheet.cell(i,0).value)
        content = sheet.cell(i,1).value
        url = sheet.cell(i,2).value
        # print(id)

        contents[id] = content
        URLs[id] = url



    #create a set to remove duplicates automatically
    t = set()

    for c in contents.values():
        t = t.union(tokenize(c))

    #then convert to list again
    tokens = convert(t)


    f = open("inverted_index.txt", "a")
    f.truncate(0)
    f.write(I_index(tokens , contents))
    f.close()

    f1 = open("contents.txt", "a")
    f1.truncate(0)
    f1.write(contents)
    f1.close()

    f2 = open("urls.txt", "a")
    f2.truncate(0)
    f2.write(URLs)
    f2.close()

if __name__ == "__main__":
    main()