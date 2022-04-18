import os
import clr
import time

clr.AddReference('Microsoft.Office.Interop.Excel')

from sub_DB import *
from sub_functions import *
from Microsoft.Office.Interop import Excel

path = os.path.dirname(os.path.abspath(__file__))

def run_CompTest(Waveform, self):
    #####################################
    # 1. Load Compliance Specifications #
    #####################################
    try:
        sub_DB.Cal_Form.Text = "Compliance Testing"
        sub_DB.Cal_Form._Label_Vref.Text = "Load Spec"
        sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
        Log("	    (Load Compliance Specifications) = Start")
        Load_Spec(self)
        Log("	    (Load Compliance Specifications) = Done")

    except Exception as e:
        Log("	    (Load Compliance Specifications) = Failed")
        Log(traceback.format_exc())
        MessageBox.Show("Compliance test - Loading compliance spec. failed","Warning")
        EXIT()

    #########################
    # 2. Testing Compliance #
    #########################
    try:
        Log("	    (Compliance Test) = Start")
        Result = Comp_Test(Waveform, self, sub_DB.Cal_Form)
        Log("	    (Compliance Test) = Done")

    except Exception as e:
        Log("	    (Load Compliance Specifications) = Failed")
        Log(traceback.format_exc())
        MessageBox.Show("Compliance test - Loading compliance spec. failed","Warning")
        EXIT()

    ##########################
    # 3. Create Excel Report #
    ##########################
    try:
        Log("	    (Reporting) = Start")
        Excel_Report(Result)
        Log("	    (Reporting) = Done")

    except Exception as e:
        Log("	    (Reporting) = Failed")
        Log(traceback.format_exc())
        MessageBox.Show("Compliance test - Reporting failed","Warning")
        EXIT()



def sort_list(List):
    # "abc" -> [a, b, c] -> ord(a) + ord(b) + ord(c) = val
    # # sort val and get index => Name_idx
    Name_idx = []
    Result = []
    for name in List:
        temp_list = list(name)
        val = 0
        flag = True
        for text in temp_list:
            if 47 < ord(text) < 58:
                val += ord(text)
            else:
                if flag:
                    val += ord(text)*1000
                    flag = False
                else:
                    val += ord(text)
        Name_idx.append(val)
    Name_idx = sorted(range(len(Name_idx)),key=lambda k: Name_idx[k], reverse=False)

    Result = list(List)
    for i in range(0, len(List)):
        Result[Name_idx[i]] = List[i]

    return Result

def Load_Spec(self):
    ##########
	#  DDR3  #
	##########
    if self._ComboBox_DDRGen.Text == "DDR3":
        Log("            = Target DDR Type : DDR3")

        # Set the specification file according to the DDR type in Resources folder
        File = path + r'\Resources\Compliance_Spec_DDR3.xlsx'
        Log("	        = Spec. File : %s" % File)

        # Data setup and hold time - 1 & 2
        if sub_DB.Compliance_Form._DataGridView.Rows[1].Cells[0].Value:
            try:
                Log("            = Load Data setup & hold spec. : Start")
                Load_Spec_DDR3_DQ_SetupHold(File, "tDS & tDH")
                Log("            = Load Data setup & hold spec. : Done")
            except Exception as e:
                Log("            = Load Data setup & hold spec. : Failed")
                Log(traceback.format_exc())
                MessageBox.Show("Compliance test - Loading data setup & hold spec. failed","Warning")
                EXIT()

        # Strobe to data skew
        if sub_DB.Compliance_Form._DataGridView.Rows[3].Cells[0].Value:
            sheet_name = "tDQSQ"

        # Data output hold time
        if sub_DB.Compliance_Form._DataGridView.Rows[4].Cells[0].Value:
            sheet_name = "tQH"

        # Input Pulse Width
        if sub_DB.Compliance_Form._DataGridView.Rows[5].Cells[0].Value:
            sheet_name = "tDIPW"

        # Valid transition time
        if sub_DB.Compliance_Form._DataGridView.Rows[6].Cells[0].Value:
            sheet_name = "tVAD(DQ)"

        # Address setup and hold time - 7 & 8
        if sub_DB.Compliance_Form._DataGridView.Rows[7].Cells[0].Value:
            sheet_name = "tIS & tIH"

        # Input pulse width
        if sub_DB.Compliance_Form._DataGridView.Rows[9].Cells[0].Value:
            sheet_name = "tIPW"

        # Valid transition time
        if sub_DB.Compliance_Form._DataGridView.Rows[10].Cells[0].Value:
            sheet_name = "tVAD(ADDR)"

        # Differential input low/high pusle width - 11 & 12
        if sub_DB.Compliance_Form._DataGridView.Rows[11].Cells[0].Value:
            sheet_name = "tDQSL ?& tDQSH"

        # Average & absolute clock period - 13 & 16
        if sub_DB.Compliance_Form._DataGridView.Rows[13].Cells[0].Value:
            sheet_name = "tCK"

        # Average & absolute clock low/high pulse width - 14, 15, 17, & 18
        if sub_DB.Compliance_Form._DataGridView.Rows[14].Cells[0].Value:
            sheet_name = "tCL & tCH"

        # clock period jitter & clock cycle to cycle period jitter - 19 & 20
        if sub_DB.Compliance_Form._DataGridView.Rows[19].Cells[0].Value:
            sheet_name = "tCL & tCH"

        # Allowed time before ringback for DQS
        if sub_DB.Compliance_Form._DataGridView.Rows[21].Cells[0].Value:
            sheet_name = "tDVAD(DQS)"

        # Single-ended low/high level for strobes - 22 & 23
        if sub_DB.Compliance_Form._DataGridView.Rows[22].Cells[0].Value:
            sheet_name = "VSEL & VSEH (DQS)"

        # Differential input cross point voltage DQS
        if sub_DB.Compliance_Form._DataGridView.Rows[24].Cells[0].Value:
            sheet_name = "VIX(DQS)"

        # Allowed time before ringback for CLK
        if sub_DB.Compliance_Form._DataGridView.Rows[25].Cells[0].Value:
            sheet_name = "tDVAD(DQS)"

        # Single-ended low/high level for CLK - 26 & 27
        if sub_DB.Compliance_Form._DataGridView.Rows[26].Cells[0].Value:
            sheet_name = "VSEL & VSEH (CLK)"

        # Differential input cross point voltage CLK
        if sub_DB.Compliance_Form._DataGridView.Rows[28].Cells[0].Value:
            sheet_name = "VIX(CLK)"

        # Average of Vref(t)
        if sub_DB.Compliance_Form._DataGridView.Rows[29].Cells[0].Value:
            sheet_name = "VRefDQ(DC)"

    ##########
	#  DDR4  #
	##########
    if self._ComboBox_DDRGen.Text == "DDR4":
        # TODO : Load Spec for DDR4
        pass

    ##########
	#  DDR5  #
	##########
    if self._ComboBox_DDRGen.Text == "DDR5":
        # TODO : Load Spec for DDR5
        pass

