import os
import clr
import re
import time
import shutil
import traceback
import sub_ScriptEnv
import sub_AEDT
import sub_DB
import GUI_subforms

clr.AddReference('Microsoft.Office.Interop.Excel')

import System.Drawing
import System.Windows.Forms

from sub_functions import *
from sub_Vref import *
from System.Drawing import *
from System.Windows.Forms import *
from Microsoft.Office.Interop import Excel

def IBIS_Init():	
	sub_DB.IBISInfo_Tx_Form = ""
	sub_DB.IBISInfo_Rx_Form = ""
	sub_DB.IBIS_ResultForm = ""

	sub_DB.IBIS_Tx = ""
	sub_DB.IBIS_Rx = ""
	sub_DB.IBIS_Tx_Model = []
	sub_DB.IBIS_Tx_Model_idx = []
	sub_DB.IBIS_Rx_Model = []
	sub_DB.IBIS_Rx_Model_idx = []
	sub_DB.IBIS_Sim_Case = []

def IBIS_Parsing(File):
	IBIS = {}
	IBIS['Component'] = []
	IBIS['Model Selector'] = {}

	with open(File) as fp:
		Text = list(enumerate(fp))
	
		line_num = 0
		while(1):
			line = Text[line_num][1]
			# If not the line is comment
			if not line[0] == "|":
				###################
				# Find Components #
				###################
				if '[component]' in line.lower():				
					comp = ' '.join(line.split()).split()[1]
					IBIS['Component'].append(comp)

				#######################
				# Find Model Selector #
				#######################
				if '[model selector]' in line.lower():
					# Get Model Name
					model_name = line.split(']')[-1].strip()

					temp_list = []
					while(1):
						line_num += 1
						line = Text[line_num][1]
						if line[0] != "|" and line.strip() != "":
							if line[0] == "[":
								line_num -= 1
								break
							else:
								model = ' '.join(line.split()).split(" ", 1)[0]
								note = ' '.join(line.split()).split(" ", 1)[1]
								temp_list.append([model, note])
					IBIS["Model Selector"][model_name] = temp_list

				# TODO
				##############
				# Find Model #
				##############
				if '[model]' in line.lower():
					pass

			line_num += 1
			if line_num==len(Text):
				break

	return IBIS

