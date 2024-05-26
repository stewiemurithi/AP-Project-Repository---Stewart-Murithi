import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
import joblib
from PIL import Image, ImageTk

# Load the model
model_filename = 'Oklahoma_RFR_model.joblib'
loaded_model = joblib.load(model_filename)

# Load the Excel file into a DataFrame
excel_file = '1950-2023 6.xlsx'
df = pd.read_excel(excel_file)

# Get the list of counties
counties = [
    "Adair", "Alfalfa", "Atoka", "Beaver", "Beckham", "Blaine", "Bryan", "Caddo", "Canadian", "Carter",
    "Cherokee", "Choctaw", "Cimarron", "Cleveland", "Coal", "Comanche", "Cotton", "Craig", "Creek",
    "Custer", "Delaware", "Dewey", "Ellis", "Garfield", "Garvin", "Grady", "Grant", "Greer", "Harmon",
    "Harper", "Haskell", "Hughes", "Jackson", "Jefferson", "Johnston", "Kay", "Kingfisher", "Kiowa",
    "Latimer", "Le Flore", "Lincoln", "Logan", "Love", "Major", "Marshall", "Mayes", "McClain",
    "McCurtain", "McIntosh", "Murray", "Muskogee", "Noble", "Nowata", "Okfuskee", "Oklahoma",
    "Okmulgee", "Osage", "Ottawa", "Pawnee", "Payne", "Pittsburg", "Pontotoc", "Pottawatomie",
    "Pushmataha", "Roger Mills", "Rogers", "Seminole", "Sequoyah", "Stephens", "Texas", "Tillman",
    "Tulsa", "Wagoner", "Washington", "Washita", "Woods", "Woodward"
]


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tornadoes of Oklahoma")
        self.geometry("800x600")

        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.pages = {}
        for Page in (Page1, Page2, Page3, Page4):
            page_name = Page.__name__
            page = Page(parent=self.container, controller=self)
            self.pages[page_name] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_page("Page1")

    def show_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()


class Page1(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="TORNADOES OF OKLAHOMA (1950-2023)")
        label.pack(pady=10, padx=10)

        # Introduction text
        text_content = (
            "Welcome to the Tornadoes of Oklahoma platform. Available for your experimentation are a forecasting model "
            "and archival feature. This interface is designed to present you with the basics of meteorological "
            "modelling and the world of tornadoes.\n\n"
            "Forecasting model\n"
            "The forecasting model is designed to compute the expected number of tornadoes in Oklahoma "
            "in a given month. It’s calculations are based on a series of meteorological variables, "
            "principally temperature and humidity (in this specific model, precipitation is being "
            "used as a proxy for humidity). Available to you is the possibility to enter your own values "
            "for these variables as well as the date for which you would like to predict the incidence.\n\n"
            "Archival feature\n"
            "The archival feature includes a dataset containing all recorded tornadoes in Oklahoma from 1950 to 2023. "
            "Made available to you is the possibility to find any recorded tornado according to the desired date, "
            "rating, or county. Entering a search without any chosen entries allows you to view the full dataset. "
            "For the date functionality, to find a corresponding tornado please specify an "
            "exact date.\n\n"
            "Key Terminology\n"
            "Fujita-Scale: The Fujita scale is a tornado classification index that categorises tornadoes "
            "based on their associated wind speed and capacity for structural damage. It was in use from 1971 to "
            "2006 before being replaced with the Enhanced Fujita scale in 2007. In the archival feature you will find "
            "options for 'Unrated1' and 'Unrated2' which correspond to unknown ratings in the Fujita and Enhanced "
            "Fujita periods respectively."
        )

        # Introduction Label
        text_label = ttk.Label(self, text=text_content, wraplength=600, justify="left")
        text_label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Go to Forecasting Model",
                            command=lambda: controller.show_page("Page2"))
        button.pack()

        button2 = ttk.Button(self, text="Go to Tornado Archive",
                             command=lambda: controller.show_page("Page3"))
        button2.pack()

        button3 = ttk.Button(self, text="Go to Visuals",
                             command=lambda: controller.show_page("Page4"))
        button3.pack()