def Load_Spec_DDR3_DQ_SetupHold(File, sheet_name):
    sub_DB.Spec["DQ Setup Base"]={}
    sub_DB.Spec["DQ Hold Base"]={}
    sub_DB.Spec["DQ Setup Derating"]={}
    sub_DB.Spec["DQ Hold Derating"]={}
    #################################################
    # Open Excel spec. file and set Excel instances #
    #################################################
    try:
        xlApp = Excel.ApplicationClass()
        xlApp.Visible = False
        xlApp.DisplayAlerts = False
        xlbook = xlApp.Workbooks.Open(File)

        xlsheet = xlbook.Worksheets[sheet_name]
        Log("            = Open spec. file : Done")

    except Exception as e:
        Log("            = Open spec. file : Failed")
        Log(traceback.format_exc())
        MessageBox.Show("Compliance test - Open spec. file failed","Warning")
        EXIT()

    ########################
    # Get Setup base value #
    ########################
    try:
        start_row = 4
        end_row = 6
        start_col = 3
        end_col = 8
        
        for row in range(start_row, end_row+1):
            AC_key = str(xlsheet.Cells[row, start_col-1].Value2).replace("tDS(base) ","")
            sub_DB.Spec["DQ Setup Base"][AC_key] = {}
            for col in range(start_col, end_col+1):
                if not xlsheet.Cells[row, col].Value2 == "-":
                    Datarate_key = str(int(xlsheet.Cells[start_row-1, col].Value2))
                    sub_DB.Spec["DQ Setup Base"][AC_key][Datarate_key] = xlsheet.Cells[row, col].Value2        
        Log("            = Load data setup base Value : Done")

    except Exception as e:
        Log("            = Load data setup base Value : Failed")
        Log(traceback.format_exc())
        MessageBox.Show("Compliance test - Loading data setup base value failed","Warning")
        EXIT()

    #######################
    # Get Hold base value #
    #######################
    try:
        start_row = 7
        end_row = 7
        start_col = 3
        end_col = 8

        for row in range(start_row, end_row+1):
            AC_key = str(xlsheet.Cells[row, start_col-1].Value2).replace("tDH(base) ","")
            sub_DB.Spec["DQ Hold Base"][AC_key] = {}
            for col in range(start_col, end_col+1):
                if not xlsheet.Cells[row, col].Value2 == "-":
                    Datarate_key = str(int(xlsheet.Cells[start_row-4, col].Value2))
                    sub_DB.Spec["DQ Hold Base"][AC_key][Datarate_key] = xlsheet.Cells[row, col].Value2        
        Log("            = Load data hold base Value : Done")

    except Exception as e:
        Log("            = Load data hold base Value : Failed")
        Log(traceback.format_exc())
        MessageBox.Show("Compliance test - Loading data hold base value failed","Warning")
        EXIT()

    ############################
    # Get Setup derating value #
    ############################
    try:        
        sub_DB.Spec["DQ Setup Derating"]["AC175"]={}
        sub_DB.Spec["DQ Setup Derating"]["AC150"]={}
        sub_DB.Spec["DQ Setup Derating"]["AC135"]={}

        sub_DB.Spec["DQ Setup Derating"]["AC175"]["800"]={}
        sub_DB.Spec["DQ Setup Derating"]["AC175"]["1066"]={}

        sub_DB.Spec["DQ Setup Derating"]["AC150"]["800"]={}
        sub_DB.Spec["DQ Setup Derating"]["AC150"]["1066"]={}
        sub_DB.Spec["DQ Setup Derating"]["AC150"]["1333"]={}
        sub_DB.Spec["DQ Setup Derating"]["AC150"]["1600"]={}

        sub_DB.Spec["DQ Setup Derating"]["AC135"]["1866"]={}
        sub_DB.Spec["DQ Setup Derating"]["AC135"]["2133"]={}

        start_col = 4
        end_col = 19
        # for AC175        
        start_row = 14
        end_row = 22        
        for i in range(start_col, end_col+1, 2):
            Strobe_Slew = str(xlsheet.Cells[start_row-2,i].Value2)
            sub_DB.Spec["DQ Setup Derating"]["AC175"]["800"][Strobe_Slew] = {}
            for j in range(start_row, end_row+1):
                if not xlsheet.Cells[j,i].Value2 == "-":
                    DQ_slew = str(xlsheet.Cells[j,start_col-1].Value2)
                    sub_DB.Spec["DQ Setup Derating"]["AC175"]["800"][Strobe_Slew][DQ_slew]=xlsheet.Cells[j,i].Value2
        sub_DB.Spec["DQ Setup Derating"]["AC175"]["1066"] = sub_DB.Spec["DQ Setup Derating"]["AC175"]["800"]
        Log("            = Load data setup derating value for AC175 : Done")

        # for AC150 
        start_row = 29
        end_row = 37
        for i in range(start_col, end_col+1, 2):
            Strobe_Slew = str(xlsheet.Cells[start_row-2,i].Value2)
            sub_DB.Spec["DQ Setup Derating"]["AC150"]["800"][Strobe_Slew] = {}
            for j in range(start_row, end_row+1):
                if not xlsheet.Cells[j,i].Value2 == "-":
                    DQ_slew = str(xlsheet.Cells[j,start_col-1].Value2)
                    sub_DB.Spec["DQ Setup Derating"]["AC150"]["800"][Strobe_Slew][DQ_slew]=xlsheet.Cells[j,i].Value2
        sub_DB.Spec["DQ Setup Derating"]["AC150"]["1066"] = sub_DB.Spec["DQ Setup Derating"]["AC150"]["800"]
        sub_DB.Spec["DQ Setup Derating"]["AC150"]["1333"] = sub_DB.Spec["DQ Setup Derating"]["AC150"]["800"]
        sub_DB.Spec["DQ Setup Derating"]["AC150"]["1600"] = sub_DB.Spec["DQ Setup Derating"]["AC150"]["800"]
        Log("            = Load data setup derating value for AC150 : Done")

        # for AC135
        start_row = 44
        end_row = 52
        for i in range(start_col, end_col+1, 2):
            Strobe_Slew = str(xlsheet.Cells[start_row-2,i].Value2)
            sub_DB.Spec["DQ Setup Derating"]["AC135"]["1866"][Strobe_Slew] = {}
            for j in range(start_row, end_row+1):
                if not xlsheet.Cells[j,i].Value2 == "-":
                    DQ_slew = str(xlsheet.Cells[j,start_col-1].Value2)
                    sub_DB.Spec["DQ Setup Derating"]["AC135"]["1866"][Strobe_Slew][DQ_slew]=xlsheet.Cells[j,i].Value2
        sub_DB.Spec["DQ Setup Derating"]["AC135"]["2133"] = sub_DB.Spec["DQ Setup Derating"]["AC135"]["1866"]
        Log("            = Load data setup derating value for AC135 : Done")

    except Exception as e:
        Log("            = Load data setup derating Value : Failed")
        Log(traceback.format_exc())
        MessageBox.Show("Compliance test - Loading data setup derating value failed","Warning")
        EXIT()

    ############################
    # Get Hold derating value #
    ############################
    try:        
        sub_DB.Spec["DQ Hold Derating"]["AC175"]={}
        sub_DB.Spec["DQ Hold Derating"]["AC150"]={}
        sub_DB.Spec["DQ Hold Derating"]["AC135"]={}

        sub_DB.Spec["DQ Hold Derating"]["AC175"]["800"]={}
        sub_DB.Spec["DQ Hold Derating"]["AC175"]["1066"]={}

        sub_DB.Spec["DQ Hold Derating"]["AC150"]["800"]={}
        sub_DB.Spec["DQ Hold Derating"]["AC150"]["1066"]={}
        sub_DB.Spec["DQ Hold Derating"]["AC150"]["1333"]={}
        sub_DB.Spec["DQ Hold Derating"]["AC150"]["1600"]={}

        sub_DB.Spec["DQ Hold Derating"]["AC135"]["1866"]={}
        sub_DB.Spec["DQ Hold Derating"]["AC135"]["2133"]={}

        start_col = 5
        end_col = 19
        # for AC175        
        start_row = 14
        end_row = 22        
        for i in range(start_col, end_col+1, 2):
            Strobe_Slew = str(xlsheet.Cells[start_row-2,i-1].Value2)
            sub_DB.Spec["DQ Hold Derating"]["AC175"]["800"][Strobe_Slew] = {}
            for j in range(start_row, end_row+1):
                if not xlsheet.Cells[j,i].Value2 == "-":
                    DQ_slew = str(xlsheet.Cells[j,start_col-2].Value2)
                    sub_DB.Spec["DQ Hold Derating"]["AC175"]["800"][Strobe_Slew][DQ_slew]=xlsheet.Cells[j,i].Value2
        sub_DB.Spec["DQ Hold Derating"]["AC175"]["1066"] = sub_DB.Spec["DQ Hold Derating"]["AC175"]["800"]
        Log("            = Load data hold derating value for AC175 : Done")

        # for AC150 
        start_row = 29
        end_row = 37
        for i in range(start_col, end_col+1, 2):
            Strobe_Slew = str(xlsheet.Cells[start_row-2,i-1].Value2)
            sub_DB.Spec["DQ Hold Derating"]["AC150"]["800"][Strobe_Slew] = {}
            for j in range(start_row, end_row+1):
                if not xlsheet.Cells[j,i].Value2 == "-":
                    DQ_slew = str(xlsheet.Cells[j,start_col-2].Value2)
                    sub_DB.Spec["DQ Hold Derating"]["AC150"]["800"][Strobe_Slew][DQ_slew]=xlsheet.Cells[j,i].Value2
        sub_DB.Spec["DQ Hold Derating"]["AC150"]["1066"] = sub_DB.Spec["DQ Hold Derating"]["AC150"]["800"]
        sub_DB.Spec["DQ Hold Derating"]["AC150"]["1333"] = sub_DB.Spec["DQ Hold Derating"]["AC150"]["800"]
        sub_DB.Spec["DQ Hold Derating"]["AC150"]["1600"] = sub_DB.Spec["DQ Hold Derating"]["AC150"]["800"]
        Log("            = Load data hold derating value for AC150 : Done")

        # for AC135
        start_row = 44
        end_row = 52
        for i in range(start_col, end_col+1, 2):
            Strobe_Slew = str(xlsheet.Cells[start_row-2,i-1].Value2)
            sub_DB.Spec["DQ Hold Derating"]["AC135"]["1866"][Strobe_Slew] = {}
            for j in range(start_row, end_row+1):
                if not xlsheet.Cells[j,i].Value2 == "-":
                    DQ_slew = str(xlsheet.Cells[j,start_col-2].Value2)
                    sub_DB.Spec["DQ Hold Derating"]["AC135"]["1866"][Strobe_Slew][DQ_slew]=xlsheet.Cells[j,i].Value2
        sub_DB.Spec["DQ Hold Derating"]["AC135"]["2133"] = sub_DB.Spec["DQ Hold Derating"]["AC135"]["1866"]
        Log("            = Load data hold derating value for AC135 : Done")

    except Exception as e:
        Log("            = Load data hold derating Value : Failed")
        Log(traceback.format_exc())
        MessageBox.Show("Compliance test - Loading data hold derating value failed","Warning")
        EXIT()
    
    xlbook.Close()
    xlApp.Quit()
    ReleaseObject(xlsheet)
    ReleaseObject(xlbook)
    ReleaseObject(xlApp)

