import re

def extract_numbers_from_string(message): 
    match = re.search("[-+]?\d*\.\d+|\d+", message)
    if match:
        return int(match.group())
    return None

def remove_numbers_from_string(message):
    return re.sub("[-+]?\d*\.\d+|\d+", "", message)

def get_number_meaning(number):
    number_meanings = {
        0: "Operacion completada exitosamente",
        1: "SAPH pulseLowPhasePeriod error",
        2: "SAPH pulseHighPhasePeriod error",
        3: "SAPH numOfExcitationPulses error",
        4: "SAPH numOfStopPulses error",
        5: "SAPH update error ongoing conversion",
        6: "SAPH time startPPGCount error",
        7: "SAPH time turnOnADCCount error",
        8: "SAPH time startADCsamplingCount error",
        9: "SAPH time restartCaptureCount error",
        10: "SAPH time captureTimeOutCount error",
        11: "SAPH time startPGAandINBiasCount error",
        12: "SAPH invalid bias impedance error",
        13: "SAPH invalid rx charge pump mode error",
        14: "SAPH invalid pulse configuration error",
        21: "HSPLL pllXtalFreq inHz error",
        22: "HSPLL pllOutputFreq inHz error",
        23: "HSPLL plllock error",
        24: "HSPLL pll unlock error",
        26: "HSPLL update error ongoing conversion",
        27: "HSPLL verification expected count error",
        28: "HSPLL invalid settling count error",
        41: "SDHS threshold error",
        43: "SDHS conversion overflow error",
        44: "SDHS sample size error",
        45: "SDHS update error ongoing conversion",
        46: "SDHS window low threshold reached",
        47: "SDHS window high threshold reached",
        48: "SDHS max size error",
        61: "UUPS update error ongoing conversion",
        62: "UUPS power up time out error",
        63: "UUPS power up error",
        64: "UUPS power down error",
        81: "data error abort",
        82: "ASQ time out",
        101: "measurement stopped",
        102: "error conversion stopped by debugger",
        103: "measurement period overflow",
        121: "parameter check failed",
        122: "valid results",
        123: "algorithm error",
        124: "algorithm error invalid iteration value",
        125: "algorithm error no signal detected ups channel",
        126: "algorithm error no signal detected ups dns channel",
        127: "algorithm error no signal detected dns channel",
        128: "algorithm captures accumulated",
        129: "algorithm error invalid clock relative error",
        130: "algorithm error invalid filter length",
        131: "algorithm error generating binary pattern",
        132: "algorithm error invalid absToF computation option",
        133: "algorithm error invalid meter constant calib data",
        135: "algorithm error dtof shift range",
        136: "algorithm error dtof corr overrun",
        137: "algorithm error dtof interpolation",
        138: "algorithm error dtof corr threshold",
        139: "algorithm error temperature object",
        142: "interrupt update error ongoing conversion",
        161: "invalid conversion data",
        171: "Calibration DAC success",
        172: "Calibration DAC error",
        173: "Calibration Gain error",
        174: "Calibration DCO error",
        175: "Signal Gain Calibration timeout",
        176: "Signal Gain Calibration settling",
        177: "Signal Gain Calibration successful",
        178: "Calibration DAC timeout error",
        179: "Calibration ToF Offset error",
        180: "Calibration Offset invalid configuration",
        181: "Calibration VFR pt inside quadrilateral",
        182: "Calibration VFR pt outside quadrilateral",
        240: "ACLK settling time out",
        241: "silicon version does not support this functionality",
        253: "USSXT oscillator not stable error",
        254: "USS ongoing active conversion error",
        255: "error occurred"
    }

    if number is None:
        return "Número desconocido"
    return number_meanings.get(number, "Número desconocido")

def is_a_message_to_get_code_meaning(message):
    messages_to_get_code_meaning = ["configuracion Result",
                                    "HSPLL Frequency Results",
                                    "USS initAlgorithms Result",
                                    "start LowPower Ultrasonic Capture Result",
                                    "USS runAlgorithms Result",
                                    ]
    for msg in messages_to_get_code_meaning:
        if message.startswith(msg):
            return True
    return False