class Page4(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="These are the Visuals")
        label.pack(pady=10, padx=10)

        # Load and display images
        self.images = []
        for img_path in ["Fujita Scale Percentages.jpg", "Enhanced Fujita Scale Percentages.jpg",
                         "FreqTornOKCounty.jpg"]:
            img = Image.open(img_path)
            img = img.resize((200, 200))
            photo = ImageTk.PhotoImage(img)
            self.images.append(photo)
            label = tk.Label(self, image=photo)
            label.pack(pady=5)

        button = ttk.Button(self, text="Go to Forecasting Model",
                            command=lambda: controller.show_page("Page2"))
        button.pack()

        button1 = ttk.Button(self, text="Go to About",
                             command=lambda: controller.show_page("Page1"))
        button1.pack()

        button2 = ttk.Button(self, text="Go to Tornado Archive",
                             command=lambda: controller.show_page("Page3"))
        button2.pack()


class Page2(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="This is the Forecasting Model")
        label.pack(pady=10, padx=10)

        self.create_forecasting_model_ui()

        button1 = ttk.Button(self, text="Go to About",
                             command=lambda: controller.show_page("Page1"))
        button1.pack()

        button2 = ttk.Button(self, text="Go to Tornado Archive",
                             command=lambda: controller.show_page("Page3"))
        button2.pack()

        button3 = ttk.Button(self, text="Go to Visuals",
                             command=lambda: controller.show_page("Page4"))
        button3.pack()

    def create_forecasting_model_ui(self):
        ttk.Label(self, text="Month (1-12):").pack(padx=10, pady=5)
        self.month_entry = ttk.Entry(self)
        self.month_entry.pack(padx=10, pady=5)

        ttk.Label(self, text="Year (post-1950):").pack(padx=10, pady=5)
        self.year_entry = ttk.Entry(self)
        self.year_entry.pack(padx=10, pady=5)

        ttk.Label(self, text="Temperature Difference (Dallas-Wichita) F°:").pack(padx=10, pady=5)
        self.temp_diff_entry = ttk.Entry(self)
        self.temp_diff_entry.pack(padx=10, pady=5)

        ttk.Label(self, text="Precipitation Difference (Dallas-Wichita) Inches:").pack(padx=10, pady=5)
        self.precip_diff_entry = ttk.Entry(self)
        self.precip_diff_entry.pack(padx=10, pady=5)

        ttk.Label(self, text="Oklahoma Temperature F°:").pack(padx=10, pady=5)
        self.ok_temp_entry = ttk.Entry(self)
        self.ok_temp_entry.pack(padx=10, pady=5)

        ttk.Label(self, text="Oklahoma Precipitation Inches:").pack(padx=10, pady=5)
        self.ok_precip_entry = ttk.Entry(self)
        self.ok_precip_entry.pack(padx=10, pady=5)

        predict_button = ttk.Button(self, text="Predict", command=self.on_predict)
        predict_button.pack(pady=10)

    def on_predict(self):
        try:
            month = int(self.month_entry.get())
            year = int(self.year_entry.get())
            temp_diff = float(self.temp_diff_entry.get())
            precip_diff = float(self.precip_diff_entry.get())
            ok_temp = float(self.ok_temp_entry.get())
            ok_precip = float(self.ok_precip_entry.get())

            result = self.predict_tornado_count(month, year, temp_diff, precip_diff, ok_temp, ok_precip)
            result_base = int(result)
            messagebox.showinfo("Prediction Result", f'Predicted Tornado Count: {result_base}')
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numerical values.")

    def predict_tornado_count(self, month, year, temp_diff, precip_diff, ok_temp, ok_precip):
        input_data = pd.DataFrame({
            'Month': [month],
            'Year': [year],
            'Month_sin': [np.sin(2 * np.pi * month / 12)],
            'Month_cos': [np.cos(2 * np.pi * month / 12)],
            'TempDiff': [temp_diff],
            'PrecipDiff': [precip_diff],
            'OkTemp': [ok_temp],
            'OkPrecip': [ok_precip]
        })

        prediction = loaded_model.predict(input_data)
        return prediction[0]