def Comp_Test(Waveform, self, Form):
    Result = {}
    ##########
	#  DDR3  #
	##########    
    if self._ComboBox_DDRGen.Text == "DDR3":
        Log("            = Target DDR Type : DDR3")

        # Data setup and hold time - 1 & 2
        if sub_DB.Compliance_Form._DataGridView.Rows[1].Cells[0].Value:
            Result["Data Setup Time"] = {}
            Result["Data Hold Time"] = {}
            checking_item = "data setup & hold time"
            try:                
                sub_DB.Cal_Form._Label_Vref.Text = "Checking %s" % checking_item
                sub_DB.Cal_Form._ProgressBar_Vref.Value += 2
                sub_DB.Cal_Form.Refresh()
                Log("            = Check %s : Start" % checking_item)
                Result["Data Setup Time"], Result["Data Hold Time"] = Comp_Test_DDR3_DQ_SetupHold(Waveform, self)
                Log("            = Check %s : Done" % checking_item)

            except Exception as e:
                Log("            = Check %s : Failed" % checking_item)
                Log(traceback.format_exc())
                MessageBox.Show("Compliance test - Check %s failed" % checking_item,"Warning")
                EXIT()

        # Strobe to data skew - 3
        if sub_DB.Compliance_Form._DataGridView.Rows[3].Cells[0].Value:
            time.sleep(1)
            checking_item = "strobe to data skew"
            try:                
                sub_DB.Cal_Form._Label_Vref.Text = "Checking %s" % checking_item
                sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
                sub_DB.Cal_Form.Refresh()
                Log("            = Check %s : Start" % checking_item)
                # TODO : Checking strobe to data skew
                Log("            = Check %s : Done" % checking_item)

            except Exception as e:
                Log("            = Check %s : Failed" % checking_item)
                Log(traceback.format_exc())
                MessageBox.Show("Compliance test - Check %s failed" % checking_item,"Warning")
                EXIT()

        # Data output hold time - 4
        if sub_DB.Compliance_Form._DataGridView.Rows[4].Cells[0].Value:
            time.sleep(1)
            checking_item = "data output hold time"
            try:                
                sub_DB.Cal_Form._Label_Vref.Text = "Checking %s" % checking_item
                sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
                sub_DB.Cal_Form.Refresh()
                Log("            = Check %s : Start" % checking_item)
                # TODO : Checking Data output hold time
                Log("            = Check %s : Done" % checking_item)

            except Exception as e:
                Log("            = Check %s : Failed" % checking_item)
                Log(traceback.format_exc())
                MessageBox.Show("Compliance test - Check %s failed" % checking_item,"Warning")
                EXIT()

        # Input Pulse Width - 5
        if sub_DB.Compliance_Form._DataGridView.Rows[5].Cells[0].Value:
            time.sleep(1)
            checking_item = "input Pulse Width"
            try:                
                sub_DB.Cal_Form._Label_Vref.Text = "Checking %s" % checking_item
                sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
                sub_DB.Cal_Form.Refresh()
                Log("            = Check %s : Start" % checking_item)
                # TODO : Input Pulse Width
                Log("            = Check %s : Done" % checking_item)

            except Exception as e:
                Log("            = Check %s : Failed" % checking_item)
                Log(traceback.format_exc())
                MessageBox.Show("Compliance test - Check %s failed" % checking_item,"Warning")
                EXIT()

        # Valid transition time - 6
        if sub_DB.Compliance_Form._DataGridView.Rows[6].Cells[0].Value:
            time.sleep(1)
            checking_item = "valid transition time"
            try:                
                sub_DB.Cal_Form._Label_Vref.Text = "Checking %s" % checking_item
                sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
                sub_DB.Cal_Form.Refresh()
                Log("            = Check %s : Start" % checking_item)
                # TODO : Valid transition time
                Log("            = Check %s : Done" % checking_item)

            except Exception as e:
                Log("            = Check %s : Failed" % checking_item)
                Log(traceback.format_exc())
                MessageBox.Show("Compliance test - Check %s failed" % checking_item,"Warning")
                EXIT()

        # Address setup and hold time - 7 & 8
        if sub_DB.Compliance_Form._DataGridView.Rows[7].Cells[0].Value:
            time.sleep(1)
            checking_item = "address setup & hold time"
            try:                
                sub_DB.Cal_Form._Label_Vref.Text = "Checking %s" % checking_item
                sub_DB.Cal_Form._ProgressBar_Vref.Value += 2
                sub_DB.Cal_Form.Refresh()
                Log("            = Check %s : Start" % checking_item)
                # TODO : Address setup & hold time
                Log("            = Check %s : Done" % checking_item)

            except Exception as e:
                Log("            = Check %s : Failed" % checking_item)
                Log(traceback.format_exc())
                MessageBox.Show("Compliance test - Check %s failed" % checking_item,"Warning")
                EXIT()

        # Input pulse width - 9
        if sub_DB.Compliance_Form._DataGridView.Rows[9].Cells[0].Value:
            time.sleep(1)
            checking_item = "input pulse width"
            try:                
                sub_DB.Cal_Form._Label_Vref.Text = "Checking %s" % checking_item
                sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
                sub_DB.Cal_Form.Refresh()
                Log("            = Check %s : Start" % checking_item)
                # TODO : Input pulse width
                Log("            = Check %s : Done" % checking_item)

            except Exception as e:
                Log("            = Check %s : Failed" % checking_item)
                Log(traceback.format_exc())
                MessageBox.Show("Compliance test - Check %s failed" % checking_item,"Warning")
                EXIT()

        # Valid transition time - 10
        if sub_DB.Compliance_Form._DataGridView.Rows[10].Cells[0].Value:
            time.sleep(1)
            checking_item = "valid transition time"
            try:                
                sub_DB.Cal_Form._Label_Vref.Text = "Checking %s" % checking_item
                sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
                sub_DB.Cal_Form.Refresh()
                Log("            = Check %s : Start" % checking_item)
                # TODO : Valid transition time
                Log("            = Check %s : Done" % checking_item)

            except Exception as e:
                Log("            = Check %s : Failed" % checking_item)
                Log(traceback.format_exc())
                MessageBox.Show("Compliance test - Check %s failed" % checking_item,"Warning")
                EXIT()

        # Differential input low/high pusle width - 11 & 12
        if sub_DB.Compliance_Form._DataGridView.Rows[11].Cells[0].Value:
            time.sleep(1)
            checking_item = "diff. input low/high pusle width"
            try:                
                sub_DB.Cal_Form._Label_Vref.Text = "Checking %s" % checking_item
                sub_DB.Cal_Form._ProgressBar_Vref.Value += 2
                sub_DB.Cal_Form.Refresh()
                Log("            = Check %s : Start" % checking_item)
                # TODO : Differential input low/high pusle width
                Log("            = Check %s : Done" % checking_item)

            except Exception as e:
                Log("            = Check %s : Failed" % checking_item)
                Log(traceback.format_exc())
                MessageBox.Show("Compliance test - Check %s failed" % checking_item,"Warning")
                EXIT()

        # Average & absolute clock period - 13 & 16
        if sub_DB.Compliance_Form._DataGridView.Rows[13].Cells[0].Value:
            time.sleep(1)
            checking_item = "average & absolute clock period"
            try:                
                sub_DB.Cal_Form._Label_Vref.Text = "Checking %s" % checking_item
                sub_DB.Cal_Form._ProgressBar_Vref.Value += 2
                sub_DB.Cal_Form.Refresh()
                Log("            = Check %s : Start" % checking_item)
                # TODO : Average & absolute clock period
                Log("            = Check %s : Done" % checking_item)

            except Exception as e:
                Log("            = Check %s : Failed" % checking_item)
                Log(traceback.format_exc())
                MessageBox.Show("Compliance test - Check %s failed" % checking_item,"Warning")
                EXIT()

        # Average & absolute clock low/high pulse width - 14, 15, 17, & 18
        if sub_DB.Compliance_Form._DataGridView.Rows[14].Cells[0].Value:
            time.sleep(1)
            checking_item = "average & absolute clock low/high pulse width"
            try:                
                sub_DB.Cal_Form._Label_Vref.Text = "Checking %s" % checking_item
                sub_DB.Cal_Form._ProgressBar_Vref.Value += 4
                sub_DB.Cal_Form.Refresh()
                Log("            = Check %s : Start" % checking_item)
                # TODO : Average & absolute clock low/high pulse width
                Log("            = Check %s : Done" % checking_item)

            except Exception as e:
                Log("            = Check %s : Failed" % checking_item)
                Log(traceback.format_exc())
                MessageBox.Show("Compliance test - Check %s failed" % checking_item,"Warning")
                EXIT()

        # clock period jitter & clock cycle to cycle period jitter - 19 & 20
        if sub_DB.Compliance_Form._DataGridView.Rows[19].Cells[0].Value:
            time.sleep(1)
            checking_item = "clock period jitter & clock cycle to cycle period jitter"
            try:                
                sub_DB.Cal_Form._Label_Vref.Text = "Checking %s" % checking_item
                sub_DB.Cal_Form._ProgressBar_Vref.Value += 2
                sub_DB.Cal_Form.Refresh()
                Log("            = Check %s : Start" % checking_item)
                # TODO : Clock period jitter & clock cycle to cycle period jitter
                Log("            = Check %s : Done" % checking_item)

            except Exception as e:
                Log("            = Check %s : Failed" % checking_item)
                Log(traceback.format_exc())
                MessageBox.Show("Compliance test - Check %s failed" % checking_item,"Warning")
                EXIT()

        # Allowed time before ringback for DQS - 21
        if sub_DB.Compliance_Form._DataGridView.Rows[21].Cells[0].Value:
            time.sleep(1)
            checking_item = "allowed time before ringback for DQS"
            try:                
                sub_DB.Cal_Form._Label_Vref.Text = "Checking %s" % checking_item
                sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
                sub_DB.Cal_Form.Refresh()
                Log("            = Check %s : Start" % checking_item)
                # TODO : Allowed time before ringback for DQS
                Log("            = Check %s : Done" % checking_item)

            except Exception as e:
                Log("            = Check %s : Failed" % checking_item)
                Log(traceback.format_exc())
                MessageBox.Show("Compliance test - Check %s failed" % checking_item,"Warning")
                EXIT()

        # Single-ended low/high level for strobes - 22 & 23
        if sub_DB.Compliance_Form._DataGridView.Rows[22].Cells[0].Value:
            time.sleep(1)
            checking_item = "single-ended low/high level for strobes"
            try:                
                sub_DB.Cal_Form._Label_Vref.Text = "Checking %s" % checking_item
                sub_DB.Cal_Form._ProgressBar_Vref.Value += 2
                sub_DB.Cal_Form.Refresh()
                Log("            = Check %s : Start" % checking_item)
                # TODO : Single-ended low/high level for strobes
                Log("            = Check %s : Done" % checking_item)

            except Exception as e:
                Log("            = Check %s : Failed" % checking_item)
                Log(traceback.format_exc())
                MessageBox.Show("Compliance test - Check %s failed" % checking_item,"Warning")
                EXIT()

        # Differential input cross point voltage DQS - 24
        if sub_DB.Compliance_Form._DataGridView.Rows[24].Cells[0].Value:
            time.sleep(1)
            checking_item = "diff. input cross point voltage DQS"
            try:                
                sub_DB.Cal_Form._Label_Vref.Text = "Checking %s" % checking_item
                sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
                sub_DB.Cal_Form.Refresh()
                Log("            = Check %s : Start" % checking_item)
                # TODO : Differential input cross point voltage DQS
                Log("            = Check %s : Done" % checking_item)

            except Exception as e:
                Log("            = Check %s : Failed" % checking_item)
                Log(traceback.format_exc())
                MessageBox.Show("Compliance test - Check %s failed" % checking_item,"Warning")
                EXIT()

        # Allowed time before ringback for CLK - 25
        if sub_DB.Compliance_Form._DataGridView.Rows[25].Cells[0].Value:
            time.sleep(1)
            checking_item = "allowed time before ringback for CLK"
            try:                
                sub_DB.Cal_Form._Label_Vref.Text = "Checking %s" % checking_item
                sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
                sub_DB.Cal_Form.Refresh()
                Log("            = Check %s : Start" % checking_item)
                # TODO : Allowed time before ringback for CLK
                Log("            = Check %s : Done" % checking_item)

            except Exception as e:
                Log("            = Check %s : Failed" % checking_item)
                Log(traceback.format_exc())
                MessageBox.Show("Compliance test - Check %s failed" % checking_item,"Warning")
                EXIT()

        # Single-ended low/high level for CLK - 26 & 27
        if sub_DB.Compliance_Form._DataGridView.Rows[26].Cells[0].Value:
            time.sleep(1)
            checking_item = "single-ended low/high level for CLK"
            try:                
                sub_DB.Cal_Form._Label_Vref.Text = "Checking %s" % checking_item
                sub_DB.Cal_Form._ProgressBar_Vref.Value += 2
                sub_DB.Cal_Form.Refresh()
                Log("            = Check %s : Start" % checking_item)
                # TODO : Single-ended low/high level for CLK
                Log("            = Check %s : Done" % checking_item)

            except Exception as e:
                Log("            = Check %s : Failed" % checking_item)
                Log(traceback.format_exc())
                MessageBox.Show("Compliance test - Check %s failed" % checking_item,"Warning")
                EXIT()

        # Differential input cross point voltage CLK - 28
        if sub_DB.Compliance_Form._DataGridView.Rows[28].Cells[0].Value:
            time.sleep(1)
            checking_item = "diff. input cross point voltage CLK"
            try:                
                sub_DB.Cal_Form._Label_Vref.Text = "Checking %s" % checking_item
                sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
                sub_DB.Cal_Form.Refresh()
                Log("            = Check %s : Start" % checking_item)
                # TODO : Differential input cross point voltage CLK
                Log("            = Check %s : Done" % checking_item)

            except Exception as e:
                Log("            = Check %s : Failed" % checking_item)
                Log(traceback.format_exc())
                MessageBox.Show("Compliance test - Check %s failed" % checking_item,"Warning")
                EXIT()

        # Average of Vref(t) - 29
        if sub_DB.Compliance_Form._DataGridView.Rows[29].Cells[0].Value:
            time.sleep(1)
            checking_item = "average of Vref(t)"
            try:                
                sub_DB.Cal_Form._Label_Vref.Text = "Checking %s" % checking_item
                sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
                sub_DB.Cal_Form.Refresh()
                Log("            = Check %s : Start" % checking_item)
                # TODO : Average of Vref(t)
                Log("            = Check %s : Done" % checking_item)

            except Exception as e:
                Log("            = Check %s : Failed" % checking_item)
                Log(traceback.format_exc())
                MessageBox.Show("Compliance test - Check %s failed" % checking_item,"Warning")
                EXIT()

    ##########
	#  DDR4  #
	##########
    if self._ComboBox_DDRGen.Text == "DDR4":
        # TODO : Compliance test for DDR4
        pass

    ##########
	#  DDR5  #
	##########
    if self._ComboBox_DDRGen.Text == "DDR5":
        # TODO : Compliance test for DDR5
        pass

    return Result