def IBIS_Opt_Run(self):	
	###############################
	# 1. Create Optimetric Design #
	###############################
	try:
		# Set AEDT Objects
		oProject = sub_DB.AEDT['Project']
		oDesktop = sub_DB.AEDT['Desktop']		
		oDesign = sub_DB.AEDT['Design']	
		oDesktop.RestoreWindow()
		Design = oDesign.GetName()

		# Get Current Design List
		pre_design_list = []
		for design in oProject.GetDesigns():
			pre_design_list.append(design.GetName().split(";")[-1])
		if Design.split(";")[-1] + "_IBIS_Opt" in pre_design_list:
			oProject.DeleteDesign(Design.split(";")[-1] + "_IBIS_Opt")
			oProject.Save()
			pre_design_list = []
			for design in oProject.GetDesigns():
				pre_design_list.append(design.GetName().split(";")[-1])

		# Copy & Past Design
		oProject.CopyDesign(Design.split(";")[-1])
		oProject.Paste()
		oProject.Save()

		# Get Pasted Design List
		post_design_list = []
		for design in oProject.GetDesigns():
			post_design_list.append(design.GetName().split(";")[-1])			

		# Get Pasted Design Name
		for design in pre_design_list:
			del post_design_list[post_design_list.index(design)]
		pasted_design = post_design_list[0]
		
		# Rename
		oDesign = oProject.SetActiveDesign(pasted_design)
		oDesign.RenameDesignInstance(pasted_design, Design.split(";")[-1] + "_IBIS_Opt")
		Design = oDesign.GetName()

	except Exception as e:		
		#Log("	<Run IBIS Opt> = Failed")
		#Log(traceback.format_exc())
		print traceback.format_exc()
		#MessageBox.Show("Fail to create auto saved Cnf header","Warning")						
		EXIT()		
	
	##############################
	# 2. Get Tx/Rx Model & Index #
	##############################
	try:
		# Get Tx Model & Index
		idx = 0
		for row in self._DataGridView_Tx.Rows:		
			if row.Cells[0].Value:
				sub_DB.IBIS_Tx_Model.append(row.Cells[1].Value)
				sub_DB.IBIS_Tx_Model_idx.append(idx)
				idx += 1

		# Get Rx Model & Index
		idx = 0
		for row in self._DataGridView_Rx.Rows:
			if row.Cells[0].Value:
				sub_DB.IBIS_Rx_Model.append(row.Cells[1].Value)
				sub_DB.IBIS_Rx_Model_idx.append(idx)
				idx += 1

	except Exception as e:		
		#Log("	<Run IBIS Opt> = Failed")
		#Log(traceback.format_exc())
		print traceback.format_exc()
		#MessageBox.Show("Fail to create auto saved Cnf header","Warning")						
		EXIT()

	##############################
	# 3. Set Tx/Rx Model & Index #
	##############################
	try:
		# Set Tx Model
		tx_str = "["		
		for i in range(0, len(sub_DB.IBIS_Tx_Model)):
			if not i == len(sub_DB.IBIS_Tx_Model)-1:
				tx_str += "\"" + sub_DB.IBIS_Tx_Model[i] + "\", "				
			else:
				tx_str += "\"" + sub_DB.IBIS_Tx_Model[i] + "\"]"

		oDesign.ChangeProperty(
			["NAME:AllTabs",
				["NAME:LocalVariableTab",
					["NAME:PropServers", "Instance:" + Design],
					["NAME:NewProps",
						["NAME:Tx_IBIS_Model",
							"PropType:=",
							"VariableProp",
							"UserDef:=", True,
							"Value:=", tx_str]]]])

		# Set Tx Model Index : Initial Value = 0
		oDesign.ChangeProperty(
			["NAME:AllTabs",
				["NAME:LocalVariableTab",
					["NAME:PropServers", "Instance:" + Design],
					["NAME:NewProps",
						["NAME:Tx_IBIS_Model_idx",
							"PropType:=",
							"VariableProp",
							"UserDef:=", True,
							"Value:=", "0"]]]])

		# Set Rx Model
		rx_str = "["		
		for i in range(0, len(sub_DB.IBIS_Rx_Model)):
			if not i == len(sub_DB.IBIS_Rx_Model)-1:
				rx_str += "\"" + sub_DB.IBIS_Rx_Model[i] + "\", "
			else:
				rx_str += "\"" + sub_DB.IBIS_Rx_Model[i] + "\"]"

		oDesign.ChangeProperty(
			["NAME:AllTabs",
				["NAME:LocalVariableTab",
					["NAME:PropServers", "Instance:" + Design],
					["NAME:NewProps",
						["NAME:Rx_IBIS_Model",
							"PropType:=",
							"VariableProp",
							"UserDef:=", True,
							"Value:=", rx_str]]]])

		# Set Rx Model Index : Initial Value = 0
		oDesign.ChangeProperty(
			["NAME:AllTabs",
				["NAME:LocalVariableTab",
					["NAME:PropServers", "Instance:" + Design],
					["NAME:NewProps",
						["NAME:Rx_IBIS_Model_idx",
							"PropType:=",
							"VariableProp",
							"UserDef:=", True,
							"Value:=", "0"]]]])

	except Exception as e:		
		#Log("	<Run IBIS Opt> = Failed")
		#Log(traceback.format_exc())
		print traceback.format_exc()
		#MessageBox.Show("Fail to create auto saved Cnf header","Warning")						
		EXIT()

	##############################
	# 4. Apply Variables to IBIS #
	##############################
	try:
		# Get All Component Info
		oEditor = oDesign.SetActiveEditor("SchematicEditor")
		comp_array = oEditor.GetAllComponents()

		# Get Tx/Rx Component List
		tx_comp = []
		tx_comp.append("NAME:PropServers")
		rx_comp = []
		rx_comp.append("NAME:PropServers")
		for comp in comp_array:
			if self.def_Tx_model in comp:
				tx_comp.append(comp)
			elif self.def_Rx_model in comp:
				rx_comp.append(comp)

		# Apply Variables to Tx IBIS
		oEditor.ChangeProperty(
			["NAME:AllTabs",
				["NAME:PassedParameterTab",
					tx_comp,
					["NAME:ChangedProps",
						["NAME:model",
							"OverridingDef:="	, True,
							"Value:="		, "Tx_IBIS_Model[Tx_IBIS_Model_idx]",
							"HasPin:="		, False,
							"ShowPin:="		, False,
							"Display:="		, False,
							"Sweep:="		, False,
							"DefaultOutput:="	, False,
							"SDB:="			, False]]]])

		# Apply Variables to Rx IBIS
		oEditor.ChangeProperty(
			["NAME:AllTabs",
				["NAME:PassedParameterTab",
					rx_comp,
					["NAME:ChangedProps",
						["NAME:model",
							"OverridingDef:="	, True,
							"Value:="		, "Rx_IBIS_Model[Rx_IBIS_Model_idx]",
							"HasPin:="		, False,
							"ShowPin:="		, False,
							"Display:="		, False,
							"Sweep:="		, False,
							"DefaultOutput:="	, False,
							"SDB:="			, False]]]])

	except Exception as e:		
		#Log("	<Run IBIS Opt> = Failed")
		#Log(traceback.format_exc())
		print traceback.format_exc()
		#MessageBox.Show("Fail to create auto saved Cnf header","Warning")						
		EXIT()

	###########################
	# 5. Set Parametric Sweep #
	###########################
	try:
		if len(sub_DB.IBIS_Tx_Model) > 1:
			tx_data = "LIN 0 %d 1" % (len(sub_DB.IBIS_Tx_Model)-1)
		else:
			tx_data = "0"

		if len(sub_DB.IBIS_Rx_Model) > 1:
			rx_data = "LIN 0 %d 1" % (len(sub_DB.IBIS_Rx_Model)-1)
		else:
			rx_data = "0"

		oModule = oDesign.GetModule("Optimetrics")
		oModule.InsertSetup("OptiParametric", 
			["NAME:ParametricSetup1",
			"UseFastCalculationUpdateAlgo:=", True,
			"FastCalcOptCtrledByUser:=", False,
			"IsEnabled:="		, True,
			"SaveSolutions:="	, True,
				["NAME:StartingPoint"],
				"Sim. Setups:=",
				[sub_DB.Eye_Form._ComboBox_SolutionName.Text],
				["NAME:Sweeps",
					["NAME:SweepDefinition",
					"Variable:=", "Tx_IBIS_Model_idx",
					"Data:=", tx_data,
					"OffsetF1:=", False,
					"Synchronize:=", 0],
					["NAME:SweepDefinition",
					"Variable:=", "Rx_IBIS_Model_idx",
					"Data:=", rx_data,
					"OffsetF1:="		, False,
					"Synchronize:=", 0]],
				["NAME:Sweep Operations"
				#	"add:=", ["3","3"],
				#	"add:=", ["3","3"],
				#	"del:=", ["3","3"]
				],
				["NAME:Goals"]])

	except Exception as e:		
		#Log("	<Run IBIS Opt> = Failed")
		#Log(traceback.format_exc())
		print traceback.format_exc()
		#MessageBox.Show("Fail to create auto saved Cnf header","Warning")						
		EXIT()

	###########################
	# 6. Run Parametric Sweep #
	###########################
	try:
		oProject.Save()
		oModule = oDesign.GetModule("Optimetrics")
		oModule.SolveSetup("ParametricSetup1")
		pass

	except Exception as e:		
		#Log("	<Run IBIS Opt> = Failed")
		#Log(traceback.format_exc())
		print traceback.format_exc()
		#MessageBox.Show("Fail to create auto saved Cnf header","Warning")						
		EXIT()

	################################
	# 7. Create Report and Measure #
	################################
	try:
		oModule = oDesign.GetModule("ReportSetup")
		# Get Target Net List
		Net_list = []
		for row in sub_DB.Net_Form._DataGridView.Rows:
			if row.Cells[0].Value:
				Net_list.append(row.Cells[1].Value)

		Eye_Measure_Results = {}	
		case = 0
		# Create Report for each cases		
		for row in sub_DB.IBIS_ResultForm._DataGridView.Rows:
			case += 1			
			report_name = "case%d:[%s]  [%s]" % (case, row.Cells[1].Value, row.Cells[2].Value)
			Tx_IBIS_Model_idx = sub_DB.IBIS_Tx_Model.index(row.Cells[1].Value)
			Rx_IBIS_Model_idx = sub_DB.IBIS_Rx_Model.index(row.Cells[2].Value)
			
			# Create Report
			oModule.CreateReport(report_name, "Eye Diagram", "Rectangular Plot", "Transient", 
				[
					"NAME:Context",
					"SimValueContext:="	, [1,0,2,0,False,False,-1,1,0,1,1,"",0,0,"NUMLEVELS",False,"0"]
				], 
				[
					"Time:="		, ["All"],
					[
						"NAME:VariableValues",
						"Rx_IBIS_Model_idx:="	, str(Rx_IBIS_Model_idx),
						"Tx_IBIS_Model_idx:="	, str(Tx_IBIS_Model_idx)
					]
				], 
				[
					"Component:="		, Net_list
				], 
				[
					"Unit Interval:="	, "(1/%s000000) s" % sub_DB.Eye_Form._ComboBox_DataRate.Text,
					"Offset:="		, sub_DB.Eye_Form._TextBox_Offset.Text  + "ns",
					"Auto Delay:="		, True,
					"Manual Delay:="	, "0ps",
					"AutoCompCrossAmplitude:=", True,
					"CrossingAmplitude:="	, "0mV",
					"AutoCompEyeMeasurementPoint:=", True,
					"EyeMeasurementPoint:="	, "2.3441162681669e-10s"
				])

			# for New Eye
			# Vref Calculation
			Vref = float(Cal_Vref_AEDT_IBIS(report_name, Design.split(";")[-1], Tx_IBIS_Model_idx, Rx_IBIS_Model_idx))
			
			# Measure Eye Diagram
			Eye_Measure_Results["case%d" % case] = Measure_Eye_IBIS(sub_DB.Eye_Form, Vref)			
			Width = []
			Margin = []
			for key in Eye_Measure_Results["case%d" % case].keys():				
				Width.append(Eye_Measure_Results["case%d" % case][key][0])
				Margin.append(Eye_Measure_Results["case%d" % case][key][2])

			Avg_Width = sum(Width)/len(Width)
			Avg_Margin = sum(Margin)/len(Margin)
			Worst_Width = min(Width)
			Worst_Margin = min(Margin)			

			# Add Analyze Result
			sub_DB.IBIS_ResultForm._DataGridView.Rows[case-1].Cells[4].Value = round(Avg_Width, 1)
			sub_DB.IBIS_ResultForm._DataGridView.Rows[case-1].Cells[5].Value = round(Avg_Margin, 1)
			sub_DB.IBIS_ResultForm._DataGridView.Rows[case-1].Cells[6].Value = round(Worst_Width, 1)
			sub_DB.IBIS_ResultForm._DataGridView.Rows[case-1].Cells[7].Value = round(Worst_Margin, 1)
			sub_DB.IBIS_ResultForm._DataGridView.Rows[case-1].Cells[8].Value = round(Vref, 1)

	except Exception as e:		
		#Log("	<Run IBIS Opt> = Failed")
		#Log(traceback.format_exc())
		print traceback.format_exc()
		#MessageBox.Show("Fail to create auto saved Cnf header","Warning")						
		EXIT()