class Page3(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="This is the Tornado Archive")
        label.pack(pady=10)

        self.create_tornado_archive_ui()

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        button1 = ttk.Button(button_frame, text="Go to About",
                             command=lambda: controller.show_page("Page1"))
        button1.pack(side=tk.LEFT, padx=5)

        button2 = ttk.Button(button_frame, text="Go to Forecasting Model",
                             command=lambda: controller.show_page("Page2"))
        button2.pack(side=tk.LEFT, padx=5)

        button3 = ttk.Button(self, text="Go to Visuals",
                            command=lambda: controller.show_page("Page4"))
        button3.pack(side=tk.LEFT, padx=5)

    def create_tornado_archive_ui(self):
        form_frame = ttk.Frame(self)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="Day").pack(side=tk.LEFT, padx=5)
        self.day_var = tk.StringVar()
        day_menu = ttk.Combobox(form_frame, textvariable=self.day_var)
        day_menu['values'] = [""] + list(range(1, 32))
        day_menu.pack(side=tk.LEFT, padx=5)

        ttk.Label(form_frame, text="Month").pack(side=tk.LEFT, padx=5)
        self.month_var = tk.StringVar()
        month_menu = ttk.Combobox(form_frame, textvariable=self.month_var)
        month_menu['values'] = [""] + list(range(1, 13))
        month_menu.pack(side=tk.LEFT, padx=5)

        ttk.Label(form_frame, text="Year").pack(side=tk.LEFT, padx=5)
        self.year_var = tk.StringVar()
        year_menu = ttk.Combobox(form_frame, textvariable=self.year_var)
        year_menu['values'] = [""] + sorted(df['Date'].dt.year.unique())
        year_menu.pack(side=tk.LEFT, padx=5)

        ttk.Label(form_frame, text="F-Scale").pack(side=tk.LEFT, padx=5)
        self.fscale_var = tk.StringVar()
        fscale_menu = ttk.Combobox(form_frame, textvariable=self.fscale_var)
        fscale_menu['values'] = [""] + ["Unrated1", "Unrated2", "F0", "F1", "F2", "F3", "F4",
                                        "F5", "EF0", "EF1", "EF2", "EF3", "EF4", "EF5"]
        fscale_menu.pack(side=tk.LEFT, padx=5)

        ttk.Label(form_frame, text="County").pack(side=tk.LEFT, padx=5)
        self.county_var = tk.StringVar()
        county_menu = ttk.Combobox(form_frame, textvariable=self.county_var)
        county_menu['values'] = [""] + counties
        county_menu.pack(side=tk.LEFT, padx=5)

        search_button = ttk.Button(self, text="Search", command=self.search)
        search_button.pack(pady=10)

        columns = ('Tornado Number', 'Date', 'F-Scale', 'County')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

    def search(self):
        query_df = df.copy()

        day = self.day_var.get()
        month = self.month_var.get()
        year = self.year_var.get()
        if day and month and year:
            query_date = f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
            query_df = query_df[query_df['Date'] == query_date]

        fscale = self.fscale_var.get()
        if fscale:
            query_df = query_df[query_df['F-Scale'] == fscale]

        county = self.county_var.get()
        if county:
            query_df = query_df[query_df['County'] == county]

        for row in self.tree.get_children():
            self.tree.delete(row)

        if not query_df.empty:
            for idx, row in query_df.iterrows():
                self.tree.insert("", "end", values=(row['Tornado Number'], row['Date'], row['F-Scale'], row['County']))


if __name__ == "__main__":
    app = App()
    app.mainloop()
