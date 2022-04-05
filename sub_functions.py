import os
import re
import time
import clr
import shutil
import traceback
import sub_ScriptEnv
import sub_AEDT
import sub_DB

clr.AddReference('Microsoft.Office.Interop.Excel')

import System.Drawing
import System.Windows.Forms

from sub_functions import *
from System.Drawing import *
from System.Windows.Forms import *
from Microsoft.Office.Interop import Excel

def HighLight(key, TextBox):
	# Creat List from TextBox	
	temp_text = TextBox.Text.split("\n")

	# Initialize : Set all color black
	for i in range(0, len(temp_text)):
		TextBox.Select(TextBox.GetFirstCharIndexFromLine(i), len(temp_text[i]))
		if temp_text[i].find("#") != -1:		
			TextBox.SelectionColor = Color.Green
		else:
			TextBox.SelectionColor = Color.Black
		TextBox.SelectionFont = Font("Arial", 9)

	# Find the position(line number) = iter
	iter = 0
	for line in temp_text:
		if line.find(key[0]) != -1:
			del key[0]
			if key==[]:
				break
		iter += 1
	
	TextBox.Select(TextBox.GetFirstCharIndexFromLine(iter), len(temp_text[iter]))
	TextBox.Focus()
	TextBox.SelectionColor = Color.Blue
	TextBox.SelectionFont = Font("Arial", 10, FontStyle.Bold)

def Load_env(File):
	# Open *.cenv or *.uenv File
	temp_DB = {}	
	#level = 0
	with open(File) as fp:
		# Load Input File
		for line in fp:			
			# not blank and comment
			#temp_list = []
			if line.strip() != "" and line.lstrip()[0] != "#":
				# find parent node symbol : []				
				key = ""
				if line.find("[") != -1:
					str_parent = "[" + line.split("[")[1].split("]")[0] + "]"
					str_child = ""
					str_grandchild = ""
					# find data symbol : =
					temp_list = []
					if line.find("=") != -1:
						# back up the data
						line = line.strip().replace(" ","")
						key = str_parent
						for cell in list(filter(None, line.strip().split("=")[-1].split(","))):
							temp_list.append(cell)
				# find child node symbol : <>
				elif line.find("<") != -1:
					str_child = "<" + line.split("<")[1].split(">")[0] + ">"
					str_grandchild = ""
					# find data symbol : =
					temp_list = []
					if line.find("=") != -1:
						# back up the data
						line = line.strip().replace(" ","")
						key = str_child + str_parent
						for cell in list(filter(None, line.strip().split("=")[-1].split(","))):
							temp_list.append(cell)

				# find grandchild node symbol : ()
				elif line.find("(") != -1:
					str_grandchild = "(" + line.split("(")[1].split(")")[0] + ")"
					# find data symbol : =
					temp_list = []
					if line.find("=") != -1:
						# back up the data
						line = line.strip().replace(" ","")
						key = str_grandchild + str_child + str_parent
						for cell in list(filter(None, line.strip().split("=")[-1].split(","))):
							temp_list.append(cell)

				# find grandchild node symbol : ()				
				elif line.find("=") != -1:
					# back up the data
					line = line.strip().replace(" ","")
					key = str_grandchild + str_child + str_parent
					for cell in list(filter(None, line.strip().split("=")[-1].split(","))):
							temp_list.append(cell)

				if key:
					temp_DB[key] = temp_list

	fp.close()

	return temp_DB

def Net_Identify(name, Uenv):
	Group = 5 # OTHER
	Match = ""

	for key in Uenv:
		if "<Ignore>" in key:
			name = name.replace(Uenv[key][0], "")

	for keyword in Uenv["<DM>[Net Identification]"]:
		keyword = keyword.replace("?","[0-9]+")
		m = re.search(keyword, name, re.I) # re.I (or re.IGNORECASE) = No distinction between upper and lower case letters.
		if m:
			Match = m.group()
			Group = 0 # "DM"
			break

	for keyword in Uenv["<CLK>[Net Identification]"]:
		keyword = keyword.replace("?","[0-9]+")
		m = re.search(keyword, name, re.I)
		if m:
			Match = m.group()
			Group = 3 # CLK
			break

	for keyword in Uenv["<ADDR>[Net Identification]"]:		
		keyword = keyword.replace("?","[0-9]+")
		m = re.search(keyword, name, re.I)
		if m:
			Match = m.group()
			Group = 4 # ADDR
			break

	for keyword in Uenv["<DQS>[Net Identification]"]:
		keyword = keyword.replace("?","[0-9]+")
		m = re.search(keyword, name, re.I)
		if m:
			Match = m.group()
			Group = 2 # DQS
			break

	for keyword in Uenv["<DQ>[Net Identification]"]:
		keyword = keyword.replace("?","[0-9]+")
		m = re.search(keyword, name, re.I)
		if m:
			Match = m.group()
			Group = 1 # DQ
			break

	return Group, Match