def Comp_Test_DDR3_DQ_SetupHold(Waveform, self):
    #############
    # Set Spec. #
    #############
    AC_V = float(self._ComboBox_AC_DQ.Text)
    DC_V = float(self._TextBox_DC_DQ.Text)
    Vref = float(self._TextBox_Vref.Text)
    Datarate = float(self._ComboBox_DataRate.Text)

    V_IHdiff_min = 200 #[mV]
    V_ILdiff_max = -200 #[mV]
    V_IHdiff_AC_min = 2*AC_V #[mV]
    V_ILdiff_AC_max = -2*AC_V #[mV]

    setup_base = sub_DB.Spec["DQ Setup Base"]["AC" + str(int(AC_V))][str(int(Datarate))]
    hold_base = sub_DB.Spec["DQ Hold Base"]["DC" + str(int(DC_V))][str(int(Datarate))]

    ###########################################
    # Set Target Net & Reference Net Wavefrom #
    ###########################################
    Target_net = {}
    Ref_net = {}
    for net in Waveform.keys():
        Group_idx, Match = Net_Identify(net.strip(), Uenv) # Match = "Group prefix / Net Number prefix"
        if Group_idx == 1: # DQ
            Target_net[Match] = Waveform[net]
        elif Group_idx == 2: # DQS_P
            pos = Waveform[net]
            Ref_key = Match
        elif Group_idx == 3: # DQS_N
            neg = Waveform[net]
    Ref_net[Ref_key] = [i-j for i, j in zip(pos,neg)]

    ######################################################
    # Find Zero Crossing Points and Slew Rate for Strobe #
    ######################################################
    Zero_crossing = []
    DQS_slew = []
    for time_idx in range(int(float(sub_DB.Option_Form._TextBox_EyeOffset.Text)*1000), len(Ref_net[Ref_key]) - 1):
        # for rising transition
        if float(Ref_net[Ref_key][time_idx]) < 0 and float(Ref_net[Ref_key][time_idx+1]) > 0:
            # Get Zero crossing point
            Zero_crossing.append(time_idx)

            # Get slew rate for t1
            temp_idx = time_idx
            while(1):
                if float(Ref_net[Ref_key][temp_idx]) > V_ILdiff_max and float(Ref_net[Ref_key][temp_idx-1]) < V_ILdiff_max:
                    t1 = temp_idx
                    break
                temp_idx -= 1

            # Get slew rate for t2
            temp_idx = time_idx
            while(1):
                if float(Ref_net[Ref_key][temp_idx]) < V_IHdiff_min and float(Ref_net[Ref_key][temp_idx+1]) > V_IHdiff_min:
                    t2 = temp_idx
                    break
                temp_idx +=1

            # Set slew rate
            slew = float(V_IHdiff_min-V_ILdiff_max)/float(t2-t1)            
            if slew >= 4.0:
                DQS_slew.append("4.0")
            elif slew >= 3.0:
                DQS_slew.append("3.0")
            elif slew >= 2.0:
                DQS_slew.append("2.0")
            elif slew >= 1.8:
                DQS_slew.append("1.8")
            elif slew >= 1.6:
                DQS_slew.append("1.6")
            elif slew >= 1.4:
                DQS_slew.append("1.4")
            elif slew >= 1.2:
                DQS_slew.append("1.2")
            else:
                DQS_slew.append("1.0")

        # for falling transition
        if float(Ref_net[Ref_key][time_idx]) > 0 and float(Ref_net[Ref_key][time_idx+1]) < 0:
            # Get Zero crossing point
            Zero_crossing.append(time_idx)

            # Get slew rate for t1
            temp_idx = time_idx
            while(1):
                if float(Ref_net[Ref_key][temp_idx]) < V_IHdiff_min and float(Ref_net[Ref_key][temp_idx-1]) > V_IHdiff_min:
                    t1 = temp_idx
                    break
                temp_idx -=1

            # Get slew rate for t2
            temp_idx = time_idx
            while(1):
                if float(Ref_net[Ref_key][temp_idx]) > V_ILdiff_max and float(Ref_net[Ref_key][temp_idx+1]) < V_ILdiff_max:
                    t2 = temp_idx
                    break
                temp_idx += 1

            # Set slew rate
            slew = float(V_IHdiff_min-V_ILdiff_max)/float(t2-t1)            
            if slew >= 4.0:
                DQS_slew.append("4.0")
            elif slew >= 3.0:
                DQS_slew.append("3.0")
            elif slew >= 2.0:
                DQS_slew.append("2.0")
            elif slew >= 1.8:
                DQS_slew.append("1.8")
            elif slew >= 1.6:
                DQS_slew.append("1.6")
            elif slew >= 1.4:
                DQS_slew.append("1.4")
            elif slew >= 1.2:
                DQS_slew.append("1.2")
            else:
                DQS_slew.append("1.0")

    ######################
    # Measure Setup/Hold #
    ######################
    Setup_Result = {}
    Hold_Result = {}
    # for each Target net
    for key in Target_net.keys():
        time_idx = int(float(sub_DB.Option_Form._TextBox_EyeOffset.Text)*1000)
        zero_idx = 0    
        Setup_Result[key] = []
        Hold_Result[key] = []        
        net = Target_net[key]
        while(1):
            # Detect Transition - Rising
            if float(net[time_idx-1]) < Vref and float(net[time_idx]) > Vref:
                # Initialize Spec., default = False
                temp_setup_result = []
                temp_hold_result = []                
                temp_setup_result.append(False) #[0] - Spec. In/Out
                temp_hold_result.append(False) #[0] - Spec. In/Out

                transition = "Rising"                
                # Find zero crossing point
                while(1):
                    if Zero_crossing[zero_idx] > time_idx:
                        t0_s = Zero_crossing[zero_idx]
                        t0_s_slew = DQS_slew[zero_idx]
                        t0_h = Zero_crossing[zero_idx-1]
                        t0_h_slew = DQS_slew[zero_idx-1]
                        break
                    zero_idx += 1
                temp_setup_result.append(t0_s) #[1] - Reference time
                temp_hold_result.append(t0_h) #[1] - Reference time

                # Find Hold Time                
                temp_idx = t0_h
                while(1):
                    temp_idx += 1
                    if float(net[temp_idx-1]) < Vref - DC_V and float(net[temp_idx]) > Vref - DC_V:
                        t_h = temp_idx - t0_h
                        break                
                temp_hold_result.append(temp_idx) #[2] - Sampled time
                temp_hold_result.append(t_h) #[3] - Measured hold time

                # Calculate slew rate & waveform type for hold
                temp_idx = time_idx
                while(1):
                    if float(net[temp_idx]) < Vref - DC_V:
                        break
                    temp_idx -= 1
                slew = float(DC_V)/float(time_idx-temp_idx)

                iter = 0
                wave_type = "nominal"
                for i in range(temp_idx, time_idx):
                    v_slew_now = Vref - DC_V + iter * slew
                    v_wave_now = net[i]
                    v_slew_next = Vref - DC_V + (iter+1) * slew
                    v_wave_next = net[i+1]
                    if (v_slew_now-v_wave_now)*(v_slew_next-v_wave_next) < 0:
                        wave_type = "tangent"
                        break
                    iter += 1
                    
                if slew >= 2.0:
                    dq_hold_slew = "2.0"
                elif slew >= 1.5:
                    dq_hold_slew = "1.5"
                elif slew >= 1.0:
                    dq_hold_slew = "1.0"
                elif slew >= 0.9:
                    dq_hold_slew = "0.9"
                elif slew >= 0.8:
                    dq_hold_slew = "0.8"
                elif slew >= 0.7:
                    dq_hold_slew = "0.7"
                elif slew >= 0.6:
                    dq_hold_slew = "0.6"
                elif slew >= 0.5:
                    dq_hold_slew = "0.5"
                elif slew >= 0.4:
                    dq_hold_slew = "0.4"

                # Find Setup Time                
                temp_idx = time_idx
                while(1):
                    temp_idx += 1
                    if float(net[temp_idx-1]) < Vref + AC_V and float(net[temp_idx]) > Vref + AC_V:
                        t_s = t0_s - temp_idx
                        break
                temp_setup_result.append(temp_idx) #[2] - Sampled time
                temp_setup_result.append(t_s) #[3] - Measured setup time

                # Calculate slew rate and waveform type for setup
                temp_idx = time_idx
                while(1):
                    if float(net[temp_idx]) > Vref + AC_V:
                        break
                    temp_idx += 1
                slew = float(AC_V)/float(temp_idx-time_idx)

                iter = 0
                wave_type = "nominal"
                for i in range(time_idx, temp_idx):
                    v_slew_now = Vref + iter * slew
                    v_wave_now = net[i]
                    v_slew_next = Vref + (iter+1) * slew
                    v_wave_next = net[i+1]
                    if (v_slew_now-v_wave_now)*(v_slew_next-v_wave_next) < 0:
                        wave_type = "tangent"
                        break

                if slew >= 2.0:
                    dq_setup_slew = "2.0"
                elif slew >= 1.5:
                    dq_setup_slew = "1.5"
                elif slew >= 1.0:
                    dq_setup_slew = "1.0"
                elif slew >= 0.9:
                    dq_setup_slew = "0.9"
                elif slew >= 0.8:
                    dq_setup_slew = "0.8"
                elif slew >= 0.7:
                    dq_setup_slew = "0.7"
                elif slew >= 0.6:
                    dq_setup_slew = "0.6"
                elif slew >= 0.5:
                    dq_setup_slew = "0.5"
                elif slew >= 0.4:
                    dq_setup_slew = "0.4"

                setup_derating = sub_DB.Spec["DQ Setup Derating"]["AC" + str(int(AC_V))][str(int(Datarate))][t0_s_slew][dq_setup_slew]
                hold_derating = sub_DB.Spec["DQ Hold Derating"]["AC" + str(int(AC_V))][str(int(Datarate))][t0_h_slew][dq_hold_slew]

                temp_hold_result.append(float(hold_base)+float(hold_derating)) #[4] - hold time spec
                temp_hold_result.append(hold_base) #[5] - base hold time
                temp_hold_result.append(hold_derating) #[6] - derating for hold time
                temp_hold_result.append(t0_h_slew) #[7] - slew for DQS
                temp_hold_result.append(dq_hold_slew) #[8] - slew for DQ
                temp_hold_result.append(transition) #[9] - transition
                temp_hold_result.append(wave_type) #[10] - waveform type
                if temp_hold_result[3] >= temp_hold_result[4]:
                    temp_hold_result[0] = True

                temp_setup_result.append(float(setup_base)+float(setup_derating)) #[4] - setup time spec
                temp_setup_result.append(setup_base) #[5] - base setup time
                temp_setup_result.append(setup_derating) #[6] - derating for setup time
                temp_setup_result.append(t0_s_slew) #[7] - slew for DQS
                temp_setup_result.append(dq_setup_slew) #[8] - slew for DQ
                temp_setup_result.append(transition) #[9] - transition
                temp_setup_result.append(wave_type) #[10] - waveform type
                if temp_setup_result[3] >= temp_setup_result[4]:
                    temp_setup_result[0] = True

                Setup_Result[key].append(temp_setup_result)
                Hold_Result[key].append(temp_hold_result)                

            # Detect Transition - Falling
            elif float(net[time_idx-1]) > Vref and float(net[time_idx]) < Vref:
                # Initialize Spec., default = False
                temp_setup_result = []
                temp_hold_result = []                
                temp_setup_result.append(False) #[0] - Spec. In/Out
                temp_hold_result.append(False) #[0] - Spec. In/Out

                transition = "Falling"                
                # Find zero crossing point
                while(1):
                    if Zero_crossing[zero_idx] > time_idx:
                        t0_s = Zero_crossing[zero_idx]
                        t0_s_slew = DQS_slew[zero_idx]
                        t0_h = Zero_crossing[zero_idx-1]
                        t0_h_slew = DQS_slew[zero_idx-1]
                        break
                    zero_idx += 1
                temp_setup_result.append(t0_s) #[1] - Reference time
                temp_hold_result.append(t0_h) #[1] - Reference time

                # Find Hold Time                
                temp_idx = t0_h
                while(1):
                    temp_idx += 1
                    if float(net[temp_idx-1]) > Vref + DC_V and float(net[temp_idx]) < Vref + DC_V:
                        t_h = temp_idx - t0_h
                        break
                temp_hold_result.append(temp_idx) #[2] - Sampled time
                temp_hold_result.append(t_h) #[3] - Measured hold time

                # Calculate slew rate & waveform type for hold
                temp_idx = time_idx
                while(1):
                    if float(net[temp_idx]) > Vref + DC_V:
                        break
                    temp_idx -= 1
                slew = float(DC_V)/float(time_idx-temp_idx)

                iter = 0
                wave_type = "nominal"
                for i in range(temp_idx, time_idx):
                    v_slew_now = Vref + DC_V - iter * slew
                    v_wave_now = net[i]
                    v_slew_next = Vref + DC_V - (iter+1) * slew
                    v_wave_next = net[i+1]
                    if (v_slew_now-v_wave_now)*(v_slew_next-v_wave_next) < 0:
                        wave_type = "tangent"
                        break
                    iter += 1

                if slew >= 2.0:
                    dq_hold_slew = "2.0"
                elif slew >= 1.5:
                    dq_hold_slew = "1.5"
                elif slew >= 1.0:
                    dq_hold_slew = "1.0"
                elif slew >= 0.9:
                    dq_hold_slew = "0.9"
                elif slew >= 0.8:
                    dq_hold_slew = "0.8"
                elif slew >= 0.7:
                    dq_hold_slew = "0.7"
                elif slew >= 0.6:
                    dq_hold_slew = "0.6"
                elif slew >= 0.5:
                    dq_hold_slew = "0.5"
                elif slew >= 0.4:
                    dq_hold_slew = "0.4"

                # Find Setup Time                
                temp_idx = time_idx
                while(1):
                    temp_idx += 1
                    if float(net[temp_idx-1]) > Vref - AC_V and float(net[temp_idx]) < Vref - AC_V:
                        t_s = t0_s - temp_idx
                        break
                temp_setup_result.append(temp_idx) #[2] - Sampled time
                temp_setup_result.append(t_s) #[3] - Measured setup time

                # Calculate slew rate and waveform type for setup
                temp_idx = time_idx
                while(1):
                    if float(net[temp_idx]) < Vref - AC_V:
                        break
                    temp_idx += 1
                slew = float(AC_V)/float(temp_idx-time_idx)

                iter = 0
                wave_type = "nominal"
                for i in range(time_idx, temp_idx):
                    v_slew_now = Vref - iter * slew
                    v_wave_now = net[i]
                    v_slew_next = Vref - (iter+1) * slew
                    v_wave_next = net[i+1]
                    if (v_slew_now-v_wave_now)*(v_slew_next-v_wave_next) < 0:
                        wave_type = "tangent"
                        break

                if slew >= 2.0:
                    dq_setup_slew = "2.0"
                elif slew >= 1.5:
                    dq_setup_slew = "1.5"
                elif slew >= 1.0:
                    dq_setup_slew = "1.0"
                elif slew >= 0.9:
                    dq_setup_slew = "0.9"
                elif slew >= 0.8:
                    dq_setup_slew = "0.8"
                elif slew >= 0.7:
                    dq_setup_slew = "0.7"
                elif slew >= 0.6:
                    dq_setup_slew = "0.6"
                elif slew >= 0.5:
                    dq_setup_slew = "0.5"
                elif slew >= 0.4:
                    dq_setup_slew = "0.4"

                setup_derating = sub_DB.Spec["DQ Setup Derating"]["AC" + str(int(AC_V))][str(int(Datarate))][t0_s_slew][dq_setup_slew]
                hold_derating = sub_DB.Spec["DQ Hold Derating"]["AC" + str(int(AC_V))][str(int(Datarate))][t0_h_slew][dq_hold_slew]

                temp_hold_result.append(float(hold_base)+float(hold_derating)) #[4] - hold time spec
                temp_hold_result.append(hold_base) #[5] - base hold time
                temp_hold_result.append(hold_derating) #[6] - derating for hold time
                temp_hold_result.append(t0_h_slew) #[7] - slew for DQS
                temp_hold_result.append(dq_hold_slew) #[8] - slew for DQ
                temp_hold_result.append(transition) #[9] - transition
                temp_hold_result.append(wave_type) #[10] - waveform type
                if temp_hold_result[3] >= temp_hold_result[4]:
                    temp_hold_result[0] = True

                temp_setup_result.append(float(setup_base)+float(setup_derating)) #[4] - setup time spec
                temp_setup_result.append(setup_base) #[5] - base setup time
                temp_setup_result.append(setup_derating) #[6] - derating for setup time
                temp_setup_result.append(t0_s_slew) #[7] - slew for DQS
                temp_setup_result.append(dq_setup_slew) #[8] - slew for DQ
                temp_setup_result.append(transition) #[9] - transition
                temp_setup_result.append(wave_type) #[10] - waveform type
                if temp_setup_result[3] >= temp_setup_result[4]:
                    temp_setup_result[0] = True

                Setup_Result[key].append(temp_setup_result)
                Hold_Result[key].append(temp_hold_result)                
                
            time_idx += 1

            # quit while
            if time_idx >= Zero_crossing[len(Zero_crossing)-1]:                
                break

    return Setup_Result, Hold_Result

