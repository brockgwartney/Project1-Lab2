from tkinter import *
import csv
import os


class GUI:
    def __init__(self,window):
        self.window = window
        self.repeat = True
        self.repeat_scale = True
        self.check_fail = []
        self.check_pass = []
        self.scale = []
        self.scale_types = []
        self.scale_final = []
        self.scale_count = 1
        self.get_filename()

        self.scale_frame = Frame(self.window)
        self.scale_label = Label(self.scale_frame)
        self.scale_entry = Entry(self.scale_frame, width = 50)
        self.scale_button = Button(self.scale_frame, text = 'Set Scale')
        self.scale_label_help = Label(self.scale_frame, text = 'This will determine the scale used for the assigment, say the scale is 10, and the highest score is a 90, a A would be a 90, B a 80, ..., F a 50 ')
        self.failure_label = Label(self.scale_frame,text = 'Invalid Input!')


    
    def get_filename(self):

        self.filename_clicked_choice = False

        self.file_name_frame = Frame(self.window)
        file_name_label = Label(self.file_name_frame, text = 'File Name')
        self.file_name_entry = Entry(self.file_name_frame, width= 50)
        file_name_button = Button(self.file_name_frame, text = 'Get File',command= lambda: self.filename_clicked(self.file_name_entry.get()))
        manual_entry_button = Button(self.file_name_frame, text = 'Manual  Entry', command = self.manual_clicked)
        self.file_name_help = Label(self.file_name_frame, text = 'Provide .csv file (filename.csv)')
        self.file_name_help2 = Label(self.file_name_frame, text = '.csv Files should be 3 rows with the following Header: Name, Assigment, Score')
        self.file_name_help3 = Label(self.file_name_frame, text = 'Manual Entry should be used when you may need to input your own data (No CSV file Needed)')

        file_name_label.pack(pady = 10)
        self.file_name_entry.pack()
        file_name_button.pack(pady = 10)
        manual_entry_button.pack(pady = 10)
        self.file_name_help.pack(pady = 10)
        self.file_name_help2.pack(pady = 10)
        self.file_name_help3.pack(pady = 10)
        self.file_name_frame.place(relx=.5, rely=.5,anchor= CENTER)

        
        

    def filename_clicked(self,filename):
        if os.path.exists(filename):
            self.file_name_frame.destroy()
            self.file_check(filename)
        else:
            if self.repeat:
                self.file_name_failure = Label(self.file_name_frame, text = 'File Not Found!')
                self.file_name_failure.pack()
                self.repeat = False

    
    def file_check(self,filename):

        with open(filename, newline='') as csvfile:
            csvreader = csv.reader(csvfile)

            for row in csvreader:
                try:
                    float(row[2])
                    self.check_pass.append(row)
                except:
                    self.check_fail.append(row)

            self.determine_scale()

        
    def determine_scale(self):

        for items in self.check_pass:
            if items[1] not in self.scale_types:
                self.scale_types.append(items[1])
        
        self.window.geometry('850x500')

        self.scale_frame = Frame(self.window)
        self.scale_label = Label(self.scale_frame)
        self.scale_entry = Entry(self.scale_frame, width = 50)
        self.scale_button = Button(self.scale_frame, text = 'Set Scale')
        self.scale_label_help = Label(self.scale_frame, text = 'This will determine the scale used for the assigment, say the scale is 10, and the highest score is a 90, a A would be a 90, B a 80, ..., F a 50 ')
        self.failure_label = Label(self.scale_frame,text = 'Invalid Input!')

        self.scale_label = Label(self.scale_frame, text = f'{self.scale_types[0]} Scale')
        self.scale_button = Button(self.scale_frame, text = 'Set Scale',command= self.scale_button_clicked)

        self.scale_label.pack(pady=10)
        self.scale_entry.pack(pady = 10)
        self.scale_button.pack(pady=10)
        self.scale_label_help.pack(pady=10)
        self.scale_frame.place(relx=.5, rely=.5,anchor= CENTER)


    def scale_button_clicked(self):
        try:
            scale_amount = self.scale_entry.get()
            float(scale_amount)
            self.scale.append(scale_amount)
            if self.scale_count == len(self.scale_types):
                self.scale_count = len(self.scale_types) + 1
                self.scale_frame.destroy()
                self.divide_scales()
            else:
                self.scale_label['text'] = str(self.scale_types[self.scale_count])
            self.scale_count += 1
            if not self.repeat_scale:
                self.failure_label.forget()
                self.repeat_scale = True
        
        except:
            if self.repeat_scale:
                self.failure_label.pack(pady= 10)
                self.repeat_scale = False


    
    def divide_scales(self):
        assigment_list = {}
        scales = []
        max = []
        for i in range(len(self.scale_types)):
            self.scale_final.append([])
        
        for i in range(len(self.scale_types)):
            assigment_list[self.scale_types[i]] = i
            max.append(0)
            scales.append([])

        for items in self.check_pass:
            test = assigment_list[items[1]]
            self.scale_final[test].append([items[0],items[2]])


        for items in self.check_pass:
            if float(items[2]) > float(max[assigment_list[items[1]]]):
                max[assigment_list[items[1]]] = items[2]
        
        for i in range(len(self.scale_types)):
            for j in range(5):
                scales[i].append(float(max[i]) - (float(self.scale[i]) *  j))


        for i in range(len(self.scale_final)):
            for j in range(len(self.scale_final[i])):
                if float(self.scale_final[i][j][1]) > scales[i][1]:
                    self.scale_final[i][j].append('A')
                elif float(self.scale_final[i][j][1]) > scales[i][2]:
                    self.scale_final[i][j].append('B')
                elif float(self.scale_final[i][j][1]) > scales[i][3]:
                    self.scale_final[i][j].append('C')
                elif float(self.scale_final[i][j][1]) > scales[i][4]:
                    self.scale_final[i][j].append('D')
                else:
                    self.scale_final[i][j].append('F')
                

                
            

            
        
        

        for i in range(len(self.scale_final)):
            scale_frame = Frame(self.window)
            scale_frame_label = Label(scale_frame,text = self.scale_types[i])
            scale_frame_label.pack(pady = 10)
            for j in range(len(self.scale_final[i])):
                scale_label = Label(scale_frame,text = f'{self.scale_final[i][j][0]} {self.scale_final[i][j][1]} {self.scale_final[i][j][2]}')
                scale_label.pack(pady = 10)
            csv_button = Button(scale_frame, text = 'Create Csv', command = lambda i=i : self.create_csv(self.scale_final[i],self.scale_types[i]))
            #I reused  the code lambda i=i : from BrenBarn on https://stackoverflow.com/a/10865170
            csv_button.pack()
            scale_frame.pack(side = LEFT, expand= True, fill= BOTH)



    def create_csv(self,csv_list,name):
        with open(f'{name}.csv', 'a',newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=' ')
            for elements in csv_list:
                csvwriter.writerow(elements)

    def manual_clicked(self):
        self.file_name_frame.destroy()
        self.manual_entry_frame = Frame(self.window)
        self.question_check = True

        question_label = Label(self.manual_entry_frame, text ='How many Students Would you like to add?')
        self.question_entry = Entry(self.manual_entry_frame, width = 5)
        question_button = Button(self.manual_entry_frame, text = 'Confirm', command= self.question_clicked)
        question_help_label = Label(self.manual_entry_frame, text = 'Input should be a Non-Decimal Number greater than 0')

        question_label.pack(pady = 5)
        self.question_entry.pack(pady = 5)
        question_button.pack(pady = 5)
        question_help_label.pack(pady = 5)
        self.manual_entry_frame.place(relx=.5,rely=.5,anchor=CENTER)

    def question_clicked(self):
        question_input = self.question_entry.get()
        try:
            int(question_input)
            if int(question_input) < 1:
                raise ValueError
            self.get_students()
            
            
        except:
            if self.question_check:
                self.question_check = False
                fail_label = Label(self.manual_entry_frame, text = 'Error, Please Input Valid Number')
                fail_label.pack(pady = 10)



    def get_students(self):
        self.question_input =int(self.question_entry.get())
        self.manual_entry_frame.destroy()
        self.get_frame = Frame(self.window)
        self.get_name_label = Label( self.get_frame, text = 'NAME', bd=1, relief='solid',)
        self.get_assigment_label = Label( self.get_frame, text = 'ASSIGMENT' ,bd=1, relief='solid')
        self.get_grade_label = Label( self.get_frame, text = 'GRADE' ,bd=1, relief='solid')

        self.window.geometry('650x500')


        self.get_name_label.pack(side= LEFT, fill = X,expand=True)
        self.get_assigment_label.pack(side= LEFT, fill = X,expand=True)
        self.get_grade_label.pack(side= LEFT, fill = X,expand=True)

        self.get_frame.pack(side = TOP, fill = X)


        self.name_list = []
        self.assigment_list = []
        self.grade_list = []
        'Concept For Storing Entrys in list found from https://www.reddit.com/r/learnpython/comments/rxo5b0/need_help_creating_unique_entry_boxes_with_a_for/'

        for i in range(self.question_input):
            frame_entry = Frame(self.window)

            name_entry = Entry(frame_entry)
            assigment_entry = Entry(frame_entry)
            grade_entry = Entry(frame_entry)

            name_entry.pack(side = LEFT, fill = X, expand= True)
            assigment_entry.pack(side = LEFT, fill = X, expand= True)
            grade_entry.pack(side = LEFT, fill = X, expand= True)

            frame_entry.pack(fill = X)

            self.name_list.append(name_entry)
            self.assigment_list.append(assigment_entry)
            self.grade_list.append(grade_entry)
        create_button = Button(self.window,width=25,text = 'CREATE', command = self.manual_csv)
        help_label = Label(self.window, text = 'NOTE, Any boxs that are empty, or are filled with the wrong input types will discarded and not used\n Both the name and assigment entry boxs will take anything other than a empty box, Grade Entry boxs should be Numbers, Decimals allowed')
        create_button.pack()
        help_label.pack()

    def manual_csv(self):
        self.write_csv_list = []
        for i in range(self.question_input):
            if self.name_list[i].get().isspace() or self.assigment_list[i].get().isspace() or self.grade_list[i].get().isspace():
                continue
            elif not self.name_list[i].get() or not self.assigment_list[i].get() or not self.grade_list[i].get():
                continue
            else:
                try:
                    float(self.grade_list[i].get())

                    self.check_pass.append([self.name_list[i].get(),self.assigment_list[i].get(),self.grade_list[i].get()])
                    
                except:
                    continue
            
        for frames in self.window.winfo_children():
                frames.destroy()
        self.determine_scale()
        
        



    
            
        

                
                    





        
        

        


        
        
        


    