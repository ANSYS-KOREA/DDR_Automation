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
from GUI_subforms import *
from sub_functions import *

import GUI_3_EyeAnalyzer

###########################
# Get Ref. dir & User dir #
###########################
path = os.path.dirname(os.path.abspath(__file__))
sub_DB.user_dir = os.getenv('USERPROFILE')

######################
# Record Log. Header #
######################
sub_DB.Log += "############################################################"
sub_DB.Log += "\n" + "#	Header"
sub_DB.Log += "\n" + "############################################################"
sub_DB.Log += "\n" + "# Launched Eye Analyzer Independently on %s" % time.strftime('%Y.%m.%d, %H:%M:%S') + '\n'
sub_DB.start_time = time.strftime('%Y.%m.%d, %H:%M:%S')

##################################
# Load Preserved Definition File #
##################################
sub_DB.resource_dir = path + r'\Resources'
File = sub_DB.resource_dir + r'\config\Ref.def'
Cenv = Load_env(File)
Cenv["File"] = File
sub_DB.Cenv = Cenv
Log("[Definition File] = %s" % File)

#####################################
# Load Preserved Configuration File #
#####################################
if sub_DB.Debug_Mode:    
    File = sub_DB.resource_dir + r'\config\Ref.cnf'
else:
    File = sub_DB.resource_dir + r'\config\Ref.cnf'
Uenv = Load_env(File)
Uenv["File"] = File
sub_DB.Uenv = Uenv
Log("[Configuration File] = %s" % File + '\n')
if "[Eye]" in sub_DB.Uenv:
    sub_DB.Uenv["[Eye]"][0] = "True"
else:
    sub_DB.Uenv["[Eye]"] = ["True"]

###########################
# Create Winforms Objects #
###########################
sub_DB.Eye_Form = GUI_3_EyeAnalyzer.Eye_Form()
sub_DB.Option_Form = OptionForm(2)
sub_DB.Net_Form = NetForm()
sub_DB.Compliance_Form = ComplianceForm()
sub_DB.IBIS_Form = IBIS_OptForm()
sub_DB.Var_Form = Env_variable()
###########################
# Launch Eye Analyzer GUI #
###########################
sub_DB.Eye_Form.ShowDialog()
#sub_DB.Env_Form.ShowDialog()
#sub_DB.IBIS_ResultForm = IBIS_Case()
#sub_DB.IBIS_ResultForm._DataGridView.Size = System.Drawing.Size(699, 300)
#sub_DB.IBIS_ResultForm.Size = System.Drawing.Size(740, 390)
#sub_DB.IBIS_ResultForm.Text = "IBIS Optimization Results"
#sub_DB.IBIS_ResultForm.ShowDialog()

#sub_DB.IBIS_ResultForm = IBIS_Case()
#sub_DB.IBIS_ResultForm._DataGridView.Size = System.Drawing.Size(699, 300)
#sub_DB.IBIS_ResultForm.Size = System.Drawing.Size(740, 390)
#sub_DB.IBIS_ResultForm.Text = "IBIS Optimization Results"
#sub_DB.IBIS_ResultForm.ShowDialog()

# End Ansys DDR Wizard
# exit()