def Excel_Report(Result):
    try:        
        for item in Result.keys():
            xlApp = Excel.ApplicationClass()
            xlApp.Caption = sub_DB.File.split("\\")[-1].split(".")[0] + ": Compliance test - %s" % item
            xlApp.Visible = True
            xlApp.DisplayAlerts = False	
            xlbook = xlApp.Workbooks.Add()

            if item == "Data Setup Time" or item == "Data Hold Time":
                try:
                    # Create Worksheet
                    net_list = sort_list(Result[item].keys())
                    for i in range(len(net_list)-1,-1,-1):
                        xlsheet = xlbook.Worksheets.Add()
                        xlsheet.Name = net_list[i]
                
                        # Create Column Header
                        if "Setup" in item:
                            xlsheet.Cells[1,1] = "Spec. In/Out"
                            xlsheet.Cells[1,2] = "tDS [ps]\n(meas.)"
                            xlsheet.Cells[1,5] = "tDS [ps]\n(spec.)"
                            xlsheet.Cells[1,10] = "Transition"
                            xlsheet.Cells[1,11] = "Waveform Type"

                            xlsheet.Cells[2,2] = "tREF"
                            xlsheet.Cells[2,3] = "tSample"
                            xlsheet.Cells[2,4] = "tDS_meas"
                            xlsheet.Cells[2,5] = "tDS_spec"
                            xlsheet.Cells[2,6] = "tDS_base"
                            xlsheet.Cells[2,7] = u"\u0394" + "tDS"
                            xlsheet.Cells[2,8] = "Slew Rate"

                            xlsheet.Cells[3,8] = "Strobe"
                            xlsheet.Cells[3,9] = "Data"

                        elif "Hold" in item:
                            xlsheet.Cells[1,1] = "Spec. In/Out"
                            xlsheet.Cells[1,2] = "tDH [ps]\n(meas.)"
                            xlsheet.Cells[1,5] = "tDH [ps]\n(spec.)"
                            xlsheet.Cells[1,10] = "Transition"
                            xlsheet.Cells[1,11] = "Waveform Type"

                            xlsheet.Cells[2,2] = "tREF"
                            xlsheet.Cells[2,3] = "tSample"
                            xlsheet.Cells[2,4] = "tDH_meas"
                            xlsheet.Cells[2,5] = "tDH_spec"
                            xlsheet.Cells[2,6] = "tDH_base"
                            xlsheet.Cells[2,7] = u"\u0394" + "tDH"
                            xlsheet.Cells[2,8] = "Slew Rate"

                            xlsheet.Cells[3,8] = "Strobe"
                            xlsheet.Cells[3,9] = "Data"

                        # Merge Column Header
                        Merge_Cell = xlsheet.Range[xlsheet.Cells[1, 1], xlsheet.Cells[3, 1]]
                        Merge_Cell.Merge(False)
                        Merge_Cell.Cells.HorizontalAlignment = Excel.XlHAlign.xlHAlignCenter
                        Merge_Cell.Cells.VerticalAlignment = Excel.XlHAlign.xlHAlignCenter

                        Merge_Cell = xlsheet.Range[xlsheet.Cells[1, 2], xlsheet.Cells[1, 4]]
                        Merge_Cell.Merge(False)
                        Merge_Cell.Cells.HorizontalAlignment = Excel.XlHAlign.xlHAlignCenter
                        Merge_Cell.Cells.VerticalAlignment = Excel.XlHAlign.xlHAlignCenter

                        Merge_Cell = xlsheet.Range[xlsheet.Cells[1, 5], xlsheet.Cells[1, 9]]
                        Merge_Cell.Merge(False)
                        Merge_Cell.Cells.HorizontalAlignment = Excel.XlHAlign.xlHAlignCenter
                        Merge_Cell.Cells.VerticalAlignment = Excel.XlHAlign.xlHAlignCenter

                        Merge_Cell = xlsheet.Range[xlsheet.Cells[1, 10], xlsheet.Cells[3, 10]]
                        Merge_Cell.Merge(False)
                        Merge_Cell.Cells.HorizontalAlignment = Excel.XlHAlign.xlHAlignCenter
                        Merge_Cell.Cells.VerticalAlignment = Excel.XlHAlign.xlHAlignCenter

                        Merge_Cell = xlsheet.Range[xlsheet.Cells[1, 11], xlsheet.Cells[3, 11]]
                        Merge_Cell.Merge(False)
                        Merge_Cell.Cells.HorizontalAlignment = Excel.XlHAlign.xlHAlignCenter
                        Merge_Cell.Cells.VerticalAlignment = Excel.XlHAlign.xlHAlignCenter

                        for i in range(2, 8):
                            Merge_Cell = xlsheet.Range[xlsheet.Cells[2, i], xlsheet.Cells[3, i]]
                            Merge_Cell.Merge(False)
                            Merge_Cell.Cells.HorizontalAlignment = Excel.XlHAlign.xlHAlignCenter
                            Merge_Cell.Cells.VerticalAlignment = Excel.XlHAlign.xlHAlignCenter

                        Merge_Cell = xlsheet.Range[xlsheet.Cells[2, 8], xlsheet.Cells[2, 9]]
                        Merge_Cell.Merge(False)
                        Merge_Cell.Cells.HorizontalAlignment = Excel.XlHAlign.xlHAlignCenter
                        Merge_Cell.Cells.VerticalAlignment = Excel.XlHAlign.xlHAlignCenter
                
                        # Set font, boarder, back color for column header                
                        Col_Header = xlsheet.Range[xlsheet.Cells[1, 1], xlsheet.Cells[3, 11]]
                
                        # Set Column Font
                        Col_Header.Font.Name = "Arial"
                        Col_Header.Font.Size = 11
                        Col_Header.Font.Bold = True
                        #Col_Header.Font.Italic = False
                        #Col_Header.Font.Underline = False
                        #Col_Header.Font.Strikethrough = False
                        #Col_Header.Font.Color = Color.FromArgb(0,0,0)
                
                        # Set Column Border
                        Col_Header.Borders.LineStyle = Excel.XlLineStyle.xlContinuous
                        Col_Header.Borders.Weight = Excel.XlBorderWeight.xlThin
                
                        # Set Column Back Color
                        Col_Header.Interior.Color = Color.FromArgb(218,240,254)

                        # Add Rows - Compliance Test Results
                        row_idx = 4                                                 
                        for j in range(0, len(Result[item][net_list[i]])):
                            for k in range(0,11):                                
                                xlsheet.Cells[row_idx+j,k+1] = Result[item][net_list[i]][j][k]

                        # Set Result Column font & back color
                        Result_Cell = xlsheet.Range[xlsheet.Cells[4, 4], xlsheet.Cells[len(Result[item][net_list[i]]), 5]]
                        Result_Cell.Font.Name = "Arial"
                        Result_Cell.Font.Size = 11
                        Result_Cell.Font.Bold = True
                        Result_Cell.Interior.Color = Color.FromArgb(255,255,139)

                        # Set Result Cell borders and autofit
                        Result_Cell = xlsheet.Range[xlsheet.Cells[4, 1], xlsheet.Cells[len(Result[item][net_list[i]])+row_idx-1, 11]]
                        Result_Cell.Borders.LineStyle = Excel.XlLineStyle.xlContinuous
                        Result_Cell.Borders.Weight = Excel.XlBorderWeight.xlThin

                        # Final Autofit
                        Result_Cell = xlsheet.Range[xlsheet.Cells[1, 1], xlsheet.Cells[len(Result[item][net_list[i]])+row_idx-1, 11]]
                        Result_Cell.Columns.AutoFit()

                    if "Setup" in item:
                        Log("            = Data setup time report has been generated")
                    elif "Hold" in item:
                        Log("            = Data hold time report has been generated")

                except Exception as e:
                    Log("            = Fail to create data setup report")
                    Log(traceback.format_exc())
                    MessageBox.Show("Fail to create data setup report","Warning")
                    EXIT()

            #if item == "Data Hold Time":
            #    print "HOLD"

            xlApp.DisplayAlerts = True                
            ReleaseObject(Merge_Cell)
            ReleaseObject(Col_Header)
            ReleaseObject(xlsheet)
            ReleaseObject(xlbook)
            ReleaseObject(xlApp)

    except Exception as e:
        Log("	<Create Excel Report> = Failed")
        Log(traceback.format_exc())
        MessageBox.Show("Fail to create excel report","Warning")
        EXIT()
        
    
    
    

