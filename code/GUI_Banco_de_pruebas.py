import customtkinter as ctk
from GUI_funciones import BoardTester
import threading
from PIL import Image, ImageTk

app = ctk.CTk()
app.title("Banco de pruebas MAU")
app.geometry("865x520")
app.configure(fg_color="gray")
app.resizable(False, False)

#-------------------------------TITULO------------------------------------#

main_frame = ctk.CTkFrame(app, fg_color="gray") 
main_frame.pack(fill="both", expand=True)

titulo_diagnostico_quectel = ctk.CTkLabel(
        main_frame,
        text = "Banco de pruebas MAU",
        text_color = "white",
        font = ("Arial", 25, "bold"),
    )

titulo_diagnostico_quectel.place(x=300, y=25)

#-------------------------------ENTRADA DE NUMERO DE SERIE------------------------------------#

serial_number_var = ctk.StringVar(value="123happy")

Serial_number_input = ctk.CTkEntry(
        app, 
        width=230, 
        height=50, 
        fg_color="white",
        text_color="black",
        border_color="black",
        border_width = 4,
        corner_radius = 10,
        font=("Consolas", 20, "bold"),
        placeholder_text="num. de serie",
        textvariable=serial_number_var
    )

Serial_number_input.place(x=30, y=105)
app.after(100, Serial_number_input.focus_set)

#-------------------------------INFORMATION TERMINAL------------------------------------#

terminal = ctk.CTkFrame(
        main_frame,
        width = 530,
        height = 410,
        corner_radius = 10,
        fg_color = "white",
        border_color = "black",
        border_width = 6
    )

terminal.place(x=300, y=80)

text_in_terminal = ctk.CTkTextbox(
    terminal,
    width=500,
    height=390,
    corner_radius=10,
    font=("Consolas", 20, "bold"),   # Tamaño de letra grande
    fg_color="white",
    text_color="black",  # Color del texto
    wrap="none",
    state="normal"
)

text_in_terminal.bind("<Key>", lambda e: "break")
text_in_terminal.place(x=10, y=6)

#---------------------------------SCREEN------------------------------------#

Screen = ctk.CTkImage(light_image=Image.open("Screen_img/Screen.PNG"), size=(475, 235))
Screen_img = ctk.CTkLabel(
    terminal, 
    image=Screen, 
    text=""
)

up = 0
down = 222

pins_pos = {"P6.4": (33.66, down), "P6.0": (33.66, up), "P6.5": (44.5, down), "P5.7": (44.5, up), 
            "P6.6": (56, down), "P5.6": (56, up), "P6.7": (67, down), "P5.5": (67, up),
            "P7.0": (78, down), "P5.4": (78, up), "P7.1": (89, down), "P5.3": (89, up),
            "P7.2": (100.5, down), "P5.2": (100.5, up), "P7.3": (112, down), "P5.1": (112, up),
            "P3.0": (122.5, down), "P5.0": (122.5, up), "P3.1": (133.7, down), "P4.7": (133.7, up),
            "P3.2": (145.5, down),  "P4.6": (145.5, up), "P3.3": (156.5, down), "P4.5": (156.5, up),
            "P3.4": (167.5, down), "P4.4": (167.5, up), "P3.5": (178.5, down), "P4.3": (178.5, up),
            "P3.6": (189.5, down), "P4.2": (189.5, up), "P3.7": (200.5, down), "P4.1": (200.5, up),
            "P2.7": (211.5, down), "P4.0": (211.5, up), "P9.0": (222.5, down), "P9.3": (222.5, up),
            "P9.1": (234, up), "P9.2": (245, up),}

pins_correct_marks = {}
pins_wrong_marks = {}

green_square = ctk.CTkImage(light_image=Image.open("Screen_img/correct_color.PNG"), size=(8, 12))
red_square = ctk.CTkImage(light_image=Image.open("Screen_img/wrong_color.PNG"), size=(8, 12))

for pin, (x, y) in pins_pos.items():
    correct_mark = ctk.CTkLabel(
        Screen_img, 
        image=green_square, 
        text="",
        fg_color="transparent",
        width=5,
        height=1
    )
    pins_correct_marks[pin] = correct_mark  

for pin, (x, y) in pins_pos.items():
    wrong_mark = ctk.CTkLabel(
        Screen_img, 
        image=red_square, 
        text="",
        fg_color="transparent",
        width=5,
        height=1
    )
    pins_wrong_marks[pin] = wrong_mark  

#---------------------------------funciones para manejo de terminal---------------------------------------#
tester = BoardTester(text_widget=text_in_terminal, 
                     serial_number=Serial_number_input, 
                     LCD_image=Screen_img, 
                     pins_correct=pins_correct_marks, 
                     pins_wrong=pins_wrong_marks,
                     pins_posi=pins_pos,
                     terminal_=terminal)

def clear_terminal():
    text_in_terminal.delete("1.0", "end")
    text_in_terminal.configure(height=390)
    for mark in pins_correct_marks:
        pins_correct_marks[mark].place_forget()
    for mark in pins_wrong_marks:
        pins_wrong_marks[mark].place_forget()
    Screen_img.place_forget()

