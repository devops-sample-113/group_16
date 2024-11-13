# bash: python -m uvicorn python_fastapi_example:app
from fastapi import FastAPI, Form, Cookie, Request
from fastapi.responses import HTMLResponse, Response
import sqlite3

app = FastAPI()

@app.get('/', response_class=HTMLResponse)
def index():
    form = """
    <form method="post" action="/login">
        ID: <input type="number" name="ID">
        Password: <input name="Password">
        <input type="submit" value="登入">
    </form>
    """
    return form

@app.post('/login', response_class=HTMLResponse)
def login(response: Response, ID: int = Form(), Password: str = Form()):
    try:
        is_valid, user_name = loginSQL(ID, Password)
        if not is_valid:
            raise Exception("Invalid login credentials")
    except Exception as e:
        print(e)
        return """Error: login credential error""" + """<meta http-equiv="Refresh" content="3; URL=http://127.0.0.1:8000/" />"""
    
    response.set_cookie("ID", str(ID))
    response.set_cookie("Password", Password)
    response.set_cookie("UserName", user_name)
    
    return """<meta http-equiv="Refresh" content="0; URL=http://127.0.0.1:8000/log" />"""

def loginSQL(ID: int, Password: str):
    conn = sqlite3.connect("testdb.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT First_Name, Last_Name, Password FROM Student WHERE ID = ?", (ID,))
    row = cursor.fetchone()
    conn.close()

    if row:
        first_name, last_name, stored_password = row
        if Password == stored_password:
            return True, f"{first_name} {last_name}"
    
    return False, ""

@app.get('/log', response_class=HTMLResponse)
def log(request: Request):
    user_name = request.cookies.get("UserName", "User")
    ID = request.cookies.get("ID")

    # 獲取當前學分數
    current_credits = get_current_credits(ID)

    # 加退選表單
    add_drop_form = """
    <form method="post" action="/modify_course" style="display: flex; align-items: center;">
        <input type="text" name="course_name" id="course_name" list="course_list" placeholder="輸入課程名稱" 
               style="width: 600px; margin-right: 20px;">
        <datalist id="course_list"></datalist>
        <input type="submit" name="action" value="加選" style="margin-right: 5px;">
        <input type="submit" name="action" value="退選">
    </form>
    <script>
        document.getElementById('course_name').addEventListener('input', function() {
            fetch('/autocomplete?query=' + this.value)
                .then(response => response.json())
                .then(data => {
                    let datalist = document.getElementById('course_list');
                    datalist.innerHTML = '';
                    data.forEach(course => {
                        let option = document.createElement('option');
                        option.value = course;
                        datalist.appendChild(option);
                    });
                });
        });
    </script>
    """

    # 禁用滾動的樣式
    logout = f"""
    <style>
        /* 禁用滾動 */
        html, body {{
            overflow: hidden;
            height: 100%;
            margin: 0;
        }}
    </style>
    <h2>Welcome, {user_name}</h2>
    <h3>當前學分數: {current_credits}</h3>
    <form method="post" action="/logout" style="display: inline;">
        <input type="submit" value="登出">
    </form>
    """

    timetable = showtable(ID)

    days = ["星期一", "星期二", "星期三", "星期四", "星期五"]
    # 使用 flexbox 將課表和課程列表水平排列
    table = """
    <div style="display: flex; padding: 5px;">
        <div style="flex: 2; padding-right: 20px;">
            <table border="1" style="width: 100%; border-collapse: collapse; text-align: center; font-size: 15px;">
                <tr>
                    <th style="padding: 5px; width: 8%; height: 30px;">時間</th>""" + "".join(
        f'<th style="padding: 5px; width: 12%; height: 30px;">{day}</th>' for day in days
    ) + "</tr>"

    section_to_time = {
        1: "08:10-09:00", 2: "09:10-10:00", 3: "10:10-11:00", 4: "11:10-12:00",
        5: "12:00-13:10", 6: "13:10-14:00", 7: "14:10-15:00", 8: "15:10-16:00",
        9: "16:10-17:00", 10: "17:10-18:00", 11: "18:10-19:00", 12: "19:10-20:00",
        13: "20:10-21:00", 14: "21:10-22:00"
    }

    for section, time in section_to_time.items():
        table += f"<tr><td style='padding: 5px; width: 8%; height: 30px;'>{time}</td>"
        for day in range(1, 6):
            course = timetable[day].get(section, "")
            table += f"<td style='padding: 5px; width: 8%; height: 30px;'>{course}</td>"
        table += "</tr>"
    table += "</table></div>"

    # 將「所有課程和餘額」列表放在課表的右邊
    all_courses = get_all_courses_with_quota()
    courses_list = "<div style='flex: 1; padding-left: 10px;'><h3>所有課程和餘額</h3><ul style='list-style-type: none; padding: 0;'>"
    for course, credit, quota in all_courses:
        courses_list += f"<li style='margin-bottom: 10px;'>{course} (學分數: {credit}): 剩餘 {quota} 名額</li>"
    courses_list += "</ul></div></div>"

    return logout + '<br><br>' + add_drop_form + '<br><br>' + table + courses_list


