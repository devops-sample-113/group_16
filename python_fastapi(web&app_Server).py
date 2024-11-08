#!/usr/bin/env python3
# coding=utf-8
# -*- coding: UTF-8 -*-
from fastapi import FastAPI, Form , Cookie , Request
from fastapi.responses import *
import MySQLdb

app = FastAPI()


@app.get('/', response_class=HTMLResponse)
def index():
    form = """
    <form method="post" action="/login" >
        ID: <input type="number" name="ID">
        Password: <input name="Password">
        <input type="submit" value="登入">
    </form>
    """
    return form

@app.post('/login' , response_class=HTMLResponse)
def login( response:Response , ID: int = Form() , Password: str = Form()):
    name = "<h1>"
    try:
        name += loginSQL(ID,Password ,\
            "Select First_Name , Last_Name From Student where ID={}".format(ID)) +\
            "</h1>"
    except Exception as e:
        print(e)
        return """Error : login crediental error""" + """<meta http-equiv="Refresh" content="3; URL=http://127.0.0.1:8000/" />"""
    else:
        response.set_cookie("ID" , ID)
        response.set_cookie("Password" , Password)
    
    return name + """<meta http-equiv="Refresh" content="3; URL=http://127.0.0.1:8000/log" />"""

def loginSQL(ID:int , Password:str , Query:str):
    conn = MySQLdb.connect(host="127.0.0.1",
                           user=str(ID),
                           passwd=Password,
                           db="testdb")
    # 欲查詢的 query 指令
    #query = "Select First_Name , Last_Name From Student where ID={}".format(ID)
    # 執行查詢
    cursor = conn.cursor()
    cursor.execute(Query)

    results = "Welcome,"
    for y in cursor.fetchall():
        for x in y:
            results += " {}".format(x)
    return results

@app.get('/log' , response_class = HTMLResponse)
def log(request : Request):
    logout = """
    <form method=post action='/logout'>
        <input type = "submit" value="登出">
    </form>
    """
    add = """
    <form method=post action='/add'>
        Course_id : <input type="number" name="c_ID">
        <input type="submit" value="加選">
    </form>
    """
    drop = """
    <form method=post action='/drop'>
        Course_id : <input type="number" name="c_ID">
        <input type="submit" value="退選">
    </form>
    """
    datalist = showtable(request.cookies.get('ID') , request.cookies.get('Password'))
    data = ""
    for x in datalist:
        data += "<tr>"
        for y in x:
            data += "<td>{}</td>".format(y)
        data += "</tr>"
        
    table = """課表：<table border=1>""" +\
                """<tr><th>CourseName</th><th>CourseID</th><th>Day</th><th>Section</th>"""+\
                data + "</table>"
    
    return logout + '<br><br>' + add + '<br><br>' + drop + '<br>' + table

def showtable(ID: int , Password:str):
    conn = MySQLdb.connect(host="127.0.0.1",
                           user=str(ID),
                           passwd=Password,
                           db="testdb",
                           charset='utf8')
    query:str = "Select Name , Course.ID , Day , Section " +\
            "From Subscription CROSS JOIN Course CROSS JOIN TimeTable " +\
            "Where Course.ID = Subscription.c_id AND Course.ID = TimeTable.ID " +\
            "AND s_id = {}".format(ID) +\
            ""
    cursor = conn.cursor()
    cursor.execute(query)
    temp =[]
    for x in cursor.fetchall():
        temp.append(x)
    conn.close()
    return temp

def sql(ID:int , Password:str , Query:str):
    conn = MySQLdb.connect(host="127.0.0.1",
                           user=str(ID),
                           passwd=Password,
                           db="testdb",
                           charset='utf8')
    cursor = conn.cursor()
    cursor.execute(Query)
    temp =[]
    for x in cursor.fetchall():
        for y in x:
            temp.append(y)
    conn.commit()
    conn.close()
    return temp

