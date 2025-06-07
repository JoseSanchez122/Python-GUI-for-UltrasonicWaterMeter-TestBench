import re

def extract_numbers_from_string(message): 
    match = re.search("[-+]?\d*\.\d+|\d+", message)
    if match:
        return match.group()
    return None

def voltage_test_func(self):
    self.clear_input_buffer()
    self.Test_Status["Voltage test"]["WAS DONE?"] = True
    self.Voltage_tests_answers.clear()
    tasktry = 10
    Voltage_start_msg = "START VOLTAGE TEST\n"

    self.text_in_terminal.insert("end", "EMPEZANDO PRUEBA DE VOLTAGE")
    self.delay(1000)

    while True:
        if self.ser.in_waiting >0:
            voltage_msg = self.READ_UART()
            if voltage_msg == "STARTING VOLTAGE TEST":
                self.print_in_terminal("\n")
                self.Test_Status["Voltage test"]["DID IT WORK?"] = True
                while voltage_msg != "FINISHING VOLTAGE TEST":
                    if self.ser.in_waiting >0:
                        voltage_msg = self.READ_UART()
                        if voltage_msg.startswith("ERROR"):
                            self.Test_Status["Voltage test"]["DID IT WORK?"] = False
                        if voltage_msg.startswith("VCEL PIN VOLTAGE"):
                            self.Voltage_tests_answers.append(voltage_msg + "\n")
                            self.print_in_terminal(self.Voltage_tests_answers[-1])
                            self.print_in_terminal("Obteniendo voltage en pin 1V8 espere...\n")
                        else:
                            self.Voltage_tests_answers.append(voltage_msg + "\n")
                            self.print_in_terminal(self.Voltage_tests_answers[-1])
                return

            elif voltage_msg == "ERROR: MSP430FR60471 DIDN'T ANSWER":
                self.Voltage_tests_answers.append(voltage_msg + "\n")
                self.print_in_terminal("\n" + "ERROR: MSP430FR60471 DIDN'T ANSWER\n")
                self.Test_Status["Voltage test"]["DID IT WORK?"] = False
                return
                
            else: 
                if tasktry <= 0:
                    self.Voltage_tests_answers.append("ERROR: ESP32 no responde\n")
                    self.print_in_terminal("\n" + self.Voltage_tests_answers[-1])
                    self.Test_Status["Voltage test"]["DID IT WORK?"] = False
                    return
                tasktry = tasktry-1
                self.ser.write(Voltage_start_msg.encode())
                self.text_in_terminal.insert("end", ".")
                self.delay(1000)

        if tasktry <= 0:
          
            self.Voltage_tests_answers.append("ERROR: ESP32 no responde\n")
            self.print_in_terminal("\n" + self.Voltage_tests_answers[-1])
            self.Test_Status["Voltage test"]["DID IT WORK?"] = False
            return
        tasktry = tasktry-1
        self.ser.write(Voltage_start_msg.encode())
        self.text_in_terminal.insert("end", ".")
        self.delay(1000)