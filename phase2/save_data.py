import math
import pickle


path = 'data.xlsx'


contents = {}
URLs = {}
inverted_index = {}
token_frequency = {}
token_frequency_inDoc = {}



#some tokens like 'که' - 'از' had about 40000 frequency and 'را' about 120000
#so 60000 is pretty good
max_frequency = 60000


halfSpace_char = '\u200c'

punctuation= '''!()-[]{};:'"\,|؛؟،٪<>./?@#$%^&*_~'''

prefix = ['‌بی‌‌','با‌','بر‌','هم‌‌','نا‌','لا‌','فرا‌'
        ,'فرو‌‌','در‌','بر‌','باز‌','ور‌'
        ,'پس‌‌','پسا‌','پیش‌','سر‌']


postfix = ['تر','تری','ترین',
           'ها','های','هایی',
           'ات','یات','جات',
           'ان','ار',
           'اک','یک','ستان','گر'
           'سرا','کده','گاه']

#because it's Persion the key and value is written vise versa
plural_forms = {
            'مراکز':'مرکز',
            'مشاغل':'شغل',
            'روابط':'رابطه',
            'خدمات':'خدمت',
            'اعمال':'عمل',
            'حوادث':'حادثه',
            'اخبار':'خبر',
            'شرایط':'شرط',
            'مواقع':'موقع',
            'ارقام':'رقم',
            'عوارض':'عارضه',
            'شهداء':'شهید',
            'شهدا':'شهید',
            'مسائل':'مسئله',
            'نتایج':'نتیجه',
            'افراد':'فرد',
            'اقوام':'قوم',
            'معابر':'معبر',
            'اوایل':'اول',
            'عوامل':'عامل',
            'آحاد':'احد',
            'احاد':'احد'
            }


verbs = {
        'گرفتیم':'گرفت',
        'بتوانیم':'توان',
        'دهیم':'ده',
        'می‌رویم':'رو',
        'میرویم':'رو',
        'نخواهد':'خواه',
        'بودیم':'بود',
        'بیاوریم':'آور',
        'داشتیم':'داشت',
        'هستند':'است',
        'بتوانند':'توان',
        'کرده‌ایم':'کرد',
        'شده':'شد',
        'می‌شود':'شد',
        'میشود':'شد',
        'میکند':'کن',
        'می‌کند':'کن',
        'بیایند':'آی',
        'خواهند':'خواه',
        'آمده‌اند':'آی',
        'می‌توانند':'توان',
        'میتوانند':'توان',
        'بگذارد':'گذار',
        'میبرم':'بر',
        'می‌برم':'بر',
        'میکنم':'کن',
        'می‌کنم':'کن',
        'میخواستیم':'خواست',
        'می‌خواستیم':'خواست',
        'میشود':'شد',
        'می‌شود':'شد'
        }
repeated = ["انتهای","پیام"]


# set into a list
def convert(set):
    return sorted(set)


#logarithm
def logarithm(number , b):
    return math.log(number , b)


#remove punctuations
def remove_punctuations(content):
    for x in punctuation:
        content = content.replace(x,'')
    return content




#remove character half space
def remove_halfSpace(token):
    return token.replace(halfSpace_char, '')




#tokenize and filter '![](https://...)' and 'انتهای پیام'
def tokenize(txt):
    t1 = [x for x in txt.split() if (not x.startswith('![]') )]
    return t1



def calculate_tf(token , id):

    w=0

    tf = token_frequency_inDoc[token][id]
    
    if (tf > 0):
        w = 1 + logarithm(tf , 10)

    return w




def I_index(tokens , contents):

    for token in tokens:

        token_frequency[token] = 0
        token_frequency_inDoc[token] = {}

        for i in contents.keys():

            token_frequency_inDoc[token][i] = 0

            if token in contents[i]:
                #calculate the frequency of each token
                token_frequency_inDoc[token][i] += contents[i].count(token)


                if token not in inverted_index:
                    inverted_index[token] = {}

                if token in inverted_index:

                    inverted_index[token][i] = calculate_tf(token, i)

        token_frequency[token] += token_frequency_inDoc[token][i]

        #filter tokens with high frequency
        if(token_frequency[token] >= max_frequency):
            inverted_index.pop(token, None)

    return inverted_index



def update_invertedIndex(token , new_token , inverted_index):
    
    if new_token in inverted_index.keys():
        #union of two dicts
        inverted_index[new_token] = set().union(inverted_index[new_token], inverted_index[token])
    else :
        # print(token)
        # print(new_token)
        inverted_index[new_token] = inverted_index[token]
    
    del inverted_index[token]

    return inverted_index