@app.get('/autocomplete')
def autocomplete(query: str):
    conn = sqlite3.connect("testdb.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT Name FROM Course WHERE LOWER(Name) LIKE ?", (query.lower() + "%",))
    courses = [row[0] for row in cursor.fetchall()]
    conn.close()
    return courses

def showtable(ID: str):
    conn = sqlite3.connect("testdb.sqlite")
    cursor = conn.cursor()
    query = """
    SELECT Name, Course.ID, Day, Section
    FROM Subscription
    JOIN Course ON Course.ID = Subscription.c_id
    JOIN TimeTable ON Course.ID = TimeTable.ID
    WHERE s_id = ?
    """
    cursor.execute(query, (ID,))
    temp = cursor.fetchall()
    conn.close()

    timetable = {day: {hour: "" for hour in range(1, 15)} for day in range(1, 6)}
    for name, course_id, day, section in temp:
        if day in timetable and section in timetable[day]:
            timetable[day][section] = f"{name}"

    return timetable

def get_all_courses_with_quota():
    conn = sqlite3.connect("testdb.sqlite")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Name, Credit, Quota - (SELECT COUNT(*) FROM Subscription WHERE c_id = Course.ID) AS RemainingQuota 
        FROM Course
    """)
    courses = cursor.fetchall()
    conn.close()
    return courses

def get_current_credits(ID: str):
    conn = sqlite3.connect("testdb.sqlite")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(Credit) FROM Subscription
        JOIN Course ON Subscription.c_id = Course.ID
        WHERE Subscription.s_id = ?
    """, (ID,))
    current_credits = cursor.fetchone()[0] or 0
    conn.close()
    return current_credits

@app.post('/modify_course', response_class=HTMLResponse)
def modify_course(request: Request, course_name: str = Form(), action: str = Form()):
    ID = request.cookies.get('ID')
    redirect = """<meta http-equiv="Refresh" content="3; URL=http://127.0.0.1:8000/log"/>"""

    conn = sqlite3.connect("testdb.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Course WHERE Name = ?", (course_name,))
    c_data = cursor.fetchone()
    
    if not c_data:
        conn.close()
        return "課程名稱無效" + redirect

    c_dict = {'ID': c_data[0], 'Name': c_data[1], 'Credit': c_data[2], 'Required': c_data[3],
              'Quota': c_data[4], 'Dept': c_data[5], 'Year': c_data[6]}

    # 獲取當前學分數
    current_credits = get_current_credits(ID)
    
    if action == "加選":
        # 檢查是否已加選
        cursor.execute("SELECT * FROM Subscription WHERE s_id = ? AND c_id = ?", (ID, c_dict['ID']))
        if cursor.fetchone():
            conn.close()
            return "該課程已加選!請重新輸入欲加選課程" + redirect

        # 檢查課程衝堂
        cursor.execute("""
            SELECT 1 FROM Subscription
            JOIN TimeTable ON Subscription.c_id = TimeTable.ID
            WHERE s_id = ? AND Day = (SELECT Day FROM TimeTable WHERE ID = ?) 
            AND Section = (SELECT Section FROM TimeTable WHERE ID = ?)
        """, (ID, c_dict['ID'], c_dict['ID']))
        if cursor.fetchone():
            conn.close()
            return "加選失敗! 課程衝堂" + redirect


        # 檢查學分上限
        if current_credits + c_dict['Credit'] > 25:
            conn.close()
            return "加選失敗! 請填寫超修單" + redirect
        
        # 執行加選
        cursor.execute("INSERT INTO Subscription (s_id, c_id, type) VALUES (?, ?, 1)", (ID, c_dict['ID']))
        conn.commit()
        conn.close()
        return "加選成功!" + redirect

    elif action == "退選":
        # 檢查退選是否會低於9學分
        if current_credits - c_dict['Credit'] < 9:
            conn.close()
            return "退選失敗! 不可低於低修9學分" + redirect

        # 如果是必修課程，加入必修退選名單
        if c_dict['Required'] == 1:
            text = "加入必修退選名單，"
        else:
            text = ""

        # 執行退選
        cursor.execute("DELETE FROM Subscription WHERE s_id = ? AND c_id = ?", (ID, c_dict['ID']))
        conn.commit()
        conn.close()
        return text + "退選成功!" + redirect

    conn.close()
    return "操作失敗" + redirect

@app.post('/logout', response_class=HTMLResponse)
def logout(response: Response):
    response.delete_cookie("ID")
    response.delete_cookie("Password")
    response.delete_cookie("UserName")
    return "logout success" + """<meta http-equiv="Refresh" content="3; URL=http://127.0.0.1:8000/" />"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)