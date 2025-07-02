import customtkinter as ctk
from GUI_funciones import BoardTester
import threading
from PIL import Image, ImageTk
import os
import sys

RESIZE_SIZE = 1.6   #en caso que la interfaz se vea muy pequeña o grande con solo aumentar o disminuir
                    #este parametro (RESIZE_SIZE) se puede aumentar o disminuir el tamaño de toda la 
                    #interfaz. 
                    #Agrandar: RESIZE_SIZE = 1.1, RESIZE_SIZE = 1.2, RESIZE_SIZE = 1.3 ... RESIZE_SIZE = n
                    #hacer pequeño: RESIZE_SIZE = 0.9, RESIZE_SIZE = 0.8, RESIZE_SIZE = 0.7 ... RESIZE_SIZE = n

def resize(size, resize_for_LCD=False):
    global RESIZE_SIZE
    if resize_for_LCD:
        return float(size*RESIZE_SIZE)
    else:
        return int(size*RESIZE_SIZE)

app = ctk.CTk()
app.title("Banco de pruebas MAU")
app.title_color = "black"
app.geometry(str(resize(865)) + "x" + str(resize(520)))
app.configure(fg_color="gray")
app.resizable(False, False)

#-------------------------------TITULO------------------------------------#

main_frame = ctk.CTkFrame(app, fg_color="gray") 
main_frame.pack(fill="both", expand=True)

titulo_diagnostico_quectel = ctk.CTkLabel(
        main_frame,
        text = "Banco de pruebas MAU",
        text_color = "black",
        font = ("Arial", resize(25), "bold")
    )

titulo_diagnostico_quectel.place(x=resize(300), y=resize(25))

#-------------------------------ENTRADA DE NUMERO DE SERIE------------------------------------#

serial_number_var = ctk.StringVar()

Serial_number_input = ctk.CTkEntry(
        app, 
        width=resize(230), 
        height=resize(50), 
        fg_color="white",
        text_color="black",
        border_color="black",
        border_width = resize(4),
        corner_radius = resize(10),
        font=("Consolas", resize(20), "bold"),
        placeholder_text="num. de serie",
        placeholder_text_color="gray",
        textvariable=serial_number_var
    )

Serial_number_input.place(x=resize(30), y=resize(105))
app.after(100, Serial_number_input.focus_set)

#-------------------------------INFORMATION TERMINAL------------------------------------#

terminal = ctk.CTkFrame(
        main_frame,
        width = resize(530),
        height = resize(410),
        corner_radius = resize(10),
        fg_color = "white",
        border_color = "black",
        border_width = resize(6)
    )

terminal.place(x=resize(300), y=resize(80))

text_in_terminal = ctk.CTkTextbox(
    terminal,
    width=resize(500),
    height=resize(390),
    corner_radius=resize(10),
    font=("Consolas", resize(20), "bold"),   # Tamaño de letra grande
    fg_color="white",
    text_color="black",  # Color del texto
    wrap="none",
    state="normal"
)

text_in_terminal.bind("<Key>", lambda e: "break")
text_in_terminal.place(x=resize(10), y=resize(6))

#---------------------------------SCREEN------------------------------------#
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

Screen = ctk.CTkImage(light_image=Image.open(resource_path("Screen.PNG")), size=(resize(475), resize(235)))
Screen_img = ctk.CTkLabel(
    terminal, 
    image=Screen, 
    text=""
)

up = 0
down = resize(222)