def Cal_Vref_AEDT(self, Location):
	try:
		global path
		path = os.path.dirname(os.path.abspath(__file__))		

		# Initialize
		Log("		(AEDT Launch) = Done")
		oProject = sub_DB.AEDT["Project"]
		oDesign = sub_DB.AEDT["Design"]
		oModule = oDesign.GetModule("ReportSetup")
		Report_Name = []
		Report_Name = self._CheckedListBox_ReportName.CheckedItems
		for report in Report_Name:	
			oModule.UpdateReports([report])

		# find total simulation time
		# Export Report using "ExportToFile" to find total simulation time		
		File = sub_DB.temp_dir + "\\temp.csv"
		oModule.UpdateReports([Report_Name[0]])
		oModule.ExportToFile(Report_Name[0], File)		

		#	Get time unit
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

		#	Get Variable string
		idx = 1
		pre_var_string = ""
		for i in range(1, len(temp_data)):
			if "-" in temp_data[i]:
				var_string = temp_data[i].split("]")[-1].split("-")[-1].strip().replace("\"","")				
			else:
				var_string = ""
				break
		sub_DB.var_string = var_string

		#	Get last time value
		with open(File) as fp:
			for line in reversed(list(fp)):
				t_total = line.split(",")[iter] + t_unit
				break
		fp.close()
		
		sub_DB.total_waveform_length = t_total
		#os.remove(File)
		Log("		(Get total waveform Length) = %s" % t_total)

		# Create temp eye diagram	
		PlotList = []
		for i in range(0, sub_DB.Net_Form._DataGridView.Rows.Count):
			if sub_DB.Net_Form._DataGridView.Rows[i].Cells[0].Value:
				PlotList.append(sub_DB.Net_Form._DataGridView.Rows[i].Cells[1].Value.replace("\"","").split("[")[0].strip())

		# Create Variable List
		Var_list = []
		Var_list.append("Time:=")
		Var_list.append(["All"])
		Sim_type = oDesign.GetDesignType()			
		if Sim_type == "Circuit Netlist":
			pass
		else:
			Global_Varlist = oProject.GetVariables()
			Local_Varlist = oDesign.GetVariables()					
			for var in Global_Varlist:
				Var_list.append(var + ":=")
				Var_list.append(["All"])
		
		oModule.CreateReport("temp_eye", "Eye Diagram", "Rectangular Plot", self._ComboBox_SolutionName.Text, 
		[
			"NAME:Context",
			"SimValueContext:="	, [1,0,2,0,False,False,-1,1,0,1,1,"",0,0,"DE",False,"0","DP",False,"500000000","DT",False,"0.001","NUMLEVELS",False,"0","WE",False,sub_DB.total_waveform_length,"WM",False,sub_DB.total_waveform_length,"WN",False,"0ps","WS",False,"0ps"]
		], 
		Var_list, 
		[
			"Component:="		, PlotList
		], 
		[
			"Unit Interval:="	, str(1/(float(sub_DB.Eye_Form._ComboBox_DataRate.Text)*1000000))+"s",
			"Offset:="		, str(sub_DB.Option_Form._TextBox_EyeOffset.Text) + "ns",
			"Auto Delay:="		, True,
			"Manual Delay:="	, "0ps",
			"AutoCompCrossAmplitude:=", True,
			"CrossingAmplitude:="	, "0mV",
			"AutoCompEyeMeasurementPoint:=", True,
			"EyeMeasurementPoint:="	, (1/(float(self._ComboBox_DataRate.Text)*1000000))/2		
		])
		Log("		(Create temp eye-diagram) = Done")

		# Creat Eye Measure Data	
		oModule.AddTraceCharacteristics("temp_eye", "EyeJitterRMS", ["0"], ["Full"])
		oModule.AddTraceCharacteristics("temp_eye", "EyeLevelZero", ["0"], ["Full"])
		oModule.AddTraceCharacteristics("temp_eye", "EyeLevelOne", ["0"], ["Full"])
		oModule.AddTraceCharacteristics("temp_eye", "EyeJitterP2P", ["0"], ["Full"])
	
		# Export Eye Measure Data .\Resources\temp.csv
		legend_file = sub_DB.temp_dir + "\\temp1.csv"		
		oModule.ExportTableToFile("temp_eye", legend_file, "Legend")
		Log("		(Export Eye Measure Data) = Done")
	
		# Export Uniform Report	
		File = sub_DB.temp_dir + "\\Waveforms.csv"		
		oModule.UpdateReports(["temp_eye"])
		oModule.ExportUniformPointsToFile("temp_eye", File, "0ns", t_total, "1ps", False)
		sub_DB.Waveform_File = File
		Log("		(Export Uniform Wavefrom File) = Done")

		# Delete temp Report	
		oModule.DeleteReports(["temp_eye"])
		Log("		(Delete temp eye-diagram) = Done")

		# Read Exported Eye Measure Data	
		Jitter_RMS = []
		Level_0 = []
		Level_1 = []
		Jitter_P2P = []
		Jitter = {}
		with open(legend_file) as fp:
			# skip the first line
			fp.readline()
			for line in fp:			
				Jitter_RMS.append(float(line.split(",")[1].strip()))
				Level_0.append(float(line.split(",")[2].strip()))
				Level_1.append(float(line.split(",")[3].strip()))
				Jitter_P2P.append(float(line.split(",")[4].strip()))
				Jitter[line.split(",")[0].split(" ")[0].strip()] = float(line.split(",")[1].strip())
		fp.close()
		#os.remove(legend_file)
		Log("		(Read Eye Measure Data) = Done")

		# Check time and voltage unit
		if max(Jitter_RMS) < 1: # Time unit should be "ns"
			for i in range(0, len(Jitter_RMS)):
				Jitter_RMS[i] = Jitter_RMS[i]*1000
				Jitter_P2P[i] = Jitter_P2P[i]*1000

			for key in Jitter:
				Jitter[key] = Jitter[key]*1000
		if max(Level_1) < 5:
			for i in range(0, len(Level_1)):
				Level_0[i] = Level_0[i]*1000
				Level_1[i] = Level_1[i]*1000		
		sub_DB.Jitter_RMS = Jitter
		Log("		(Check Voltage and Time Unit) = Done")

		# Analyze Jitter - Find mean RMS Jitter Net	
		Jitter_RMS_Min = min(Jitter_RMS)
		Min_idx = Jitter_RMS.index(min(Jitter_RMS))
		Log("		(Find min. RMS Jitter) = Done")
		
		# Calculate Vref	
		Vref = round((float(Level_0[Min_idx]) + float(Level_1[Min_idx]))/2,2)
		Log("		(Calculate Vref) = Done, %s[mV]" % Vref)
	
		time.sleep(0.5)	

		sub_DB.Vref = Vref	
		return Vref

	except Exception as e:		
		Log("	<AEDT Vref Calculation> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to AEDT Calculate Vref","Warning")		
		EXIT()