def USS_test_func(self): 
    self.clear_input_buffer()
    self.Test_Status["USS test"]["WAS DONE?"] = True
    self.USS_tests_answers.clear()
    tasktry = 6
    USS_start_msg = "START USS TEST"
    temporary_msg_list = []

    self.text_in_terminal.insert("end", "EMPEZANDO PRUEBA DE ULTRASONIDO")
    self.delay(1000)

    while True:
        if self.ser.in_waiting >0:
            USS_msg = self.READ_UART()
            if USS_msg == "STARTING USS TEST":
                self.print_in_terminal("\n")
                self.Test_Status["USS test"]["DID IT WORK?"] = True
                while True:
                    if self.ser.in_waiting >0:
                        USS_msg = self.READ_UART()
                        temporary_msg_list.append(USS_msg)
                        tasktry = tasktry+1
                        
                        if USS_msg == "FINISHING USS TEST":
                            for msg in temporary_msg_list:
                                if is_a_message_to_get_code_meaning(msg):
                                    message_without_code = remove_numbers_from_string(msg)
                                    code_meaning = get_number_meaning(extract_numbers_from_string(msg))
                                    if msg.startswith("USS runAlgorithms Result"):
                                        self.print_in_terminal("\n-----------------------------------------------------\n\n")
                                        self.USS_tests_answers.append("\n//=================================================//\n\n")
                                        self.USS_tests_answers.append("Resultado de medicion ultrasonica:\n" + code_meaning)
                                        self.USS_tests_answers.append("\n\n//=================================================//\n\n")
                                        self.print_in_terminal(self.USS_tests_answers[-2] + "\n")
                                        self.print_in_terminal("\n-----------------------------------------------------\n\n")
                                        if code_meaning != "valid results":
                                            self.Test_Status["USS test"]["DID IT WORK?"] = False
                                    else:
                                        self.USS_tests_answers.append(message_without_code + code_meaning + "\n")
                                        self.print_in_terminal(self.USS_tests_answers[-1]) 
                                else:
                                    self.USS_tests_answers.append(msg + "\n")
                                    self.print_in_terminal(self.USS_tests_answers[-1])
                            return
                    
                    else: 
                        if tasktry <= 0:
                            
                            self.USS_tests_answers.append("ERROR: ESP32 no responde\n")
                            self.print_in_terminal("\n" + self.USS_tests_answers[-1])
                            self.Test_Status["USS test"]["DID IT WORK?"] = False
                            return
                        tasktry = tasktry-1
                        self.ser.write(USS_start_msg.encode())
                        self.text_in_terminal.insert("end", ".")
                        self.delay(1000)
                    
            elif USS_msg == "ERROR: MSP430FR60471 DIDN'T ANSWER":
                
                self.USS_tests_answers.append(USS_msg + "\n")
                self.print_in_terminal("\n" + "ERROR: MSP430FR60471 DIDN'T ANSWER\n")
                self.Test_Status["USS test"]["DID IT WORK?"] = False
                return

            else: 
                if tasktry <= 0:
                    
                    self.USS_tests_answers.append("ERROR: ESP32 no responde\n")
                    self.print_in_terminal("\n" + self.USS_tests_answers[-1])
                    self.Test_Status["USS test"]["DID IT WORK?"] = False
                    return
                tasktry = tasktry-1
                self.ser.write(USS_start_msg.encode())
                self.text_in_terminal.insert("end", ".")
                self.delay(1000)

        if tasktry <= 0:
            
            self.USS_tests_answers.append("ERROR: ESP32 no responde\n")
            self.print_in_terminal("\n" + self.USS_tests_answers[-1])
            self.Test_Status["USS test"]["DID IT WORK?"] = False
            return
        tasktry = tasktry-1
        self.ser.write(USS_start_msg.encode())
        self.text_in_terminal.insert("end", ".")
        self.delay(1000)