def Create_Excel_Report():
	try:
		xlApp = Excel.ApplicationClass()
		xlApp.Caption = sub_DB.File.split("\\")[-1].split(".")[0]		
		xlApp.Visible = True
		xlApp.DisplayAlerts = False	

		xlbook = xlApp.Workbooks.Add()
	
		# Create Eye Diagram Image Report Worksheet
		xlsheet = xlbook.Worksheets['Sheet1']
		xlsheet.Name = "EYE Diagrams"
		Log("		(Launch Excel) = Done")

		#Save_File = sub_DB.Option_Form._TextBox_OutputExcelFile.Text

		imgw = int(sub_DB.Option_Form._TextBox_ImageWidth.Text)
		imgh = imgw / 5 * 4
		for i in range(0, len(sub_DB.Excel_Img_File)):
			j = (i-4*(int(i/4)))*imgw
			k = int(i/4)*imgh
			last_k = k

			insert_img = sub_DB.Excel_Img_File[i]
			xlApp.ActiveSheet.Shapes.AddPicture(insert_img, False, True, j, k, imgw, imgh)
			#os.remove(insert_img)
		Log("		(Add Image) = Done")

		#	Eye_Measure_Results[Trace_Name][0] = Width
		#	Jitter_RMS[Trance_Name] = Exported Value from eye measurement
		#	Eye_Measure_Results[Trace_Name][1] = Jitter
		#	Eye_Measure_Results[Trace_Name][2] = Margin

		# Create Eye Measurement Table Worksheet
		xlsheet_table = xlbook.Worksheets.Add()
		xlsheet_table.Name = "EYE Measure Results"

		# Create Column
		xlsheet_table.Cells[1,1] = ""
		xlsheet_table.Cells[1,2] = "Analyze Group"
		xlsheet_table.Cells[1,3] = "Width [ps]"
		xlsheet_table.Cells[1,4] = "Jitter_RMS [ps]"
		xlsheet_table.Cells[1,5] = "Jitter [ps]"
		xlsheet_table.Cells[1,6] = "Timin Margin [ps]"
		xlsheet_table.Cells[1,7] = "Vcent_DQ [mV]"
		Log("		(Create Column) = Done")

		# Create Column Range
		Col_Header = xlsheet_table.Range[xlsheet_table.Cells[1, 1], xlsheet_table.Cells[1, 7]]

		# Set Column Font
		Col_Header.Font.Name = "Arial"
		Col_Header.Font.Size = 11
		Col_Header.Font.Bold = True
		#Col_Header.Font.Italic = False
		#Col_Header.Font.Underline = False
		#Col_Header.Font.Strikethrough = False
		#Col_Header.Font.Color = Color.FromArgb(0,0,0)
		Log("		(Set Column Font) = Done")

		# Set Column Border
		Col_Header.Borders.LineStyle = Excel.XlLineStyle.xlContinuous
		Col_Header.Borders.Weight = Excel.XlBorderWeight.xlThin
		Log("		(Set Column Border) = Done")
	
		# Set Column Back Color
		Col_Header.Interior.Color = Color.FromArgb(218,240,254)
		Log("		(Set Column Color) = Done")

		# Add Rows - Eye Measurement Results
		row_idx = 2
		for row in sub_DB.Net_Form._DataGridView.Rows:
			if row.Cells[0].Value:
				net_name = row.Cells[1].Value
				xlsheet_table.Cells[row_idx,1] = net_name
				xlsheet_table.Cells[row_idx,2] = row.Cells[4].Value
				xlsheet_table.Cells[row_idx,3] = sub_DB.Eye_Measure_Results[net_name][0] # Width
				xlsheet_table.Cells[row_idx,4] = round(sub_DB.Jitter_RMS[net_name], 1) # Jitter_RMS
				xlsheet_table.Cells[row_idx,5] = sub_DB.Eye_Measure_Results[net_name][1] # Jitter
				xlsheet_table.Cells[row_idx,6] = sub_DB.Eye_Measure_Results[net_name][2] # Margin
				xlsheet_table.Cells[row_idx,7] = round(sub_DB.Vref, 1) # Vref
				row_idx += 1
		row_idx -= 1
		Log("		(Add Data) = Done")

		# Create Row Range
		Row_Header = xlsheet_table.Range[xlsheet_table.Cells[1, 1], xlsheet_table.Cells[row_idx, 1]]

		# Set Row Font
		Row_Header.Font.Name = "Arial"
		Row_Header.Font.Size = 11
		Row_Header.Font.Bold = True
		Log("		(Set Row Font) = Done")

		# Set Row Border
		Row_Header.Borders.LineStyle = Excel.XlLineStyle.xlContinuous
		Row_Header.Borders.Weight = Excel.XlBorderWeight.xlThin
		Log("		(Set Row Border) = Done")

		# Set Row Back Color
		Row_Header.Interior.Color = Color.FromArgb(218,240,254)
		Log("		(Set Row Color) = Done")

		# Create Merge Cell Range
		Merge_Cell = xlsheet_table.Range[xlsheet_table.Cells[2, 7], xlsheet_table.Cells[row_idx, 7]]
		Merge_Cell.Merge(False)
		Merge_Cell.Cells.HorizontalAlignment = Excel.XlHAlign.xlHAlignCenter
		Merge_Cell.Cells.VerticalAlignment = Excel.XlHAlign.xlHAlignCenter
		Log("		(Cell Merge) = Done")

		# Merge Group
		start_idx = 2
		for i in range(2, row_idx):
			if xlsheet_table.Cells[i, 2].Value2 != "None":
				if xlsheet_table.Cells[i, 2].Value2 != xlsheet_table.Cells[i+1, 2].Value2:				
					xlsheet_table.Range[xlsheet_table.Cells[start_idx, 2], xlsheet_table.Cells[i, 2]].Merge(False)
					xlsheet_table.Range[xlsheet_table.Cells[start_idx, 2], xlsheet_table.Cells[i, 2]].HorizontalAlignment = Excel.XlHAlign.xlHAlignCenter
					xlsheet_table.Range[xlsheet_table.Cells[start_idx, 2], xlsheet_table.Cells[i, 2]].VerticalAlignment = Excel.XlHAlign.xlHAlignCenter
					start_idx = i+1

				if i+1 == row_idx:
					xlsheet_table.Range[xlsheet_table.Cells[start_idx, 2], xlsheet_table.Cells[row_idx, 2]].Merge(False)
					xlsheet_table.Range[xlsheet_table.Cells[start_idx, 2], xlsheet_table.Cells[row_idx, 2]].HorizontalAlignment = Excel.XlHAlign.xlHAlignCenter
					xlsheet_table.Range[xlsheet_table.Cells[start_idx, 2], xlsheet_table.Cells[row_idx, 2]].VerticalAlignment = Excel.XlHAlign.xlHAlignCenter
		Log("		(Cell Merge by Group) = Done")

		# Create Data Range
		Data_Cell = xlsheet_table.Range[xlsheet_table.Cells[2, 2], xlsheet_table.Cells[row_idx, 7]]
		Data_Cell.Borders.LineStyle = Excel.XlLineStyle.xlContinuous
		Data_Cell.Borders.Weight = Excel.XlBorderWeight.xlThin

		# Auto Fit
		xlsheet_table.Range[xlsheet_table.Cells[1, 1], xlsheet_table.Cells[2, 7]].Columns.AutoFit()
		Log("		(Column Width AutoFit) = Done")
	
		# Save and Release
		#xlbook.SaveAs(Save_File)
		#xlbook.Close()
		#xlApp.Quit()
		xlApp.DisplayAlerts = True
		ReleaseObject(Col_Header)
		ReleaseObject(Row_Header)
		ReleaseObject(Data_Cell)
		ReleaseObject(Merge_Cell)
		ReleaseObject(xlsheet)
		ReleaseObject(xlbook)
		ReleaseObject(xlApp)

		#Log("		(File Save) = Done, %s" % Save_File)

	except Exception as e:		
		Log("	<Create Excel Report> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to create excel report","Warning")						
		EXIT()