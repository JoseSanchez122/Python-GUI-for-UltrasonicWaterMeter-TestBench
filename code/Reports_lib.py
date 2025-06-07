import os
from datetime import date
from tkinter import messagebox 

day_folder_created = False

def create_folder(name):
    global day_folder_created
    if not os.path.exists(name) and day_folder_created == False:
        day_folder_created = True
        os.makedirs(name)
    else:
        return
    
def get_Date(self):
    return date.today().strftime("%d-%m-%Y")

def get_serial_number(self):
        num = self.serial_number.get()  
        return num

def file_exists_in_folder(file_name, folder_name):
    file_path = os.path.join(folder_name, file_name)
    if os.path.isfile(file_path):
        response = messagebox.askyesno("Pregunta", "Reporte con este numero de serie ya existe, ¿deseas remplazarlo con este nuevo reporte?")
        if response:  
                return True
        else:  
            return False
    return True

def reset_status(self):
    for test, status in self.Test_Status.items():
        for key in status:
            status[key] = False  # Asignar False a cada clave dentro del subdiccionario
    self.quectel_answers.clear()
    self.LCD_tests_answers.clear()
    self.Current_tests_answers.clear()
    self.USS_tests_answers.clear()
    self.Voltage_tests_answers.clear()

def verify_missing_tests(self, was_test_ended):
    tests_not_done = ""
    are_there_tests_missing = False
    keys = ["Voltage test", "Current test", "Quectel test", "USS test", "LCD electrical test"]

    for key in keys:
        if not self.Test_Status[key]["WAS DONE?"]:
            are_there_tests_missing = True
            tests_not_done += key+", "
    
    if are_there_tests_missing and was_test_ended:
        response = messagebox.askyesno("Pruebas Detenidas!!", "Las pruebas fueron Detenidas!!. " + tests_not_done + 
                                       "no fueron ejecutadas\n¿Quieres crear el reporte sin estas pruebas?")
        if response:  
            return True
        else:  
            return False
        
    if are_there_tests_missing:
        response = messagebox.askyesno("Pruebas no ejecutadas", "Las pruebas: " + tests_not_done + 
                                       "no fueron ejecutadas\n¿Quieres crear el reporte sin estas pruebas?")
        if response:  
            return True
        else:  
            return False
    return True

def Create_report_func(self, was_test_ended):
    was_a_test_donde = False
    was_not_a_test_done = False
    folder_name = get_Date(self)
    file_name = get_serial_number(self) + ".txt"
    keys = ["Voltage test", "Current test", "Quectel test", "USS test", "LCD electrical test"]

    create_folder(folder_name)
    file_path = os.path.join(folder_name, file_name)

    if  file_name == ".txt":
        self.print_in_terminal("Error: numero de serie no fue ingresado")

    if not file_exists_in_folder(file_name, folder_name):
        return

    if not verify_missing_tests(self, was_test_ended):
        return

    with open(file_path, "w") as file:
        file.write("RESULTADOS DE PRUEBAS DE TABLILLA: " + file_name[:-4] + "\n\n")
#------------------------------------Voltage report----------------------------------------# 
        file.write("#-------------------------PRUEBA DE VOLTAGES-------------------------#\n\n")
        for answer in self.Voltage_tests_answers:
            file.write(answer)
        file.write("\n")
#------------------------------------Current report----------------------------------------# 
        file.write("#-------------------------PRUEBA CONSUMO DE CORRIENTE-------------------------#\n\n") 
        for answer in self.Current_tests_answers:
            file.write(answer)
        file.write("\n")
#------------------------------------Quectel report----------------------------------------#
        file.write("#-------------------------PRUEBA QUECTEL-------------------------#\n\n")
        for answer in self.quectel_answers:
            file.write(answer + "\n")
        file.write("\n")
#------------------------------------Ultrasonic report----------------------------------------# 
        file.write("#-------------------------PRUEBA SENSORES ULTRASONICOS-------------------------#\n\n")
        for answer in self.USS_tests_answers:
            file.write(answer)
        file.write("\n")
#------------------------------------LCD report----------------------------------------#
        file.write("#-------------------------PRUEBA PINES LCD-------------------------#\n\n")
        for i, pin in enumerate(self.LCD_tests_answers):
            if i % 2 == 0:
                file.write("| " + pin + " |")
            else:
                file.write(" " + pin + " |\n") 
        file.write("\n")

    for key in keys:
        if self.Test_Status[key]["WAS DONE?"]:
            was_a_test_donde = True
        if not self.Test_Status[key]["WAS DONE?"]:
            was_not_a_test_done = True

    if was_a_test_donde:
        self.print_in_terminal("Resultados de pruebas realizadas\n")
        for key in keys:
            if self.Test_Status[key]["WAS DONE?"]:
                if self.Test_Status[key]["DID IT WORK?"]:
                    self.print_in_terminal(key + " ✅\n")
                else:
                    self.print_in_terminal(key + " ❌\n")
        self.print_in_terminal("\n")
    
    if was_not_a_test_done:
        self.print_in_terminal("Pruebas no realizadas\n")
        for key in keys:
            if not self.Test_Status[key]["WAS DONE?"]:
                    self.print_in_terminal(key + "\n")
        self.print_in_terminal("\n")

    self.print_in_terminal("REPORTE CREADO EXITOSAMENTE!!\n")
    reset_status(self)