pins_pos = {"P6.4": (resize(33.66, resize_for_LCD=True), down), "P6.0": (resize(33.66, resize_for_LCD=True), up), "P6.5": (resize(44.5, resize_for_LCD=True),  down), "P5.7": (resize(44.5, resize_for_LCD=True),  up), 
            "P6.6": (resize(56, resize_for_LCD=True),    down), "P5.6": (resize(56, resize_for_LCD=True),    up), "P6.7": (resize(67, resize_for_LCD=True),    down), "P5.5": (resize(67, resize_for_LCD=True),    up),
            "P7.0": (resize(78, resize_for_LCD=True),    down), "P5.4": (resize(78, resize_for_LCD=True),    up), "P7.1": (resize(89, resize_for_LCD=True),    down), "P5.3": (resize(89, resize_for_LCD=True),    up),
            "P7.2": (resize(100.5, resize_for_LCD=True), down), "P5.2": (resize(100.5, resize_for_LCD=True), up), "P7.3": (resize(112, resize_for_LCD=True),   down), "P5.1": (resize(112, resize_for_LCD=True),   up),
            "P3.0": (resize(122.5, resize_for_LCD=True), down), "P5.0": (resize(122.5, resize_for_LCD=True), up), "P3.1": (resize(133.7, resize_for_LCD=True), down), "P4.7": (resize(133.7, resize_for_LCD=True), up),
            "P3.2": (resize(145.5, resize_for_LCD=True), down), "P4.6": (resize(145.5, resize_for_LCD=True), up), "P3.3": (resize(156.5, resize_for_LCD=True), down), "P4.5": (resize(156.5, resize_for_LCD=True), up),
            "P3.4": (resize(167.5, resize_for_LCD=True), down), "P4.4": (resize(167.5, resize_for_LCD=True), up), "P3.5": (resize(178.5, resize_for_LCD=True), down), "P4.3": (resize(178.5, resize_for_LCD=True), up),
            "P3.6": (resize(189.5, resize_for_LCD=True), down), "P4.2": (resize(189.5, resize_for_LCD=True), up), "P3.7": (resize(200.5, resize_for_LCD=True), down), "P4.1": (resize(200.5, resize_for_LCD=True), up),
            "P2.7": (resize(211.5, resize_for_LCD=True), down), "P4.0": (resize(211.5, resize_for_LCD=True), up), "P9.0": (resize(222.5, resize_for_LCD=True), down), "P9.3": (resize(222.5, resize_for_LCD=True), up),
            "P9.1": (resize(234, resize_for_LCD=True), up),     "P9.2": (resize(245, resize_for_LCD=True), up)}

pins_correct_marks = {}
pins_wrong_marks = {}

green_square = ctk.CTkImage(light_image=Image.open(resource_path("correct_color.PNG")), size=(resize(8), resize(12)))
red_square = ctk.CTkImage(light_image=Image.open(resource_path("wrong_color.PNG")), size=(resize(8), resize(12)))

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
                     terminal_=terminal,
                     _resize_size=RESIZE_SIZE)

def clear_terminal():
    text_in_terminal.delete("1.0", "end")
    text_in_terminal.configure(height=resize(390))
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
        elif test == "Current Test":
            tester.Current_Test_only()
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

def verify_serial_number():
        num = Serial_number_input.get()
        num += ".txt"
        if  num == ".txt":
            clear_terminal()
            print_in_terminal("Error: numero de serie no fue ingresado")
            return False
        else:
            return True
    
def Run_All_Tests():
    global stop_test
    if not verify_serial_number():
        return
    
    Stop_Next_Test_Button.place(x=resize(30), y=resize(330))
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
    width=resize(230),
    height=resize(70), 
    corner_radius=resize(10),
    text_color="black",
    border_color = "black", 
    border_width = resize(3.7),
    font=("Arial", resize(20), "bold")
    )

Run_All_Tests_Button.place(x=resize(30), y=resize(250))

def Stop_Next_Test():
    global stop_test
    stop_test = True

Stop_Next_Test_Button = ctk.CTkButton(
    app, 
    text="Stop Next Test", 
    command=Stop_Next_Test,
    width=resize(140),
    height=resize(50),
    corner_radius=resize(10),
    text_color="black",
    border_color = "black",
    fg_color="orange",
    hover_color="darkorange",
    border_width = resize(3.5),
    font=("Arial", resize(16), "bold")
    )

#-----------------------------------DROP DOWN MENU---------------------------------------#
opciones = ["Voltage Test","Current Test", "Probar Quectel", "Prueba electrica LCD",
            "Ultrasonic Test","Crear Reporte"]
            
def drop_down_menu_functios(opcion):
        Run_Test(opcion)

dropdown_menu = ctk.CTkComboBox(
    app, 
    values=opciones, 
    command=drop_down_menu_functios,  
    width=resize(230), 
    height=resize(50), 
    corner_radius=resize(10), 
    fg_color="white",
    text_color="black",
    border_color = "#2B6CB0",
    button_color="#2B6CB0",
    button_hover_color="#2B6CB0",
    border_width = resize(4),
    dropdown_fg_color="white",
    dropdown_text_color="black",
    dropdown_hover_color="#2B6CB0",
    font=("Arial", resize(17), "bold"),
    dropdown_font=("Arial", resize(17), "bold"),
    state="readonly"
)

dropdown_menu.set("Tests")
dropdown_menu.place(x=resize(30), y=resize(172))


print_in_terminal("               Bienvenido!!\n\n")
print_in_terminal(" Ingrese el número de serie y seleccione\n          la prueba a verificar\n")

#---------------------------------MAIN GUI LOOP---------------------------------------#

def close_app():
    tester.close_ser()
    app.destroy()

app.protocol("WM_DELETE_WINDOW", close_app)

app.mainloop()
