import pathlib
import json
import numpy as np
from school_api import SchoolClient
from retry import retry
from tkinter import messagebox
from tkinter import ttk
from tkinter import *


class popUpEntry(Toplevel):
    def __init__(self, value='', col=1):
        super().__init__()
        self.title(u'修改')
        self.setupUI()
        self.value = value
        self.col = col

    def setupUI(self):
        row1 = Frame(self)
        row1.pack(fill='x')
        l1 = Label(row1, text=u'请输入：', height=2, width=10)
        l1.pack(side=LEFT)
        self.xls_text = StringVar()
        Entry(row1, textvariable=self.xls_text).pack(side=RIGHT, padx=10)
        row2 = Frame(self)
        row2.pack(fill='x')
        Button(row2, text=u'确定', command=self.on_click).pack(side=RIGHT, padx=10, pady=5)

    def on_click(self):
        get_value = self.xls_text.get().strip()
        if len(get_value) == 0:
            messagebox.showwarning(title=u'系统提示', message=u'您还未输入！', parent=self)   # Specify the parent parameter so that messagebox can pop up above the entry
            return False
        if self.col == 4 and (not((is_number(get_value) and 0 <= eval(get_value) <= 100) or get_value in LEVEL)):
            messagebox.showwarning(title=u'系统提示', message=u'成绩请输入0-100间的数！\n或输入五级制成绩：“优秀”、“良好”、“中等”、“及格”、“不及格”、“合格”', parent=self)
            return False
        if self.col == 3 and (not is_number(get_value) or eval(get_value) < 0):
            messagebox.showwarning(title=u'系统提示', message=u'学分请输入大于等于0的数！', parent=self)
            return False
        self.value = get_value
        self.quit()
        self.destroy()

    def set_center(self, _root):
        # move the window to the center of the root window
        _x, _y, _dx, _dy = _root.winfo_x(), _root.winfo_y(), _root.winfo_width() // 2, _root.winfo_height() // 2
        self.geometry('+{}+{}'.format(int(_x + _dx) - 119, int(_y + _dy) - 55))


root = Tk()
root.title(u'GPA计算器')
root.iconbitmap('calculator.ico')
# center the window
window_width, window_height = 570, 460
dx, dy = (root.winfo_screenwidth() - window_width) // 2, (root.winfo_screenheight() - window_height) // 2
root.geometry('{}x{}+{}+{}'.format(window_width, window_height, dx, dy))
root.resizable(width=False, height=False)
columns = (u'学期', u'课程名', u'学分', u'成绩')
frame = Frame(root)
frame.pack()
treeview = ttk.Treeview(frame, height=18, show='headings', columns=columns)
vbar = ttk.Scrollbar(frame, orient=VERTICAL, command=treeview.yview)
treeview.configure(yscrollcommand=vbar.set)
treeview.tag_configure('gray', background='#cccccc')    # make the background color gray and white
treeview.tag_configure('common', background='#ffffff')
treeview.tag_configure('NORMAL', font=('微软雅黑', 9))
treeview.tag_configure('ITALIC', font=('微软雅黑', 9, 'italic'), foreground='#ff0033')
treeview.column(u'学期', width=100, anchor='center')
treeview.column(u'课程名', width=250, anchor='center')
treeview.column(u'学分', width=100, anchor='center')
treeview.column(u'成绩', width=100, anchor='center')
treeview.heading(u'学期', text=u'学期')
treeview.heading(u'课程名', text=u'课程名')
treeview.heading(u'学分', text=u'学分')
treeview.heading(u'成绩', text=u'成绩')
treeview.pack(side=LEFT, fill=BOTH)
vbar.pack(side=RIGHT, fill=Y)


def treeview_sort_column(tv, col, reverse):  # Treeview, column name, sort pattern
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)  # sort pattern
    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):  # move by sorted index
        tv.move(k, '', index)
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))  # rewrite the title so that it is in reverse order
    t = treeview.get_children()  # traverse the table
    even = True
    for i in t:
        treeview.item(i, tags=('common' if even else 'gray', 'ITALIC' if treeview.item(i, 'values')[1] in Free_Electives else 'NORMAL'))
        even = not even


def set_cell_value(event):  # double-click to edit the value
    global app
    def save_edit():
        try:
            treeview.set(item, column=column, value=app.value)
            value1, value2 = calculate()
            var1.set('GPA = %.2f' % value1)
            var2.set(u'当前已修学分（除任选课）: %.1f' % value2)
            treeview.item(item, tags=('gray' if treeview.tag_has(item=item, tagname='gray') else 'common', 'ITALIC' if treeview.item(item, 'values')[1] in Free_Electives else 'NORMAL'))
        except TclError:
            pass

    def close():
        # fix the unexpected exception(_tkinter.TclError: invalid command name ".!frame.!treeview").
        # I have no idea why it is so, but it works. Fine.
        app.quit()
        app.destroy()

    try:
        if app.winfo_exists() == 1:
            root.bell()     # make alarm noise
            return
    except NameError:
        pass

    column = treeview.identify_column(event.x)  # column
    row = treeview.identify_row(event.y)  # row
    try:
        cn = int(str(column).replace('#', ''), 16)  # default base is hex.
        rn = int(str(row).replace('I', ''), 16)
    except ValueError:
        # It means that the user has double-clicked the header column of the table. Don't need pop-up window.
        return
    current_value = ''
    for item in treeview.selection():
        item_text = treeview.item(item, 'values')
        current_value = str(item_text[cn - 1])  # outputs the value of the selected row
    try:
        item
    except NameError:
        # It also means the user has double-clicked the header column of the table. And it's after clicking "Add lesson".
        return
    app = popUpEntry(value=current_value, col=cn)
    app.attributes('-toolwindow', 1)
    app.wm_attributes('-topmost', 1)            # always shows at top
    app.resizable(width=False, height=False)
    app.protocol('WM_DELETE_WINDOW', close)
    app.set_center(root)
    app.mainloop()
    save_edit()


