from sub_functions import *

# AEDT Export Based Vref input
def Cal_Vref_AEDT_Eye_Measure(self, Location):
	try:
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
		File = sub_DB.result_dir + "\\temp.csv"
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
		legend_file = sub_DB.result_dir + "\\temp1.csv"		
		oModule.ExportTableToFile("temp_eye", legend_file, "Legend")
		Log("		(Export Eye Measure Data) = Done")		
	
		# Export Uniform Report	
		File = sub_DB.result_dir + "\\Waveforms.csv"		
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

		return Vref

	except Exception as e:		
		Log("	<AEDT Vref Calculation> = Failed")
		Log(traceback.format_exc())
		print traceback.format_exc()
		MessageBox.Show("Fail to AEDT Calculate Vref","Warning")		
		EXIT()

# Default Vref
def Cal_Vref_AEDT(self, Location):	
	##############
	# Initialize #
	##############
	try:		
		oProject = sub_DB.AEDT["Project"]
		oDesign = sub_DB.AEDT["Design"]
		oModule = oDesign.GetModule("ReportSetup")
		Log("		(AEDT Launch) = Done")

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
		Report_Name = []
		Report_Name = self._CheckedListBox_ReportName.CheckedItems
		for report in Report_Name:	
			oModule.UpdateReports([report])

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
		oModule.UpdateReports([Report_Name[0]])
		oModule.ExportToFile(Report_Name[0], File)		
	
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
		Log("	<Vref Calculation> = Failed to Get Time Unit")
		Log(traceback.format_exc())
		print traceback.format_exc()
		MessageBox.Show("Vref Calculation - Fail to get time unit","Warning")		
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
		
		oModule.CreateReport("temp", "Standard", "Rectangular Plot", self._ComboBox_SolutionName.Text, 
		[
			"NAME:Context",
			"SimValueContext:="	, [1,0,2,0,False,False,-1,1,0,1,1,"",0,0,"DE",False,"0","DP",False,"500000000","DT",False,"0.001","NUMLEVELS",False,"0","WE",False,sub_DB.total_waveform_length,"WM",False,sub_DB.total_waveform_length,"WN",False,"0ps","WS",False,"0ps"]
		], 
		Var_list, 
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

	

# Auto-default for CSV input
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
	
		return Vref	

	except Exception as e:		
		Log("	<CSV Vref Calculation> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to CSV Calculate Vref","Warning")		
		EXIT()

# Get Waveform for Manual Vref
def Get_Waveform(self):
	try:
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
		File = sub_DB.result_dir + "\\temp.csv"
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
	
		# Export Uniform Report	
		File = sub_DB.result_dir + "\\Waveforms.csv"		
		oModule.UpdateReports(["temp_eye"])
		oModule.ExportUniformPointsToFile("temp_eye", File, "0ns", t_total, "1ps", False)
		sub_DB.Waveform_File = File
		Log("		(Export Uniform Wavefrom File) = Done")

		# Delete temp Report	
		oModule.DeleteReports(["temp_eye"])
		Log("		(Delete temp eye-diagram) = Done")

	except Exception as e:		
		Log("	<AEDT Vref Calculation> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to Export Waveform","Warning")		
		EXIT()

# Vref Calculation Method - Default
def Cal_Vref(Waveform):	
	# Get Min./Max. Voltage value	
	max_val = []
	min_val = []
	for key in Waveform:
		max_val.append(max(Waveform[key]))
		min_val.append(min(Waveform[key]))

	# Calculate Initial Vref
	Vref_init = (max(max_val) + min(min_val))/2

	# Get Voltage Levels for 1 & 0
	Ones = []
	Zeros = []
	UI = int(round(1/(float(sub_DB.Eye_Form._ComboBox_DataRate.Text))*1000000))
	t_offset = int(UI*float(sub_DB.Eye_Form._TextBox_TdIVW.Text)/2)	
	
	for key in Waveform:
		iter = 0
		# True for Rising, False for Falling
		flag = True 
		for i in range(1, len(Waveform[key])):
			# Detect Transition
			if (Waveform[key][i-1] - Vref_init)*(Waveform[key][i]-Vref_init) < 0:
				# R/F
				if (Waveform[key][i-1] - Vref_init) < 0:
					flag = True # Rising
				else:
					flag = False # Falling

				if iter == 0:
					t_pre = i					
				else:
					t_post = i					

				if iter > 0:
					t_cent = int((t_post + t_pre)/2)
					t_start = t_cent - t_offset
					t_end = t_cent + t_offset
					for j in range(t_start, t_end):
						if flag: # Rising -> Zeros
							Zeros.append(Waveform[key][j])
						else: # Falling -> Ones
							Ones.append(Waveform[key][j])
					t_pre = t_post

				iter += 1

	# Calculate Vref
	Avg_one = sum(Ones)/len(Ones)
	Avg_zero = sum(Zeros)/len(Zeros)
	Vref = (Avg_one + Avg_zero) / 2

	return round(Vref,2)