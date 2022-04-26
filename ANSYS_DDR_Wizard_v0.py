import clr
import sub_DB
import time
import os

clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

import System.Drawing
import System.Windows.Forms

from System.Drawing import *
from System.Windows.Forms import *

Debug_Mode = False
#Debug_Mode = True
sub_DB.Debug_Mode = Debug_Mode

###################################################################################################
################## Main GUI #######################################################################
###################################################################################################
# Open Main GUI
import GUI_0_Main
sub_DB.Start_Form = GUI_0_Main.StartForm()
sub_DB.Start_Form.ShowDialog()

################## Creat GUI Clasees ##############################################################
import GUI_3_EyeAnalyzer
sub_DB.Eye_Form = GUI_3_EyeAnalyzer.Eye_Form()

# Create Sub Form Classes
import GUI_subforms
sub_DB.Option_Form = GUI_subforms.OptionForm(2)
sub_DB.Net_Form = GUI_subforms.NetForm()

# Create Temp Directory
#path = os.path.dirname(os.path.abspath(__file__))
#temp_time = time.strftime('%Y%m%d_%H%M%S')
#temp_dir = path + '\\temp_' + temp_time
#sub_DB.temp_dir = temp_dir

###################################################################################################
################## EM Analysis Process ############################################################
###################################################################################################
if sub_DB.Uenv["[EM]"][0] == "True":
    MessageBox.Show("EM Analysis Process will be done", "To Be Done")
    pass



###################################################################################################
################# Transient Analysis Process ######################################################
###################################################################################################
if sub_DB.Uenv["[Tran]"][0] == "True":
    MessageBox.Show("Transient Analysis Process will be done", "To Be Done")
    pass



###################################################################################################
################# Eye Analysis Process ############################################################
###################################################################################################
if sub_DB.Uenv["[Comp]"][0] == "True":
    sub_DB.Eye_Form.ShowDialog()    

# End Ansys DDR Wizard
#exit()