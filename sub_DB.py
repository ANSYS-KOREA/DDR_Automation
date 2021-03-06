Version = "v0.5"
Title = ["0:Main","1:Input File","2:Vref","3:Analyze Method", "False", "False"]
Title[0] = "ADEA %s" % Version

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
IBIS_Case_ResultForm = "test"

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
IBIS_Tx = ""
IBIS_Rx = ""
IBIS_Tx_Model = []
IBIS_Tx_Model_idx = []
IBIS_Rx_Model = []
IBIS_Rx_Model_idx = []
IBIS_Sim_Case = []
IBIS_Result_Init_Flag = True