def new_row():
    term.append('-')
    lesson_name.append('-')
    credit.append(0.0)
    point.append(0.0)
    score.append('0.0')
    treeview.insert('', len(lesson_name) - 1, values=(term[-1], lesson_name[-1], credit[-1], score[-1]), tags=('common' if len(lesson_name) & 1 else 'gray', 'ITALIC' if lesson_name[-1] in Free_Electives else 'NORMAL'))
    treeview.yview_moveto(1)  # scroll to the bottom
    treeview.update()
    newb.place(y=400)
    newb.update()


treeview.bind('<Double-1>', set_cell_value)
var1, var2 = StringVar(), StringVar()
var1.set('GPA = %.2f' % 0.00)
var2.set(u'当前已修学分（除任选课）: %.1f' % 0.0)
show_GPA = Label(root, textvariable=var1, font=('Arial', 14, 'bold'), width=30, height=2)
show_credit = Label(root, textvariable=var2, font=('', 10, 'bold'), width=30, height=2)
newb = ttk.Button(root, text=u'添加课程', width=20, command=new_row)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


def change(ss):
    global LEVEL
    LEVEL = {u'优秀': 95, u'良好': 85, u'中等': 75, u'及格': 65, u'不及格': 0, u'合格': 61}
    if is_number(ss):
        score_num = eval(ss)
    elif ss in LEVEL:
        score_num = LEVEL[ss]
    else:
        score_num = 0
    return score_num


def calculate():
    to_GPA = lambda num: round(num / 10 - 5, 2) if is_number(num) and 60 <= num <= 100 else 0.00
    po, cr, tot_credit = [], [], 0
    t = treeview.get_children()     # traverse the table
    for i in t:
        ter, name, cre, sco = treeview.item(i, 'values')
        if name not in Free_Electives:
            po.append(to_GPA(change(sco)))
            cr.append(eval(cre))
            tot_credit += eval(cre)
    return np.average(po, weights=cr), tot_credit


@retry(AttributeError, tries=3)
def main():
    global term, lesson_name, credit, point, score, Free_Electives
    jwxt_url, username, password = '', '', ''
    path = pathlib.Path('config.json')
    if not path.is_file():
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, u'配置文件不存在！请检查！', u'错误', 16)  # 16: error icon
        exit(0)
    else:
        with open('config.json', 'r', encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
        try:
            jwxt_url = load_dict['jwxt_url']
            username = load_dict['username']
            password = load_dict['password']
            Free_Electives = load_dict['Free_Electives']
        except KeyError:
            '''
            The correct format for config.json:
            {"jwxt_url": "xxx", "username": "xxx", "password": "xxx", "Free_Electives": ["xxx", "xxx", ..., "xxx"]}
            '''
            import ctypes
            ctypes.windll.user32.MessageBoxW(0, u'配置文件格式有误！请检查！', u'错误', 16)  # 16: error icon
            exit(0)
    school = SchoolClient(url=jwxt_url)
    user = school.user_login(username, password)
    schedule_data = user.get_score()
    term, lesson_name, credit, point, score = [], [], [], [], []
    for key, value in schedule_data.items():
        for key1, value1 in value.items():
            current_term = [key + '-' + key1] * len(value1)
            term += current_term
            for lesson in value1:
                lesson_name.append(lesson['lesson_name'])
                credit.append(lesson['credit'])
                point.append(lesson['point'])
                now = str(lesson['score'])
                current_score = change(now)
                if 'cxcj' in lesson:
                    cxcj = change(str(lesson['cxcj']))
                    if cxcj > current_score:
                        now = str(lesson['cxcj'])
                        current_score = cxcj
                if 'bkcj' in lesson:
                    bkcj = change(str(lesson['bkcj']))
                    if bkcj > current_score:
                        now = str(lesson['bkcj'])
                        current_score = bkcj
                score.append(now)

    for i in range(min(len(term), len(lesson_name), len(credit), len(score))):
        treeview.insert('', i, values=(term[i], lesson_name[i], credit[i], score[i]), tags=('gray' if i & 1 else 'common', 'ITALIC' if lesson_name[i] in Free_Electives else 'NORMAL'))
    treeview.yview_moveto(1)
    treeview.update()
    show_GPA.place(y=390)
    show_credit.place(x=60, y=425)
    newb.place(x=404, y=400)
    for col in columns:  # bind functions to make table heads sortable
        treeview.heading(col, text=col, command=lambda _col=col: treeview_sort_column(treeview, _col, False))
    value1, value2 = calculate()
    var1.set('GPA = %.2f' % value1)
    var2.set(u'当前已修学分（除任选课）: %.1f' % value2)
    root.mainloop()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, u'程序异常！\n详情：%s' % str(e), u'错误', 16)    # 16: error icon