@app.post('/add' , response_class = HTMLResponse)
def add(request : Request , c_ID:int = Form()):
    ID:int = request.cookies.get('ID')
    Pd:str = request.cookies.get('Password')
    redirect = """<meta http-equiv="Refresh" content="3; URL=http://127.0.0.1:8000/log"/>"""
    c_data = sql(ID,Pd,"Select * From Course Where ID={}".format(c_ID))
    if(len(c_data) < 1):
        return "ID not vaild"+redirect
    c_dict = {'ID':c_data[0],'Name':c_data[1],'Credit':c_data[2],'Required':c_data[3],'Quota':c_data[4],'Dept':c_data[5],'Year':c_data[6]}
    s_data = sql(ID,Pd,"Select * From Student Where ID={}".format(ID))
    s_dict = {'ID':s_data[0],'First_Name':s_data[1],'Last_Name':s_data[2],'Year':s_data[3],'Dept':s_data[4]}
    if(c_dict['Dept'] != s_dict['Dept']):
        return "同學只能加選本系的課程"+redirect
    check = sql(ID,Pd,"Select Count(*) From Subscription Where type=1 AND c_id={}".format(c_ID))
    if(check[0] >= c_data[4]):
        return "人數已滿的課程不可加選"+redirect
    check =sql(ID,Pd,"Select x.Day,x.Section FROM \
        (Select Day,Section From TimeTable cross join Course ON Course.ID=TimeTable.ID \
        Cross JOIN Subscription ON Subscription.c_id = Course.ID Where s_id={}) as x \
        INNER JOIN ( Select Day,Section From TimeTable Cross Join Course ON Course.ID = TimeTable.ID \
        Where Course.ID = {}) as y ON x.Day=y.Day AND x.Section=y.Section; ".format(ID,c_ID))
    print(len(check))
    if(len(check) > 0):
        for x in check:
            print(x)
        return "不可加選衝堂的課程"+redirect
    check = sql(ID,Pd,"Select ID From Course Cross Join Subscription \
        Where Course.ID=Subscription.c_id \
        AND Subscription.s_ID= {} AND Name Like \'{}\'".format(str(ID) , c_dict['Name']))
    if(len(check) != 0):
        return "不可加選與已選課程同名的課程"+redirect
    check = sql(ID ,Pd,"Select Sum(Credit) From Subscription Cross Join Course \
        Where Subscription.c_id = Course.ID AND Subscription.s_id = {}".format(ID))
    if(check[0]+c_dict['Credit'] >30):
        return "加選後學分不可超過最高學分限制 (30 學分)"+redirect
    check = sql(ID,Pd,"INSERT INTO Subscription VALUES ({},{},1);".format(ID,c_ID))
    return "已加選:" + c_dict['Name']+redirect

@app.post('/drop' , response_class = HTMLResponse)
def drop(request : Request , c_ID:int = Form()):
    ID:int = request.cookies.get('ID')
    Pd:str = request.cookies.get('Password')
    redirect = """<meta http-equiv="Refresh" content="5; URL=http://127.0.0.1:8000/log"/>"""
    c_data = sql(ID,Pd,"Select * From Course Where ID={}".format(c_ID))    
    if(len(c_data) < 1):
        return "ID not vaild"+redirect
    c_dict = {'ID':c_data[0],'Name':c_data[1],'Credit':c_data[2],'Required':c_data[3],'Quota':c_data[4],'Dept':c_data[5],'Year':c_data[6]}
    s_data = sql(ID,Pd,"Select * From Student Where ID={}".format(ID))
    s_dict = {'ID':s_data[0],'First_Name':s_data[1],'Last_Name':s_data[2],'Year':s_data[3],'Dept':s_data[4]}
    text = ""
    if(c_dict['Required'] == 1):
        text += "警告!退選必修課"
    check = sql(ID,Pd,"Select Sum(Credit) From Subscription Cross Join Course \
        Where Subscription.c_id = Course.ID AND Subscription.s_id = {}".format(ID))
    if(check[0] - c_dict['Credit'] < 9):
        return text + "<br>低於最低學分限制" +redirect
    else:
        check = sql(ID,Pd,"Delete From Subscription where s_id={} AND c_id={}".format(ID,c_ID))
        text += "<br>已退選:"+c_dict['Name']
        return text + redirect
    return text

@app.post('/logout', response_class=HTMLResponse)
def logout(response: Response):
    response.delete_cookie("ID")
    response.delete_cookie("Password")
    return "logout success" + """<meta http-equiv="Refresh" content="3; URL=http://127.0.0.1:8000/" />"""