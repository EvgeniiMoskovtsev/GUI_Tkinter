import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import tkinter.filedialog as fl
import statistics
import numpy as np
import math

class App:
    def __init__(self, window, window_title):
        self.first_click = True
        self.second_click = False
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
        self.btn_open = tkinter.Button(self.buttonPanel, text="Select_image", width=50,
                                       command=lambda: self.select_images())
        self.btn_open.grid(row=0, column=0)
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.info_label_flag = True
        self.destroy_frame = False
        self.converted_length = None
        self.revert_btn_rescale = None
        self.btn_set_reference_size = None
        self.confirm_btn_rescale = None
        self.rescale_flag = None
        self.distance_measurement_flag = False
        self.labeltext = ''
        self.list_points = []
        self.i = 1
        self.ill_or_not = []

    def select_images(self):
        self.btn_open.grid_remove()
        path = tkinter.filedialog.askopenfilename()
        self.image = cv2.imread(path)
        self.canvas = tkinter.Canvas(self.canvasPanel, width=self.image.shape[1], height=self.image.shape[0])
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.image))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.canvas.grid(row=0, column=0)
        self.btn_subctr = tkinter.Button(self.buttonPanel, text="Субтракция", width=20, command=lambda: self.substr())
        self.btn_func_dim = tkinter.Button(self.buttonPanel, text="Функция измерений", width=20,
                                           command=lambda: self.func_dim())
        self.btn_subctr.grid(row=0, column=1)
        self.btn_func_dim.grid(row=1, column=1)

    def substr(self):
        im = self.image
        gr = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=10.0, tileGridSize=(8, 8))
        tit = clahe.apply(gr)
        self.result = cv2.cvtColor(tit, cv2.COLOR_GRAY2BGR)
        self.substr_photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.result))
        self.canvas.create_image(0, 0, image=self.substr_photo, anchor=tkinter.NW)
        if self.revert_btn_rescale is not None:
            self.revert_btn_rescale.grid_remove()
            self.btn_set_reference_size.grid_remove()
        if self.confirm_btn_rescale is not None:
            self.confirm_btn_rescale.grid_remove()
            # self.canvas.pack()

    def func_dim(self):
        if self.converted_length is None:
            self.btn_set_reference_size = tkinter.Button(self.buttonPanel, width=20,
                                                         text="Задать эталонный размер",
                                                         background='green', activebackground='green',
                                                         command=lambda: self.set_size())

            self.btn_set_reference_size.grid(row=2, column=1)
            if self.info_label_flag is True:
                self.info_label = tkinter.Label(self.buttonPanel, text='Отметьте 2 точки на \nизображении,\n'
                                                                       'расстояние между\n которыми будет\n '
                                                                       'принято,''как эталонное', font=("Arial 32", 8))
                self.info_label.grid(row=3, column=1)
            # self.btn_set_reference_size.pack()
            # self.info_label.pack()
        elif self.rescale_flag is True:
            self.btn_set_reference_size = tkinter.Button(self.buttonPanel, width=20,
                                                         text="Масштабирование",
                                                         background='green', activebackground='green',
                                                         command=lambda: self.rescale())

            self.btn_set_reference_size.grid(row=2, column=1)

        # elif self.distance_measurement_flag is True:


    def set_size(self):
        self.canvas.bind('<Button-1>', self.draw_line)

    def draw_line(self, event):

        if self.first_click is True:
            if self.x1 is None and self.y1 is None:
                self.x1 = event.x
                self.y1 = event.y
                self.first_click = False

        else:
            if self.x2 is None and self.y2 is None:
                self.x2 = event.x
                self.y2 = event.y
                if self.converted_length is None:
                    self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill='yellow', width=2)
                    self.info_label.destroy()
                    self.btn_cancel_draw = tkinter.Button(self.buttonPanel, width=20,
                                                          text="Отмена",
                                                          background='red', activebackground='red',
                                                          command=lambda: self.cancel())
                    self.btn_cancel_draw.grid(row=2, column=2)

                # Длина, обхват

                    self.length_btn = tkinter.Button(self.buttonPanel, width=10,
                                                     text="Длина",
                                                     background='green', activebackground='green',
                                                     command=lambda: self.set_length())
                    self.girth_btn = tkinter.Button(self.buttonPanel, width=10,
                                                    text="Обхват",
                                                    background='green', activebackground='green',
                                                    command=lambda: self.set_girth())
                    self.length_btn.grid(row=3, column=1)
                    self.girth_btn.grid(row=3, column=2)

    def cancel(self):
        self.first_click = True
        self.info_label_flag = False
        self.x1, self.y1, self.x2, self.y2 = None, None, None, None
        self.substr()
        self.btn_cancel_draw.grid_remove()
        self.girth_btn.grid_remove()
        self.length_btn.grid_remove()

    def set_length(self):
        self.btn_cancel_draw.grid_remove()
        self.girth_btn.grid_remove()
        self.length_entry = tkinter.Entry(self.buttonPanel, width=10)
        self.length_entry.grid(row=5, column=2)
        self.ok_btn = tkinter.Button(self.buttonPanel, width=10,
                                     text="Ок",
                                     background='green', activebackground='green',
                                     command=lambda: self.set_text_lenght())
        self.info_label_length_btn = tkinter.Label(self.buttonPanel, text='Введите длину \n'
                                                                   'выбранной области\n '
                                                                   '(мм)', font=("Arial 32", 11))
        self.info_label_length_btn.grid(row=5, column=1)
        self.ok_btn.grid(row=6, column=2)

    def set_girth(self):
        self.btn_cancel_draw.grid_remove()
        self.length_btn.grid_remove()
        self.girth_btn.grid(row=3, column=1)
        self.girth_entry = tkinter.Entry(self.buttonPanel, width=20)
        self.girth_entry.grid(row=5, column=2)
        self.ok_btn = tkinter.Button(self.buttonPanel, width=10,
                                     text="Ок",
                                     background='green', activebackground='green',
                                     command=lambda: self.set_text_girth())
        self.info_label_girth_btn = tkinter.Label(self.buttonPanel, text=self.labeltext, font=("Arial 32", 11))
        self.info_label_girth_btn.grid(row=5, column=1)

        self.ok_btn.grid(row=6, column=2)

    def set_text_lenght(self):
        self.text = int(self.length_entry.get())
        self.length_btn.grid_remove()
        self.length_entry.grid_remove()
        self.info_label_length_btn.grid_remove()
        self.ok_btn.grid_remove()
        self.btn_set_reference_size.grid_remove()
        self.substr()
        self.count_real_lenght()

    def set_text_girth(self):
        self.text = int(self.girth_entry.get())
        self.girth_btn.grid_remove()
        self.girth_entry.grid_remove()
        self.info_label_girth_btn.grid_remove()
        self.ok_btn.grid_remove()
        self.btn_set_reference_size.grid_remove()
        self.substr()
        self.count_real_lenght()

    def count_real_lenght(self):
        delta_pix = ((self.x2 - self.x1)**2 + (self.y2 - self.y1)**2)**(1/2)
        self.converted_length = delta_pix / self.text
        self.x1, self.y1, self.x2, self.y2 = None, None, None, None
        self.first_click = True
        self.rescale_flag = True

    def rescale(self):
        self.canvas.bind('<Button-1>', self.draw_line)
        if self.x1 is not None and self.x2 is not None:
            self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, width=3, outline='red')
            self.canvas.grid(row=0, column=0)
            self.ok_btn_rescale = tkinter.Button(self.buttonPanel, width=10,
                                     text="Ок",
                                     background='green', activebackground='green',
                                     command=lambda: self.rescale_image())
            self.ok_btn_rescale.grid(row=5, column=1)
            # self.x1, self.y1, self.x2, self.y2 = None, None, None, None

    def rescale_image(self):
        self.revert_btn_rescale = tkinter.Button(self.buttonPanel, width=20,
                                             text="Вернуть к исходному",
                                             background='green', activebackground='green',
                                             command=lambda: self.substr())
        self.revert_btn_rescale.grid(row=5, column=1)
        self.confirm_btn_rescale = tkinter.Button(self.buttonPanel, width=10,
                                             text="Ок",
                                             background='green', activebackground='green',
                                             command=lambda: self.delete())
        self.confirm_btn_rescale.grid(row=6, column=1)

        self.canvas = tkinter.Canvas(self.canvasPanel, width=self.image.shape[1], height=self.image.shape[0])
        self.image_rescale = self.result[self.y1:self.y2, self.x1:self.x2]
        self.scale_percent = 300
        width = int(self.image_rescale.shape[1] * self.scale_percent / 100)
        height = int(self.image_rescale.shape[0] * self.scale_percent / 100)
        dim = (width, height)
        self.resized = cv2.resize(self.image_rescale, dim, interpolation=cv2.INTER_AREA)
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.resized))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.canvas.grid(row=0, column=0)
        self.ok_btn_rescale.grid_remove()
        self.x1, self.y1, self.x2, self.y2 = None, None, None, None
        self.first_click = True

    def delete(self):
        self.revert_btn_rescale.grid_remove()
        self.confirm_btn_rescale.grid_remove()
        self.rescale_flag = False
        self.distance_measurement_flag = True

        self.measure_vessel = tkinter.Button(self.buttonPanel, width=20,
                                                     text="Измерение расстояние",
                                                     background='green', activebackground='green',
                                                     command=lambda: self.draw_line_list_event())

        self.measure_vessel.grid(row=3, column=1)


        self.uniformity_vessel = tkinter.Button(self.buttonPanel, width=20,
                                                     text="Равномерность\n диаметра сосуда",
                                                     background='green', activebackground='green',
                                                     command=lambda: self.count_uniformity_vessel())
        self.uniformity_vessel.grid(row=5, column=1)

        self.measure_vessel_reset = tkinter.Button(self.buttonPanel, width=20,
                                                     text="Сбросить",
                                                     background='green', activebackground='green',
                                                     command=lambda: self.reset())

        self.measure_vessel_reset.grid(row=2, column=2)

        self.entry_label_out = tkinter.Label(self.buttonPanel, text=self.labeltext, font=("Arial 32", 11), bg='white')
        self.entry_label_out.grid(row=4, column=2)

        self.measure_angle = tkinter.Button(self.buttonPanel, width=20,
                                                     text="Измерение углов",
                                                     background='green', activebackground='green',
                                                     command=lambda: self.measure_angle_event())
        self.measure_angle.grid(row=4, column=1)
    def draw_line_list_event(self):
        self.canvas.bind('<Button-1>', self.draw_line_list)

    def measure_angle_event(self):
        self.canvas.bind('<Button-1>', self.draw_angle)

    def draw_angle(self, event):
        if self.first_click is True:
            if self.x1 is None and self.y1 is None:
                self.x1 = event.x
                self.list_points.append(self.x1)
                self.y1 = event.y
                self.list_points.append(self.y1)
                self.first_click = False
                self.second_click = True

        elif self.second_click is True:
            if self.x2 is None and self.y2 is None:
                self.x2 = event.x
                self.y2 = event.y
                self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill='yellow', width=2)
                self.second_click = False

        else:
            self.x3 = event.x
            self.y3 = event.y
            self.canvas.create_line(self.x2, self.y2, self.x3, self.y3, fill='yellow', width=2)
            A = (self.x1, self.y1)
            B = (self.x2, self.y2)
            C = (self.x3, self.y2)
            a = np.radians(np.array(A))
            b = np.radians(np.array(B))
            c = np.radians(np.array(C))
            avec = a - b
            cvec = c - b

            # Adjust vectors for changed longitude scale at given latitude into 2D space
            lat = b[0]
            avec[1] *= math.cos(lat)
            cvec[1] *= math.cos(lat)

            # Find the angle between the vectors in 2D space
            angle2deg = np.degrees(
                math.acos(np.dot(avec, cvec) / (np.linalg.norm(avec) * np.linalg.norm(cvec))))

            self.first_click = True
            self.labeltext = self.labeltext + '\n' + 'a({})= {}'.format(str(self.i), str(angle2deg))
            self.entry_label_out['text'] = self.labeltext
            self.x1, self.y1, self.x2, self.y2, self.x3, self.y3 = None, None, None, None, None, None

    def draw_line_list(self, event):

        if self.first_click is True:
            if self.x1 is None and self.y1 is None:
                self.x1 = event.x
                self.list_points.append(self.x1)
                self.y1 = event.y
                self.list_points.append(self.y1)
                self.first_click = False

        else:
            if self.x2 is None and self.y2 is None:
                self.x2 = event.x
                self.list_points.append(self.x2)
                self.y2 = event.y
                self.list_points.append(self.y2)
                self.first_click = True
                self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill='yellow', width=2)
                self.count_radius()
                self.x1, self.y1, self.x2, self.y2 = None, None, None, None

    def count_radius(self):
        delta_pix = ((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2) ** (1 / 2)
        real_length = (delta_pix / self.converted_length) / (self.scale_percent / 100)
        self.ill_or_not.append(real_length)
        self.labeltext = self.labeltext + '\n' + 'r({})= {} мм'.format(str(self.i), str(real_length))
        self.entry_label_out['text'] = self.labeltext

    def reset(self):
        self.ill_or_not = []
        self.labeltext = ''
        self.entry_label_out['text'] = self.labeltext
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.resized))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.canvas.grid(row=0, column=0)

    def count_uniformity_vessel(self):
        median_ = statistics.median(self.ill_or_not)
        mean_ = statistics.mean(self.ill_or_not)
        max_value = max(self.ill_or_not)
        if mean_ > 0 and mean_ < 1:
            text_4='Диагноз: В норме'
        elif mean_>=1 and mean_ < 1.5:
            text_4='Диагноз: Стадия: С1-телеангиэктазии'
        elif median_>=1.5 and median_ < 4 and (max_value - median_) < 0.7:
            text_4='Неравномерность диаметра сосуда: отсутсвует\n' \
                   'Диагноз: Ретикулярный варикоз'
        elif median_>=1.5 and median_ < 4 and (max_value - median_) > 0.7:
            text_4 = 'Неравномерность диаметра сосуда: присутствует\n' \
                     'Диагноз: Ретикулярный варикоз'
        elif median_ >=4 and median_ < 8:
            text_4='Диагноз: Стадия С1- ретикулярный варикоз'

        else:
            text_4='Данная алгоритм не знает\n' \
                   'Такой патологии'

        text_1 = 'Программа считает медиану значений всех  измеренных радиусов.'
        text_2 = 'Средний диаметр сосуда: {} мм'.format(mean_)
        text_3 = 'Максимальный раудис {} мм'.format(max_value)
        self.entry_label_out['text'] = text_1 + '\n' + text_2 + '\n' + text_3 \
                                        + '\n' + text_4




root = tkinter.Tk()
gui = App(root, '')
root.mainloop()