def Cal_Vref_WaveForm():
	try:
		Log("		(Get Target Waveforms) = Done")
		# Delete non-target trace data	
		for row in sub_DB.Net_Form._DataGridView.Rows:
			if not row.Cells[0].Value:
				if row.Cells[1].Value in sub_DB.Waveform.keys():				
					del sub_DB.Waveform[row.Cells[1].Value]			

		Log("		(Get Min./Max Waveform Values) = Done")
		# Get Min/Max Average and Calculate Vref	
		Max = []
		Min = []	
		for key in sub_DB.Waveform:
			Max.append(max(sub_DB.Waveform[key]))
			Min.append(min(sub_DB.Waveform[key]))

		Vref = round((sum(Max, 0.0)/len(Max) + sum(Min, 0.0)/len(Min))/2, 2)
		Log("		(Calculate Vref) = Done, %s[mV]" % Vref)
	
		sub_DB.Vref = Vref	
		return Vref	

	except Exception as e:		
		Log("	<CSV Vref Calculation> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to CSV Calculate Vref","Warning")		
		EXIT()

def Measure_Eye(self, Location):
	try:
		sub_DB.Cal_Form.Text = "Analyzing Eye..."	

		# Get Vref
		sub_DB.Cal_Form._Label_Vref.Text = "Analyzing Eye."
		sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
		Vref = float(self._TextBox_VcentDQ.Text)
		Log("		(Vref) = %s[mV]" % Vref)

		# Calculate Voltage Boundary
		sub_DB.Cal_Form._Label_Vref.Text = "Analyzing Eye.."
		sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
		V_high = Vref + float(self._TextBox_VdIVW.Text)/2
		V_low = Vref - float(self._TextBox_VdIVW.Text)/2
		Log("		(V_high) = %s[mV]" % V_high)
		Log("		(V_low) = %s[mV]" % V_low)

		# Calculate Unit Interval [ps]
		sub_DB.Cal_Form._Label_Vref.Text = "Analyzing Eye..."
		sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
		UI = int(round(1/(float(self._ComboBox_DataRate.Text))*1000000))
		Log("		(Unit Interval) = %s[ps]" % UI)

		# Get Waveform
		if sub_DB.InputFile_Flag == 1: # *.aedt input file
			sub_DB.Cal_Form._Label_Vref.Text = "Analyzing Eye...."
			sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
			Log("		(Waveform)")
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

			for cell in data:
				key = cell[0].split("[")[0]
				del cell[0]
				Waveform[key] = cell
				Log("			= %s" % key)

			# Check time unit - Does not check time unit in AEDT input file process (1ps uniform exported)
			#if sub_DB.Unit["Time"].lower() == "ps":
			#	pass
			#elif sub_DB.Unit["Time"].lower() == "ns":
			#	for i in range(0, len(Time)):
			#		Time[i] = Time[i]*1000
			#else:
			#	MessageBox.Show("The time unit in the input csv file is not supported.","Warning",MessageBoxButtons.OK, MessageBoxIcon.Warning)
			#sub_DB.Time = Time

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

		elif sub_DB.InputFile_Flag == 2: # *.csv input file
			Log("		(Waveform)")
			Log("			= Imported from CSV")
			Waveform = sub_DB.Waveform

		# Measure Eye Width & Margin
		sub_DB.Cal_Form._Label_Vref.Text = "Analyzing Eye."	
		Eye_Measure_Results = {}
		temp_Resutls = {}
		T_Vhigh=[]
		T_Vlow=[]
		T_Vref=[]
		if not sub_DB.CSV_flag:
			for key in Waveform:		
				sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
				T_Vhigh=[]
				T_Vlow=[]
				T_Vref=[]
				# Calculate eye offset
				input_eye_offset = int(float(sub_DB.Option_Form._TextBox_EyeOffset.Text)*1000)
				time_idx = 0
				while(1):
					vol_pre = Waveform[key][time_idx]
					vol_post = Waveform[key][time_idx+1]
					if (vol_pre - Vref) * (vol_post - Vref) < 0 : # for rising transition					
						eye_offset = Interpolate_1st(sub_DB.Time[time_idx], vol_pre, sub_DB.Time[time_idx+1], vol_post, Vref) - int(round(UI/2))					
						break
					time_idx += 1

				# Measure Time points			
				for i in range(eye_offset + input_eye_offset, len(Waveform[key])-1):
					vol_pre = Waveform[key][i]
					vol_post = Waveform[key][i+1]
					# Measure T_Vhigh
					if (vol_pre - V_high) * (vol_post - V_high) < 0 :					
						time_idx = Interpolate_1st(sub_DB.Time[i], vol_pre, sub_DB.Time[i+1], vol_post, V_high)
						T_Vhigh.append(time_idx % UI)
					
					# Measure T_low
					if (vol_pre - V_low) * (vol_post - V_low) < 0 :
						time_idx = Interpolate_1st(sub_DB.Time[i], vol_pre, sub_DB.Time[i+1], vol_post, V_low)
						T_Vlow.append(time_idx % UI)

					# Measure T_Vref
					if (vol_pre - Vref) * (vol_post - Vref) < 0 :
						time_idx = Interpolate_1st(sub_DB.Time[i], vol_pre, sub_DB.Time[i+1], vol_post, Vref)
						T_Vref.append(time_idx % UI)

				# Calculate eye width, jitter, and margin
				margin = UI - (max([max(T_Vhigh), max(T_Vlow)]) - min([min(T_Vhigh), min(T_Vlow)])) - float(self._TextBox_TdIVW.Text)*UI
				jitter = max(T_Vref) - min(T_Vref)
				#width = UI - jitter
				width = UI - (max([max(T_Vhigh), max(T_Vlow)]) - min([min(T_Vhigh), min(T_Vlow)]))

				# Back-up the measured data
				Eye_Measure_Results[key] = []
				Eye_Measure_Results[key].append(width)
				Eye_Measure_Results[key].append(jitter)
				Eye_Measure_Results[key].append(margin)
				Eye_Measure_Results[key].append(T_Vhigh)
				Eye_Measure_Results[key].append(T_Vref)
				Eye_Measure_Results[key].append(T_Vlow)

		else:
			for key in Waveform:			
				sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
				T_Vhigh=[]
				T_Vlow=[]
				T_Vref=[]
				#t_Vhigh=[]
				#t_Vlow=[]
				#t_Vref=[]

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
				#width = UI - jitter
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

		#print sub_DB.Cal_Form._ProgressBar_Vref.Value
		sub_DB.Eye_Measure_Results = Eye_Measure_Results
		Log("		(Eye Measure) = Done")
		return Eye_Measure_Results

	except Exception as e:		
		Log("	<Eye Analyze> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to analyze eye","Warning")						
		EXIT()

