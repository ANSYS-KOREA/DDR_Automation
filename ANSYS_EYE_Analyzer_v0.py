import clr
import sub_DB
import time
import os

clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

import System.Drawing
import System.Windows.Forms

from GUI_subforms import *
from sub_functions import *
from System.Drawing import *
from System.Windows.Forms import *

path = os.path.dirname(os.path.abspath(__file__))

# Create Temp Directory
temp_time = time.strftime('%Y%m%d_%H%M%S')
temp_dir = path + '\\temp_' + temp_time
os.makedirs(temp_dir)
sub_DB.temp_dir = temp_dir

# Record Log. Header
sub_DB.Log += "############################################################"
sub_DB.Log += "\n" + "#	Header"
sub_DB.Log += "\n" + "############################################################"
sub_DB.Log += "\n" + "# Launched Eye Analyzer Independently on %s" % time.strftime('%Y.%m.%d, %H:%M:%S') + '\n'

# Load Preserved Definition File
File = path + r'\Resources\Ref.def'
Cenv = Load_env(File)
Cenv["File"] = File
sub_DB.Cenv = Cenv
Log("[Definition File] = %s" % File)

# Load Preserved Configuration File
if sub_DB.Debug_Mode:
    #File = path + r'\Resources\Test_0215.cnf'
    File = path + r'\Resources\Ref.cnf'
else:
    File = path + r'\Resources\Ref.cnf'

Uenv = Load_env(File)
Uenv["File"] = File
sub_DB.Uenv = Uenv
Log("[Configuration File] = %s" % File + '\n')

if "[Eye]" in sub_DB.Uenv:
    sub_DB.Uenv["[Eye]"][0] = "True"
else:
    sub_DB.Uenv["[Eye]"] = ["True"]

import GUI_3_EyeAnalyzer

sub_DB.Eye_Form = GUI_3_EyeAnalyzer.Eye_Form()

# Create Sub Form Classes
import GUI_subforms
sub_DB.Option_Form = GUI_subforms.OptionForm(2)
sub_DB.Net_Form = GUI_subforms.NetForm()
sub_DB.Compliance_Form = GUI_subforms.ComplianceForm()

sub_DB.Eye_Form.ShowDialog()

# End Ansys DDR Wizard
# exit()