def print_in_terminal(msg):
    text_in_terminal.insert("end", msg)
    text_in_terminal.see("end")

def Run_Test(test):
    dropdown_menu.configure(state="disabled")
    Run_All_Tests_Button.configure(state="disabled")
    Serial_number_input.configure(state="disabled")
    clear_terminal()
    def run_test():
        if test == "Voltage Test":
            tester.Voltage_Test()
        elif test == "Current Test only":
            tester.Current_Test_only()
        #elif test == "Current Plot":
            
        elif test == "Probar Quectel":
            tester.Diagnosticar_Quectel()
        elif test == "Prueba electrica LCD":
            tester.LCD_Electrical_Test(True)
        elif test == "Ultrasonic Test":
            tester.USS_Test()
        elif test == "Crear Reporte":
            tester.Create_report()
        dropdown_menu.configure(state="readonly")
        Run_All_Tests_Button.configure(state="normal")
        Serial_number_input.configure(state="normal")
    hilo = threading.Thread(target=run_test, daemon=True)
    hilo.start()

#---------------------------------BUTONS---------------------------------------#
stop_test = False

def Run_All_Tests():
    global stop_test
    Stop_Next_Test_Button.place(x=30, y=330)
    dropdown_menu.configure(state="disabled")
    Run_All_Tests_Button.configure(state="disabled")
    Serial_number_input.configure(state="disabled")
    clear_terminal()
    def run_test():
        global stop_test
        if not tester.is_serial_port_working():
            print_in_terminal("Error: El ESP32 no se conecto.\n")
            dropdown_menu.configure(state="readonly")
            Run_All_Tests_Button.configure(state="normal")
            Serial_number_input.configure(state="normal")
            Stop_Next_Test_Button.place_forget()
            return
        
        tester.Voltage_Test()
        print_in_terminal("\n#-------------------------------------#\n\n")
        if not stop_test:
            tester.Current_Test_only()
            print_in_terminal("\n#-------------------------------------#\n\n")
        if not stop_test:
            tester.Diagnosticar_Quectel()
            print_in_terminal("\n#-------------------------------------#\n\n")
        if not stop_test:
            tester.USS_Test() 
            print_in_terminal("\n#-------------------------------------#\n\n")
        if not stop_test:
            tester.LCD_Electrical_Test(False)
            print_in_terminal("\n\n#-------------------------------------#\n\n")
        
        if stop_test:
            tester.Create_report(True)
        else:
            tester.Create_report()
        stop_test = False
        dropdown_menu.configure(state="readonly")
        Run_All_Tests_Button.configure(state="normal")
        Serial_number_input.configure(state="normal")
        Stop_Next_Test_Button.place_forget()
    hilo = threading.Thread(target=run_test, daemon=True)
    hilo.start()

Run_All_Tests_Button = ctk.CTkButton(
    app, 
    text="Run All Tests", 
    command=Run_All_Tests,
    width=230,
    height=70, 
    corner_radius=10,
    text_color="black",
    border_color = "black", 
    border_width = 3.7,
    font=("Arial", 20, "bold")
    )

Run_All_Tests_Button.place(x=30, y=250)

def Stop_Next_Test():
    global stop_test
    stop_test = True

Stop_Next_Test_Button = ctk.CTkButton(
    app, 
    text="Stop Next Test", 
    command=Stop_Next_Test,
    width=140,
    height=50,
    corner_radius=10,
    text_color="black",
    border_color = "black",
    fg_color="orange",
    hover_color="darkorange",
    border_width = 3.5,
    font=("Arial", 16, "bold")
    )

#-----------------------------------DROP DOWN MENU---------------------------------------#
opciones = ["Voltage Test","Current Test only", "Current Plot", 
            "Probar Quectel", "Prueba electrica LCD", "Ultrasonic Test","Crear Reporte"]
            
def drop_down_menu_functios(opcion):
        if opcion == "Current Plot":
            while not tester.is_plotting_done:
                app.after(50, tester.Current_Test_plot())
        Run_Test(opcion)

dropdown_menu = ctk.CTkComboBox(
    app, 
    values=opciones, 
    command=drop_down_menu_functios,  
    width=230, 
    height=50, 
    corner_radius=10, 
    fg_color="white",
    text_color="black",
    border_color = "#2B6CB0",
    button_color="#2B6CB0",
    button_hover_color="#2B6CB0",
    border_width = 4,
    dropdown_fg_color="white",
    dropdown_text_color="black",
    dropdown_hover_color="#2B6CB0",
    font=("Arial", 17, "bold"),
    dropdown_font=("Arial", 17, "bold"),
    state="readonly"
)

dropdown_menu.set("Tests")
dropdown_menu.place(x=30, y=172)

#---------------------------------MAIN GUI LOOP---------------------------------------#

def close_app():
    tester.close_ser()
    app.destroy()

app.protocol("WM_DELETE_WINDOW", close_app)

app.mainloop()