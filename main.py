# -*- coding: utf-8 -*-
from PIL import Image
import pytesseract
import tkinter
from tkinter.scrolledtext import ScrolledText
import time
import threading
import tkinter.filedialog
import tkinter.messagebox


class Main(object):
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("提取图片内容转换为markdown表格代码")
        self.window.geometry("1040x650")
        # 图片路径
        self.photo_path = ""
        # 保存markdown内容路径
        self.txt_path = ""
        # 保存markdown内容
        self.content = None
        # 初始化控件
        '''显示基本信息'''
        self.label_content = tkinter.Label(self.window,
                                           text="提取图片内容转换为markdown表格代码\n" + "限于个人学习使用,实际工作中建议使用现成商业OCR软件\n"
                                                + "输入列名和列属性(左对齐,居中,右对齐)时,以空格分开,简写成(左,中,右)",
                                           bg='green',
                                           font=('Arial', 14))
        self.label_content.place(relwidth=0.7, relheight=0.2, relx=0, rely=0)
        '''结果显示'''
        self.label_show = tkinter.Label(self.window, text='参考markdown代码', bg='#a3cf62', font=('Arial', 12))
        self.label_show.place(relwidth=0.8, relheight=0.05, relx=0, rely=0.2)
        '''结果展示'''
        self.text_result = ScrolledText(self.window, bg='green',
                                        font=('Arial', 16))
        self.text_result.place(relwidth=0.8, relheight=0.75, relx=0.0, rely=0.25)
        '''时间'''
        self.now_time = None
        self.label_time = tkinter.Label(self.window, text='时间', bg='#a3cf62')
        self.label_time.place(relwidth=0.3, relheight=0.08, relx=0.7, rely=0)
        '''显示当前时间'''
        self.text_time = tkinter.Label(self.window, font=('Arial', 16))
        self.text_time.place(relwidth=0.3, relheight=0.12, relx=0.7, rely=0.08)
        self.show_time()
        '''5x0.16,0.3'''
        '''打开文件'''
        self.button_open = tkinter.Button(self.window, text='打开', bg='#a3cf62', font=('Arial', 12),
                                          command=self.button_open_click)
        self.button_open.place(relwidth=0.2, relheight=0.16, relx=0.8, rely=0.2)
        '''保存结果'''
        self.button_save = tkinter.Button(self.window, text='保存', bg='green', font=('Arial', 12),
                                          command=self.button_save_click)
        self.button_save.place(relwidth=0.2, relheight=0.16, relx=0.8, rely=0.36)
        '''输入行数列数 0.52-0.68'''
        self.label_l = tkinter.Label(self.window, text="列数", font=('Arial', 11))
        self.label_l.place(relwidth=0.08, relheight=0.05, relx=0.81, rely=0.54)
        self.var_l_num = tkinter.StringVar()
        self.entry_l_num = tkinter.Entry(self.window, textvariable=self.var_l_num, bg='#a3cf62', font=('Arial', 11))
        self.entry_l_num.place(relwidth=0.07, relheight=0.05, relx=0.82, rely=0.6)
        self.label_r = tkinter.Label(self.window, text="行数", font=('Arial', 11))
        self.label_r.place(relwidth=0.08, relheight=0.05, relx=0.91, rely=0.54)
        self.var_r_num = tkinter.StringVar()
        self.entry_r_num = tkinter.Entry(self.window, textvariable=self.var_r_num, bg='#a3cf62', font=('Arial', 11))
        self.entry_r_num.place(relwidth=0.07, relheight=0.05, relx=0.91, rely=0.6)
        '''输入列名,列属性 0.68-0.84'''
        self.label_n = tkinter.Label(self.window, text="列名", font=('Arial', 11))
        self.label_n.place(relwidth=0.08, relheight=0.05, relx=0.81, rely=0.7)
        self.var_n_num = tkinter.StringVar()
        self.entry_n_num = tkinter.Entry(self.window, textvariable=self.var_n_num, bg='green', font=('Arial', 11))
        self.entry_n_num.place(relwidth=0.07, relheight=0.05, relx=0.82, rely=0.76)
        self.label_a = tkinter.Label(self.window, text="列属性", font=('Arial', 11))
        self.label_a.place(relwidth=0.08, relheight=0.05, relx=0.91, rely=0.7)
        self.var_a_num = tkinter.StringVar()
        self.entry_a_num = tkinter.Entry(self.window, textvariable=self.var_a_num, bg='green', font=('Arial', 12))
        self.entry_a_num.place(relwidth=0.07, relheight=0.05, relx=0.91, rely=0.76)
        '''确定0.84-1.0'''
        self.button_sure = tkinter.Button(self.window, text="确定", bg='#a3cf62', font=('Arial', 12),
                                          command=self.button_sure_click)
        self.button_sure.place(relwidth=0.2, relheight=0.16, relx=0.8, rely=0.84)
        self.window.mainloop()

    def show_time(self):
        """
        显示当前时间
        循环以一秒钟的间隔显示时间
        :return: NULL
        """
        self.now_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.text_time.configure(text=self.now_time)
        self.window.after(1000, self.show_time)

    def button_open_click(self):
        """
        使用多线程，创建一个线程用于打开并读取文件
        :return: NULL
        """
        thread = threading.Thread(target=self.button_open_click_thread)
        thread.setDaemon(True)
        thread.start()

    def button_open_click_thread(self):
        self.photo_path = tkinter.filedialog.askopenfilename(title="请选择图片文件")
        if self.photo_path == "":
            tkinter.messagebox.showwarning(title="警告", message="您未选择任何文件!")
        else:
            self.content = pytesseract.image_to_string(Image.open(self.photo_path), lang="eng")
            self.content = self.content.split()
            tkinter.messagebox.showinfo(title="已选择文件", message="该文件的路径是 " + self.photo_path)

    def button_save_click(self):
        """
        使用多线程，创建一个子线程用来保存文件
        :return:
        """
        thread = threading.Thread(target=self.button_save_click_thread)
        thread.setDaemon(True)
        thread.start()

    def button_save_click_thread(self):
        """
        保存文件操作
        保存文件的格式是*.txt , *.data , *.* 三种方式
        若未选择文件，提示先选择文件
        选择文件后
        若结果未生成，则提示先选择算法
        否则将结果写入文件中
        :return: NULL
        """
        self.txt_path = tkinter.filedialog.asksaveasfilename(defaultextension=".txt",
                                                             filetypes=[("txt Files", "*.txt"),
                                                                        ("data Files", "*.data")])
        if self.txt_path != "":
            file = open(self.txt_path, "w")
            for c in self.content:
                file.write(c + "\n")
            file.close()
            tkinter.messagebox.showinfo(title="成功", message="程序已经成功写入文件中\n" + "路径是 " + self.txt_path)
        else:
            tkinter.messagebox.showerror(title="保存失败", message="您得先选择您的文件!")

    def button_sure_click(self):
        """
        使用多线程，创建一个子线程用来处理特征选择过程
        :return: NULL
        """
        thread = threading.Thread(target=self.button_sure_click_thread)
        thread.setDaemon(True)
        thread.start()

    def button_sure_click_thread(self):
        """
        """
        if self.photo_path == "":
            tkinter.messagebox.showerror(title="错误", message="您未导入文件!")
        else:
            self.text_result.delete(1.0, "end")
            rows = int(self.var_r_num.get())
            lists = int(self.var_l_num.get())
            list_name = self.var_n_num.get()
            list_name = str(list_name).split(" ")
            list_attr = self.var_a_num.get()
            list_attr = str(list_attr).split(" ")
            md_text = [["|"], ["|"]]
            if str(lists) != str(len(list_name)):
                tkinter.messagebox.showerror(title="错误", message="列名和列数不统一!")
            else:
                for name in list_name:
                    md_text[0].append(str(name) + "|")
                md_text[0] = "".join(md_text[0])
                for d in list_attr:
                    if str(d) == "左":
                        md_text[1].append(":----|")
                    if str(d) == "中":
                        md_text[1].append(":----:|")
                    if str(d) == "右":
                        md_text[1].append("----:|")
                md_text[1] = "".join(md_text[1])
                for r in range(rows):
                    res = "|"
                    for l in range(lists):
                        res += (self.content[r + l * rows] + "|")
                    md_text.append(res)
                self.content = md_text
                for c in self.content:
                    self.text_result.insert('insert', c + "\n")


Main()
