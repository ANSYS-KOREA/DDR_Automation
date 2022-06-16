import os
import time
import sys
import clr

clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

import System.Drawing
import System.Windows.Forms
import sub_ScriptEnv
import sub_AEDT
import sub_DB
import sub_Compliance
import sub_EyeAnalyze
import traceback

from GUI_subforms import *
from sub_functions import *
from System.Drawing import *
from System.Windows.Forms import *

'''
$begin 'AnsoftProject'
	$begin 'Desktop'
		Version(2021, 2)
		'
		'
		'
	$begin 'Definitions'
		$begin 'Folders'
		'
		'
		'
		$begin 'Compdefs'
			$begin 'Circuit1' --- Design Name
			$end 'Circuit1'
			'
			'
			Component List
			'
			'
			$begin 'DQ_ODT_60_DDR_EAN64108201_i_k4b4g1646e_bcxx_june23'
				'
				'
				'
				$begin 'Parameters'
					ButtonProp('file', 'D', 'Name of IBIS file (required)', 'DDR_EAN64108201_i_k4b4g1646e_bcxx_june23.ibs', '<Project>restored_files\\DDR_EAN64108201_i_k4b4g1646e_bcxx_june23.ibs', 3, ButtonPropClientData(InternalFormatText='<Project>restored_files\\DDR_EAN64108201_i_k4b4g1646e_bcxx_june23.ibs'))
					'
					'
					'
					TextProp('comp_type', 'HD', '', 'IBIS')
					TextValueProp('IBIS_Model_Text', 'SRHD', '', 'DQ_ODT_60 : 2 : input : IbisInput4 : 0 : 0 : Non-Inverting : No Enable : b_input_@ID;')
					'
				$end 'Parameters'
				'
				'
				'
			$end 'DQ_ODT_60_DDR_EAN64108201_i_k4b4g1646e_bcxx_june23'
			'
			'
			'
			$begin 'ddr_tx_drv0_msd94bcg-ddr3'
				'
				'
				'
				$begin 'Parameters'
					ButtonProp('file', 'D', 'Name of IBIS file (required)', 'msd94bcg-ddr3.ibs', '<Project>restored_files\\msd94bcg-ddr3.ibs', 3, ButtonPropClientData(InternalFormatText='<Project>restored_files\\msd94bcg-ddr3.ibs'))
					'
					'
					'
					TextProp('comp_type', 'HD', '', 'IBIS')
					TextValueProp('IBIS_Model_Text', 'SRHD', '', 'ddr_tx_drv0 : 4 : input_output : IbisIO8 : 0 : 0 : Non-Inverting : Active-Low : b_io8_@ID;')
					'
				$end 'Parameters'
				'
				'
				'
			$end 'ddr_tx_drv0_msd94bcg-ddr3'


'''

File = r'D:\1_Work\20220106_DDR_Compliance\0_DB\0_Input_Examples\AEDT_Schematic\Galileo_R21_DDR_SSN_siwave.aedt'
Design = "Circuit1"
sub_AEDT.Delete_LockFile(File)
Version = sub_AEDT.Get_AEDT_Version()
oApp, oDesktop = sub_ScriptEnv.Initialize("Ansoft.ElectronicsDesktop." + Version)
oDesktop.RestoreWindow()

Project_list = oDesktop.GetProjectList()
Input_Project_Name = File.split("\\")[-1].split(".")[0]
if not Input_Project_Name in Project_list:		
	oDesktop.OpenProject(File)
oProject = oDesktop.SetActiveProject(Input_Project_Name)
oDesign = oProject.SetActiveDesign(Design)
oEditor = oDesign.SetActiveEditor("SchematicEditor")
comp_array = oEditor.GetAllComponents()

IBIS_file_name = []

flag = True
with open(File) as fp:
	while(flag):
		# Read line
		temp_data = fp.readline()

		if "$begin \'Compdefs\'" in temp_data:
			while(flag):
				# Read line
				temp_data = fp.readline()

				if Design in temp_data:
					while(flag):
						# Read line
						temp_data = fp.readline()

						if 'Name of IBIS file' in temp_data:
							IBIS_file_name.append(temp_data.split(',')[3].replace('\'',''))

						if "$end \'Compdefs\'" in temp_data:
							flag = False
	print IBIS_file_name
	pass
