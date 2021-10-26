import xlrd

path = 'data.xlsx'


contents = {}
URLs = {}
inverted_index = {}
frequency = {}


#some tokens like 'که' - 'از' had about 40000 frequency and 'را' about 120000
#so 60000 is pretty good
max_frequency = 60000


halfSpace_char = '\u200c'

punctuation= '''!()-[]{};:'"\,|؛؟،٪<>./?@#$%^&*_~'''

prefix = ['بی','با','بر','هم','نا','لا','فرا'
        ,'فرو','در','بر','باز','ب','ور'
        ,'آ','پس','پسا','پیش','سر','ش','ن']


postfix = ['تر','تری','ترین',
           'ها','های','هایی',
           'ات','یات','جات',
           'ان','ی','ا','ار',
           'اک','یک','ستان','گر'
           'سرا','ش','کده','گاه']

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
    t1 = [x for x in txt.split() if (not x.startswith('![]') and (not x in repeated))]
    return t1



def I_index(tokens , contents):

    for token in tokens:
        frequency[token]=0

        for i in contents.keys():

            if token in contents[i]:
                #calculate the frequency of each token
                frequency[token] += contents[i].count(token)


                if token not in inverted_index:
                    inverted_index[token] = []

                if token in inverted_index:
                    inverted_index[token].append(i)


        ##filter tokens with high frequency
        if(frequency[token] >= max_frequency):
            inverted_index.pop(token, None)

    return inverted_index




def remove_suffix(str , token):
    if str in token:
        token = token.replace(str , '')
    return token




def update_invertedIndex(token , new_token , inverted_index):
    
    if new_token in inverted_index.keys():
        inverted_index[new_token] = inverted_index[new_token].union(inverted_index[token])
    else :
        inverted_index[new_token] = inverted_index[token]
    
    del inverted_index[token]

    return inverted_index




def remove_prefix(inverted_index):

    for key in inverted_index.keys():

        for p in prefix :

            if p in key and halfSpace_char in key :

                new_key = remove_halfSpace(key)
                new_key = remove_suffix(p , new_key)
                update_invertedIndex(key , new_key , inverted_index)

    return inverted_index




def remove_postfix(inverted_index):

    for key in inverted_index.keys():

        for p in postfix :

            if p in key and halfSpace_char in key :

                new_key = remove_halfSpace(key)
                new_key = remove_suffix(p , new_key)
                update_invertedIndex(key , new_key , inverted_index)

    return inverted_index


#حذف جمع مکسر
def remove_plural(inverted_index):

    for key in inverted_index.keys():

        for i in plural_forms.keys():

            new_key = plural_forms[i]
            update_invertedIndex(key , new_key , inverted_index)

    return inverted_index



#ریشه یابی افعال
def verbs_root(inverted_index):

    for key in inverted_index.keys():

        for i in verbs.keys():

            new_key = verbs[i]
            update_invertedIndex(key , new_key , inverted_index)

    return inverted_index



def one_word(token):
    result = {}

    if token in inverted_index.keys():
        list = inverted_index[token]
        for x in list :
            result[x] = URLs[x]
        return result
        
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
    
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_index(0)

    for i in range(1 , sheet.nrows):

        id = int(sheet.cell(i,0).value)
        content = remove_punctuations(sheet.cell(i,1).value)
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

    inverted_index = I_index(tokens , contents)

    remove_postfix(inverted_index)

    remove_prefix(inverted_index)

    remove_plural(inverted_index)

    verbs_root(inverted_index)

    number = input("1:Single Query\n2:Multi Query")
    val = input("Please Enter Your Query: ")

    if (number==1):
        one_word(val)
    elif(number==2):
        multi_words(val)
    else :
        print('invalid input')





if __name__ == "__main__":
    main()