def Plot_Eye(Report_Name, PlotList, vmin, vmax, Eye_Measure_Results, Bitmap_Flag):
	try:
		oProject = sub_DB.AEDT["Project"]
		oDesign = sub_DB.AEDT["Design"]
		oModule = oDesign.GetModule("ReportSetup")	
		Log("		(AEDT Setup) = Done")

		Report_names = oModule.GetAllReportNames()
		if Report_Name in Report_names:
			oModule.DeleteReports([Report_Name])
		Log("		(Delete Duplicate Reports) = Done")

		# Create Variable List
		Var_list = []
		Var_list.append("Time:=")
		Var_list.append(["All"])
		Sim_type = oDesign.GetDesignType()			
		if Sim_type == "Circuit Netlist":
			pass
		else:
			Global_Varlist = oProject.GetVariables()
			Local_Varlist = oDesign.GetVariables()					
			for var in Global_Varlist:
				Var_list.append(var + ":=")
				Var_list.append(["All"])
		Log("		(Create Variable List) = Done")

		# Plot Eye
		oModule.CreateReport(Report_Name, "Eye Diagram", "Rectangular Plot", sub_DB.Eye_Form._ComboBox_SolutionName.Text, 
		[
			"NAME:Context",
			"SimValueContext:="	, [1,0,2,0,False,False,-1,1,0,1,1,"",0,0,"DE",False,"0","DP",False,"500000000","DT",False,"0.001","NUMLEVELS",False,"0","WE",False,sub_DB.total_waveform_length,"WM",False,sub_DB.total_waveform_length,"WN",False,"0ps","WS",False,"0ps"]
		], 
		Var_list, 
		[
			"Component:="		, PlotList
		], 
		[
			"Unit Interval:="	, str(1/(float(sub_DB.Eye_Form._ComboBox_DataRate.Text)*1000000))+"s",
			"Offset:="		, str(sub_DB.Option_Form._TextBox_EyeOffset.Text) + "ns",
			"Auto Delay:="		, True,
			"Manual Delay:="	, "0ps",
			"AutoCompCrossAmplitude:=", True,
			"CrossingAmplitude:="	, "0mV",
			"AutoCompEyeMeasurementPoint:=", True,
			"EyeMeasurementPoint:="	, (1/(float(sub_DB.Eye_Form._ComboBox_DataRate.Text)*1000000))/2
		])
		Log("		(Plot Eye) = Done")

		Log("		(Change Property)")
		for eyename in PlotList:			
			if sub_DB.var_string == "":
				oModule.ChangeProperty(["NAME:AllTabs",
						  ["NAME:Eye", ["NAME:PropServers", Report_Name + ":EyeDisplayTypeProperty"], ["NAME:ChangedProps"
							, ["NAME:Rectangular Plot", "Value:=", False]]],
						  ["NAME:Attributes", ["NAME:PropServers", Report_Name + ":" + eyename + ":Curve1:Eye"], ["NAME:ChangedProps"
							, ["NAME:View Type", "Value:=", "Line"]
							, ["NAME:Line Color", "R:=", 0, "G:=", 0, "B:=", 255]
							, ["NAME:Line Width", "Value:=", "2"]]],
						  ["NAME:Legend", ["NAME:PropServers", Report_Name + ":Legend"], ["NAME:ChangedProps"
							, ["NAME:Show Trace Name", "Value:=", False]
							, ["NAME:Show Variation Key", "Value:=", False]
							, ["NAME:Show Solution Name", "Value:=", True]]],
						  ["NAME:Axis", ["NAME:PropServers", Report_Name + ":AxisY1"], ["NAME:ChangedProps"
							, ["NAME:Display Name", "Value:=", False]]],
						  ["NAME:Scaling", ["NAME:PropServers", Report_Name + ":AxisY1"], ["NAME:ChangedProps"
							, ["NAME:Specify Min", "Value:=", True]
							, ["NAME:Specify Max", "Value:=", True]
							, ["NAME:Min", "Value:=", str(vmin) + "mV"]
							, ["NAME:Max", "Value:=", str(vmax) + "mV"]]]])
			else:
				oModule.ChangeProperty(["NAME:AllTabs",
						  ["NAME:Eye", ["NAME:PropServers", Report_Name + ":EyeDisplayTypeProperty"], ["NAME:ChangedProps"
							, ["NAME:Rectangular Plot", "Value:=", False]]],
						  ["NAME:Attributes", ["NAME:PropServers", Report_Name + ":" + eyename + ":" + sub_DB.var_string + " [Curve1]:Eye"], ["NAME:ChangedProps"
							, ["NAME:View Type", "Value:=", "Line"]
							, ["NAME:Line Color", "R:=", 0, "G:=", 0, "B:=", 255]
							, ["NAME:Line Width", "Value:=", "2"]]],
						  ["NAME:Legend", ["NAME:PropServers", Report_Name + ":Legend"], ["NAME:ChangedProps"
							, ["NAME:Show Trace Name", "Value:=", False]
							, ["NAME:Show Variation Key", "Value:=", False]
							, ["NAME:Show Solution Name", "Value:=", True]]],
						  ["NAME:Axis", ["NAME:PropServers", Report_Name + ":AxisY1"], ["NAME:ChangedProps"
							, ["NAME:Display Name", "Value:=", False]]],
						  ["NAME:Scaling", ["NAME:PropServers", Report_Name + ":AxisY1"], ["NAME:ChangedProps"
							, ["NAME:Specify Min", "Value:=", True]
							, ["NAME:Specify Max", "Value:=", True]
							, ["NAME:Min", "Value:=", str(vmin) + "mV"]
							, ["NAME:Max", "Value:=", str(vmax) + "mV"]]]])
		Log("			= Report Name Changed, %s" % Report_Name)
		Log("			= Line Width Changed, 2")
		Log("			= Line Color Changed, R:0, G:0, B:255")
		Log("			= Y Axis Changed, Max.:%s[mV] Min.:%s[mV]" % (str(vmax), str(vmin)))
	
		oModule.ChangeProperty(["NAME:AllTabs",
			["NAME:Axis", ["NAME:PropServers", Report_Name + ":AxisX"], ["NAME:ChangedProps", ["NAME:Display Name", "Value:=", False]]],
			["NAME:Scaling", ["NAME:PropServers", Report_Name + ":AxisX"], ["NAME:ChangedProps", ["NAME:Specify Max", "Value:=", True],
			["NAME:Max", "Value:=", str(2/(float(sub_DB.Eye_Form._ComboBox_DataRate.Text)*1000000)) + "s"]]]])
		Log("			= X Axis Changed")

		oModule.ChangeProperty(["NAME:AllTabs",["NAME:Legend",["NAME:PropServers", Report_Name + ":Legend"],
				["NAME:ChangedProps",["NAME:Show Trace Name","Value:=", False]]]])
		Log("			= Show Trace Name, False")

		oModule.ChangeProperty(["NAME:AllTabs",["NAME:Legend",["NAME:PropServers", Report_Name + ":Legend"],
				["NAME:ChangedProps",["NAME:Show Solution Name","Value:=", False]]]])
		Log("			= Show Solution Name, False")

		oModule.ChangeProperty(["NAME:AllTabs",["NAME:Legend",["NAME:PropServers", Report_Name + ":Legend"],
				["NAME:ChangedProps",["NAME:Show Variation Key","Value:=", False]]]])
		Log("			= Show Variation Key, False")
	
		oModule.ChangeProperty(["NAME:AllTabs",["NAME:Legend",["NAME:PropServers", Report_Name + ":Legend"],
				["NAME:ChangedProps",["NAME:DockMode","Value:=", "Dock Left"]]]])
		Log("			= Legend Location (Dock Left)")
	
	
		Vref = float(sub_DB.Eye_Form._TextBox_VcentDQ.Text)
		V_high = Vref + float(sub_DB.Eye_Form._TextBox_VdIVW.Text)/2
		V_low = Vref - float(sub_DB.Eye_Form._TextBox_VdIVW.Text)/2
		T_left = round(1/float(sub_DB.Eye_Form._ComboBox_DataRate.Text)*1000000) - Eye_Measure_Results[PlotList[0]][0]/float(2)
		T_right = round(1/float(sub_DB.Eye_Form._ComboBox_DataRate.Text)*1000000) + Eye_Measure_Results[PlotList[0]][0]/float(2)
	
		oModule.ChangeProperty(["NAME:AllTabs", ["NAME:Mask", ["NAME:PropServers",
				  Report_Name + ":EyeDisplayTypeProperty"], ["NAME:ChangedProps", ["NAME:Mask", "Version:=",
				  1, "ShowLimits:=", False, "UpperLimit:=", 1, "LowerLimit:=", 0, "XUnits:=", "ps", "YUnits:=",
				  "mV", ["NAME:MaskPoints",T_left, V_high,T_left, V_low,T_right, V_low,T_right, V_high]]]]])
		Log("			= Create Eye Mask")

		noteh = (vmax - Vref) / (vmax - vmin) * 9500
		oModule.AddNote(Report_Name, ["NAME:NoteDataSource", ["NAME:NoteDataSource", "SourceName:=",
						"Note1", "HaveDefaultPos:=", True, "DefaultXPos:=", 5500, "DefaultYPos:=",
						noteh, "String:=", str(Eye_Measure_Results[PlotList[0]][0]) + " / " + str(round(sub_DB.Jitter_RMS[PlotList[0]],1))]])
		Log("			= Add Note, Width:%s[ps] Jitter(RMS):%s[ps]" % (str(Eye_Measure_Results[PlotList[0]][0]), str(round(sub_DB.Jitter_RMS[PlotList[0]],1))))

		oModule.ChangeProperty(["NAME:AllTabs",
					  ["NAME:Note", ["NAME:PropServers", Report_Name + ":Note1"], ["NAME:ChangedProps"
					  , ["NAME:Background Visibility", "Value:=", False]
					  , ["NAME:Border Visibility", "Value:=", False]
					  , ["NAME:Note Font", "Height:=", -17, "Width:=",
						0, "Escapement:=", 0, "Orientation:=", 0, "Weight:=", 700, "Italic:=", 0, "Underline:=",
						0, "StrikeOut:=", 0, "CharSet:=", 0, "OutPrecision:=", 3, "ClipPrecision:=", 2, "Quality:=",
						1, "PitchAndFamily:=", 34, "FaceName:=", "Arial", "R:=", 0, "G:=", 0, "B:=", 0]]]])

		if Bitmap_Flag:		
			imgw = int(sub_DB.Option_Form._TextBox_ImageWidth.Text)
			imgh = imgw / 5 * 4
			img_path = sub_DB.Option_Form._TextBox_OutputExcelFile.Text
			img_path = img_path.replace("\\"+img_path.split("\\")[-1],"")
			oModule.ExportImageToFile(Report_Name, img_path + "\\" + Report_Name + ".gif", imgw * 2, imgh * 2)
			sub_DB.Excel_Img_File.append(img_path + "\\" + Report_Name + ".gif")
			Log("			= Save Image File, %s" % img_path + "\\" + Report_Name + ".gif")

	except Exception as e:		
		Log("	<Eye Plot> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to plot eye","Warning")						
		EXIT()

