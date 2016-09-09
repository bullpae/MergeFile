#! Python 3.5.2
"""
File Merge Program.
"""
import os
import struct
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename


class GUI(Frame):
    doc_file_path = ""
    zip_file_path = ""
    merge_file_path = ""

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()

        # Input Document File Path
        # self.Title = master.title("File Merger")
        self.label = ttk.Label(master, text="Merge File", foreground="green", font=("Helvetica", 14))
        self.label.grid(row=0, column=0)
        self.label = ttk.Label(master, text="Document File Path: ", foreground="blue", font=("Helvetica", 12))
        self.label.grid(row=1, column=0)

        self.doc_path = Entry(master)
        self.doc_path.grid(row=1, column=1)

        self.doc_sel_file = Button(master, text="File", command=self.doc_sel_btn_click)
        self.doc_sel_file.grid(row=1, column=2)

        # Input ZIP File Path
        self.label = ttk.Label(master, text="ZIP File Path: ", foreground="blue", font=("Helvetica", 12))
        self.label.grid(row=2, column=0)

        self.zip_path = Entry(master)
        self.zip_path.grid(row=2, column=1)

        self.zip_sel_file = Button(master, text="File", command=self.zip_sel_btn_click)
        self.zip_sel_file.grid(row=2, column=2)

        # self.merge_btn = Button(master, text="Merge", command=self.merge_file(self.doc_file_path, self.zip_file_path))
        # self.merge_btn = Button(master, text="Merge", command=self.open_file)
        self.merge_btn = Button(master, text="Merge", command=self.merge_file)
        self.merge_btn.grid(row=2, column=5)

        # Divide File
        self.label = ttk.Label(master, text="Divide File", foreground="green", font=("Helvetica", 14))
        self.label.grid(row=3, column=0)

        self.label = ttk.Label(master, text="Merge File Path: ", foreground="blue", font=("Helvetica", 12))
        self.label.grid(row=4, column=0)

        self.merge_path = Entry(master)
        self.merge_path.grid(row=4, column=1)

        self.merge_sel_file = Button(master, text="File", command=self.merge_sel_btn_click)
        self.merge_sel_file.grid(row=4, column=2)

        self.divide_btn = Button(master, text="Divide", command=self.divide_file)
        self.divide_btn.grid(row=4, column=5)

    def open_file(self):
        name = askopenfilename(initialdir="C:/",
                               filetypes=(("All Files", "*.*"), ("Text File", "*.txt"), ("ZIP File", "*.zip")),
                               title="Choose a file.")
        print(name)

        # try:
        #     with open(name, 'r') as UseFile:
        #         print(UseFile.read())
        # except:
        #     print("No file exists")

        return name

    def doc_sel_btn_click(self):
        file_path = self.open_file()
        print("Selected File Path:" + file_path)
        self.doc_path.insert(0, file_path)
        self.doc_file_path = file_path

    def zip_sel_btn_click(self):
        file_path = self.open_file()
        print("Selected File Path:" + file_path)
        self.zip_path.insert(0, file_path)
        self.zip_file_path = file_path

    def merge_sel_btn_click(self):
        file_path = self.open_file()
        print("Selected File Path:" + file_path)
        self.merge_path.insert(0, file_path)
        self.merge_file_path = file_path

    # def merge_file(self, file1, file2):
    def merge_file(self):
        file1 = self.doc_file_path
        file2 = self.zip_file_path
        print("Input File1: " + file1 + " File2:" + file2)
        if file1 == "" or file2 == "":
            print("Error!! File1: " + file1 + " File2:" + file2)
            return

        doc_file = open(file1, 'rb')
        zip_file = open(file2, 'rb')

        s = os.path.split(file1)
        new_file = open(s[0]+"/mg_"+s[1], 'w+b')
        new_file.write(doc_file.read())
        new_file.write(zip_file.read())
        file_size = os.path.getsize(file1)
        print("DOC FILE SIZE:", file_size)
        int_data = struct.pack('i', file_size)
        new_file.write(int_data)

        doc_file.close()
        zip_file.close()
        new_file.close()

    def divide_file(self):
        file = self.merge_file_path
        print("Input File1: " + file)
        if file == "":
            print("Error!! File: " + file)
            return

        mg_file = open(file, 'rb')

        intsize = struct.calcsize('i')
        filesize = os.path.getsize(file)
        mg_file.seek(filesize - intsize)
        data = mg_file.read(intsize)
        tudata = struct.unpack('i', data)
        docsize = tudata[0]

        mg_file.seek(0)

        s = os.path.split(file)
        doc_file = open(s[0]+"/doc.txt", 'wb')
        doc_file.write(mg_file.read(docsize))

        zip_file = open(s[0]+"/data.zip", 'wb')
        zip_file.write(mg_file.read(filesize - docsize - intsize))

        mg_file.close()
        doc_file.close()
        zip_file.close()


root = Tk()

if __name__ == "__main__":
    guiFrame = GUI(master=root)
    guiFrame.mainloop()
