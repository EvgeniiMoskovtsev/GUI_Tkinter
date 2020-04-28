import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import tkinter.filedialog as fl


class App:
    def __init__(self, window, window_title):
        self.first_click = True
        self.window = window
        self.window.title(window_title)
        self.buttonPanel = tkinter.Frame(self.window)
        self.canvasPanel = tkinter.Frame(self.window)

        # because these two panels are side-by-side, pack is the
        # best choice:
        # self.buttonPanel.pack(side="left", fill="y")
        # self.canvasPanel.pack(side="right", fill="both", expand=True)
        self.buttonPanel.grid(row=0, column=1)
        self.canvasPanel.grid(row=0, column=0)

        self.btn_open = tkinter.Button(self.buttonPanel, text="Select_image", width=50, command=lambda: self.select_images())
        self.btn_open.grid(row=0, column=0)

    def select_images(self):
        self.btn_open.grid_remove()
        path = tkinter.filedialog.askopenfilename()
        self.image = cv2.imread(path)

        self.canvas = tkinter.Canvas(self.canvasPanel, width=self.image.shape[1], height=self.image.shape[0])
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.image))
        self.canvas.create_image(0, 0,  image=self.photo, anchor=tkinter.NW)
        # self.canvas.pack(fill=tkinter.BOTH, expand=1)
        # self.btn_open.forget()
        self.canvas.grid(row=0, column=0)
        self.btn_subctr = tkinter.Button(self.buttonPanel, text="Субтракция", width=20, command=lambda: self.substr())
        self.btn_func_dim = tkinter.Button(self.buttonPanel, text="Функция измерений", width=20,
                                           command=lambda: self.func_dim())
        self.btn_subctr.grid(row=0, column=1)
        self.btn_func_dim.grid(row=1, column=1)
        # self.btn_subctr.pack()
        # self.btn_func_dim.pack()

    def substr(self):
        im = self.image
        gr = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=10.0, tileGridSize=(8, 8))
        tit = clahe.apply(gr)
        result = cv2.cvtColor(tit, cv2.COLOR_GRAY2BGR)
        self.substr_photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(result))
        self.canvas.create_image(0, 0, image=self.substr_photo, anchor=tkinter.NW)
        # self.canvas.pack()
    def func_dim(self):
        self.btn_set_reference_size = tkinter.Button(self.buttonPanel, width=20,
                                                     text="Задать эталонный размер",
                                                     background='green',activebackground='green',
                                                     command=lambda: self.set_size())

        self.info_label = tkinter.Label(self.buttonPanel,text='Отметьте 2 точки на \nизображении,\n'
                                             'расстояние между\n которыми будет\n '
                                             'принято,''как эталонное', font=("Arial 32", 8))

        self.btn_set_reference_size.grid(row=2, column=1)
        self.info_label.grid(row=3, column=1)
        # self.btn_set_reference_size.pack()
        # self.info_label.pack()

    def set_size(self):
        self.canvas.bind('<Button-1>', self.draw_line)

    def draw_line(self, event):

        if self.first_click is True:
            self.x1 = event.x
            self.y1 = event.y
            self.first_click = False

        else:
            self.x2 = event.x
            self.y2 = event.y
            self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill='yellow', width=2)
            self.info_label.destroy()
            self.btn_cancel_draw = tkinter.Button(self.buttonPanel, width=20,
                                                         text="Отмена",
                                                         background='red', activebackground='red',
                                                         command=lambda: self.cancel())
            self.btn_cancel_draw.grid(row=3, column=1)

    def cancel(self):
        self.substr()
        self.btn_cancel_draw.grid_remove()






# Create a window and pass it to the Application object
root = tkinter.Tk()

gui = App(root, '')
root.mainloop()