def Plot_Eye_Import(Report_Name, Import_file, PlotList, vmin, vmax, Eye_Measure_Results, Bitmap_Flag):
	try:
		oProject = sub_DB.AEDT["Project"]
		oDesign = sub_DB.AEDT["Design"]
		oModule = sub_DB.AEDT["Module"]
		Log("		(AEDT Setup) = Done")

		# Delete duplicate reports
		Report_names = oModule.GetAllReportNames()
		if Report_Name in Report_names:
			oModule.DeleteReports([Report_Name])
		Log("		(Delete Duplicate Reports) = Done")

		# Create Variable List
		Global_Varlist = oProject.GetVariables()
		Local_Varlist = oDesign.GetVariables()
		Var_list = []
		Var_list.append("Time:=")
		Var_list.append(["All"])
		for var in Global_Varlist:
			Var_list.append(var + ":=")
			Var_list.append(["All"])
		Log("		(Create Variable List) = Done")

		oModule.CreateReport(Report_Name, "Eye Diagram", "Rectangular Plot", "NexximTransient", 
		[
			"NAME:Context",
			"SimValueContext:="	, [1,0,2,0,False,False,-1,1,0,1,1,"",0,0,"DE",False,"0","DP",False,"500000000","DT",False,"0.001","NUMLEVELS",False,"1","WE",False,"10ns","WM",False,"10ns","WN",False,"0ns","WS",False,"0ns"]
		], 
		Var_list, 
		[
			"Component:="		, ["V(net_1)"]
		], 
		[
			"Unit Interval:="	, str(1/(float(sub_DB.Eye_Form._ComboBox_DataRate.Text)*1000000))+"s",
			"Offset:="		, str(sub_DB.Option_Form._TextBox_EyeOffset.Text) + "ns",
			"Auto Delay:="		, True,
			"Manual Delay:="	, "0ps",
			"AutoCompCrossAmplitude:=", True,
			"CrossingAmplitude:="	, "0mV",
			"AutoCompEyeMeasurementPoint:=", True,
			"EyeMeasurementPoint:="	, (1/(float(sub_DB.Eye_Form._ComboBox_DataRate.Text)*1000000))/2
		])
		oModule.ImportIntoReport(Report_Name, Import_file)
		
		oModule.DeleteTraces(["%s:=" % Report_Name, ["V(net_1)"]])
		Log("		(Plot Eye) = Done")

		Log("		(Change Property)")
		for eyename in PlotList:
			oModule.ChangeProperty(["NAME:AllTabs",
					  ["NAME:Eye", ["NAME:PropServers", Report_Name + ":EyeDisplayTypeProperty"], ["NAME:ChangedProps"
						, ["NAME:Rectangular Plot", "Value:=", False]]],
					  ["NAME:Attributes", ["NAME:PropServers", Report_Name + ":" + eyename + ":Curve1:Eye"], ["NAME:ChangedProps"
						, ["NAME:View Type", "Value:=", "Line"]
						, ["NAME:Line Color", "R:=", 0, "G:=", 0, "B:=", 255]
						, ["NAME:Line Width", "Value:=", "2"]]],
					  ["NAME:Legend", ["NAME:PropServers", Report_Name + ":Legend"], ["NAME:ChangedProps"
						, ["NAME:Show Trace Name", "Value:=", False]
						, ["NAME:Show Variation Key", "Value:=", False]
						, ["NAME:Show Solution Name", "Value:=", True]]],
					  ["NAME:Axis", ["NAME:PropServers", Report_Name + ":AxisY1"], ["NAME:ChangedProps"
						, ["NAME:Display Name", "Value:=", False]]],
					  ["NAME:Scaling", ["NAME:PropServers", Report_Name + ":AxisY1"], ["NAME:ChangedProps"
						, ["NAME:Specify Min", "Value:=", True]
						, ["NAME:Specify Max", "Value:=", True]
						, ["NAME:Min", "Value:=", str(vmin) + "mV"]
						, ["NAME:Max", "Value:=", str(vmax) + "mV"]]]])
		Log("			= Report Name Changed, %s" % Report_Name)
		Log("			= Line Width Changed, 2")
		Log("			= Line Color Changed, R:0, G:0, B:255")
		Log("			= Y Axis Changed, Max.:%s[mV] Min.:%s[mV]" % (str(vmax), str(vmin)))

		oModule.ChangeProperty(["NAME:AllTabs",
			["NAME:Axis", ["NAME:PropServers", Report_Name + ":AxisX"], ["NAME:ChangedProps", ["NAME:Display Name", "Value:=", False]]],
			["NAME:Scaling", ["NAME:PropServers", Report_Name + ":AxisX"], ["NAME:ChangedProps", ["NAME:Specify Max", "Value:=", True],
			["NAME:Max", "Value:=", str(2/(float(sub_DB.Eye_Form._ComboBox_DataRate.Text)*1000000)) + "s"]]]])
		Log("			= X Axis Changed")

		oModule.ChangeProperty(["NAME:AllTabs",["NAME:Legend",["NAME:PropServers", Report_Name + ":Legend"],
				["NAME:ChangedProps",["NAME:Show Trace Name","Value:=", False]]]])
		Log("			= Show Trace Name, False")

		oModule.ChangeProperty(["NAME:AllTabs",["NAME:Legend",["NAME:PropServers", Report_Name + ":Legend"],
				["NAME:ChangedProps",["NAME:Show Solution Name","Value:=", False]]]])
		Log("			= Show Solution Name, False")

		oModule.ChangeProperty(["NAME:AllTabs",["NAME:Legend",["NAME:PropServers", Report_Name + ":Legend"],
				["NAME:ChangedProps",["NAME:Show Variation Key","Value:=", False]]]])
		Log("			= Show Variation Key, False")
	
		oModule.ChangeProperty(["NAME:AllTabs",["NAME:Legend",["NAME:PropServers", Report_Name + ":Legend"],
				["NAME:ChangedProps",["NAME:DockMode","Value:=", "Dock Left"]]]])
		Log("			= Legend Location (Dock Left)")
	
		Vref = float(sub_DB.Eye_Form._TextBox_VcentDQ.Text)
		V_high = Vref + float(sub_DB.Eye_Form._TextBox_VdIVW.Text)/2
		V_low = Vref - float(sub_DB.Eye_Form._TextBox_VdIVW.Text)/2
		T_left = round(1/float(sub_DB.Eye_Form._ComboBox_DataRate.Text)*1000000) - Eye_Measure_Results[PlotList[0]][0]/float(2)
		T_right = round(1/float(sub_DB.Eye_Form._ComboBox_DataRate.Text)*1000000) + Eye_Measure_Results[PlotList[0]][0]/float(2)
	
		oModule.ChangeProperty(["NAME:AllTabs", ["NAME:Mask", ["NAME:PropServers",
				  Report_Name + ":EyeDisplayTypeProperty"], ["NAME:ChangedProps", ["NAME:Mask", "Version:=",
				  1, "ShowLimits:=", False, "UpperLimit:=", 1, "LowerLimit:=", 0, "XUnits:=", "ps", "YUnits:=",
				  "mV", ["NAME:MaskPoints",T_left, V_high,T_left, V_low,T_right, V_low,T_right, V_high]]]]])
		Log("			= Create Eye Mask")

		noteh = (vmax - Vref) / (vmax - vmin) * 9500
		oModule.AddNote(Report_Name, ["NAME:NoteDataSource", ["NAME:NoteDataSource", "SourceName:=",
						"Note1", "HaveDefaultPos:=", True, "DefaultXPos:=", 5500, "DefaultYPos:=",
						noteh, "String:=", str(Eye_Measure_Results[PlotList[0]][0]) + " / " + str(Eye_Measure_Results[PlotList[0]][1])]])
		Log("			= Add Note, Width:%s[ps] Jitter(RMS):%s[ps]" % (str(Eye_Measure_Results[PlotList[0]][0]), str(Eye_Measure_Results[PlotList[0]][1])))

		oModule.ChangeProperty(["NAME:AllTabs",
					  ["NAME:Note", ["NAME:PropServers", Report_Name + ":Note1"], ["NAME:ChangedProps"
					  , ["NAME:Background Visibility", "Value:=", False]
					  , ["NAME:Border Visibility", "Value:=", False]
					  , ["NAME:Note Font", "Height:=", -17, "Width:=",
						0, "Escapement:=", 0, "Orientation:=", 0, "Weight:=", 700, "Italic:=", 0, "Underline:=",
						0, "StrikeOut:=", 0, "CharSet:=", 0, "OutPrecision:=", 3, "ClipPrecision:=", 2, "Quality:=",
						1, "PitchAndFamily:=", 34, "FaceName:=", "Arial", "R:=", 0, "G:=", 0, "B:=", 0]]]])

		if Bitmap_Flag:
			imgw = int(sub_DB.Option_Form._TextBox_ImageWidth.Text)
			imgh = imgw / 5 * 4
			img_path = sub_DB.Option_Form._TextBox_OutputExcelFile.Text
			img_path = img_path.replace("\\"+img_path.split("\\")[-1],"")
			oModule.ExportImageToFile(Report_Name, img_path + "\\" + Report_Name + ".gif", imgw * 2, imgh * 2)
			sub_DB.Excel_Img_File.append(img_path + "\\" + Report_Name + ".gif")
			Log("			= Save Image File, %s" % img_path + "\\" + Report_Name + ".gif")

	except Exception as e:		
		Log("	<Eye Plot> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to plot eye","Warning")						
		EXIT()

