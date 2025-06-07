def LCD_Electrical_Test_lib(self, show_image):
    self.clear_input_buffer()
    self.Test_Status["LCD electrical test"]["WAS DONE?"] = True
    self.LCD_tests_answers.clear()
    tasktry = 15
    LCD_start_msg = "START LCD ELECTRICAL TEST"
    test_finished = False
    
    self.text_in_terminal.insert("end", "EMPEZANDO PRUEBA ELECTRICA LCD")
    self.delay(1000)
    
    while True:
        if self.ser.in_waiting >0:
            LCD_msg = self.READ_UART()
            if LCD_msg == "STARTING LCD ELECTRICAL TEST":
                self.Test_Status["LCD electrical test"]["DID IT WORK?"] = True
                while True:
                    if self.ser.in_waiting >0:
                        while test_finished == False:
                            if self.ser.in_waiting >0:
                                LCD_msg = self.READ_UART()
                                if LCD_msg == "FINISHING LCD ELECTRICAL TEST": 
                                    test_finished = True
                                    self.print_in_terminal("\nPrueba Electrica LCD Terminada")
                                    return
                                elif LCD_msg.endswith("NOT WORKING RETRYING..."):
                                    self.print_in_terminal("\n" + LCD_msg)
                                    pin_not_working(self, LCD_msg[:4], show_image)
                                elif LCD_msg.endswith("IS DEFINITELY NOT WORKING"):
                                    self.print_in_terminal("\n" + LCD_msg)
                                    pin_not_working(self, LCD_msg[:4], show_image)
                                    self.LCD_tests_answers.append(LCD_msg[:4] + " NOT WORKING")
                                    self.Test_Status["LCD electrical test"]["DID IT WORK?"] = False
                                else:
                                    self.LCD_tests_answers.append(LCD_msg)
                                    pin_working(self, LCD_msg[:4], show_image)
                                    self.print_in_terminal("\n" + LCD_msg  )
                                
            elif LCD_msg == "ERROR: MSP430FR60471 DIDN'T ANSWER":
                self.Test_Status["LCD electrical test"]["DID IT WORK?"] = False
                self.LCD_tests_answers.append(LCD_msg + "\n")
                self.print_in_terminal("\n" + LCD_msg)
                return
        
        if tasktry <= 0:
          
            self.LCD_tests_answers.append("ERROR: ESP32 no responde\n")
            self.print_in_terminal("\n" + self.LCD_tests_answers[-1])
            self.Test_Status["LCD electrical test"]["DID IT WORK?"] = False
            return
        tasktry = tasktry-1
        self.ser.write(LCD_start_msg.encode())
        self.text_in_terminal.insert("end", ".")
        self.delay(1000)

def pin_working(self, pin, show_image):
    if show_image:
        xpos,ypos = self.pins_pos[pin]
        self.pins_correct_marks[pin].place(x=xpos, y=ypos)

def pin_not_working(self, pin, show_image):
    if show_image:
        xpos,ypos = self.pins_pos[pin]
        self.pins_wrong_marks[pin].place(x=xpos, y=ypos)



            