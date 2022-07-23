import numpy as np
from flask import Flask, request, jsonify, render_template, url_for
import pickle
from prediction import book_predict
import json
import http.client
import threading
import pandas as pd

df = pd.read_excel('dataset/book_links1.xlsx')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods = ['POST'])
def predict():
    title = request.form.to_dict()
    print(title)
    prediction = book_predict(title['book_name'])
    # if prediction == 'book not in dataset':
    #     URLlist = prediction
    if type(prediction) == type(0):
        print("BOOK NOT IN THE DATASET")
        return render_template('result.html', result = ['https://cdn-d8.nypl.org/s3fs-public/blogs/J5LVHEL.jpg'])

    URLlist = list()
    ##
    t0 = threading.Thread(target=get_poster,args=(prediction[0],URLlist))
    t1 = threading.Thread(target=get_poster,args=(prediction[1],URLlist))
    t2 = threading.Thread(target=get_poster,args=(prediction[2],URLlist))
    t3 = threading.Thread(target=get_poster,args=(prediction[3],URLlist))
    t4 = threading.Thread(target=get_poster,args=(prediction[4],URLlist))
    t5 = threading.Thread(target=get_poster,args=(prediction[5],URLlist))
    t6 = threading.Thread(target=get_poster,args=(prediction[6],URLlist))
    t7 = threading.Thread(target=get_poster,args=(prediction[7],URLlist))
    t8 = threading.Thread(target=get_poster,args=(prediction[8],URLlist))
    t9 = threading.Thread(target=get_poster,args=(prediction[9],URLlist))
    t0.start()
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
    t0.join()
    t1.join()
    t2.join()
    t3.join()
    t4.join() 
    t5.join()
    t6.join()
    t7.join()
    t8.join()
    t9.join()
    

    return render_template('result.html', result = URLlist)

#returns URL of the poster, "-1" on error
def get_poster(book_name,URLlist):
    
    
    try:
        for i in ((df['thumbnail'][df['title']==book_name])):
            if(pd.isna(i)==False):
                URLlist.append(i)
            else:
                URLlist.append("https://cdn-d8.nypl.org/s3fs-public/blogs/J5LVHEL.jpg")

        return
    except:
        return "-1"
   


if __name__ == '__main__':
    app.run(debug=True, port=5000)

