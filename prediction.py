import pandas as pd
import math
import difflib 
import random


fhand = open('stop_words.txt','r')
stopwords_list = (fhand.read()).split()
fhand.close()
df = pd.read_excel('dataset/dataset_book.xlsx') 
strength = 20 
inpt_name = None

def find_closest(inpt_title):
    title_list = df['title'].tolist()
    for i in range(0,len(title_list)):
        title_list[i] = str(title_list[i])
    title = (difflib.get_close_matches(str(inpt_title),list(title_list)))[0]
    return title


def remove_stopwords(text_list):
    list_append = list()
    for i in text_list:
        if i not in stopwords_list:
            list_append.append(i.strip(' '))
    rand_list = list()
    for i in range(0,strength):
        rand_index = random.randrange(max(0,len(list_append)-100),len(list_append))
        rand_list.append(list_append[rand_index])
    return list_append[:strength] + rand_list 


def get_book_id(book_name):
    try:
        book_id = int((df['book_id'][df['title']==book_name]))
    except:
        book_id = -1
    return book_id

#Returns all the non-stop words
def good_words(book_id):
    string = None
    for i in (df['meta_data'][df['book_id']==book_id]):
        string = i
    if string is None:
        return inpt_name.split(' ')*3
    good_words = remove_stopwords(string.split())
    good_words = set(good_words)
    good_words = list(good_words)
    return good_words + inpt_name.split(' ')*3

def IDF_helper(x,good_word,idf_dict):
    if good_word in str(x):
        idf_dict[good_word] = idf_dict.get(good_word,0)+1

# inverse document frequency
def IDF(idf_dict,good_words_list):
    for word in good_words_list:
        df['meta_data'].apply(IDF_helper,args=[word,idf_dict])
    for i,j in idf_dict.items():
        idf_dict[i]=math.log(df.shape[0]/j,10)


#Calculates term frequency and multiplies it with idf
def TF_helper(x,good_word,tf_dict,idf_dict):
    xlist = x.split()
    tf_dict[xlist[0]] = tf_dict.get(xlist[0],0) + (x.count(good_word)/len(xlist))*(idf_dict.get(good_word,0))

#Calculates the Term frequency 
def TF(tf_dict,good_words_list,idf_dict):
    for word in good_words_list:
        df['meta_data'].apply(TF_helper,args=[word,tf_dict,idf_dict])


def book_predict(book_name):
    global inpt_name
    book_name = book_name.lower()
    inpt_name = book_name
    idf_dict = dict()
    tf_dict = dict()
    tf_idf_list = list()
    book_id = get_book_id(book_name)
    if book_id == -1:
        try:
            book_name = find_closest(book_name)
            book_id = get_book_id(book_name)
        except:
            book_name = inpt_name
    print(book_name)
    good_words_list = good_words(book_id)  
    print(good_words_list)  
    IDF(idf_dict,good_words_list)
    TF(tf_dict,good_words_list,idf_dict)
    tup_list = list()
    for i,j in tf_dict.items(): 
        tup_list.append((j,i))
    tup_list.sort(reverse=True) 
    print(tup_list[:5])
    book_list = list()
    for i,j in tup_list[:20]:   
        for i in (df['title'][df['book_id']==float(j)]):
            s_temp = str(i).strip(' ')
            if s_temp != '' and s_temp != 'nan' and s_temp != ' ' and s_temp!=book_name:
                book_list.append(i)
    return book_list[:10] #Return 10 similar books

    

