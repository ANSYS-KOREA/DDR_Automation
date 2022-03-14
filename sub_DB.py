Start_Form = ""
Eye_Form = ""
Net_Form = ""
Env_Form = ""
Cal_Form = ""
Option_Form = ""

temp_dir = ""
Log = ""

Eye_Option_Init_Flag = True
Eye_Analyze_Flag = True

Debug_Mode = False
Cenv = {}
Uenv = {}

# Eye_flag
#   True = New Eye
#   False = Old Eye
Eyeflag = True

Netlist = []
Waveform = {}
Jitter_RMS = {}
total_waveform_length = ""
Waveform_File = ""
Excel_Img_File = []
NetSort_Flag = False
Eye_Measure_Results = {}
Vref = ""
InputFile_Flag = 1 # 1:*.aedt, 2:*.csv
Unit = {}
Unit["Time"]=""
Unit["Voltage"]=""
Time = []
CSV_flag = True # True : Uniform, False : Arbitrary
var_string = ""
Result_Flag = False