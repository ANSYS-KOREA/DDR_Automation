Version = "v0.0"

Start_Form = ""
Eye_Form = ""
Net_Form = ""
Env_Form = ""
Cal_Form = ""
Option_Form = ""

File = ""
Input_File = ""
temp_dir = ""
result_dir = ""
Log = ""

Eye_Analyze_Flag = True

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
Strobe_Waveform = {}
Jitter_RMS = {}
total_waveform_length = ""
Waveform_File = ""
Excel_Img_File = []
NetSort_Flag = False
Eye_Measure_Results = {}
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