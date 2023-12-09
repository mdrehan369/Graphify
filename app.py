import customtkinter as tk
from customtkinter import filedialog
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
import os
from tkinter import messagebox
from PIL import Image

class App(tk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Graphify")
        self.geometry("850x500")
        self.iconbitmap("Images/logo.ico")
        self._light = "#00FF00"
        self._dark = "#228B22"
        self._filter = tk.StringVar(value="None")
        tk.set_appearance_mode("light")
        self._plot = tk.StringVar(value="Line Plot")
        self._slider = tk.DoubleVar()
        self.dataset = None
        self.df = None
        self._graph = {
            "Line Plot": "plot",
            "Scatter Plot": "scatter"
        }
        self._missingValues = tk.IntVar(value=1)

        self._featureX = tk.StringVar(value="X-Feature")
        self._featureY = tk.StringVar(value="Y-Feature")

        self.startPage()

    def _clearAll(self):

        for widget in self.winfo_children():
            widget.destroy()

    def _takeData(self):

        self.dataset = filedialog.askopenfilename(filetypes=[("Sheet", "*.xlsx"), ("csv", "*.csv")])
        if self.dataset == "":
            self.startPage()
        else:
            self.mainPage()

    def startPage(self):

        self._clearAll()

        (tk.CTkButton(self, text="Add Data", border_width=2, font=("lucida", 18)
                      , fg_color=self._light, command=self._takeData, text_color="black", corner_radius=8,
                      border_color="black", hover_color=self._dark)
         .place(relx=0.5, rely=0.5, anchor="center", relwidth=0.13, relheight=0.1))

    def mainPage(self):

        def configureSlider(event):
            if self._filter.get() != "None":
                mini = self.df[self._filter.get()].min()
                maxi = self.df[self._filter.get()].max()
                slider.configure(from_=mini, to=maxi, command=configureLabel)
                slider.place_configure(relx=0.5, rely=0.6, anchor="center", relwidth=0.4, relheight=0.02)

        def configureLabel(event):
            filterValueLabel.configure(text=f"{self._filter.get()}: {round(self._slider.get(), 2)}")

        self._clearAll()

        # Declaring left and right frames
        left = tk.CTkFrame(self, border_width=2)
        left.place(relx=0.25, rely=0.5, anchor="center", relwidth=0.5, relheight=1)

        right = tk.CTkFrame(self, border_width=2)
        right.place(relx=0.75, rely=0.5, anchor="center", relwidth=0.5, relheight=1)

        # back button
        img = Image.open("Images/arrow.png")
        (tk.CTkButton(left, text="", image=tk.CTkImage(img, size=(20, 20)), command=self.startPage, text_color="black",
                      fg_color=self._light, border_color="black", border_width=2,
                      hover_color=self._dark)
         .place(relx=0.1, rely=0.08, anchor="center", relwidth=0.08, relheight=0.08))

        # Type of plot
        (tk.CTkOptionMenu(left, values=["Line Plot", "Scatter Plot"], variable=self._plot, font=("lucida", 14),
                          fg_color="white", button_color="white"
                          , dropdown_fg_color="white",hover=False,text_color="black", corner_radius=5)
         .place(relx=0.5, rely=0.1, anchor="center", relwidth=0.4, relheight=0.05))

        # Checking file type
        if os.path.splitext(self.dataset)[1] == ".xlsx":
            self.df = pd.read_excel(self.dataset, "Sheet1")
        else:
            self.df = pd.read_csv(self.dataset)

        # Extracting features
        features = []
        for col in self.df.columns:
            features.append(col)

        self._featureX.set(features[0])
        self._featureY.set(features[0])

        # Designing the left frame
        # X-variable
        (tk.CTkLabel(left, text="X-Variable:", font=("lucida", 16), justify="center")
         .place(relx=0.4, rely=0.2, anchor="center", relwidth=0.25, relheight=0.05))

        (tk.CTkOptionMenu(left, values=features, variable=self._featureX, font=("lucida", 14),
                          fg_color="white", button_color="white"
                          , dropdown_fg_color="white", hover=False, text_color="black", corner_radius=5)
         .place(relx=0.5, rely=0.25, anchor="center", relwidth=0.4, relheight=0.05))

        # Y-variable
        (tk.CTkLabel(left, text="Y-Variable:", font=("lucida", 16), justify="center")
         .place(relx=0.4, rely=0.35, anchor="center", relwidth=0.25, relheight=0.05))

        (tk.CTkOptionMenu(left, values=features, variable=self._featureY, font=("lucida", 14),
                          fg_color="white", button_color="white"
                          , dropdown_fg_color="white", hover=False,text_color="black", corner_radius=5)
         .place(relx=0.5, rely=0.40, anchor="center", relwidth=0.4, relheight=0.05))

        # Filter
        (tk.CTkLabel(left, text="Filter:", font=("lucida", 16), justify="center")
        .place(relx=0.4, rely=0.5, anchor="center", relwidth=0.25, relheight=0.05))

        features.append("None")

        filterMenu = tk.CTkOptionMenu(left, values=features, variable=self._filter, font=("lucida", 14),
                          fg_color="white",command=configureSlider
                          , dropdown_fg_color="white", hover=False, text_color="black", corner_radius=5, button_color="white")
        filterMenu.place(relx=0.5, rely=0.55, anchor="center", relwidth=0.4, relheight=0.05)

        # slider
        slider = tk.CTkSlider(left, border_width=2, border_color='black', variable=self._slider, corner_radius=5,
                              button_color=self._dark, progress_color=self._light, button_hover_color=self._light,
                              fg_color='white', button_length=1)

        filterValueLabel = tk.CTkLabel(left, text="", font=("lucida", 14), justify="center")
        filterValueLabel.place(relx=0.4, rely=0.65, anchor="center", relwidth=0.5, relheight=0.05)

        # radio button
        (tk.CTkRadioButton(left, text="Auto-Fill", value=2, font=("lucida", 16),
                           variable=self._missingValues, fg_color=self._light, hover_color=self._dark,text_color="black")
         .place(relx=0.4, rely=0.75, anchor="center", relwidth=0.2, relheight=0.1))

        (tk.CTkRadioButton(left, text="Skip Missing Values", value=1, font=("lucida", 16),
                           variable=self._missingValues, fg_color=self._light, hover_color=self._dark, text_color="black")
         .place(relx=0.6, rely=0.75, anchor="center", relwidth=0.3, relheight=0.1))

        (tk.CTkButton(left, text="Plot", border_width=2, font=("lucida", 18), text_color="black",
                    command=lambda: self._plt(right), fg_color=self._light, hover_color=self._dark)

         .place(relx=0.5, rely=0.9, anchor="center", relwidth=0.12, relheight=0.07))

    def createCanvas(self, frame):
        # the figure that will contain the plot
        for widget in frame.winfo_children():
            widget.destroy()

        self.fig = Figure(figsize=(8, 8),
                     dpi=100)

        # adding the subplot
        plot1 = self.fig.add_subplot(111)

        # plotting the graph

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(self.fig,
                                   master=frame)
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor="center")

        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas,
                                       frame)
        toolbar.update()

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

        return plot1

    def _plt(self, frame):
        plot1 = self.createCanvas(frame)

        if self._missingValues.get() == 1:
            newDf = self.df.dropna()
        else:
            meanX = self.df[self._featureX.get()].mean()
            meanY = self.df[self._featureY.get()].mean()
            newDf = self.df.copy()
            newDf[self._featureX.get()].fillna(meanX, inplace=True)
            newDf[self._featureY.get()].fillna(meanY, inplace=True)

        x = newDf.loc[:, [self._featureX.get()]]
        y = newDf.loc[:, [self._featureY.get()]]

        if x.dtypes[self._featureX.get()] != 'int64' and x.dtypes[self._featureX.get()] != 'float64':
            messagebox.showerror(title="Values Not Compatible",
                                 message="The Selected Features Are Not Int Or Float Datatype")
            return

        if y.dtypes[self._featureY.get()] != 'int64' and y.dtypes[self._featureY.get()] != 'float64':
            messagebox.showerror(title="Values Not Compatible",
                                 message="The Selected Features Are Not Int Or Float Datatype")
            return

        func = self._graph[self._plot.get()]
        if self._filter.get() != 'None':

            newDf1 = newDf[newDf[self._filter.get()] < self._slider.get()]
            newDf2 = newDf[newDf[self._filter.get()] > self._slider.get()]

            x1 = newDf1.loc[:, [self._featureX.get()]]
            y1 = newDf1.loc[:, [self._featureY.get()]]

            x2 = newDf2.loc[:, [self._featureX.get()]]
            y2 = newDf2.loc[:, [self._featureY.get()]]

            if func == 'plot':
                plot1.plot(x1, y1, 'b-')
                plot1.plot(x2, y2, 'r-')

            elif func == 'scatter':
                plot1.scatter(x1, y1)
                plot1.scatter(x2, y2)

            plot1.legend([f'{self._filter.get()} < {round(self._slider.get(), 2)}', f'{self._filter.get()} > {round(self._slider.get(), 2)}'])
        else:
            if func == 'plot':
                plot1.plot(x, y)
            elif func == 'scatter':
                plot1.scatter(x, y)

        plot1.set_title(f"{self._featureX.get()}    VS    {self._featureY.get()}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