# Default Vref for IBIS
def Cal_Vref_AEDT_IBIS(report_name, design_name, Tx_IBIS_Model_idx, Rx_IBIS_Model_idx):	
	##############
	# Initialize #
	##############
	try:		
		oProject = sub_DB.AEDT["Project"]		
		oDesign = oProject.SetActiveDesign(design_name)
		oModule = oDesign.GetModule("ReportSetup")
		#Log("		(AEDT Launch) = Done")
		pass

	except Exception as e:		
		Log("	<Vref Calculation> = Failed to Generate AEDT Object")
		Log(traceback.format_exc())
		print traceback.format_exc()
		MessageBox.Show("Vref Calculation - Fail to generate AEDT objects","Warning")
		EXIT()

	#################
	# Update report #
	#################
	try:
		oModule.UpdateReports(report_name)
		pass

	except Exception as e:		
		Log("	<Vref Calculation> = Failed to Update Reports")
		Log(traceback.format_exc())
		print traceback.format_exc()
		MessageBox.Show("Vref Calculation - Fail to update Report","Warning")		
		EXIT()	

	#################
	# Get time unit #
	#################	
	try:
		# export report as temp
		File = sub_DB.result_dir + "\\temp.csv"		
		oModule.ExportToFile(report_name, File)
		#time.sleep(time_delay)
	
		# load report to get time unit
		with open(File) as fp:
			temp_data = fp.readline().split(",")			
			iter = 0
			while(1):
				if not "Time" in temp_data[0]:
					del temp_data[0]
					iter += 1
				else:
					break
		fp.close()		
		t_unit = temp_data[0].split("[")[-1].split("]")[0]
		Log("		(Get Time Unit) = %s" % t_unit)

	except Exception as e:		
		#Log("	<Vref Calculation> = Failed to Get Time Unit")
		#Log(traceback.format_exc())
		print traceback.format_exc()
		#MessageBox.Show("Vref Calculation - Fail to get time unit","Warning")		
		EXIT()	

	#######################
	# Get variable string #
	#######################
	try:
		idx = 1
		pre_var_string = ""
		for i in range(1, len(temp_data)):
			if "-" in temp_data[i]:
				var_string = temp_data[i].split("]")[-1].split("-")[-1].strip().replace("\"","")				
			else:
				var_string = ""
				break
		sub_DB.var_string = var_string
		Log("		(Get Variables) = Done")

	except Exception as e:		
		Log("	<Vref Calculation> = Failed to Get Variables")
		Log(traceback.format_exc())
		print traceback.format_exc()
		MessageBox.Show("Vref Calculation - Fail to get variables","Warning")		
		EXIT()

	#############################
	# Get total simulation time #
	#############################
	try:
		with open(File) as fp:
			for line in reversed(list(fp)):
				t_total = line.split(",")[iter] + t_unit
				break
		fp.close()
		
		sub_DB.total_waveform_length = t_total
		Log("		(Get total simulation time) = %s" % t_total)

	except Exception as e:		
		Log("	<Vref Calculation> = Failed to Get Total Simulation Time")
		Log(traceback.format_exc())
		print traceback.format_exc()
		MessageBox.Show("Vref Calculation - Fail to get total simulation time","Warning")		
		EXIT()

	######################
	# Create temp report #
	######################
	try:
		# generate plot list
		PlotList = []
		for i in range(0, sub_DB.Net_Form._DataGridView.Rows.Count):
			if sub_DB.Net_Form._DataGridView.Rows[i].Cells[0].Value:
				PlotList.append(sub_DB.Net_Form._DataGridView.Rows[i].Cells[1].Value.replace("\"","").split("[")[0].strip())

		oModule.CreateReport("temp", "Standard", "Rectangular Plot", sub_DB.Eye_Form._ComboBox_SolutionName.Text, 
		[
			"NAME:Context",
			"SimValueContext:="	, [1,0,2,0,False,False,-1,1,0,1,1,"",0,0,"DE",False,"0","DP",False,"500000000","DT",False,"0.001","NUMLEVELS",False,"0","WE",False,sub_DB.total_waveform_length,"WM",False,sub_DB.total_waveform_length,"WN",False,"0ps","WS",False,"0ps"]
		], 
		[
			"Time:="		, ["All"],
			[
				"NAME:VariableValues",
				"Rx_IBIS_Model_idx:="	, str(Rx_IBIS_Model_idx),
				"Tx_IBIS_Model_idx:="	, str(Tx_IBIS_Model_idx)
			]
		],
		[
			"X Component:="		, "Time",
			"Y Component:="		, PlotList
		])
		Log("		(Create temp report) = Done")

	except Exception as e:		
		Log("	<Vref Calculation> = Failed to Create temp Report")
		Log(traceback.format_exc())
		print traceback.format_exc()
		MessageBox.Show("Vref Calculation - Fail to create temp report","Warning")		
		EXIT()

	############################
	# Export Uniform Wavefomrs #
	############################
	try:
		# Export Uniform Report	
		File = sub_DB.result_dir + "\\Waveforms.csv"		
		oModule.UpdateReports(["temp"])
		oModule.ExportUniformPointsToFile("temp", File, "0ns", t_total, "1ps", False)
		#time.sleep(time_delay)
		sub_DB.Waveform_File = File
		
		# Delete temp Report	
		oModule.DeleteReports(["temp"])		
		Log("		(Export Uniform Point Waveforms) = Done")

	except Exception as e:		
		Log("	<Vref Calculation> = Failed to Export temp Report")
		Log(traceback.format_exc())
		print traceback.format_exc()
		MessageBox.Show("Vref Calculation - Fail to export temp report","Warning")		
		EXIT()

	##########################
	# Load Uniform Wavefomrs #
	##########################
	try:
		# Open Waveform.csv and Load
		Waveform = {}
		with open(sub_DB.Waveform_File) as fp:
			# Get Netlist and Create Waveform Dictionary keys
			temp_data = fp.readline().replace("\"","").replace(" ","").strip().split(",")

			# Delete global & local variable data
			iter = 0
			while(1):
				if not "Time" in temp_data[0]:
					del temp_data[0]
					iter += 1
				else:
					break
			
			# Get time and voltage unit
			sub_DB.Unit["Time"] = temp_data[0].split("[")[-1].split("]")[0]
			sub_DB.Unit["Voltage"] = temp_data[1].split("[")[-1].split("]")[0]
			
			# Delete Time Column
			del temp_data[0]

			data = [[0 for col in range(0)] for row in range(len(temp_data))]
			for i in range(0, len(temp_data)):
				data[i].append(temp_data[i])

			# Get Waveform Data				
			for line in fp:
				for i in range(0, len(temp_data)):
					data[i].append(float(line.split(",")[i+1+iter]))
		fp.close()

		Log("		(Load Uniform Point Waveforms)")
		for cell in data:
			key = cell[0].split("[")[0]
			del cell[0]
			Waveform[key] = cell
			Log("			= %s" % key)

		# Check voltage unit
		if sub_DB.Unit["Voltage"].lower() == "mv":
			pass
		elif sub_DB.Unit["Voltage"].lower() == "v":
			for key in Waveform:
				for i in range(0, len(Waveform[key])):
					Waveform[key][i] = Waveform[key][i]*1000		
		sub_DB.Waveform = Waveform

	except Exception as e:		
		Log("	<Vref Calculation> = Failed to Get Waveforms")
		Log(traceback.format_exc())
		print traceback.format_exc()
		MessageBox.Show("Vref Calculation - Fail to get waveforms","Warning")		
		EXIT()

	#################
	# Cacluate Vref #
	#################
	try:		
		Vref = Cal_Vref(Waveform)
		Log("		(Vref Calculation) = Done, %fmV" % Vref)

	except Exception as e:		
		Log("	<Vref Calculation> = Failed to Calculate Vref")
		Log(traceback.format_exc())
		print traceback.format_exc()
		MessageBox.Show("Vref Calculation - Fail to calculate Vref","Warning")		
		EXIT()

	return Vref