def remove_suffix(str , token):
    if str in token:
        token = token.replace(str , '')
    return token



def remove_prefix(inverted_index):

    for key in list(inverted_index):

        for p in prefix :

            if key.startswith(p) :

                if key in list(inverted_index):
                    new_key = remove_halfSpace(key)
                    new_key = remove_suffix(p , new_key)
                    update_invertedIndex(key , new_key , inverted_index)

    return inverted_index



def remove_postfix(inverted_index):

    for key in list(inverted_index):

        for p in postfix :

            if key.endswith(p) :

                if key in list(inverted_index):
                    new_key = remove_halfSpace(key)
                    new_key = remove_suffix(p , new_key)
                    update_invertedIndex(key , new_key , inverted_index)

    return inverted_index



#حذف جمع مکسر
def remove_plural(inverted_index):

    for key in list(inverted_index):

        if key in plural_forms.keys():
            # print('key is : ' , key)
            new_key = plural_forms[key]
            # print('new key is : ' , new_key)
            update_invertedIndex(key , new_key , inverted_index)

    return inverted_index


#ریشه یابی افعال
def verbs_root(inverted_index):

    for key in list(inverted_index):

        if key in verbs.keys():

            new_key = verbs[key]
            update_invertedIndex(key , new_key , inverted_index)

    return inverted_index




def one_word(query):

    docs_res = {}

    if query in inverted_index.keys():
        docs = inverted_index[query]

        for d in docs :
            docs_res[d] = URLs[d]

        return d , docs_res
        
    else :
        return 'Sorry! The Query Does Not Found'


def multi_words(tokens):

    relation = {}

    for token in tokens.split():

        if token in inverted_index.keys():

            for i in inverted_index[token]:
                relation[i] += 1

    relation = sorted(relation.items(), key=lambda x: x[1], reverse=True)
    index = list(relation.keys())[0]
    return index,URLs[index]



def main():
    
    # workbook = xlrd.open_workbook(path)
    # sheet = workbook.sheet_by_index(0)

    # start = time.time()
    # # print(sheet.nrows)
    # for i in range(1 , sheet.nrows):

    #     id = int(sheet.cell(i,0).value)
    #     content = remove_punctuations(sheet.cell(i,1).value)
    #     url = sheet.cell(i,2).value
    #     # print(id)

    #     contents[id] = content
    #     URLs[id] = url


    # #create a set to remove duplicates automatically
    # t = set()

    # for c in contents.values():
    #     t = t.union(tokenize(c))

    # #then convert to list again
    # tokens = convert(t)

    # inverted_index = I_index(tokens , contents)


    # # print('\n\n\n\n')

    # # print(inverted_index)

    # inverted_index = remove_postfix(inverted_index)

    # inverted_index = remove_prefix(inverted_index)

    # inverted_index = remove_plural(inverted_index)

    # inverted_index = verbs_root(inverted_index)

    # # print(inverted_index)


    with open("inverted_index.txt", "rb+") as fp1:   # Unpickling
        inverted_index = pickle.load(fp1)


    with open("contents.txt", "rb+") as fp2:
        contents = pickle.load(fp2)


    # print(contents[1])

    # print(len(contents))
    # print('\n\n\n')


    with open("URLS.txt", "rb+") as fp3:
        URLs = pickle.load(fp3)

    with open("token_frequency_inDoc.txt", "rb+") as fp4:
        token_frequency_inDoc = pickle.load(fp4)

    
    with open("tokens.txt", "rb+") as fp5:
        tokens = pickle.load(fp5)




    # with open("inverted_index.txt", "wb") as fp1:   #Pickling
    #     pickle.dump(inverted_index, fp1)
    #     fp1.close()


    # with open("contents.txt", "wb") as fp2:
    #     pickle.dump(contents, fp2)
    #     fp2.close()


    # with open("URLS.txt", "wb") as fp3:
    #     pickle.dump(URLs, fp3)
    #     fp3.close()


    # with open("token_frequency_inDoc.txt", "wb") as fp4:
    #     pickle.dump(token_frequency_inDoc, fp4)
    #     fp4.close()


    # with open("tokens.txt", "wb") as fp5:
    #     pickle.dump(tokens, fp5)
    #     fp5.close()
    
    # end = time.time()

    # print(end-start)

    number = input("1:Single Query\n2:Multi Query\n")
    query = input("Please Enter Your Query: ")

    if (int(number)==1):
        print(one_word(query))

    elif(int(number)==2):
        print(multi_words(query))




if __name__ == "__main__":
    main()