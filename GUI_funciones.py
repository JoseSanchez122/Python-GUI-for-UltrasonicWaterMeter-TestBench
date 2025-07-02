import serial
import time
import glob
from Quectel_test_func import Diagnosticar_Quectel_2
from LCD_test_func import LCD_Electrical_Test_lib
from Current_Test_lib import Current_Test_with_Plot, Current_Test_Only
from USS_Test_lib import USS_test_func
from Voltage_Test_lib import voltage_test_func
from Reports_lib import Create_report_func

def where_is_ESP32():
    posibles_puertos = glob.glob('/dev/ttyUSB*')  # Busca dispositivos USB en /dev/
    
    if posibles_puertos:
        return posibles_puertos[0]  # Devuelve el primer puerto encontrado
    else:
        return "/dev/ttyUSB999"

class BoardTester:
    Test_Status = {"Quectel test": {"WAS DONE?": False, "DID IT WORK?": False},
                   "LCD electrical test": {"WAS DONE?": False, "DID IT WORK?": False},
                   "Current test": {"WAS DONE?": False, "DID IT WORK?": False},
                   "USS test":  {"WAS DONE?": False, "DID IT WORK?": False},
                   "Voltage test":  {"WAS DONE?": False, "DID IT WORK?": False}}
    
    quectel_answers = []
    LCD_tests_answers = []
    Current_tests_answers = []
    USS_tests_answers = []
    Voltage_tests_answers = []
    num_tablillas = 0
    Grafica = None

    def delay(self, ms):
        time.sleep(ms/1000)

#-------------------------------CONSTRUCTOR-----------------------------------#
    def __init__(self, port=None, 
                 baudrate=115200, 
                 text_widget=None, 
                 serial_number=None, 
                 LCD_image=None, 
                 pins_correct=None, 
                 pins_wrong =None,
                 pins_posi=None,
                 terminal_=None,
                 _resize_size=None):
        
        self.text_in_terminal = text_widget
        self.text_in_terminal.configure(text_color="black")
        self.serial_number = serial_number
        self.Screen_img = LCD_image
        self.pins_correct_marks = pins_correct
        self.pins_wrong_marks = pins_wrong
        self.pins_pos = pins_posi
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.terminal = terminal_
        self.port = where_is_ESP32()
        self.resize_size = _resize_size

#-------------------------------Funcione para generar reportes-----------------------------------#
    def Create_report(self, was_test_ended=False):
        self.remove_graph()
        Create_report_func(self, was_test_ended)

#-------------------------------Funciones de UART-----------------------------------#

    def is_serial_port_working(self):
        self.port = where_is_ESP32()
        try:       
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
            )
        except serial.SerialException as e:
            self.ser = None
            self.was_ser_created = False
            return False
        if self.ser and self.ser.is_open:
            self.was_ser_created = True
            return True
        else:
            self.was_ser_created = False
            return False
        
    def READ_UART(self):
        if self.ser and self.ser.is_open:
            return self.ser.readline().decode().replace("\r", "").replace("\n", "")
        return None

    def clear_input_buffer(self):
        self.ser.reset_input_buffer()

    def close_ser(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Puerto serial cerrado correctamente.")

#-------------------------------Funciones de TERMINAL-----------------------------------#
    def print_in_terminal(self, msg):
        if self.text_in_terminal:
            self.text_in_terminal.insert("end", msg)
            self.text_in_terminal.see("end")
        else:
            print(msg)

    def clear_terminal(self):
        self.text_in_terminal.delete("1.0", "end")

    def remove_graph(self):
        if self.Grafica:  # Verifica si existe una gráfica
            self.Grafica.get_tk_widget().destroy()  # Elimina el gráfico del terminal
            self.Grafica = None

#-------------------------------Funcion de QUECTEL-----------------------------------#
    def Diagnosticar_Quectel(self):
        if self.is_serial_port_working():
            self.remove_graph()
            Diagnosticar_Quectel_2(self)
        else:
            self.print_in_terminal("Error: El ESP32 no se conecto.\n")
            return

#-------------------------------Funcion de Preba voltages-----------------------------------#
    def Voltage_Test(self):
        if self.is_serial_port_working():
            self.remove_graph()
            voltage_test_func(self)
        else:
            self.print_in_terminal("Error: El ESP32 no se conecto.\n")
            return 

#-------------------------------Funcion de Preba corrientes-----------------------------------#
    def Current_Test_plot(self):
        if self.is_serial_port_working():
            self.remove_graph()
            Current_Test_with_Plot(self)
        else:
            self.print_in_terminal("Error: El ESP32 no se conecto.\n")
            return
        
    def Current_Test_only(self):
        if self.is_serial_port_working():
            self.remove_graph()
            Current_Test_Only(self)
        else:
            self.print_in_terminal("Error: El ESP32 no se conecto.\n")
            return

#-------------------------------Funcion de Preba LCD-----------------------------------#
    def LCD_Electrical_Test(self, show_image):
        if show_image:
            self.Screen_img.place(x=self.resize(22), y=self.resize(150))
            self.text_in_terminal.configure(height=self.resize(130))
        if self.is_serial_port_working():
            self.remove_graph()
            LCD_Electrical_Test_lib(self, show_image)
        else:
            self.print_in_terminal("Error: El ESP32 no se conecto.\n")
            return
    
#-------------------------------Funcion de Preba ULSTRASONICA-----------------------------------#
    def USS_Test(self):
        if self.is_serial_port_working():
            self.remove_graph()
            USS_test_func(self)
        else:
            self.print_in_terminal("Error: El ESP32 no se conecto.\n")
            return
        
#-------------------------------Funcion de redimension-----------------------------------#
    def resize(self, size):
        return int(size*self.resize_size)
        