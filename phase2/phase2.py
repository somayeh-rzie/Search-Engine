import math
from heapq import heappop, heappush
import pickle
from itertools import islice


k=5
threshhold = 10

doc_length = {}
champion_list = {}
scores = {}

heap_flag = 1
champion_flag = 1
index_elimination_flag = 1

# set into a list
def convert(set):
    return sorted(set)


#sort
def sort(list):
    return sorted(list.items(), key=lambda x: x[1], reverse=True)


#power
def power(b , p):
    return math.pow(b ,p)



#logarithm
def logarithm(number , b):
    return math.log(number , b)





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




# def one_word(query):

#     docs_res = {}

#     if query in inverted_index.keys():
#         docs = inverted_index[query]

#         for d in docs :
#             docs_res[d] = URLs[d]

#         return d , docs_res
        
#     else :
#         return 'Sorry! The Query Does Not Found'




# def multi_words(tokens):

#     token_relevance = {}

#     for token in tokens.split():

#         if((index_elimination_flag and calculate_idf(token)<threshhold) or (not index_elimination_flag)):

#             if (token in inverted_index.keys()):

#                 for i in inverted_index[token]:
#                     token_relevance[i] += 1

#     token_relevance = sort(token_relevance)
    
#     d = list(token_relevance.keys())[0]

#     return d,URLs[d]





def C_list(tokens):

    for t in tokens:

        champion_list[t] = {}
        if t in inverted_index.values():
            for id in inverted_index[t].keys():

                champion_list[t][id] = inverted_index[t][id] / calculate_doc_length(id)

            champion_list[t] = sort(champion_list[t])

    return champion_list





def calculate_doc_length(id):

    l = 0
    for token in contents[id].split():
        # print(inverted_index[token])
        # print('\n\n\n')
        if token in inverted_index.keys():
            for id , num in enumerate(inverted_index[token]):
                l += power(num , 2)  
    
    l= power(l , 1.0/2)

    return l




def calculate_tf(token , id):

    w=0

    tf = token_frequency_inDoc[token][id]
    
    if (tf > 0):
        w = 1 + logarithm(tf , 10)

    return w




def calculate_idf(token):

    N = len(contents)
    df = len(inverted_index[token])

    idf = logarithm((N / df) , 10)
    return idf




def tf_idf(token, id):

    return calculate_tf(token, id) * calculate_idf(token)




def cosine_similarity(query, id):

    result = 0

    for token in query.split():
        if token in contents[id].split():
            result += tf_idf(token, id) * inverted_index[token][id]
    
    result /= doc_length[id]
    return result




def calculate_score(query , champion_list):
    
    for token in query.split():
        # print('helllllllllllooooooooooooo')
        # print('token is : ' , token)

        if (champion_flag == 1) :
            if ((token in champion_list.keys()) and (not champion_list[token])):
                # print('+++++++',champion_list[token])
                for j in champion_list[token]:
                    print(j)
                    # print('helllllllllllooooooooooooo')
                    id = j[0]
                    scores[id] = 0
                    if id in scores.keys():
                        scores[id] += cosine_similarity(token,id)
        
        else :
            for j in inverted_index[token]:
                id = j[0]
                scores[id] = 0
                if id in scores.keys():
                    scores[id] += cosine_similarity(token,id)

    return scores




def bubble_sort(my_list):

    for mx in range(len(my_list)-1, -1, -1):
        swapped = False
        for i in range(mx):
            if my_list[i][1] < my_list[i+1][1]:
                my_list[i], my_list[i+1] = my_list[i+1], my_list[i]
                swapped = True
        if not swapped:
            break

    return my_list



def k_scores(query , champion_list):
    scores = calculate_score(query , champion_list)
    # print(scores)

    best_scores = {}

    if (heap_flag == 1):

        heap = []

        # print(scores)
        for id in scores.keys():
            heappush(heap, (-scores[id], id))
            # print(id)


        for i in range(k):
            max, id = heappop(heap)
            best_scores[id] = -max

    else :
        best_scores = bubble_sort(scores)
        return list(islice(best_scores, k))


    return best_scores






def main():

    global inverted_index , contents , URLs , token_frequency_inDoc , champion_list
    

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


    champion_list = C_list(tokens)
    # print('champion list : ' , champion_list)


    number = input("1:Single Query\n2:Multi Query\n")
    query = input("Please Enter Your Query: ")

    if (int(number)==1):
        print(one_word(query))

    elif(int(number)==2):
        print(multi_words(query))

    else :
        print('invalid input')

    # else :
    #     print('invalid input')



if __name__ == "__main__":
    main()