def Create_Excel_Report():
	try:
		xlApp = Excel.ApplicationClass()
		xlApp.Caption = "DDR EYE"
		xlApp.Visible = True
		xlApp.DisplayAlerts = False	

		xlbook = xlApp.Workbooks.Add()
	
		# Create Eye Diagram Image Report Worksheet
		xlsheet = xlbook.Worksheets['Sheet1']
		xlsheet.Name = "EYE Diagrams"
		Log("		(Launch Excel) = Done")

		Save_File = sub_DB.Option_Form._TextBox_OutputExcelFile.Text

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
		xlbook.SaveAs(Save_File)
		#xlbook.Close()
		#xlApp.Quit()
		ReleaseObject(Col_Header)
		ReleaseObject(Row_Header)
		ReleaseObject(Data_Cell)
		ReleaseObject(Merge_Cell)
		ReleaseObject(xlsheet)
		ReleaseObject(xlbook)
		ReleaseObject(xlApp)

		Log("		(File Save) = Done, %s" % Save_File)

	except Exception as e:		
		Log("	<Create Excel Report> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to create excel report","Warning")						
		EXIT()

def Create_Excel_Report_Imported():
	try:
		xlApp = Excel.ApplicationClass()
		xlApp.Caption = "DDR EYE"
		xlApp.Visible = True
		xlApp.DisplayAlerts = False	

		xlbook = xlApp.Workbooks.Add()
	
		# Create Eye Diagram Image Report Worksheet
		xlsheet = xlbook.Worksheets['Sheet1']
		xlsheet.Name = "EYE Diagrams"
		Log("		(Launch Excel) = Done")
	
		Save_File = sub_DB.Option_Form._TextBox_OutputExcelFile.Text

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
		xlsheet_table.Cells[1,4] = "Jitter [ps]"
		xlsheet_table.Cells[1,5] = "Timin Margin [ps]"
		xlsheet_table.Cells[1,6] = "Vcent_DQ [mV]"
		Log("		(Create Column) = Done")

		# Create Column Range
		Col_Header = xlsheet_table.Range[xlsheet_table.Cells[1, 1], xlsheet_table.Cells[1, 6]]

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
				xlsheet_table.Cells[row_idx,4] = sub_DB.Eye_Measure_Results[net_name][1] # Jitter
				xlsheet_table.Cells[row_idx,5] = sub_DB.Eye_Measure_Results[net_name][2] # Margin
				xlsheet_table.Cells[row_idx,6] = round(sub_DB.Vref, 1) # Vref
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
		Merge_Cell = xlsheet_table.Range[xlsheet_table.Cells[2, 6], xlsheet_table.Cells[row_idx, 6]]
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
		Data_Cell = xlsheet_table.Range[xlsheet_table.Cells[2, 2], xlsheet_table.Cells[row_idx, 6]]
		Data_Cell.Borders.LineStyle = Excel.XlLineStyle.xlContinuous
		Data_Cell.Borders.Weight = Excel.XlBorderWeight.xlThin

		# Auto Fit
		xlsheet_table.Range[xlsheet_table.Cells[1, 1], xlsheet_table.Cells[2, 7]].Columns.AutoFit()
		Log("		(Column Width AutoFit) = Done")

		# Save and Release
		xlbook.SaveAs(Save_File)
		#xlbook.Close()
		#xlApp.Quit()
		ReleaseObject(Col_Header)
		ReleaseObject(Row_Header)
		ReleaseObject(Data_Cell)
		ReleaseObject(Merge_Cell)
		ReleaseObject(xlsheet)
		ReleaseObject(xlsheet_table)
		ReleaseObject(xlbook)
		ReleaseObject(xlApp)

		Log("		(File Save) = Done, %s" % Save_File)

	except Exception as e:		
		Log("	<Create Excel Report> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to create excel report","Warning")						
		EXIT()