# Eye Measure for Default Eye Analyze - New Eye
def Measure_Eye_IBIS(self, Vref):
	try:		
		#sub_DB.Cal_Form.Text = "Analyzing Eye..."	

		# Get Vref
		#sub_DB.Cal_Form._Label_Vref.Text = "Analyzing Eye."
		#sub_DB.Cal_Form._ProgressBar_Vref.Value += 1				
		#Log("		(Vref) = %s[mV]" % Vref)

		# Calculate Voltage Boundary
		#sub_DB.Cal_Form._Label_Vref.Text = "Analyzing Eye.."
		#sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
		V_high = Vref + float(self._TextBox_VdIVW.Text)/2
		V_low = Vref - float(self._TextBox_VdIVW.Text)/2
		#Log("		(V_high) = %s[mV]" % V_high)
		#Log("		(V_low) = %s[mV]" % V_low)

		# Calculate Unit Interval [ps]
		#sub_DB.Cal_Form._Label_Vref.Text = "Analyzing Eye..."
		#sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
		UI = int(round(1/(float(self._ComboBox_DataRate.Text))*1000000))
		#Log("		(Unit Interval) = %s[ps]" % UI)

		# Get Waveform		
		#sub_DB.Cal_Form._Label_Vref.Text = "Analyzing Eye...."
		#sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
		#Log("		(Waveform)")
		Waveform = {}

		with open(sub_DB.Waveform_File) as fp:
			# Get Netlist and Create Waveform Dictionary keys
			temp_data = fp.readline().replace("\"","").replace(" ","").strip().split(",")

			# Delete global & local variable data
			iter = 0
			while(1):
				if not "Time" in temp_data[0]:
					del temp_data[0]
					iter += 1
				else:
					break
			
			# Get time and voltage unit
			sub_DB.Unit["Time"] = temp_data[0].split("[")[-1].split("]")[0]
			sub_DB.Unit["Voltage"] = temp_data[1].split("[")[-1].split("]")[0]
			
			# Delete Time Column
			del temp_data[0]

			data = [[0 for col in range(0)] for row in range(len(temp_data))]
			for i in range(0, len(temp_data)):
				data[i].append(temp_data[i])

			# Get Waveform Data				
			for line in fp:
				for i in range(0, len(temp_data)):
					data[i].append(float(line.split(",")[i+1+iter]))

		for cell in data:
			key = cell[0].split("[")[0]
			del cell[0]
			Waveform[key] = cell
			#Log("			= %s" % key)
			
		# Check voltage unit
		if sub_DB.Unit["Voltage"].lower() == "mv":
			pass
		elif sub_DB.Unit["Voltage"].lower() == "v":
			for key in Waveform:
				for i in range(0, len(Waveform[key])):
					Waveform[key][i] = Waveform[key][i]*1000
		else:
			MessageBox.Show("The voltage unit in the input csv file is not supported.","Warning",MessageBoxButtons.OK, MessageBoxIcon.Warning)
		
		sub_DB.Waveform = Waveform
		

		# Measure Eye Width & Margin
		#sub_DB.Cal_Form._Label_Vref.Text = "Analyzing Eye."	
		Eye_Measure_Results = {}
		temp_Resutls = {}
		T_Vhigh=[]
		T_Vlow=[]
		T_Vref=[]

		# Default
		if sub_DB.Option_Form._ComboBox_Analyze.SelectedIndex == 0:
			for key in Waveform:				
				#sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
				T_Vhigh=[]
				T_Vlow=[]
				T_Vref=[]

				# Get measuring start time based on Vref touch time + eye offset
				t_start = []
				input_eye_offset = int(float(sub_DB.Option_Form._TextBox_EyeOffset.Text)*1000)				
				while(1):					
					vol_pre = Waveform[key][input_eye_offset]
					vol_post = Waveform[key][input_eye_offset+1]
					if (vol_pre - Vref) * (vol_post - Vref) < 0 : # Detect Rising/Falling transition
						t_start.append(input_eye_offset + UI/2)
					input_eye_offset += 1
					if input_eye_offset + UI/2 >= len(Waveform[key]):
						break

				for t_s in t_start:
					time_idx = 0
					iter = 0
					while(1):						
						if t_s + time_idx + 1 >= len(Waveform[key]):
							break
						vol_pre = Waveform[key][t_s + time_idx]
						vol_post = Waveform[key][t_s + time_idx + 1]
						# Measure T_Vhigh
						if (vol_pre - V_high) * (vol_post - V_high) < 0 :							
							T_Vhigh.append(time_idx)
							iter += 1
							#t_Vhigh.append(i)

						# Measure T_low
						if (vol_pre - V_low) * (vol_post - V_low) < 0 :							
							T_Vlow.append(time_idx)
							iter += 1
							#t_Vlow.append(i)

						# Measure T_Vref
						if (vol_pre - Vref) * (vol_post - Vref) < 0 :							
							T_Vref.append(time_idx)
							iter += 1
							#t_Vref.append(i)

						# Initialize time index
						time_idx += 1
						if time_idx == UI or iter == 3:							
							break

				# Calculate eye width, jitter, and margin
				width = UI - max(max(T_Vhigh) - min(T_Vhigh), max(T_Vlow) - min(T_Vlow))
				margin = width - float(self._TextBox_TdIVW.Text)*UI				
				jitter = max(T_Vref) - min(T_Vref)
				
				# Back-up the measured data
				Eye_Measure_Results[key] = []
				Eye_Measure_Results[key].append(width)
				Eye_Measure_Results[key].append(jitter)
				Eye_Measure_Results[key].append(margin)
				Eye_Measure_Results[key].append(T_Vhigh)
				Eye_Measure_Results[key].append(T_Vref)
				Eye_Measure_Results[key].append(T_Vlow)
			
		# Auto-delay
		elif sub_DB.Option_Form._ComboBox_Analyze.SelectedIndex == 1:
			for key in Waveform:				
				#sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
				T_Vhigh=[]
				T_Vlow=[]
				T_Vref=[]

				# Measure Auto Delay
				input_eye_offset = 0
				t_x = [] # Get Vref crossing time point
				while(1):
					vol_pre = Waveform[key][input_eye_offset]
					vol_post = Waveform[key][input_eye_offset+1]
					if (vol_pre - Vref) * (vol_post - Vref) < 0 : # for V_low						
						t_x.append(input_eye_offset%UI)
					input_eye_offset += 1
					if input_eye_offset+1 == len(Waveform[key]):
						break
				
				if min(t_x) < 0.2*UI:
					for i in range(0, len(t_x)):
						t_x[i] = (t_x[i]+0.1*UI)%UI				
				offset = int(sum(t_x)/len(t_x))
								
				# Get measuring start time based on Vref touch time + eye offset			
				input_eye_offset = int(float(sub_DB.Option_Form._TextBox_EyeOffset.Text)*1000)				
				input_eye_offset = input_eye_offset - input_eye_offset % UI + UI - UI/2 + offset

				time_idx = 0				
				while(1):
					vol_pre = Waveform[key][input_eye_offset]
					vol_post = Waveform[key][input_eye_offset+1]

					# Measure T_Vref
					if (vol_pre - Vref) * (vol_post - Vref) < 0 :							
						T_Vref.append(time_idx)

					# V_high
					if (vol_pre - V_high) * (vol_post - V_high) < 0 :							
						T_Vhigh.append(time_idx)
					
					# Measure T_low
					if (vol_pre - V_low) * (vol_post - V_low) < 0 :							
						T_Vlow.append(time_idx)
						
					time_idx += 1
					if time_idx == UI:
						time_idx = 0						

					input_eye_offset += 1
					if input_eye_offset + 1 == len(Waveform[key]):
						break

				# Calculate eye width, jitter, and margin
				width = UI - max(max(T_Vhigh) - min(T_Vhigh), max(T_Vlow) - min(T_Vlow))
				margin = width - float(self._TextBox_TdIVW.Text)*UI				
				jitter = max(T_Vref) - min(T_Vref)
				
				# Back-up the measured data
				Eye_Measure_Results[key] = []
				Eye_Measure_Results[key].append(width)
				Eye_Measure_Results[key].append(jitter)
				Eye_Measure_Results[key].append(margin)
				Eye_Measure_Results[key].append(T_Vhigh)
				Eye_Measure_Results[key].append(T_Vref)
				Eye_Measure_Results[key].append(T_Vlow)

		# Tr-by-Tr
		elif sub_DB.Option_Form._ComboBox_Analyze.SelectedIndex == 2:
			for key in Waveform:				
				#sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
				T_Vhigh=[]
				T_Vlow=[]
				T_Vref=[]				

				# Calculate eye offset
				input_eye_offset = int(float(sub_DB.Option_Form._TextBox_EyeOffset.Text)*1000)
				eye_offset = 0				
				while(1):					
					vol_pre = Waveform[key][eye_offset]
					vol_post = Waveform[key][eye_offset+1]
					if (vol_pre - Vref) * (vol_post - Vref) < 0 : # for rising transition						
						break
					eye_offset += 1

				if eye_offset % UI > UI/2:
					eye_offset = (eye_offset % UI) - UI/2
				else:
					eye_offset = (eye_offset % UI) + UI/2
				
				# Measure Time points
				time_idx = 0
				print eye_offset + input_eye_offset
				for i in range(eye_offset + input_eye_offset, len(Waveform[key])-1):
					vol_pre = Waveform[key][i]
					vol_post = Waveform[key][i+1]
					# Measure T_Vhigh
					if (vol_pre - V_high) * (vol_post - V_high) < 0 :
						T_Vhigh.append(time_idx)
						#t_Vhigh.append(i)

					# Measure T_low
					if (vol_pre - V_low) * (vol_post - V_low) < 0 :
						T_Vlow.append(time_idx)
						#t_Vlow.append(i)

					# Measure T_Vref
					if (vol_pre - Vref) * (vol_post - Vref) < 0 :
						T_Vref.append(time_idx)
						#t_Vref.append(i)

					# Initialize time index
					time_idx += 1
					if time_idx == UI:
						time_idx = 0

				# Calculate eye width, jitter, and margin
				margin = UI - (max([max(T_Vhigh), max(T_Vlow)]) - min([min(T_Vhigh), min(T_Vlow)])) - float(self._TextBox_TdIVW.Text)*UI				
				jitter = max(T_Vref) - min(T_Vref)				
				width = UI - (max([max(T_Vhigh), max(T_Vlow)]) - min([min(T_Vhigh), min(T_Vlow)]))

				# Back-up the measured data
				Eye_Measure_Results[key] = []
				Eye_Measure_Results[key].append(width)
				Eye_Measure_Results[key].append(jitter)
				Eye_Measure_Results[key].append(margin)
				Eye_Measure_Results[key].append(T_Vhigh)
				Eye_Measure_Results[key].append(T_Vref)
				Eye_Measure_Results[key].append(T_Vlow)

		# Get Group List
		Group = []
		for row in sub_DB.Net_Form._DataGridView.Rows:
			if not row.Cells[4].Value == "None":
				if not row.Cells[4].Value in Group:
					Group.append(row.Cells[4].Value)

		# Initialize
		Group_Eye_Measure_Result = {}
		for key in Group:
			Group_Eye_Measure_Result[key] = []
			T_Vhigh=[]
			T_Vlow=[]
			T_Vref=[]		
			for row in sub_DB.Net_Form._DataGridView.Rows:		
				if key == row.Cells[4].Value:				
					for data in Eye_Measure_Results[row.Cells[1].Value][3]:
						T_Vhigh.append(data)
					for data in Eye_Measure_Results[row.Cells[1].Value][4]:
						T_Vref.append(data)
					for data in Eye_Measure_Results[row.Cells[1].Value][5]:
						T_Vlow.append(data)

			margin = UI - (max([max(T_Vhigh), max(T_Vlow)]) - min([min(T_Vhigh), min(T_Vlow)])) - float(self._TextBox_TdIVW.Text)*UI
			jitter = max(T_Vref) - min(T_Vref)
			#width = UI - jitter
			width = UI - (max([max(T_Vhigh), max(T_Vlow)]) - min([min(T_Vhigh), min(T_Vlow)]))

			for row in sub_DB.Net_Form._DataGridView.Rows:
				if key == row.Cells[4].Value:
					Eye_Measure_Results[row.Cells[1].Value][0] = width
					Eye_Measure_Results[row.Cells[1].Value][1] = jitter
					Eye_Measure_Results[row.Cells[1].Value][2] = margin		

		sub_DB.Eye_Measure_Results = Eye_Measure_Results
		#Log("		(Eye Measure) = Done")
		return Eye_Measure_Results

	except Exception as e:		
		Log("	<Eye Analyze> = Failed")
		Log(traceback.format_exc())
		print traceback.format_exc()
		MessageBox.Show("Fail to analyze eye","Warning")						
		EXIT()