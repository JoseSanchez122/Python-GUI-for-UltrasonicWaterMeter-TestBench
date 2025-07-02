import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
import re

def is_number(uart_msg):
    try:
        float(uart_msg)  # Intentar convertirlo a flotante
        return True
    except ValueError:
        return False
    
def extract_numbers_from_string(message): 
    match = re.search("[-+]?\d*\.\d+|\d+", message)
    if match:
        return match.group()
    return None

def Current_Test_Only(self):
    self.clear_input_buffer()
    self.Test_Status["Current test"]["WAS DONE?"] = True
    self.Current_tests_answers.clear()
    tasktry = 10
    current_test_start_msg = "START CURRENT TEST ONLY\n"

    self.print_in_terminal("EMPEZANDO PRUEBA DE CORRIENTE\n")
    self.print_in_terminal("ESTO PUEDE TOMAR APROX 10 SEG")

    while True:
        if self.ser.in_waiting >0:
            current_msg = self.READ_UART()
            if current_msg == "STARTING CURRENT TEST":
                self.print_in_terminal("\n")
                self.Test_Status["Current test"]["DID IT WORK?"] = True
                while True:
                    if self.ser.in_waiting >0:
                        current_msg = self.READ_UART()
                        self.Current_tests_answers.append(current_msg + "\n")
                        self.print_in_terminal(self.Current_tests_answers[-1])
                        if current_msg.startswith("Average current consumption"):
                            average_current = float(extract_numbers_from_string(current_msg))
                            if average_current > 200.0 or average_current <0.0:
                                self.Test_Status["Current test"]["DID IT WORK?"] = False
                        if current_msg == "FINISHING CURRENT TEST":
                            return
            
            elif current_msg == "ERROR: MSP430FR60471 DIDN'T ANSWER":
                self.Current_tests_answers.append(current_msg + "\n")
                self.print_in_terminal("\nERROR: MSP430FR60471 DIDN'T ANSWER\n")
                self.Test_Status["Current test"]["DID IT WORK?"] = False
                return
            
            elif current_msg == "Failed to find INA219 chip":
                self.Current_tests_answers.append(current_msg + "\n")
                self.print_in_terminal("\nFailed to find INA219 chip\n")
                self.Test_Status["Current test"]["DID IT WORK?"] = False
                return
            
            else:
                if tasktry <= 0:
                  
                    self.Current_tests_answers.append("\nERROR: ESP32 no responde\n")
                    self.print_in_terminal(self.Current_tests_answers[-1])
                    self.Test_Status["Current test"]["DID IT WORK?"] = False
                    return
                tasktry = tasktry-1
                self.ser.write(current_test_start_msg.encode())
                self.text_in_terminal.insert("end", ".")
                self.delay(1000)

        if tasktry <= 0:
            
            self.Current_tests_answers.append("\nERROR: ESP32 no responde\n")
            self.print_in_terminal(self.Current_tests_answers[-1])
            self.Test_Status["Current test"]["DID IT WORK?"] = False
            return
        tasktry = tasktry-1
        self.ser.write(current_test_start_msg.encode())
        self.text_in_terminal.insert("end", ".")
        self.delay(1000)

def Current_Test_with_Plot(self):
    self.Test_Status["Current test"]["WAS DONE?"] = True
    self.Current_tests_answers.clear()
    tasktry = 10
    current_test_start_msg = "START CURRENT TEST WITH PLOT\n"
    current_samples = []

    self.print_in_terminal("EMPEZANDO PRUEBA DE CORRIENTE\n")
    self.print_in_terminal("ESTO PUEDE TOMAR APROX 25 SEG")

    while True:
        if self.ser.in_waiting >0:
            current_msg = self.READ_UART()
            if current_msg == "STARTING CURRENT TEST":
                self.print_in_terminal("\n")
                self.Test_Status["Current test"]["DID IT WORK?"] = True
                while True:
                    if self.ser.in_waiting >0:
                        current_msg = self.READ_UART()
                        if is_number(current_msg):
                            break
                        self.Current_tests_answers.append(current_msg + "\n")

                while True:
                    if self.ser.in_waiting >0:
                        current_msg = self.READ_UART()
                        if current_msg == "FINISHING CURRENT TEST":
                            break
                        current_samples.append(float(current_msg))

                for answer in self.Current_tests_answers:
                    if answer.startswith("Average current consumption"):
                        self.print_in_terminal(answer)
                        average_current = float(extract_numbers_from_string(answer))
                        if average_current > 200.0 or average_current <0.0:
                            self.Test_Status["Current test"]["DID IT WORK?"] = False

                samples = range(len(current_samples))
                time_per_sample = 0.000587

                x = [sample*time_per_sample  for sample in samples]
                plt.figure(figsize=(8, 5))
                plt.plot(x, current_samples, linewidth=2)
                yticks_values = plt.yticks()[0]
                yticks_labels = [f"{int(val)} µA" for val in yticks_values]
                plt.yticks(yticks_values, yticks_labels)
                xticks_values = [i for i in range(0, int(max(x)), 2)]
                xticks_labels = [f"{int(val)} seg" for val in xticks_values]
                plt.xticks(xticks_values, xticks_labels)
                
                self.Grafica = FigureCanvasTkAgg(plt.gcf(), master=self.terminal)
                self.Grafica.draw()

                self.Grafica.get_tk_widget().place(x=25, y=135, width=750, height=450)
                return
            
            elif current_msg == "ERROR: MSP430FR60471 DIDN'T ANSWER":
                
                self.Current_tests_answers.append(current_msg + "\n")
                self.print_in_terminal("\nERROR: MSP430FR60471 DIDN'T ANSWER\n")
                self.Test_Status["Current test"]["DID IT WORK?"] = False
                return
            
            else:
                if tasktry <= 0:
                   
                    self.Current_tests_answers.append("ERROR: ESP32 no responde\n")
                    self.print_in_terminal("\n" + self.Current_tests_answers[-1])
                    self.Test_Status["Current test"]["DID IT WORK?"] = False
                    return
                tasktry = tasktry-1
                self.ser.write(current_test_start_msg.encode())
                self.text_in_terminal.insert("end", ".")
                self.delay(1000)

        if tasktry <= 0:
            
            self.Current_tests_answers.append("ERROR: ESP32 no responde\n")
            self.print_in_terminal("\n" + self.Current_tests_answers[-1])
            self.Test_Status["Current test"]["DID IT WORK?"] = False
            return
        tasktry = tasktry-1
        self.ser.write(current_test_start_msg.encode())
        self.text_in_terminal.insert("end", ".")
        self.delay(1000)