def Interpolate_1st(x1,y1,x2,y2,y3):
	x = abs(y3-y1)*(x2-x1)/abs(y2-y1)+x1
	return int(round(x))

def Gen_waveform_file(Input_File, Plot_list, Group_flag):
	try:
		Log("		(Get Waveform)")
		Save_File = sub_DB.temp_dir + "\\temp.csv"

		shutil.copy(Input_File, Save_File)
		Log("			= Copy File Done")

		xlApp = Excel.ApplicationClass()
		xlApp.Visible = False
		xlApp.DisplayAlerts = False
		xlbook = xlApp.Workbooks.Open(Save_File)
		xlsheet = xlbook.Worksheets.Item[1]

		if Group_flag:
			for i in range(0, len(Plot_list)):
				# Replace not allowed symbol for trace name
				xlsheet.Cells[1, i+2].Value2 = xlsheet.Cells[1, i+2].Value2.replace("-","_")
		else:	
			col_idx = 2
			while(xlsheet.Cells[1, col_idx].Value2 != None):			
				keyword = xlsheet.Cells[1, col_idx].Value2.split("[")[0].strip().replace("-","_")
				if not keyword in Plot_list:
					xlsheet.Columns(col_idx).Delete()
				else:
					col_idx += 1
			# Replace not allowed symbol for trace name
			xlsheet.Cells[1, 2].Value2 = xlsheet.Cells[1, 2].Value2.replace("-","_")

		xlbook.SaveAs(Save_File)

		xlbook.Close()
		xlApp.Quit()

		ReleaseObject(xlsheet)
		ReleaseObject(xlbook)
		ReleaseObject(xlApp)

		Log("			= Save File Done")
		return Save_File

	except Exception as e:		
		Log("	<Eye Plot> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to plot eye","Warning")						
		EXIT()

def Check_spec():	
	try:
		Log("	<Check DDR Specification>")
		# for New Eye
		if sub_DB.Eyeflag:
			pass
		else:
			pass
	except Exception as e:		
		Log("	<Check DDR Specification> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to plot eye","Warning")						
		EXIT()

def Log(msg):

	sub_DB.Log += "\n" + time.strftime('%H:%M:%S') + "\t" + msg

def LogSave():	
	f = open(sub_DB.temp_dir + '\\ddr_' + time.strftime('%Y%m%d_%H%M%S') + '.log', 'w')
	f.write(sub_DB.Log)
	f.close()

def EXIT():
	LogSave()	
	#if "App" in sub_DB.AEDT.keys():
	#	sub_ScriptEnv.Release()
	sub_ScriptEnv.Release()
	os._exit(0)

def ReleaseObject(obj):	
	System.Runtime.InteropServices.Marshal.ReleaseComObject(obj)
	System.GC.Collect()

def Initial():
	sub_ScriptEnv.Release()
	sub_DB.Eye_Form._ComboBox_Design.Items.Clear()	
	sub_DB.Net_Form.Init_Flag = True