import numpy as np;
import pandas as pd;
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import matplotlib.pyplot  as plt;
from sklearn.model_selection  import train_test_split
from sklearn.linear_model  import LogisticRegression
from sklearn.metrics import accuracy_score,confusion_matrix
import os
gmail_list=[]
password_list=[]
gmail_list1=[]
password_list1=[]
history_list=[]

from landslide_predicter import landslide_fn

import numpy as np
from flask import Flask, request, jsonify, render_template,session
import pickle

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def home():
    return render_template('login.html') 

@app.route('/logedin',methods=['POST'])
def logedin():
    
    int_features3 = [str(x) for x in request.form.values()]

    logu=int_features3[0]
    passw=int_features3[1]

# Open database connection
    db = MySQLdb.connect("localhost","root","","Login_Info" )

# prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("SELECT user FROM user_register")
    result1=cursor.fetchall()
             
    for row1 in result1:
                      gmail_list.append(str(row1[0]))
                      

    cursor1= db.cursor()
    cursor1.execute("SELECT password FROM user_register")
    result2=cursor1.fetchall()
    
    for row2 in result2:      
                      password_list.append(str(row2[0]))
                      
    print(password_list)
    if gmail_list.index(logu)==password_list.index(passw):
        session['logu'] = logu 

        user_info = session.get('logu', '')
        return render_template('index.html',message=user_info)
    else:
        return jsonify({'result':'use proper  gmail and password'})
        
@app.route('/register',methods=['POST'])
def register():
    

    int_features2 = [str(x) for x in request.form.values()]
    r1=int_features2[0]
    r2=int_features2[1]

    logu1=int_features2[0]

# Open database connection
    db = MySQLdb.connect("localhost","root",'',"Login_Info" )

# prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("SELECT user FROM user_register")
    result1=cursor.fetchall()
              
    for row1 in result1:        
                      gmail_list1.append(str(row1[0]))
                      
                      
    if logu1 in gmail_list1:
                    return jsonify({'result':'this gmail is already in use '})  
    else:
                  sql = "INSERT INTO user_register(user,password) VALUES (%s,%s)"
                  val = (r1, r2)
   
                  try:
   # Execute the SQL command
                                       cursor.execute(sql,val)
   # Commit your changes in the database
                                       db.commit()
                  except:
   # Rollback in case there is any error
                                       db.rollback()

# disconnect from server
                  db.close()
                 # return jsonify({'result':'succesfully registered'})
                  return render_template('login.html')

                      
@app.route('/index')
def index(): 
    user_info = session.get('logu', None)
    return render_template('index.html',message=user_info)


@app.route('/land_slide_detection')
def land_slide_detection(): 
    user_info = session.get('logu', None)
    return render_template('landslide_detection_page.html',message=user_info)


@app.route('/land_slide_detection/predict',methods=['POST'])
def predict():

    try:
        # Extracting form data
        int_features = [float(x) for x in request.form.values()]
        aspect = request.form.get('aspect')
        strdist = request.form.get('strdist')
        basarea = request.form.get('basarea')
        curvature = request.form.get('curvature')
        curve_cont = request.form.get('curve_cont')
        curve_prof = request.form.get('curve_prof')
        curves = request.form.get('curves')
        elev = request.form.get('elev')
        drop = request.form.get('drop')
        flowdir = request.form.get('flowdir')
        fos = request.form.get('fos')
        lith = request.form.get('lith')
        cohesion = request.form.get('cohesion')
        scarps = request.form.get('scarps')
        scarpdist = request.form.get('scarpdist')
        frictang = request.form.get('frictang')
        slope = request.form.get('slope')
        slopeleg = request.form.get('slopeleg')
        woods = request.form.get('woods')
        specwt = request.form.get('specwt')

        print("Form Data:", int_features, aspect, strdist, lith)  # Add more variables as needed for debugging
    
        output_landslide = landslide_fn(int_features)
        temp = str(output_landslide[0])

        db = MySQLdb.connect("localhost", "root", "", "Login_Info")
        cursor = db.cursor()

        
        user_info = session.get('logu', None)
        if user_info == None:
                user_info = 'admin'
      
        sql = "INSERT INTO history(username, aspect, strdist, basarea, curvature, curve_cont, curve_prof, curves, elev, drop_f, flowdir, fos, lith, cohesion, scarps, scarpdist, frictang, slope, slopeleg, woods, specwt, output) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (user_info, aspect, strdist, basarea, curvature, curve_cont, curve_prof, curves, elev, drop, flowdir, fos, lith, cohesion, scarps, scarpdist, frictang, slope, slopeleg, woods, specwt, temp)
        print(val)
      
        cursor.execute(sql, val)

        # Committing the changes to the database
        db.commit()

        # Closing the database connection
        db.close()

        if output_landslide[0] == 1:
            
            return render_template('final/pass.html', message=user_info, sound_file='posibility.mp3')

        else:
            
            return render_template('final/fail.html', message=user_info, sound_file='noposibility.mp3')

    except Exception as e:
        # Print or log the error message for debugging
        print("Error:", str(e))

        # Rollback the database changes in case of an error
        db.rollback()

        # Close the database connection
        db.close()

        # Return an error response or redirect to an error page
        return "An error occurred. Check the server logs for more details."


    

@app.route('/about')
def about(): 
    user_info = session.get('logu', None)
    return render_template('about.html',message=user_info)

@app.route('/contact')
def contact(): 
    user_info = session.get('logu', None)
    return render_template('contact.html',message=user_info)

@app.route('/description')
def description(): 
    user_info = session.get('logu', None)
    return render_template('description.html',message=user_info)

@app.route('/history')
def history(): 
    
# Open database connection
    db = MySQLdb.connect("localhost", "root", "", "Login_Info")

    # Prepare a cursor object using cursor() method
    cursor = db.cursor()

    cursor.execute("SELECT * FROM history")
    result1 = cursor.fetchall()

    # Initialize history_list before using it
    history_list = []

    for row1 in result1:
        history_list.append(row1)

    # Print or do something with history_list
    #print(history_list[1][0])

    # Close the database connection
    db.close()
    user_info = 'admin'
    return render_template('history.html',message=user_info,history_list=history_list)

@app.route('/logout',methods=['POST'])
def logout():
    # Clear the session
    session.clear()
    # Redirect to the home page or login page after logout
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)
