# Gayathri-Balachandran-Project-3_Python-for-DS

Could not upload venv folder due to size limit. In order to run this project, please download the zip file from my drive location below:

https://drive.google.com/drive/folders/1y6UptcDgkFaCSRqB1mreNWvTAriYjTkJ

After downloading zip from above location in google drive: 

Before running, please follow below instructions:
1. configure MySQL DB and create loan_prediction_db by below SQL command:
 
 create database loan_prediction_db;

2. In the app.py file in line 21, please configure your MYSQL username and password accordingly. My (username,password) is (root,root)
   so it is configured as : app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/loan_prediction_db'

3. If you open the project in pycharm, when you get a notification to install requirements, so install all of them before running.

4. Please run the application by using app.py 
   
