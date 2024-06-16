import tkinter as tk
from tkinter import messagebox
from pymysql import *
from ttkbootstrap import *
con = Connect(
    host="localhost",       # 主机名（或IP地址）
    port=3306,              # 端口号，mysql默认3306
    user='root',            # 用户名
    password='2738',        # 密码
    charset='utf8mb4'       # 字符编码
)
cursor = con.cursor()
con.select_db("stu_manager")

# 登陆操作
def login():
    global user
    username = username_entry.get()
    password = password_entry.get()

    cursor.execute('''SELECT * FROM student WHERE ID=%s AND password=%s''', (username, password))
    user = cursor.fetchone()
    if user:
        messagebox.showinfo("登录成功", "欢迎 {} 同学登录！".format(user[1]))
        frame1.destroy()
        result()
    else:
        messagebox.showerror("登录失败", "用户名或密码错误")
        username_entry.delete(0,tk.END)
        password_entry.delete(0,tk.END)

# 显示登陆窗口
def main():
    global password_entry, username_entry, frame1, root
    root = tk.Tk()
    root.geometry('+300+300')
    style = Style()
    style = Style(theme='sandstone')
    root.title("学生信息查询系统")
    frame1 = tk.Frame(root)
    frame1.pack(padx=50, pady=20)

    welcomelabel = tk.Label(frame1, text="welcome", font="'华文新魏', 100")
    welcomelabel.grid(row=0, column=0, columnspan=8, pady=20)

    wlabel = tk.Label(frame1, text="学生信息查询系统", font="'宋体', 20")
    wlabel.grid(row=1, column=0, columnspan=8)

    username_label = tk.Label(frame1, text="用户名：")
    username_label.grid(row=2, column=0, padx=10, pady=10)
    username_entry = tk.Entry(frame1, width=50)
    username_entry.grid(row=2, column=1, columnspan=4, padx=10, pady=10)

    password_label = tk.Label(frame1, text="密码：")
    password_label.grid(row=3, column=0, padx=10, pady=10)
    password_entry = tk.Entry(frame1, show="*", width=50)
    password_entry.grid(row=3, column=1, columnspan=4, padx=10, pady=10)

    login_button = tk.Button(frame1, text="登录", font="'黑体', 20", command=login)
    login_button.grid(row=4, column=1, pady=10)

    exit_button = tk.Button(frame1, text="退出", font="'黑体', 20", command=exit)
    exit_button.grid(row=4, column=2, pady=10)
    
# 查询结果
def result():
    global frame2, information
    cursor.execute(f'''select distinct s.ID, s.name,s.gender,s.entrydate, a.academyname
                      from student s, academy a 
                      where s.academyid = a.id and s.ID = '{user[0]}';''')
    information = cursor.fetchone()
    
    cursor.execute(f'''select c.coursename 
                       from  stu_cours sc, course c 
                       where sc.studentid = {user[0]} and c.id = sc.courseid;''')
    selectedcourse = cursor.fetchall()
    selected = f"{user[1]}同学选择的课程为\n\n  |  "
    for i in range(len(selectedcourse)):
        selected += selectedcourse[i][0]
        selected += '  |  '
    
    frame2 = tk.Frame(root)
    frame2.pack(padx=50, pady=80)
    
    label1 = tk.Label(frame2, text='学生基本信息\n\n', font="'华文新魏', 30")
    label1.grid(row=0, column=0, columnspan=4)
    
    labelID = tk.Label(frame2,text=f'|     ID     |\n\n{information[0]}', font="'华文新魏', 20")
    labelID.grid(row=1, column=0, padx=10)
    
    labelname = tk.Label(frame2, text=f'|   name   |\n\n{information[1]}', font="'华文新魏', 20")
    labelname.grid(row=1, column=1)
    
    labelgender = tk.Label(frame2, text=f'|gender|\n\n{information[2]}', font="'华文新魏', 20")
    labelgender.grid(row=1, column=2)
    
    labelentrydate = tk.Label(frame2, text=f'|   entrydate   |\n\n{information[3]}', font="'华文新魏', 20")
    labelentrydate.grid(row=1, column=3)
    
    labelacademy = tk.Label(frame2, text=f'|  academy  |\n\n{information[4]}', font="'华文新魏', 20")
    labelacademy.grid(row=1, column=4)
    
    label = tk.Label(frame2, text = selected, font="'华文新魏', 30")
    label.grid(row=2, column=0, pady=100, columnspan=4)
    
    scourse = tk.Button(frame2, text='前往选课界面', font="'黑体', 20", command=selectcourse)
    scourse.grid(row=2, column=4, pady=50)

#可选课程
def selectcourse():
    frame2.destroy()
    frame3 = tk.Frame(root)
    frame3.pack(pady=20)
    cursor.execute(f'''select distinct a.academyname, c.coursename
                       from student s, academy a, course_academy ca, course c 
                       where a.id = ca.academyid and c.id = ca.courseid and a.academyname = '{information[4]}';''')
    course = cursor.fetchall()
    
    select = f'{information[4]}可选课程\n\n|  '
    for i in range(len(course)):
        select += course[i][1]
        select += '  |  ' 
    
    labelcourse = tk.Label(frame3, text=select, font="'华文新魏', 30")
    labelcourse.grid(row=0, column=0, columnspan=3)


main()
root.mainloop()