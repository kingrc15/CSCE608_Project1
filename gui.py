import psycopg2
import tkinter as tk
from functools import partial
from tkcalendar import Calendar


class GUI(object):
    def __init__(self):
        super(GUI, self).__init__()

        self.conn = psycopg2.connect(
            dbname="medicaldatabase",
            user="postgres",
            password="postgres",
            host="127.0.0.1",
            port="5432",
        )
        self.cursor = self.conn.cursor()

        self.prev_page = None
        self.curr_page = None
        self.window = tk.Tk()
        self.main_window()

    def main_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.prev_page = self.curr_page
        self.curr_page = "Main"

        frame_title = tk.Frame(master=self.window)
        main_text = "Welcome to the Medical Database GUI"
        main_text += "\n Please select one of the options below to continue"
        label = tk.Label(master=frame_title, text=main_text, height=3)
        label.pack()
        frame_title.pack()

        frame_options = tk.Frame(master=self.window)
        frame_options.pack()

        opt_btn_lbls = [
            "Get Patient Data",
            "Get Hospital Data",
            "Get Provider Data",
            "Get Visit Data",
            "Get Measurement\n Data",
            "Get Condition Data",
            "Add Patient",
            "Add Visit",
            "Add Provider",
            "Add Hospital",
            "Add Condition",
            "Add Measurement",
        ]

        opt_btn_funcs = [
            self.get_patient_options_form,
            self.get_hospital_options_form,
            self.get_provider_options_form,
            self.get_visit_options_form,
            self.get_measurement_options_form,
            self.get_condition_options_form,
            self.add_patient_form,
            self.add_visit_form,
            self.add_provider_form,
            self.add_hospital_form,
            self.add_condition_form,
            self.add_measurement_form,
        ]

        n_cols = 4

        for i in range(0, 3):
            frame_options.columnconfigure(i, weight=1, minsize=150)
            frame_options.rowconfigure(i, weight=1, minsize=100)

            for j in range(0, n_cols):
                if i * n_cols + j >= len(opt_btn_lbls):
                    continue
                frame_opt_btn = tk.Frame(
                    master=frame_options, relief=tk.RAISED, borderwidth=1
                )
                frame_opt_btn.grid(row=i, column=j, padx=5, pady=5)
                button = tk.Button(
                    master=frame_opt_btn,
                    text=opt_btn_lbls[i * n_cols + j],
                    command=opt_btn_funcs[i * n_cols + j],
                    height=5,
                    width=15,
                )
                button.grid(row=i, column=j, sticky="nsew")

        self.window.mainloop()

    def get_patient_options_form(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.prev_page = self.curr_page
        self.curr_page = "Get Patient Options"
        self.generate_header()

        frame_options = tk.Frame(master=self.window)
        instructions = tk.Label(
            master=frame_options,
            text="Please Select a Patient ID from the dropdown",
            height=3,
        )
        instructions.pack()

        patient_opts = self.get_patients_table()

        clicked = tk.IntVar(master=frame_options)
        clicked.set(patient_opts[0])

        drop = tk.OptionMenu(frame_options, clicked, *patient_opts)
        drop.pack()

        get_patient_info_btn = tk.Button(
            master=frame_options,
            text="Get Patient Data",
            command=partial(self.get_patient_info, clicked),
            height=3,
        )
        get_patient_info_btn.pack()

        frame_options.pack()

        self.generate_return()

    def get_patient_info(self, patient_id):
        patient_id = patient_id.get()
        for widget in self.window.winfo_children():
            widget.destroy()

        self.prev_page = self.curr_page
        self.curr_page = f"Patient Info for Patient {patient_id}"
        self.generate_header()

        patient_opts = self.get_patient_info_table(patient_id)

        frame_table = tk.Frame(master=self.window)

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=0)
        e.insert(tk.END, "Patient ID")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=1)
        e.insert(tk.END, "Date of Birth")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=2)
        e.insert(tk.END, "Gender")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=3)
        e.insert(tk.END, "Ethnicity")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=4)
        e.insert(tk.END, "Name")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=5)
        e.insert(tk.END, "Visit ID")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=6)
        e.insert(tk.END, "Visit Start Datetime")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=7)
        e.insert(tk.END, "Visit End Datetime")

        for i, visit in enumerate(patient_opts):
            for j, info in enumerate(visit):
                if info is None:
                    info = ""
                e = tk.Entry(
                    frame_table,
                    fg="blue",
                    font=("Arial", 10, "bold"),
                )
                e.grid(row=i + 1, column=j)
                e.insert(tk.END, info)

        frame_table.pack()

        self.generate_return()

    def get_hospital_options_form(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.prev_page = self.curr_page
        self.curr_page = "Get Hospital Options"
        self.generate_header()

        frame_options = tk.Frame(master=self.window)
        instructions = tk.Label(
            master=frame_options,
            text="Please Select a Hospital ID from the dropdown",
            height=3,
        )
        instructions.pack()

        hospital_opts = self.get_hospital_table()

        clicked = tk.IntVar(master=frame_options)
        clicked.set(hospital_opts[0])

        drop = tk.OptionMenu(frame_options, clicked, *hospital_opts)
        drop.pack()

        get_patient_info_btn = tk.Button(
            master=frame_options,
            text="Get Hospital Data",
            command=partial(self.get_hospital_info, clicked),
            height=3,
        )
        get_patient_info_btn.pack()

        frame_options.pack()

        self.generate_return()

    def get_hospital_info(self, hospital_id):
        hospital_id = hospital_id.get()
        for widget in self.window.winfo_children():
            widget.destroy()

        self.prev_page = self.curr_page
        self.curr_page = f"Hospital Info for Hospital {hospital_id}"
        self.generate_header()

        hospital_info = self.get_hospital_info_table(hospital_id)

        frame_table = tk.Frame(master=self.window)

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=0)
        e.insert(tk.END, "Hospital ID")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=1)
        e.insert(tk.END, "Address")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=2)
        e.insert(tk.END, "Name")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=3)
        e.insert(tk.END, "ZIP Code")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=4)
        e.insert(tk.END, "County")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=5)
        e.insert(tk.END, "City")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=6)
        e.insert(tk.END, "Capacity")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        for i, hospital in enumerate(hospital_info):
            for j, info in enumerate(hospital):
                e = tk.Entry(
                    frame_table,
                    fg="blue",
                    font=("Arial", 10, "bold"),
                )
                e.grid(row=i + 1, column=j)
                e.insert(tk.END, info)

        frame_table.pack()

        self.generate_return()

    def get_visit_options_form(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.prev_page = self.curr_page
        self.curr_page = "Get Visit Options"
        self.generate_header()

        frame_options = tk.Frame(master=self.window)
        instructions = tk.Label(
            master=frame_options,
            text="Please select a Visit ID from the dropdown",
            height=3,
        )
        instructions.pack()

        visit_opts = self.get_visit_table()

        clicked = tk.IntVar(master=frame_options)
        clicked.set(visit_opts[0])

        drop = tk.OptionMenu(frame_options, clicked, *visit_opts)
        drop.pack()

        get_patient_info_btn = tk.Button(
            master=frame_options,
            text="Get Visit Data",
            command=partial(self.get_visit_info, clicked),
            height=3,
        )
        get_patient_info_btn.pack()

        frame_options.pack()

        self.generate_return()

    def get_visit_info(self, visit_id):
        visit_id = visit_id.get()
        for widget in self.window.winfo_children():
            widget.destroy()

        self.prev_page = self.curr_page
        self.curr_page = f"Visit Info for Visit {visit_id}"
        self.generate_header()

        visit_info = self.get_visit_info_table(visit_id)

        frame_table = tk.Frame(master=self.window)

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=0)
        e.insert(tk.END, "Visit ID")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=1)
        e.insert(tk.END, "Patient ID")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=2)
        e.insert(tk.END, "Hospital ID")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=3)
        e.insert(tk.END, "Start Datetime")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=4)
        e.insert(tk.END, "End Datetime")

        for i, visit_row in enumerate(visit_info):
            for j, info in enumerate(visit_row):
                e = tk.Entry(
                    frame_table,
                    fg="blue",
                    font=("Arial", 10, "bold"),
                )
                e.grid(row=i + 1, column=j)
                e.insert(tk.END, info)

        frame_table.pack()

        self.generate_return()

    def get_provider_options_form(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.prev_page = self.curr_page
        self.curr_page = "Get Provider Options"
        self.generate_header()

        frame_options = tk.Frame(master=self.window)
        instructions = tk.Label(
            master=frame_options,
            text="Please Select a Provider ID from the dropdown",
            height=3,
        )
        instructions.pack()

        provider_opts = self.get_provider_table()

        clicked = tk.IntVar(master=frame_options)
        clicked.set(provider_opts[0])

        drop = tk.OptionMenu(frame_options, clicked, *provider_opts)
        drop.pack()

        get_patient_info_btn = tk.Button(
            master=frame_options,
            text="Get Provider Data",
            command=partial(self.get_provider_info, clicked),
            height=3,
        )
        get_patient_info_btn.pack()

        frame_options.pack()

        self.generate_return()

    def get_provider_info(self, provider_id):
        provider_id = provider_id.get()
        for widget in self.window.winfo_children():
            widget.destroy()

        self.prev_page = self.curr_page
        self.curr_page = f"Provider Info for Provider {provider_id}"
        self.generate_header()

        provider_info = self.get_provider_info_table(provider_id)

        frame_table = tk.Frame(master=self.window)

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=0)
        e.insert(tk.END, "Provider ID")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=1)
        e.insert(tk.END, "Name")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=2)
        e.insert(tk.END, "Gender")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=3)
        e.insert(tk.END, "Specialty")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=4)
        e.insert(tk.END, "Date of Birth")

        for i, provider in enumerate(provider_info):
            for j, info in enumerate(provider):
                e = tk.Entry(
                    frame_table,
                    fg="blue",
                    font=("Arial", 10, "bold"),
                )
                e.grid(row=i + 1, column=j)
                e.insert(tk.END, info)

        frame_table.pack()

        self.generate_return()

    def get_measurement_options_form(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.prev_page = self.curr_page
        self.curr_page = "Get Measurement Options"
        self.generate_header()

        frame_options = tk.Frame(master=self.window)
        instructions = tk.Label(
            master=frame_options,
            text="Please select a Visit ID and measurement type from the dropdowns",
            height=3,
        )
        instructions.pack()

        visit_opts = self.get_visit_table()

        v_clicked = tk.IntVar(master=frame_options)
        v_clicked.set(visit_opts[0])

        v_drop = tk.OptionMenu(frame_options, v_clicked, *visit_opts)
        v_drop.pack()

        measurment_opts = self.get_measurement_table()

        m_clicked = tk.StringVar(master=frame_options)
        m_clicked.set("Heart Rate")

        m_drop = tk.OptionMenu(frame_options, m_clicked, *measurment_opts)
        m_drop.pack()

        get_patient_info_btn = tk.Button(
            master=frame_options,
            text="Get Measurement Data",
            command=partial(self.get_measurement_info, v_clicked, m_clicked),
            height=3,
        )
        get_patient_info_btn.pack()

        frame_options.pack()

        self.generate_return()

    def get_measurement_info(self, visit_id, measurement_name):
        visit_id = visit_id.get()
        measurement_name = measurement_name.get()
        for widget in self.window.winfo_children():
            widget.destroy()

        self.prev_page = self.curr_page
        self.curr_page = (
            f"Measurements for {measurement_name.strip()} during Visit {visit_id}"
        )
        self.generate_header()

        measurement_info = self.get_measurement_info_table(visit_id, measurement_name)

        frame_table = tk.Frame(master=self.window)

        e = tk.Entry(
            frame_table,
            fg="blue",
            font=("Arial", 10, "bold"),
        )

        e.grid(row=0, column=0)
        e.insert(tk.END, "Measurement ID")

        e = tk.Entry(
            frame_table,
            fg="blue",
            font=("Arial", 10, "bold"),
        )

        e.grid(row=0, column=1)
        e.insert(tk.END, "Name")

        e = tk.Entry(
            frame_table,
            fg="blue",
            font=("Arial", 10, "bold"),
        )

        e.grid(row=0, column=2)
        e.insert(tk.END, "Measurement Datetime")

        e = tk.Entry(
            frame_table,
            fg="blue",
            font=("Arial", 10, "bold"),
        )

        e.grid(row=0, column=3)
        e.insert(tk.END, "Unit")

        e = tk.Entry(
            frame_table,
            fg="blue",
            font=("Arial", 10, "bold"),
        )

        e.grid(row=0, column=4)
        e.insert(tk.END, "Value as Number")

        e = tk.Entry(
            frame_table,
            fg="blue",
            font=("Arial", 10, "bold"),
        )

        e.grid(row=0, column=5)
        e.insert(tk.END, "Provider ID")

        e = tk.Entry(
            frame_table,
            fg="blue",
            font=("Arial", 10, "bold"),
        )

        e.grid(row=0, column=6)
        e.insert(tk.END, "Patient ID")

        for i, measurement_row in enumerate(measurement_info):
            for j, info in enumerate(measurement_row):
                e = tk.Entry(
                    frame_table,
                    fg="blue",
                    font=("Arial", 10, "bold"),
                )
                e.grid(row=i + 1, column=j)
                e.insert(tk.END, info)

        frame_table.pack()

        self.generate_return()

    def get_condition_options_form(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.prev_page = self.curr_page
        self.curr_page = "Get Condition Options"
        self.generate_header()

        frame_options = tk.Frame(master=self.window)
        instructions = tk.Label(
            master=frame_options,
            text="Please select a Visit ID from the dropdown",
            height=3,
        )
        instructions.pack()

        visit_opts = self.get_visit_table()

        clicked = tk.IntVar(master=frame_options)
        clicked.set(visit_opts[0])

        drop = tk.OptionMenu(frame_options, clicked, *visit_opts)
        drop.pack()

        get_patient_info_btn = tk.Button(
            master=frame_options,
            text="Get Condition Data",
            command=partial(self.get_condition_info, clicked),
            height=3,
        )
        get_patient_info_btn.pack()

        frame_options.pack()

        self.generate_return()

    def get_condition_info(self, visit_id):
        visit_id = visit_id.get()
        for widget in self.window.winfo_children():
            widget.destroy()

        self.prev_page = self.curr_page
        self.curr_page = f"Condition for Visit {visit_id}"
        self.generate_header()

        condition_info = self.get_condition_info_table(visit_id)

        frame_table = tk.Frame(master=self.window)

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=0)
        e.insert(tk.END, "Condition ID")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=1)
        e.insert(tk.END, "Name")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=2)
        e.insert(tk.END, "Start Datetime")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=3)
        e.insert(tk.END, "End Datetime")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=4)
        e.insert(tk.END, "Stop Reason")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=5)
        e.insert(tk.END, "Provider ID")

        e = tk.Entry(frame_table, fg="blue", font=("Arial", 10, "bold"))

        e.grid(row=0, column=6)
        e.insert(tk.END, "Patient ID")

        for i, condition_row in enumerate(condition_info):
            for j, info in enumerate(condition_row):
                e = tk.Entry(
                    frame_table,
                    fg="blue",
                    font=("Arial", 10, "bold"),
                )
                e.grid(row=i + 1, column=j)
                e.insert(tk.END, info)

        frame_table.pack()

        self.generate_return()

    def add_patient_form(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.prev_page = self.curr_page
        self.curr_page = "Add Patient Form"
        self.generate_header()

        dob_frame = tk.Frame(master=self.window)

        dob_field = tk.Label(
            master=dob_frame,
            text="Please select a Date of Birth: ",
            height=3,
        )
        dob_field.grid(row=0, column=0)

        dob_field = Calendar(dob_frame, selectmode="day", year=2020, month=5, day=22)
        dob_field.grid(row=0, column=1)

        dob_frame.pack()

        gender_frame = tk.Frame(master=self.window)

        gender_field = tk.Label(
            master=gender_frame,
            text="Please select a gender from the dropdown: ",
            height=3,
        )
        gender_field.grid(row=0, column=0)

        gender_clicked = tk.StringVar(master=gender_frame)
        gender_clicked.set("Female")

        gender_drop = tk.OptionMenu(gender_frame, gender_clicked, *["Male", "Female"])
        gender_drop.grid(row=0, column=1)

        gender_frame.pack()

        ethnicity_frame = tk.Frame(master=self.window)

        gender_field = tk.Label(
            master=ethnicity_frame,
            text="Please select an ethnicity from the dropdown: ",
            height=3,
        )
        gender_field.grid(row=0, column=0)

        ethnicity_opts = self.get_ethnicities()

        ethnicity_clicked = tk.StringVar(master=ethnicity_frame)
        ethnicity_clicked.set(ethnicity_opts[0])

        ethnicity_drop = tk.OptionMenu(
            ethnicity_frame, ethnicity_clicked, *ethnicity_opts
        )
        ethnicity_drop.grid(row=0, column=1)

        ethnicity_frame.pack()

        name_frame = tk.Frame(master=self.window)

        instruction_name_field = tk.Label(
            master=name_frame,
            text="Please enter the first and last name: ",
            height=3,
        )
        instruction_name_field.grid(row=0, column=0)

        first_name_field = tk.Text(name_frame, height=1, width=15)
        first_name_field.grid(row=0, column=1)

        last_name_field = tk.Text(name_frame, height=1, width=15)
        last_name_field.grid(row=0, column=2)

        name_frame.pack()

        add_patient_btn = tk.Button(
            master=self.window,
            text="Add Patient",
            command=partial(
                self.add_patient,
                dob_field,
                gender_clicked,
                ethnicity_clicked,
                first_name_field,
                last_name_field,
            ),
            height=3,
        )
        add_patient_btn.pack()

        self.generate_return()

    def add_patient(self, dob, gender, ethnicity, first_name, last_name):
        dob = dob.get_date()
        gender = gender.get()
        ethnicity = ethnicity.get().strip()
        name = (
            first_name.get("1.0", "end-1c").strip()
            + " "
            + last_name.get("1.0", "end-1c").strip()
        )
        self.cursor.execute("SELECT MAX(patient_id) FROM patient")
        patient_id = self.cursor.fetchall()[0][0] + 1

        sql = f"INSERT INTO patient VALUES ({patient_id}, {dob}, '{gender[0]}', '{ethnicity}', '{name}')"
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()

        for widget in self.window.winfo_children():
            widget.destroy()

        self.prev_page = self.curr_page
        self.curr_page = "Patient Added Form"
        self.generate_header()

        visit_added_field = tk.Label(
            master=self.window,
            text=f"Patient added with Patient ID of {patient_id}",
            height=3,
        )
        visit_added_field.pack()

        self.generate_return()

    def add_visit_form(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.prev_page = self.curr_page
        self.curr_page = "Add Visit Form"
        self.generate_header()

        patient_id_frame = tk.Frame(master=self.window)

        patient_id_field = tk.Label(
            master=patient_id_frame,
            text="Please select a Patient ID from the dropdown: ",
            height=3,
        )
        patient_id_field.grid(row=0, column=0)

        visit_opts = self.get_patients_table()

        patient_clicked = tk.IntVar(master=patient_id_frame)
        patient_clicked.set(visit_opts[0])

        drop = tk.OptionMenu(patient_id_frame, patient_clicked, *visit_opts)
        drop.grid(row=0, column=1)

        patient_id_frame.pack()

        hospital_id_frame = tk.Frame(master=self.window)

        hospital_id_field = tk.Label(
            master=hospital_id_frame,
            text="Please select a Hospital ID from the dropdown: ",
            height=3,
        )
        hospital_id_field.grid(row=0, column=0)

        hosp_opts = self.get_hospital_table()

        hospital_clicked = tk.IntVar(master=hospital_id_frame)
        hospital_clicked.set(hosp_opts[0])

        drop = tk.OptionMenu(hospital_id_frame, hospital_clicked, *hosp_opts)
        drop.grid(row=0, column=1)

        hospital_id_frame.pack()

        start_dt_frame = tk.Frame(master=self.window)

        start_dt_field = tk.Label(
            master=start_dt_frame,
            text="Please select a start date: ",
            height=3,
        )
        start_dt_field.grid(row=0, column=0)

        start_dt_field = Calendar(
            start_dt_frame, selectmode="day", year=2020, month=5, day=22
        )
        start_dt_field.grid(row=0, column=1)

        start_dt_frame.pack()

        end_dt_frame = tk.Frame(master=self.window)

        end_dt_field = tk.Label(
            master=end_dt_frame,
            text="Please select a end date: ",
            height=3,
        )
        end_dt_field.grid(row=0, column=0)

        end_dt_field = Calendar(
            end_dt_frame, selectmode="day", year=2020, month=5, day=22
        )
        end_dt_field.grid(row=0, column=1)

        end_dt_frame.pack()

        add_visit_btn = tk.Button(
            master=self.window,
            text="Add Visit",
            command=partial(
                self.add_visit,
                patient_clicked,
                hospital_clicked,
                start_dt_field,
                end_dt_field,
            ),
            height=3,
        )
        add_visit_btn.pack()

        self.generate_return()

    def add_visit(self, patient_id, hospital_id, start_dt, end_dt):
        patient_id = patient_id.get()
        hospital_id = hospital_id.get()
        start_dt = start_dt.get_date()
        end_dt = end_dt.get_date()

        self.cursor.execute("SELECT MAX(visit_id) FROM visit")
        visit_id = self.cursor.fetchall()[0][0] + 1

        sql = f"INSERT INTO visit VALUES ({visit_id}, {patient_id}, {hospital_id}, {start_dt}, {end_dt})"

        self.cursor.execute(sql)
        self.conn.commit()

        for widget in self.window.winfo_children():
            widget.destroy()

        self.prev_page = self.curr_page
        self.curr_page = "Visit Added Form"
        self.generate_header()

        visit_added_field = tk.Label(
            master=self.window,
            text=f"Visit added with Visit ID of {visit_id}",
            height=3,
        )
        visit_added_field.pack()

        self.generate_return()

    def add_provider_form(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.prev_page = self.curr_page
        self.curr_page = "Add Provider Form"
        self.generate_header()

        name_frame = tk.Frame(master=self.window)

        name_field = tk.Label(
            master=name_frame,
            text="Please enter a First and Last name: ",
            height=3,
        )
        name_field.grid(row=0, column=0)

        first_name_field = tk.Text(name_frame, height=1, width=15)
        first_name_field.grid(row=0, column=1)

        last_name_field = tk.Text(name_frame, height=1, width=15)
        last_name_field.grid(row=0, column=2)

        name_frame.pack()

        gender_frame = tk.Frame(master=self.window)

        gender_field = tk.Label(
            master=gender_frame,
            text="Please select a gender from the dropdown: ",
            height=3,
        )
        gender_field.grid(row=0, column=0)

        gender_clicked = tk.StringVar(master=gender_frame)
        gender_clicked.set("Female")

        gender_drop = tk.OptionMenu(gender_frame, gender_clicked, *["Male", "Female"])
        gender_drop.grid(row=0, column=1)

        gender_frame.pack()

        specialty_frame = tk.Frame(master=self.window)

        specialty_field = tk.Label(
            master=specialty_frame,
            text="Please select a specialty from the dropdown: ",
            height=3,
        )
        specialty_field.grid(row=0, column=0)

        specialty_opts = self.get_specialty()

        specialty_clicked = tk.StringVar(master=specialty_frame)
        specialty_clicked.set(specialty_opts[0])

        specialty_drop = tk.OptionMenu(
            specialty_frame, specialty_clicked, *specialty_opts
        )
        specialty_drop.grid(row=0, column=1)

        specialty_frame.pack()

        dob_frame = tk.Frame(master=self.window)

        dob_field = tk.Label(
            master=dob_frame,
            text="Please select a Date of Birth: ",
            height=3,
        )
        dob_field.grid(row=0, column=0)

        dob_field = Calendar(dob_frame, selectmode="day", year=2020, month=5, day=22)
        dob_field.grid(row=0, column=1)

        dob_frame.pack()

        add_patient_btn = tk.Button(
            master=self.window,
            text="Add Doctor",
            command=partial(
                self.add_doctor,
                first_name_field,
                last_name_field,
                gender_clicked,
                specialty_clicked,
                dob_field,
            ),
            height=3,
        )
        add_patient_btn.pack()

        self.generate_return()

    def add_doctor(
        self, first_name, last_name, gender_field, specialty_field, dob_field
    ):
        first_name = first_name.get("1.0", "end-1c").strip()
        last_name = last_name.get("1.0", "end-1c").strip()
        gender_field = gender_field.get()
        specialty_field = specialty_field.get()
        dob_field = dob_field.get_date()

        name = first_name + " " + last_name

        self.cursor.execute("SELECT MAX(provider_id) FROM doctor")
        provider_id = self.cursor.fetchall()[0][0] + 1

        sql = f"INSERT INTO doctor VALUES ({provider_id}, '{name}', '{gender_field[0]}', '{specialty_field}', {dob_field})"

        self.cursor.execute(sql)
        self.conn.commit()

        for widget in self.window.winfo_children():
            widget.destroy()

        self.prev_page = self.curr_page
        self.curr_page = "Doctor Added Form"
        self.generate_header()

        visit_added_field = tk.Label(
            master=self.window,
            text=f"Doctor added with Provider ID of {provider_id}",
            height=3,
        )
        visit_added_field.pack()

        self.generate_return()

    def add_hospital_form(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.prev_page = self.curr_page
        self.curr_page = "Add Hospital Form"
        self.generate_header()

        address_frame = tk.Frame(master=self.window)

        address_field = tk.Label(
            master=address_frame,
            text="Please enter the street address: ",
            height=3,
        )
        address_field.grid(row=0, column=0)

        address_field = tk.Text(address_frame, height=1, width=15)
        address_field.grid(row=0, column=1)

        address_frame.pack()

        name_frame = tk.Frame(master=self.window)

        name_field = tk.Label(
            master=name_frame,
            text="Please enter the name: ",
            height=3,
        )
        name_field.grid(row=0, column=0)

        name_field = tk.Text(name_frame, height=1, width=15)
        name_field.grid(row=0, column=1)

        name_frame.pack()

        zip_frame = tk.Frame(master=self.window)

        zip_field = tk.Label(
            master=zip_frame,
            text="Please enter the ZIP Code: ",
            height=3,
        )
        zip_field.grid(row=0, column=0)

        zip_field = tk.Spinbox(zip_frame, from_=10000, to=99999)
        zip_field.grid(row=0, column=1)

        zip_frame.pack()

        county_frame = tk.Frame(master=self.window)

        county_field = tk.Label(
            master=county_frame,
            text="Please enter the county: ",
            height=3,
        )
        county_field.grid(row=0, column=0)

        county_field = tk.Text(county_frame, height=1, width=15)
        county_field.grid(row=0, column=1)

        county_frame.pack()

        city_frame = tk.Frame(master=self.window)

        city_field = tk.Label(
            master=city_frame,
            text="Please enter the city: ",
            height=3,
        )
        city_field.grid(row=0, column=0)

        city_field = tk.Text(city_frame, height=1, width=15)
        city_field.grid(row=0, column=1)

        city_frame.pack()

        capacity_frame = tk.Frame(master=self.window)

        capacity_field = tk.Label(
            master=capacity_frame,
            text="Please enter the capacity: ",
            height=3,
        )
        capacity_field.grid(row=0, column=0)

        capacity_field = tk.Spinbox(capacity_frame, from_=1, to=999999)
        capacity_field.grid(row=0, column=1)

        capacity_frame.pack()

        add_patient_btn = tk.Button(
            master=self.window,
            text="Add Hospital",
            command=partial(
                self.add_hospital,
                address_field,
                name_field,
                zip_field,
                county_field,
                city_field,
                capacity_field,
            ),
            height=3,
        )
        add_patient_btn.pack()

        self.generate_return()

    def add_hospital(self, address, name, zip_code, county, city, capacity):
        address = address.get("1.0", "end-1c").strip()
        name = name.get("1.0", "end-1c").strip()
        zip_code = zip_code.get()
        county = county.get("1.0", "end-1c").strip()
        city = city.get("1.0", "end-1c").strip()
        capacity = capacity.get()

        self.cursor.execute("SELECT MAX(hospital_id) FROM hospital")
        hospital_id = self.cursor.fetchall()[0][0] + 1

        sql = f"INSERT INTO hospital VALUES ({hospital_id}, '{address}', '{name}', '{zip_code}', '{county}', '{city}', '{capacity}')"

        self.cursor.execute(sql)
        self.conn.commit()

        for widget in self.window.winfo_children():
            widget.destroy()

        self.prev_page = self.curr_page
        self.curr_page = "Hospital Added Form"
        self.generate_header()

        visit_added_field = tk.Label(
            master=self.window,
            text=f"Hospital added with Hospital ID of {hospital_id}",
            height=3,
        )
        visit_added_field.pack()

        self.generate_return()

    def add_condition_form(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.prev_page = self.curr_page
        self.curr_page = "Add Condition Form"
        self.generate_header()

        name_frame = tk.Frame(master=self.window)

        name_field = tk.Label(
            master=name_frame,
            text="Please select a condition name from the dropdown: ",
            height=3,
        )
        name_field.grid(row=0, column=0)

        name_opts = self.get_condition_name_table()

        name_clicked = tk.StringVar(master=name_frame)
        name_clicked.set(name_opts[0])

        name_drop = tk.OptionMenu(name_frame, name_clicked, *name_opts)
        name_drop.grid(row=0, column=1)

        name_frame.pack()

        start_dt_frame = tk.Frame(master=self.window)

        start_dt_field = tk.Label(
            master=start_dt_frame,
            text="Please select a start date: ",
            height=3,
        )
        start_dt_field.grid(row=0, column=0)

        start_dt_field = Calendar(
            start_dt_frame, selectmode="day", year=2020, month=5, day=22
        )
        start_dt_field.grid(row=0, column=1)

        start_dt_frame.pack()

        end_dt_frame = tk.Frame(master=self.window)

        end_dt_field = tk.Label(
            master=end_dt_frame,
            text="Please select a end date: ",
            height=3,
        )
        end_dt_field.grid(row=0, column=0)

        end_dt_field = Calendar(
            end_dt_frame, selectmode="day", year=2020, month=5, day=22
        )
        end_dt_field.grid(row=0, column=1)

        end_dt_frame.pack()

        stop_reason_frame = tk.Frame(master=self.window)

        stop_reason_field = tk.Label(
            master=stop_reason_frame,
            text="Please select a stop reason from the dropdown: ",
            height=3,
        )
        stop_reason_field.grid(row=0, column=0)

        stop_reason_opts = ["Treated", "Recovered"]

        stop_reason_clicked = tk.StringVar(master=stop_reason_frame)
        stop_reason_clicked.set(stop_reason_opts[0])

        stop_reason_drop = tk.OptionMenu(
            stop_reason_frame, stop_reason_clicked, *stop_reason_opts
        )
        stop_reason_drop.grid(row=0, column=1)

        stop_reason_frame.pack()

        visit_id_frame = tk.Frame(master=self.window)

        visit_id_field = tk.Label(
            master=visit_id_frame,
            text="Please select a Visit ID from the dropdown: ",
            height=3,
        )
        visit_id_field.grid(row=0, column=0)

        visit_id_opts = self.get_visit_table()

        visit_id_clicked = tk.IntVar(master=visit_id_frame)
        visit_id_clicked.set(visit_id_opts[0])

        visit_id_drop = tk.OptionMenu(visit_id_frame, visit_id_clicked, *visit_id_opts)
        visit_id_drop.grid(row=0, column=1)

        visit_id_frame.pack()

        clinician_id_frame = tk.Frame(master=self.window)

        clinician_id_field = tk.Label(
            master=clinician_id_frame,
            text="Please select a Provider ID from the dropdown: ",
            height=3,
        )
        clinician_id_field.grid(row=0, column=0)

        clinician_id_opts = self.get_provider_table()

        clinician_id_clicked = tk.IntVar(master=clinician_id_frame)
        clinician_id_clicked.set(clinician_id_opts[0])

        clinician_id_drop = tk.OptionMenu(
            clinician_id_frame, clinician_id_clicked, *clinician_id_opts
        )
        clinician_id_drop.grid(row=0, column=1)

        clinician_id_frame.pack()

        patient_id_frame = tk.Frame(master=self.window)

        patient_id_field = tk.Label(
            master=patient_id_frame,
            text="Please select a Patient ID from the dropdown: ",
            height=3,
        )
        patient_id_field.grid(row=0, column=0)

        patient_id_opts = self.get_patients_table()

        patient_id_clicked = tk.IntVar(master=patient_id_frame)
        patient_id_clicked.set(patient_id_opts[0])

        patient_id_drop = tk.OptionMenu(
            patient_id_frame, patient_id_clicked, *patient_id_opts
        )
        patient_id_drop.grid(row=0, column=1)

        patient_id_frame.pack()

        add_patient_btn = tk.Button(
            master=self.window,
            text="Add Condition",
            command=partial(
                self.add_condition,
                name_clicked,
                start_dt_field,
                end_dt_field,
                stop_reason_clicked,
                visit_id_clicked,
                clinician_id_clicked,
                patient_id_clicked,
            ),
            height=3,
        )
        add_patient_btn.pack()

        self.generate_return()

    def add_condition(
        self, name, start_dt, end_dt, stop_reason, visit_id, provider_id, patient_id
    ):
        name = name.get()
        start_dt = start_dt.get_date()
        end_dt = end_dt.get_date()
        stop_reason = stop_reason.get()
        visit_id = visit_id.get()
        provider_id = provider_id.get()
        patient_id = patient_id.get()

        self.cursor.execute("SELECT MAX(condition_id) FROM condition")
        condition_id = self.cursor.fetchall()[0][0]
        condition_id = condition_id[0] + str(int(condition_id[1:]) + 1)

        sql = f"INSERT INTO condition VALUES ('{condition_id}', '{name}', '{start_dt}', '{end_dt}', '{stop_reason}', {visit_id})"

        self.cursor.execute(sql)
        self.conn.commit()

        sql = f"INSERT INTO diagnosed_for VALUES ({patient_id}, '{condition_id}')"

        self.cursor.execute(sql)
        self.conn.commit()

        sql = f"INSERT INTO diagnosed_by VALUES ({provider_id}, '{condition_id}')"

        self.cursor.execute(sql)
        self.conn.commit()

        for widget in self.window.winfo_children():
            widget.destroy()

        self.prev_page = self.curr_page
        self.curr_page = "Condition Added Form"
        self.generate_header()

        visit_added_field = tk.Label(
            master=self.window,
            text=f"Condition added with Condition ID of {condition_id}",
            height=3,
        )
        visit_added_field.pack()

        self.generate_return()

    def add_measurement_form(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.prev_page = self.curr_page
        self.curr_page = "Add Measurement Form"
        self.generate_header()

        measurement_dt_frame = tk.Frame(master=self.window)

        measurement_dt_field = tk.Label(
            master=measurement_dt_frame,
            text="Please select a Datetime: ",
            height=3,
        )
        measurement_dt_field.grid(row=0, column=0)

        measurement_dt_field = Calendar(
            measurement_dt_frame, selectmode="day", year=2020, month=5, day=22
        )
        measurement_dt_field.grid(row=0, column=1)

        measurement_dt_frame.pack()

        value_as_number_frame = tk.Frame(master=self.window)

        value_as_number_field = tk.Label(
            master=value_as_number_frame,
            text="Please enter the measurement value: ",
            height=3,
        )
        value_as_number_field.grid(row=0, column=0)

        value_as_number_field = tk.Spinbox(
            value_as_number_frame, from_=-500, to=50000, increment=0.01
        )
        value_as_number_field.grid(row=0, column=1)

        value_as_number_frame.pack()

        unit_frame = tk.Frame(master=self.window)

        unit_field = tk.Label(
            master=unit_frame,
            text="Please select a unit from the dropdown: ",
            height=3,
        )
        unit_field.grid(row=0, column=0)

        unit_opts = self.get_unit_table()

        unit_clicked = tk.StringVar(master=unit_frame)
        unit_clicked.set(unit_opts[0])

        unit_drop = tk.OptionMenu(unit_frame, unit_clicked, *unit_opts)
        unit_drop.grid(row=0, column=1)

        unit_frame.pack()

        name_frame = tk.Frame(master=self.window)

        name_field = tk.Label(
            master=name_frame,
            text="Please select a measurement name from the dropdown: ",
            height=3,
        )
        name_field.grid(row=0, column=0)

        name_opts = self.get_measurement_name_table()

        name_clicked = tk.StringVar(master=name_frame)
        name_clicked.set(name_opts[0])

        name_drop = tk.OptionMenu(name_frame, name_clicked, *name_opts)
        name_drop.grid(row=0, column=1)

        name_frame.pack()

        visit_id_frame = tk.Frame(master=self.window)

        visit_id_field = tk.Label(
            master=visit_id_frame,
            text="Please select a Visit ID from the dropdown: ",
            height=3,
        )
        visit_id_field.grid(row=0, column=0)

        visit_id_opts = self.get_visit_table()

        visit_id_clicked = tk.IntVar(master=visit_id_frame)
        visit_id_clicked.set(visit_id_opts[0])

        visit_id_drop = tk.OptionMenu(visit_id_frame, visit_id_clicked, *visit_id_opts)
        visit_id_drop.grid(row=0, column=1)

        visit_id_frame.pack()

        clinician_id_frame = tk.Frame(master=self.window)

        clinician_id_field = tk.Label(
            master=clinician_id_frame,
            text="Please select a Provider ID from the dropdown: ",
            height=3,
        )
        clinician_id_field.grid(row=0, column=0)

        clinician_id_opts = self.get_provider_table()

        clinician_id_clicked = tk.IntVar(master=clinician_id_frame)
        clinician_id_clicked.set(clinician_id_opts[0])

        clinician_id_drop = tk.OptionMenu(
            clinician_id_frame, clinician_id_clicked, *clinician_id_opts
        )
        clinician_id_drop.grid(row=0, column=1)

        clinician_id_frame.pack()

        patient_id_frame = tk.Frame(master=self.window)

        patient_id_field = tk.Label(
            master=patient_id_frame,
            text="Please select a Patient ID from the dropdown: ",
            height=3,
        )
        patient_id_field.grid(row=0, column=0)

        patient_id_opts = self.get_patients_table()

        patient_id_clicked = tk.IntVar(master=patient_id_frame)
        patient_id_clicked.set(patient_id_opts[0])

        patient_id_drop = tk.OptionMenu(
            patient_id_frame, patient_id_clicked, *patient_id_opts
        )
        patient_id_drop.grid(row=0, column=1)

        patient_id_frame.pack()

        add_measurement_btn = tk.Button(
            master=self.window,
            text="Add Measurement",
            command=partial(
                self.add_measurement,
                measurement_dt_field,
                value_as_number_field,
                unit_clicked,
                name_clicked,
                visit_id_clicked,
                clinician_id_clicked,
                patient_id_clicked,
            ),
            height=3,
        )
        add_measurement_btn.pack()

        self.generate_return()

    def add_measurement(
        self,
        measurement_dt,
        value_as_number,
        unit,
        name,
        visit_id,
        provider_id,
        patient_id,
    ):
        measurement_dt = measurement_dt.get_date()
        value_as_number = value_as_number.get()
        unit = unit.get()
        name = name.get()
        visit_id = visit_id.get()
        provider_id = provider_id.get()
        patient_id = patient_id.get()

        self.cursor.execute("SELECT MAX(measurement_id) FROM measurement")
        measurement_id = self.cursor.fetchall()[0][0] + 1

        sql = f"INSERT INTO measurement VALUES ({measurement_id}, {measurement_dt}, {value_as_number}, '{unit}', '{name}', {visit_id})"

        self.cursor.execute(sql)
        self.conn.commit()

        sql = f"INSERT INTO measured_on VALUES ({patient_id}, '{measurement_id}')"

        self.cursor.execute(sql)
        self.conn.commit()

        sql = f"INSERT INTO performed_by VALUES ({provider_id}, '{measurement_id}')"

        self.cursor.execute(sql)
        self.conn.commit()

        for widget in self.window.winfo_children():
            widget.destroy()

        self.prev_page = self.curr_page
        self.curr_page = "Measurement Added Form"
        self.generate_header()

        measurement_added_field = tk.Label(
            master=self.window,
            text=f"Measurement added with Measurement ID of {measurement_id}",
            height=3,
        )
        measurement_added_field.pack()

        self.generate_return()

    def generate_header(self):
        frame_title = tk.Frame(master=self.window)
        label = tk.Label(master=frame_title, text=self.curr_page, height=3)
        label.pack()
        frame_title.pack()

    def generate_return(self):
        frame_return = tk.Frame(master=self.window)
        return_btn = tk.Button(
            master=frame_return,
            text="Quit",
            command=self.main_window,
            height=3,
        )
        return_btn.pack()
        frame_return.pack()

    def get_patients_table(self):
        sql = "SELECT patient_id FROM patient;"
        self.cursor.execute(sql)
        table = self.cursor.fetchall()
        table = [row[0] for row in table]
        return table

    def get_patient_info_table(self, patient_id):
        sql = f"""
            SELECT 
                patient.patient_id,
                patient.dob,
                patient.gender,
                patient.ethnicity,
                patient.name,
                visit.visit_id,
                visit.start_datetime,
                visit.end_datetime
            FROM patient 
            LEFT JOIN visit
            ON patient.patient_id = visit.patient_id
            WHERE patient.patient_id = {patient_id}
            """
        self.cursor.execute(sql)
        table = self.cursor.fetchall()
        return table

    def get_hospital_table(self):
        sql = "SELECT hospital_id FROM hospital;"
        self.cursor.execute(sql)
        table = self.cursor.fetchall()
        table = [row[0] for row in table]
        return table

    def get_hospital_info_table(self, hospital_id):
        sql = f"""
            SELECT 
                *
            FROM hospital
            WHERE hospital_id = {hospital_id}
            """
        self.cursor.execute(sql)
        table = self.cursor.fetchall()
        return table

    def get_provider_table(self):
        sql = "SELECT provider_id FROM doctor;"
        self.cursor.execute(sql)
        table = self.cursor.fetchall()
        table = [row[0] for row in table]
        return table

    def get_provider_info_table(self, provider_id):
        sql = f"""
            SELECT 
                *
            FROM doctor
            WHERE provider_id = {provider_id}
            """
        self.cursor.execute(sql)
        table = self.cursor.fetchall()
        return table

    def get_visit_table(self):
        sql = "SELECT visit_id FROM visit;"
        self.cursor.execute(sql)
        table = self.cursor.fetchall()
        table = [row[0] for row in table]
        return table

    def get_visit_info_table(self, visit_id):
        sql = f"""
            SELECT 
                *
            FROM visit
            WHERE visit_id = {visit_id}
            """
        self.cursor.execute(sql)
        table = self.cursor.fetchall()
        return table

    def get_measurement_table(self):
        sql = "SELECT DISTINCT name FROM measurement;"
        self.cursor.execute(sql)
        table = self.cursor.fetchall()
        table = [row[0] for row in table]
        return table

    def get_measurement_info_table(self, visit_id, measurement_name):
        sql = f"""
            SELECT 
                measurement.measurement_id,
                measurement.name,
                measurement.measurement_datetime,
                measurement.unit,
                measurement.value_as_number,
                performed_by.provider_id,
                measured_on.patient_id
            FROM measurement, measured_on, performed_by
            WHERE measurement.measurement_id = measured_on.measurement_id
            AND measurement.measurement_id = performed_by.measurement_id
            AND measurement.visit_id = {visit_id}
            AND measurement.name = '{measurement_name}'
            AND nullif(measurement.value_as_number, 'NaN') IS NOT NULL
            """
        self.cursor.execute(sql)
        table = self.cursor.fetchall()
        return table

    def get_condition_info_table(self, visit_id):
        sql = f"""
            SELECT 
                condition.condition_id,
                condition.name,
                condition.start_datetime,
                condition.end_datetime,
                condition.stop_reason,
                diagnosed_for.patient_id,
                diagnosed_by.provider_id
            FROM condition,  diagnosed_for, diagnosed_by
            WHERE condition.visit_id = {visit_id}
            AND condition.condition_id = diagnosed_for.condition_id
            AND condition.condition_id = diagnosed_by.condition_id
            """
        self.cursor.execute(sql)
        table = self.cursor.fetchall()

        return table

    def get_ethnicities(self):
        sql = f"""
            SELECT 
                DISTINCT ethnicity
            FROM patient
            """
        self.cursor.execute(sql)
        table = self.cursor.fetchall()

        return [t[0] for t in table]

    def get_specialty(self):
        sql = f"""
            SELECT 
                DISTINCT specialty
            FROM doctor
            """
        self.cursor.execute(sql)
        table = self.cursor.fetchall()

        return [t[0] for t in table]

    def get_condition_name_table(self):
        sql = f"""
            SELECT 
                DISTINCT name
            FROM condition
            """
        self.cursor.execute(sql)
        table = self.cursor.fetchall()

        return [t[0] for t in table]

    def get_unit_table(self):
        sql = f"""
            SELECT 
                DISTINCT unit
            FROM measurement
            """
        self.cursor.execute(sql)
        table = self.cursor.fetchall()

        return [t[0] for t in table]

    def get_measurement_name_table(self):
        sql = f"""
            SELECT 
                DISTINCT name
            FROM measurement
            """
        self.cursor.execute(sql)
        table = self.cursor.fetchall()

        return [t[0] for t in table]


GUI()
