from flask import Flask, render_template,request,session, redirect, url_for,Response,jsonify,make_response
from flask_debug import Debug
import datetime
import json
import sys

sys.path.append('./Test/')

server_name = 'DESKTOP-S66UB4P\MSSQLSERVER_2014' 
username = 'XXX' 
password = 'XXX'
database_name= 'XXXXXX' 

db_drivertemp= pyodbc.drivers()
db_driver=db_drivertemp[0]
db_path =  str("mssql+pyodbc://"+server_name+"/"+database_name+"?driver="+db_driver+"?Trusted_Connection=yes")



@app.route('/',methods=('POST', "GET"))
def index():
   
    session['registerurl'] = 0
    if request.method == 'POST':    
        username = str(request.form['username'])
        password = str(request.form['password'])

        if(username =='admin' and password=='admin'):
            return render_template('XXX.html',username=username)
        else:
            # database_usage
            if(database_used == 1):
             
                engine = sal.create_engine(db_path)
                conn = engine.connect()
    
                command_md5_password = str("select CONVERT(NVARCHAR(50),HashBytes('MD5','"+password+"'),2)")
                sql_query = pd.read_sql_query(command_md5_password, engine)
                md5_password = sql_query.iloc[0,0]
                df = pd.read_sql_query('SELECT * FROM Xuser', engine)
                check_found = 0
                for i in range(len(df)):
                    if(username == df.iloc[i,1] and md5_password == df.iloc[i,2]):
                        check_found = 1
                print('found='+str(check_found))
                if(check_found == 1):
                    
                    engine = sal.create_engine(db_path)
                    conn = engine.connect()
                    session['username'] = str(username)
                    
                    QueryFindID =  str("Select uID from XUser where XUser.uUsername='"+session['username']+"'")
                    df_userId =pd.read_sql_query(QueryFindID,engine)
                    ID_user=str(df_userId.iloc[0,0])
                    session['user_id'] = ID_user
                    CHECKNULLSQL =  str("(select max(auditTrail.logID) from auditTrail)")
                    log_id_check =pd.read_sql_query(CHECKNULLSQL,engine)
                    log_id=str(log_id_check.iloc[0,0])
                    if(log_id=='None'):
                        FirstInsertAudit = str("insert into  auditTrail values (1,'LogIn','btn_LogIn',NULL,CONVERT(DATE, GETDATE()),CONVERT(Time, GETDATE()),'"+ID_user+"')")
                        conn.execute(FirstInsertAudit)
                        print('1 row inserted with first time')
                    else:
                        InsertAudit = InsertAudit = str("insert into  auditTrail values ((select max(auditTrail.logID)+1 from auditTrail),'LogIn','btn_LogIn',NULL,CONVERT(DATE, GETDATE()),CONVERT(Time, GETDATE()),'"+ID_user+"')")
                        conn.execute(InsertAudit)
                        print('1 row inserted')
                    
                    QueryFindrole =  str("select Role from XUser where uUsername = '"+str(session['username'])+"'")
                    df_userrole =pd.read_sql_query(QueryFindrole,engine)
                    roleuser=str(df_userrole.iloc[0,0])


                    if(roleuser=='1'):
                        print('Login by admin')
                        session['registerurl'] = 1
                        return render_template('XXX.html',username=username,createusertag = 'block')
                    else:
                        print('Login by user')
                        session['registerurl'] = 1
                        return render_template('XXX.html',username=username,createusertag = 'none')             
                else:
                    return render_template('indexflask.html', status ="incorrect username or password")
            return render_template('indexflask.html', status ="incorrect username or password")
    return render_template('indexflask.html')
	
	
	
	   
@app.route("/CheckChangePassword", methods=["POST"])
def CheckChangePassword():
  
    retieve_json = request.get_json()
    
    uusername= retieve_json['uName']
    ufirstname = retieve_json['uFirst']
    ulastname = retieve_json['uLast']
    uemail = retieve_json['uMail']
  
    status,username_new = checkcondition(uusername,ufirstname,ulastname,uemail)
    print('=====status: '+str(status),"=====")
    res = make_response(jsonify({'result_change':status,'username_forgotpw':username_new}), 200)
    
    return res

@app.route("/UpdatePassword", methods=["GET","POST"])
def UpdatePassword():

    retieve_json = request.get_json()
    newpassword = retieve_json['password']
    username = retieve_json['username']
    
    engine = sal.create_engine(db_path)
    conn = engine.connect()

    command_md5_password = str("select CONVERT(NVARCHAR(50),HashBytes('MD5','"+newpassword+"'),2)")
    sql_query = pd.read_sql_query(command_md5_password, engine)
    md5_password = sql_query.iloc[0,0]
   
    QueryFindID =  str("select uID from XUser where uUsername = '"+username+"'")
    df_userId =pd.read_sql_query(QueryFindID,engine)
    uID=str(df_userId.iloc[0,0])

    Update_pw_query = str("UPDATE XUser SET XUser.uPassword = '"+md5_password+"' WHERE XUser.uUsername = '"+username+"'")
    conn.execute(Update_pw_query)
    
    InsertAudit = str("insert into  auditTrail values ((select max(auditTrail.logID)+1 from auditTrail),'ChangePassword','btn_ChangePassword','username:"+username+"',CONVERT(DATE, GETDATE()),CONVERT(Time, GETDATE()),'"+uID+"')")
    print(InsertAudit)
    conn.execute(InsertAudit)
    print('====UpdatePassword====')
    res = make_response(jsonify({'result_change':'true'}), 200)
    return res
