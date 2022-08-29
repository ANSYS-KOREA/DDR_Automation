# -*- coding: utf-8 -*-
'''
[v0.5.1] - '22.08.06
    -. Eye 계측 Algorithm Classic Version(VB) 으로 변경 후, Excel report 생성 bug 수정
    -. Resource 폴더 정리
    -. 예제 Archive file 추가
    -. CSV input disable

[v0.5.2] - '22.08.07
    -. Excel report format 변경
    -. Jitter, Jitter_RMS 열 삭제
    -. Width & Margin UI 단위 열 추가

[v0.5.3] - '22.08.08
    -. IBIS bug fix    
    -. Show result window for each IBIS cases

[v0.6] - '22.08.09
    -. Release to SEC

[v0.6.1] - '22.08.12
    -. Modify IBIS Optimization example (buffer -> pin import)
    -. Bug fix for IBIS New & pin import case

[v0.6.2] - '22.08.24
    -. IBIS Model check시 sim case 바로 반영되지 않던 문제 수정
    -. IBIS Model refresh button click시 sim case 초기화 되지 않던 문제 수정
    -. IBIS Run Click시 초기화 문제 수정
    -. Tx/Rx 같은 *.ibs file 사용 Case update
    -. IBIS form resize event update
    -. Automatic data-rate detect algorithm are updated
[v0.6.3] - '22.08.30
    -. 
'''




Version = "v0.6.3"
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