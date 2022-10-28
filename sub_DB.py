# -*- coding: utf-8 -*-

Version = "v1.1.1"
Title = ["0:Main","1:Input File","2:Vref","3:Analyze Method", "False", "False"]
Title[0] = "ADEA %s" % Version

datarate = ""
UI = ""

start_time = ""
Start_Form = ""
Eye_Form = ""
Net_Form = ""
Env_Form = ""
Cal_Form = ""
Option_Form = ""
IBIS_Form = ""
IBISInfo_Tx_Form = ""
IBISInfo_Rx_Form = ""
IBIS_CaseForm = ""
IBIS_ResultForm = ""
Var_Form = ""

File = ""
Input_File = ""
temp_dir = ""
result_dir = ""
resource_dir = ""
user_dir = ""
Log = ""
Log_File = ""

Eye_Analyze_Flag = True

#Debug_Mode = True
Debug_Mode = False
Cenv = {}
Uenv = {}

AEDT = {}
# Eye_flag
#   True = New Eye
#   False = Old Eye
Eyeflag = True

Netlist = []
Waveform = {}
Waveform_Vref = {}
Waveform_IBIS = {}
Waveform_Vref_IBIS = {}
Strobe_Waveform = {}
Jitter_RMS = {}
total_waveform_length = ""
Waveform_Vref_File = ""
Waveform_File = ""
Excel_Img_File = []
NetSort_Flag = False
Eye_Measure_Results = {}
IBIS_Eye_Measure_Results = {}
Setup = {}
Hold = {}
Vref = ""
InputFile_Flag = 1 # 1:*.aedt, 2:*.csv
Unit = {}
Unit["Time"]=""
Unit["Voltage"]=""
Time = []
CSV_flag = True # True : Uniform, False : Arbitrary
var_string = ""
Result_Flag = False
exit_iter = 0
Spec = {}
TBD_flag = True
AutoLoad_flag = False
Parsing_data = "" # AEDT Parsing data
IBIS_Tx = "" # Tx의 *.ibs를 Parsing한 data
IBIS_Rx = "" # Tx의 *.ibs를 Parsing한 data
IBIS_Init_Tx = [] # Input Schematic에 Setting된 초기 IBIS tx buffer model
IBIS_Init_Rx = [] # Input Schematic에 Setting된 초기 IBIS rx buffer model
IBIS_Tx_Model = [] # Parametric sweep에 setup될 IBIS tx buffer model
IBIS_Tx_Model_idx = [] # Parametric sweep에 setup될 IBIS tx buffer model index
IBIS_Rx_Model = [] # Parametric sweep에 setup될 IBIS rx buffer model
IBIS_Rx_Model_idx = [] # Parametric sweep에 setup될 IBIS rx buffer model index
IBIS_Tx_comp = [] # Parametric sweep 적용할 Input Schematic의 tx component list
IBIS_Rx_comp = [] # Parametric sweep 적용할 Input Schematic의 rx component list
IBIS_Sim_Case = []
IBIS_Result_Init_Flag = True
UI_tolerance = 10e-12