def Diagnosticar_Quectel_2(self):
    self.Test_Status["Quectel test"]["WAS DONE?"] = True
    self.quectel_answers.clear()
    test_finished = False
    tasktry = 25
    Quectel_start_msg = "START QUECTEL ANALYSIS"
    
    self.ser.write(Quectel_start_msg.encode())
    self.print_in_terminal("EMPEZANDO PRUEBA DE QUECTEL\n")
    self.text_in_terminal.insert("end", "WAITING FOR APP_RDY")
    
    while True:
        if self.ser.in_waiting >0:
            Quectel_msg = self.READ_UART()
            if Quectel_msg == "APP_RDY RECIVIDO" or Quectel_msg == "ATE0 ACTIVADO" or Quectel_msg == "WAITING FOR APP_RDY":
                self.quectel_answers.append(Quectel_msg)
                self.Test_Status["Quectel test"]["DID IT WORK?"] = True
                if Quectel_msg.startswith("ERROR"):
                    self.Test_Status["Quectel test"]["DID IT WORK?"] = False
                while True:
                    if self.ser.in_waiting >0:
                        Quectel_msg = self.READ_UART()
                        if Quectel_msg.startswith("ERROR"):
                            self.Test_Status["Quectel test"]["DID IT WORK?"] = False
                        self.quectel_answers.append(Quectel_msg)
                        self.print_in_terminal("\n" + Quectel_msg + "\n")
                        while test_finished == False:
                            if self.ser.in_waiting >0:
                                Quectel_msg = self.READ_UART()
                                if Quectel_msg.startswith("ERROR"):
                                    self.Test_Status["Quectel test"]["DID IT WORK?"] = False
                                #imprimir solo una ves si termina con RETRYING...
                                if Quectel_msg.endswith("RETRYING..."):
                                    self.print_in_terminal(Quectel_msg + "\n")
                                    while Quectel_msg.endswith("RETRYING..."):
                                        if self.ser.in_waiting >0:
                                            Quectel_msg = self.READ_UART()
                                            if Quectel_msg.startswith("ERROR"):
                                                self.Test_Status["Quectel test"]["DID IT WORK?"] = False
                                            

                                self.quectel_answers.append(Quectel_msg)
                                self.print_in_terminal(Quectel_msg + "\n")

                                #imprimir solo una ves cuando no funciona CREG
                                if Quectel_msg.startswith("STATUS: Not registered") or Quectel_msg.startswith("STATUS: Registration den") or Quectel_msg.startswith("STATUS: Unknown"):
                                    while Quectel_msg.startswith("STATUS: Not registered") or Quectel_msg.startswith("STATUS: Registration den") or Quectel_msg.startswith("STATUS: Unknown") or Quectel_msg.startswith("MODE:"):    
                                        if self.ser.in_waiting >0:
                                            Quectel_msg = self.READ_UART()
                                            if Quectel_msg.startswith("ERROR"):
                                                self.Test_Status["Quectel test"]["DID IT WORK?"] = False

                                if Quectel_msg == "Quectel finished": 
                                    test_finished = True
                                    return
                    else: 
                        self.text_in_terminal.insert("end", ".")
                        self.delay(500)
                        
            elif Quectel_msg =="ERROR: MSP430FR60471 DIDN'T ANSWER":
                self.quectel_answers.append(Quectel_msg + "\n")
                self.print_in_terminal("\n" + self.quectel_answers[-1])
                self.Test_Status["Quectel test"]["DID IT WORK?"] = False
                return
                        
            elif Quectel_msg == "ERROR: APP RDY WAS NOT RECEIVED\n":
                self.quectel_answers.append(Quectel_msg + "\n")
                self.print_in_terminal("\n" + "ERROR: Quectel no inicio\n")
                self.Test_Status["Quectel test"]["DID IT WORK?"] = False
                return
            
            else:
                if tasktry <= 0:
                    self.quectel_answers.append("ERROR: ESP32 no responde\n")
                    self.print_in_terminal("\n" + self.quectel_answers[-1])
                    self.Test_Status["Quectel test"]["DID IT WORK?"] = False
                    return 
                tasktry = tasktry-1
                self.ser.write(Quectel_start_msg.encode())
                self.text_in_terminal.insert("end", ".")
                self.delay(1000)
         
        if tasktry <= 0:
           
            self.quectel_answers.append("ERROR: ESP32 no responde\n")
            self.print_in_terminal("\n" + self.quectel_answers[-1])
            self.Test_Status["Quectel test"]["DID IT WORK?"] = False
            return 
        tasktry = tasktry-1
        self.ser.write(Quectel_start_msg.encode())
        self.text_in_terminal.insert("end", ".")
        self.delay(1000)