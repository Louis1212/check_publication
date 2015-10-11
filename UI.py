from Tkinter import *
import os
from scrapy.crawler import CrawlerProcess
#from SMG.spiders.yuri_spider import publicationSpider
from scrapy.utils.project import get_project_settings



class SurveyDialog(Toplevel):

    def __init__(self, parent, title = None):
        Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)
        self.parent = parent
        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx = 5, pady = 5)

        self.buttonbox()
        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol('WM_DELETE_WINDOW', self.cancel)
        self.geometry('+%d+%d' % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))
        self.initial_focus.focus_set()
        self.wait_window(self)

    def body(self, master):
        Label(master, text='*First Name:').grid(row=0, column=1)
        Label(master, text='*Last Name:').grid(row=0, column=2)
        Label(master, text='Start Month:').grid(row=2, column=1)
        Label(master, text='Start Year:').grid(row=2, column=2)
        Label(master, text='End Month:').grid(row=4, column=1)
        Label(master, text='End year:').grid(row=4, column=2)
        Label(master, text='Max # Entry:').grid(row=6, column=1)


        self.e1 = Entry(master)
        self.e2 = Entry(master)
        self.e3 = Entry(master)
        self.e4 = Entry(master)
        self.e5 = Entry(master)
        self.e6 = Entry(master)
        self.e7 = Entry(master)

        self.e1.grid(row=1, column=1)
        self.e2.grid(row=1, column=2)
        self.e3.grid(row=3, column=1)
        self.e4.grid(row=3, column=2)
        self.e5.grid(row=5, column=1)
        self.e6.grid(row=5, column=2)
        self.e7.grid(row=7, column=1)
        
        return self.e1 # initial focus

    def buttonbox(self):
        box = Frame(self)
        
        w = Button(box, text = 'Submit', width = 10, command = self.submit,
                   default = ACTIVE)
        w.pack(side = LEFT, padx = 5, pady = 5)
        w = Button(box, text = 'Cancel', width = 10, command = self.cancel)
        w.pack(side = LEFT, padx = 5, pady = 5)

        self.bind('<Return>', self.submit)
        self.bind('Escape', self.cancel)
        box.pack()

    def submit(self, event = None):
        if not self.validate():
            self.initial_focus.focus_set()
            return
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event = None):
        self.parent.focus_set()
        self.destroy()

    def validate(self):
        if self.e1.get() != '' and self.e2.get() != '':
            return True
        else:
            return False

    def apply(self):
        self.parent.getInfo(self.e1.get(), self.e2.get(), self.e3.get(),
                            self.e4.get(), self.e5.get(), self.e6.get(),
                            self.e7.get())

class MainWindow(Tk):
    
    def __init__(self, title = None):
        Tk.__init__(self)
        if title:
            self.title_str = title

        self.first_name = ''
        self.last_name = ''
        self.start_month = ''
        self.start_year = ''
        self.end_month = ''
        self.end_year = ''
        self.entry_num = ''

        body = Frame(self)
        body.pack(padx = 5, pady = 5)

        self.buttonbox()
        self.wait_window(self)

    def title(self):
        return self.title_str


    def buttonbox(self):
        box = Frame(self)
        w = Button(box, text = 'Start', width = 10, command = self.start,
                   default = ACTIVE)
        w.pack(side = LEFT, padx = 5, pady = 5)
        w = Button(box, text = 'Exit', width = 10, command = self.cancel)
        w.pack(side = LEFT, padx = 5, pady = 5)
        self.bind('<Return>', self.start)
        self.bind('<Escape>', self.cancel)
        box.pack()

    def getInfo(self, fn, ln, sm = None, sy = None,
                em = None, ey = None, nE = None):
        self.first_name = fn
        self.last_name = ln
        if sm:
            self.start_month = sm
        if sy:
            self.start_year = sy
        if em:
            self.end_month = em
        if ey:
            self.end_year = ey


    def update(self, fn, ln, sm, sy, em, ey, en):
        process = CrawlerProcess(get_project_settings())
        process.crawl('publ', first=fn, last=ln,
                      start_month=sm, start_year=sy, end_month=em,
                      end_year=ey, entry_number=en)
        process.start()

        
    def start(self, event = None):
        SurveyDialog(self);
        self.update(self.first_name, self.last_name, self.start_month,
                    self.start_year, self.end_month, self.end_year,
                    self.entry_num)

        self.cancel()

        
    def cancel(self, event = None):
        self.destroy()
    
    
    
def main():
    window = MainWindow('Publication Checker')


main()
