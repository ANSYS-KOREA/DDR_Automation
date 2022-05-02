import os
import clr
import sub_DB

clr.AddReference('Microsoft.Office.Interop.Excel')

from sub_functions import *
from GUI_subforms import *
from sub_Vref import *
from sub_Report_Excel import *
from Microsoft.Office.Interop import Excel

path = os.path.dirname(os.path.abspath(__file__))

###############
# for New Eye #
###############

# Default Eye Analyze
def New_Default(self):
	###############################
	#   Cal. Max. Progress Number #
	###############################
	Location = Cal_Max_Process(self, 0)

	#########################
	#   Vref Calculation    #
	#########################
	try:
		sub_DB.Cal_Form.Text = "Calculating Vcent_DQ"
		sub_DB.Cal_Form._Label_Vref.Text = "Calculating Vcent_DQ..."
		sub_DB.Cal_Form._ProgressBar_Vref.Value += 1	

		if sub_DB.InputFile_Flag == 1: # *.aedt input
			# Auto-default
			if sub_DB.Option_Form._ComboBox_Vref.SelectedIndex == 0:
				Vref = Cal_Vref_AEDT(self, Location)
			else:
				pass
						
		elif sub_DB.InputFile_Flag == 2: # *.csv input
			# Auto-default
			if sub_DB.Option_Form._ComboBox_Vref.SelectedIndex == 0:
				Vref = Cal_Vref_WaveForm()
			else:
				pass

		# Manual Vref : Calculation Vref
		if sub_DB.Option_Form._ComboBox_Vref.Text.lower() == "manual":
			self._TextBox_VcentDQ.Text = sub_DB.Option_Form._TextBox_Vref.Text
			sub_DB.Vref = float(sub_DB.Option_Form._TextBox_Vref.Text)

		# Auto Vref : Calculation Vref
		else:
			self._TextBox_VcentDQ.Text = str(Vref)

		Log("	<Vref Calculation> = Done")

	except Exception as e:						
		Log("	<Launch Vref Calculation> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to launch Vref Calcultation","Warning")						
		EXIT()

	#########################
	#   Eye Analyze         #
	#########################
	try:
		sub_DB.Cal_Form.Text = "Analyzing Eye Diagram"
		sub_DB.Cal_Form._Label_Vref.Text = "Analyzing Eye Diagram..."
		sub_DB.Cal_Form._ProgressBar_Vref.Value += 1	

		Eye_Measure_Results = Measure_Eye(self, Location)

		#	Close Progress Form and change mouse cursor from defualt to wait
		sub_DB.Cal_Form._Label_Vref.Text = "Wrapping up eye measurement results"
		sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
			
		self._Button_ViewNet.BackColor = System.Drawing.SystemColors.Control			
		self._Button_Analyze.Enabled = True
		self._Button_Analyze.BackColor = System.Drawing.SystemColors.Info

		# View Analyze Result
		if sub_DB.Eye_Analyze_Flag:
			sub_DB.Net_Form._DataGridView.Columns.Add(sub_DB.Net_Form._Col_Width)
			sub_DB.Net_Form._DataGridView.Columns.Add(sub_DB.Net_Form._Col_Margin)
			sub_DB.Eye_Analyze_Flag = False
		else:
			for row in sub_DB.Net_Form._DataGridView.Rows:
				row.Cells[5].Value = ""
				row.Cells[6].Value = ""
				
		sub_DB.Net_Form._DataGridView.Columns[5].DisplayIndex = 2
		sub_DB.Net_Form._DataGridView.Columns[6].DisplayIndex = 3
		sub_DB.Net_Form._DataGridView.Columns[4].DisplayIndex = 4

		for row in sub_DB.Net_Form._DataGridView.Rows:
			if row.Cells[0].Value:								
				row.Cells[5].Value = str(Eye_Measure_Results[row.Cells[1].Value][0])
				row.Cells[6].Value = str(Eye_Measure_Results[row.Cells[1].Value][2])
		sub_DB.Net_Form.Init_Flag = False

		sub_DB.Net_Form.Text = "Eye Analyze Results"
		Log("	<Eye Analyze> = Done")

	except Exception as e:						
		Log("	<Launch Eye Analyze> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to launch Eye Analyze","Warning")						
		EXIT()

	#########################
	#   Eye Plot            #
	#########################
	try:						
		sub_DB.Cal_Form.Text = "Plotting Eye..."	
		sub_DB.Cal_Form._Label_Vref.Text = "Plotting Eye in AEDT"
		sub_DB.Cal_Form._ProgressBar_Vref.Value += 1

		if sub_DB.Option_Form._CheckBox_PlotEye.Checked:
			Log("	<Eye Plot> = Start")
			# *.aedt input
			if sub_DB.InputFile_Flag == 1:
				sub_DB.Excel_Img_File = []

				# Find min./max. voltage value for Y-axis setup
				vol_max = []
				vol_min = []
				for key in sub_DB.Waveform:
					vol_max.append(max(sub_DB.Waveform[key]))
					vol_min.append(min(sub_DB.Waveform[key]))
				vmax = (max(vol_max)//100 + 1)*100
				if min(vol_min) < 0:
					vmin = (min(vol_min)//100)*100
				else:
					vmin = (min(vol_min)//100-1)*100
				Log("		(Y-axis Max.) = %s[mV]" % vmax)
				Log("		(Y-axis Min.) = %s[mV]" % vmin)

				# Get Group List
				Group = []
				for row in sub_DB.Net_Form._DataGridView.Rows:
					if row.Cells[0].Value:
						if not row.Cells[4].Value in Group:
							Group.append(row.Cells[4].Value)

				# Get Plot List
				Plot_list = {}
				for key in Group:
					Plot_list[key] = []
					for row in sub_DB.Net_Form._DataGridView.Rows:
						if row.Cells[0].Value:
							if key == row.Cells[4].Value:
								Plot_list[key].append(row.Cells[1].Value)

				# Plot
				key_list = Plot_list.keys()
				key_list.sort()
				Log("		(Report Name)")
				for key in key_list:						
					if key == "None":
						for net in Plot_list[key]:								
							for row in sub_DB.Net_Form._DataGridView.Rows:
								if net == row.Cells[1].Value:
									Report_Name = row.Cells[3].Value
									break
							sub_DB.Cal_Form._Label_Vref.Text = "Plotting Eye in AEDT - %s" % Report_Name
							sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
							Log("			= %s" % Report_Name)
							Plot_Eye(Report_Name, [net], vmin, vmax, Eye_Measure_Results, sub_DB.Option_Form._CheckBox_ExportExcelReport.Checked)
								
					else:
						sub_DB.Cal_Form._Label_Vref.Text = "Plotting Eye in AEDT - %s" % key
						sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
						Log("			= %s" % key)
						Plot_Eye(key, Plot_list[key], vmin, vmax, Eye_Measure_Results, sub_DB.Option_Form._CheckBox_ExportExcelReport.Checked)

				#sub_ScriptEnv.Release()
				#sub_ScriptEnv.Shutdown()
				#sub_DB.AEDT = {}
					
			# *.csv input
			elif sub_DB.InputFile_Flag == 2: # *.csv input
				sub_DB.Excel_Img_File = []

				AEDT_File = sub_DB.result_dir + "\\" + sub_DB.Input_File.split(".")[0] + ".aedt"
				MessageBox.Show("The eye diagram will plot in Ansys Electronics Desktop.\n\n"+
				AEDT_File ,"Information",MessageBoxButtons.OK, MessageBoxIcon.Information)

				# Find min./max. voltage value for Y-axis setup
				vol_max = []
				vol_min = []
				for key in sub_DB.Waveform:
					vol_max.append(max(sub_DB.Waveform[key]))
					vol_min.append(min(sub_DB.Waveform[key]))
				vmax = (max(vol_max)//100 + 1)*100
				if min(vol_min) < 0:
					vmin = (min(vol_min)//100)*100
				else:
					vmin = (min(vol_min)//100-1)*100				

				if sub_DB.Unit["Voltage"]=="V":
					vmin = vmin/1000
					vmax = vmax/1000
					Log("		(Y-axis Max.) = %s[V]" % vmax)
					Log("		(Y-axis Min.) = %s[V]" % vmin)
				elif sub_DB.Unit["Voltage"]=="mV":
					Log("		(Y-axis Max.) = %s[mV]" % vmax)
					Log("		(Y-axis Min.) = %s[mV]" % vmin)

				self.TopMost = True
				sub_DB.Cal_Form.TopMost = True
				sub_AEDT.Set_AEDT_PlotTemplate()
				Log("		(Plot Template) = Done")
				self.TopMost = False
				sub_DB.Cal_Form.TopMost = False

				# Get Group List
				Group = []
				for row in sub_DB.Net_Form._DataGridView.Rows:
					if row.Cells[0].Value:
						if not row.Cells[4].Value in Group:
							Group.append(row.Cells[4].Value)

				# Get Plot List
				Plot_list = {}
				for key in Group:
					Plot_list[key] = []
					for row in sub_DB.Net_Form._DataGridView.Rows:
						if row.Cells[0].Value:
							if key == row.Cells[4].Value:
								Plot_list[key].append(row.Cells[1].Value)

				# Plot
				key_list = Plot_list.keys()
				key_list.sort()
				Log("		(Report Name)")
				for key in key_list:
					if key == "None":
						AEDT_File = AEDT_File.split(".")[0] + "_NonGroup." + AEDT_File.split(".")[-1]										
						for net in Plot_list[key]:								
							for row in sub_DB.Net_Form._DataGridView.Rows:
								if net == row.Cells[1].Value:
									Report_Name = row.Cells[3].Value
									break
							sub_DB.Cal_Form._Label_Vref.Text = "Plotting Eye in AEDT - %s" % Report_Name
							sub_DB.Cal_Form._ProgressBar_Vref.Value += 1											
							Import_file = Gen_waveform_file(self._TextBox_InputFile.Text, net, False)
							Log("			= %s" % Report_Name)
							Plot_Eye_Import(Report_Name, Import_file, [net], vmin, vmax, Eye_Measure_Results, sub_DB.Option_Form._CheckBox_ExportExcelReport.Checked)
							os.remove(Import_file)
								
					else:
						AEDT_File = AEDT_File.split(".")[0] + "_Group." + AEDT_File.split(".")[-1]										
						sub_DB.Cal_Form._Label_Vref.Text = "Plotting Eye in AEDT - %s" % key
						sub_DB.Cal_Form._ProgressBar_Vref.Value += 1										
						Import_file = Gen_waveform_file(self._TextBox_InputFile.Text, Plot_list[key], True)
						Log("			= %s" % key)
						Plot_Eye_Import(key, Import_file, Plot_list[key], vmin, vmax, Eye_Measure_Results, sub_DB.Option_Form._CheckBox_ExportExcelReport.Checked)
						os.remove(Import_file)

				if os.path.isfile(AEDT_File):									
					prj_name = AEDT_File.split("\\")[-1].split(".")[0]
					if prj_name in sub_DB.AEDT["Desktop"].GetProjectList():
						sub_DB.AEDT["Desktop"].CloseProject(prj_name)
					os.remove(AEDT_File)
					if os.path.isfile(AEDT_File + ".lock"):
						os.remove(AEDT_File + ".lock")
					sub_DB.AEDT["Project"].SaveAs(AEDT_File, True)
					sub_ScriptEnv.Release()									
					sub_DB.AEDT = {}
				else:
					sub_DB.AEDT["Project"].SaveAs(AEDT_File, True)
					sub_ScriptEnv.Release()
					sub_DB.AEDT = {}

				#sub_ScriptEnv.Release()
				#sub_ScriptEnv.Shutdown()								
			Log("	<Eye Plot> = Done")

		else:
			Log("	<Eye Plot> = False")

	except Exception as e:						
		Log("	<Launch Eye Plot> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to launch Eye Plot","Warning")						
		EXIT()

	#########################
	#  Create Excel Report  #
	#########################
	try:						
		sub_DB.Cal_Form.Text = "Creating Report..."	
		sub_DB.Cal_Form._Label_Vref.Text = "Creating Excel Report - %s" % sub_DB.Option_Form._TextBox_OutputExcelFile.Text.split("\\")[-1]
		sub_DB.Cal_Form._ProgressBar_Vref.Value += 1				

		if sub_DB.Option_Form._CheckBox_ExportExcelReport.Checked:
			Log("	<Create Excel Report> = Start")
			Log("		(Report Format) = %s" % sub_DB.Option_Form._ComboBox_ReportFormat.Text)
			# AEDT Input
			if sub_DB.InputFile_Flag == 1:
				# Default
				if sub_DB.Option_Form._ComboBox_ReportFormat.SelectedIndex == 0:
					Create_Excel_Report()
				elif sub_DB.Option_Form._ComboBox_ReportFormat.SelectedIndex == 1:
					Create_Setup_Hold_Excel_Report()

			# CSV Input
			elif sub_DB.InputFile_Flag == 2:
				# Default
				if sub_DB.Option_Form._ComboBox_ReportFormat.SelectedIndex == 0:
					Create_Excel_Report_Imported()
				#elif sub_DB.Option_Form._ComboBox_ReportFormat.SelectedIndex == 1:
				#	Create_Setup_Hold_Excel_Report_Imported()

			Log("	<Create Excel Report> = Done")

		else:
			Log("	<Create Excel Report> = False")

	except Exception as e:						
		Log("	<Launch Create Excel Report> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to launch create excel report","Warning")
		EXIT()
					
	#########################
	#  Save Log File        #
	#########################
	try:
		Log("[Eye Analyze End] = %s" % time.strftime('%Y.%m.%d, %H:%M:%S'))
		Log("[Save Log] = Done")
		LogSave()

	except Exception as e:						
		Log("[Save Log] = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to save log file","Warning")
		EXIT()

# Setup/Hold Eye Analyze
def New_SetupHold(self):
	###############################
	#   Cal. Max. Progress Number #
	###############################
	Location = Cal_Max_Process(self, 5)

	#########################
	#   Vref Calculation    #
	#########################
	try:
		sub_DB.Cal_Form.Text = "Calculating Vcent_DQ"
		sub_DB.Cal_Form._Label_Vref.Text = "Calculating Vcent_DQ..."
		sub_DB.Cal_Form._ProgressBar_Vref.Value += 1	

		if sub_DB.InputFile_Flag == 1: # *.aedt input
			# Auto-default
			if sub_DB.Option_Form._ComboBox_Vref.SelectedIndex == 0:
				Vref = Cal_Vref_AEDT(self, Location)
			else:
				pass
						
		elif sub_DB.InputFile_Flag == 2: # *.csv input
			# Auto-default
			if sub_DB.Option_Form._ComboBox_Vref.SelectedIndex == 0:
				Vref = Cal_Vref_WaveForm()
			else:
				pass

		# Manual Vref : Calculation Vref
		if sub_DB.Option_Form._ComboBox_Vref.Text.lower() == "manual":
			self._TextBox_VcentDQ.Text = sub_DB.Option_Form._TextBox_Vref.Text
			sub_DB.Vref = float(sub_DB.Option_Form._TextBox_Vref.Text)

		# Auto Vref : Calculation Vref
		else:
			self._TextBox_VcentDQ.Text = str(Vref)

		Log("	<Vref Calculation> = Done")

	except Exception as e:						
		Log("	<Launch Vref Calculation> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to launch Vref Calcultation","Warning")						
		EXIT()

	#########################
	#   Get Strobe Waveform #
	#########################
	try:
		sub_DB.Cal_Form.Text = "Getting Strobe Waveform"
		sub_DB.Cal_Form._Label_Vref.Text = "Getting Strobe Waveform..."
		sub_DB.Cal_Form._ProgressBar_Vref.Value += 1	

		if sub_DB.InputFile_Flag == 1: # *.aedt input
			Log("	<Get Strobe Waveform> = Start")
			Get_Strobe(self)
						
		elif sub_DB.InputFile_Flag == 2: # *.csv input
			#TODO : Setup/Hold for CSV input 
			pass

		Log("	<Get Strobe Waveform> = Done")

	except Exception as e:						
		Log("	<Get Strobe Waveform> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to get strobe waveform","Warning")						
		EXIT()

	#########################
	#   Eye Analyze         #
	#########################
	try:
		sub_DB.Cal_Form.Text = "Analyzing Eye Diagram"
		sub_DB.Cal_Form._Label_Vref.Text = "Analyzing Eye Diagram..."
		sub_DB.Cal_Form._ProgressBar_Vref.Value += 1	

		Eye_Measure_Results = Measure_Eye(self, Location)

		#	Close Progress Form and change mouse cursor from defualt to wait
		sub_DB.Cal_Form._Label_Vref.Text = "Wrapping up eye measurement results"
		sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
			
		self._Button_ViewNet.BackColor = System.Drawing.SystemColors.Control			
		self._Button_Analyze.Enabled = True
		self._Button_Analyze.BackColor = System.Drawing.SystemColors.Info

		sub_DB.Net_Form.Text = "Eye Analyze Results"
		Log("	<Eye Analyze> = Done")

	except Exception as e:						
		Log("	<Launch Eye Analyze> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to launch Eye Analyze","Warning")						
		EXIT()

	#########################
	#   Setup/Hold          #
	#########################
	try:
		Result = {}
		sub_DB.Cal_Form.Text = "Measuring Setup/Hold Margin"
		sub_DB.Cal_Form._Label_Vref.Text = "Measuring Setup/Hold Margin..."
		sub_DB.Cal_Form._ProgressBar_Vref.Value += 1

		Log("	<Measure setup/hold> = Start")
		Result["Data Setup Time"], Result["Data Hold Time"] = Setup_Hold(self)
		Log("	<Measure setup/hold> = Done")		

	except Exception as e:						
		Log("	<Measure setup/hold> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to measure setup/hold margin","Warning")						
		EXIT()

	#########################
	#   Show the Results    #
	#########################	
	try:
		sub_DB.Cal_Form.Text = "Measuring Setup/Hold Margin"
		sub_DB.Cal_Form._Label_Vref.Text = "Measuring Setup/Hold Margin..."
		sub_DB.Cal_Form._ProgressBar_Vref.Value += 1

		Log("	<Show analyze result> = Start")
		
		# Find the worst setup/hold value for each net
		Setup = {}
		for key in Result["Data Setup Time"]:
			temp = []
			for val in Result["Data Setup Time"][key]:
				temp.append(val[3])
			Setup[key] = min(temp)
		sub_DB.Setup = Setup

		Hold = {}
		for key in Result["Data Hold Time"]:
			temp = []		
			for val in Result["Data Hold Time"][key]:			
				temp.append(val[3])
			Hold[key] = min(temp)
		sub_DB.Hold = Hold
		
		# show the measured values in netform
		print sub_DB.Eye_Analyze_Flag
		if sub_DB.Eye_Analyze_Flag:
			sub_DB.Net_Form._DataGridView.Columns.Add(sub_DB.Net_Form._Col_Width)
			sub_DB.Net_Form._DataGridView.Columns.Add(sub_DB.Net_Form._Col_Margin)
			sub_DB.Net_Form._DataGridView.Columns.Add(sub_DB.Net_Form._Col_Setup)
			sub_DB.Net_Form._DataGridView.Columns.Add(sub_DB.Net_Form._Col_Hold)
			sub_DB.Eye_Analyze_Flag = False
		else:
			for row in sub_DB.Net_Form._DataGridView.Rows:
				row.Cells[5].Value = ""
				row.Cells[6].Value = ""
				row.Cells[7].Value = ""
				row.Cells[8].Value = ""
		
		sub_DB.Net_Form._DataGridView.Columns[5].DisplayIndex = 2
		sub_DB.Net_Form._DataGridView.Columns[6].DisplayIndex = 3
		sub_DB.Net_Form._DataGridView.Columns[7].DisplayIndex = 4
		sub_DB.Net_Form._DataGridView.Columns[8].DisplayIndex = 5
		sub_DB.Net_Form._DataGridView.Columns[4].DisplayIndex = 6

		for row in sub_DB.Net_Form._DataGridView.Rows:
			if row.Cells[0].Value:								
				row.Cells[5].Value = str(Eye_Measure_Results[row.Cells[1].Value][0])
				row.Cells[6].Value = str(Eye_Measure_Results[row.Cells[1].Value][2])
				row.Cells[7].Value = str(Setup[row.Cells[1].Value])
				row.Cells[8].Value = str(Hold[row.Cells[1].Value])

		sub_DB.Net_Form.Init_Flag = False
		Log("	<Show analyze result> = Start")

	except Exception as e:						
		Log("	<Show analyze result> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to show analyze results","Warning")						
		EXIT()

	#########################
	#   Eye Plot            #
	#########################
	try:						
		sub_DB.Cal_Form.Text = "Plotting Eye..."	
		sub_DB.Cal_Form._Label_Vref.Text = "Plotting Eye in AEDT"
		sub_DB.Cal_Form._ProgressBar_Vref.Value += 1

		if sub_DB.Option_Form._CheckBox_PlotEye.Checked:
			Log("	<Eye Plot> = Start")
			# *.aedt input
			if sub_DB.InputFile_Flag == 1:
				sub_DB.Excel_Img_File = []

				# Find min./max. voltage value for Y-axis setup
				vol_max = []
				vol_min = []
				for key in sub_DB.Waveform:
					vol_max.append(max(sub_DB.Waveform[key]))
					vol_min.append(min(sub_DB.Waveform[key]))
				vmax = (max(vol_max)//100 + 1)*100
				if min(vol_min) < 0:
					vmin = (min(vol_min)//100)*100
				else:
					vmin = (min(vol_min)//100-1)*100
				Log("		(Y-axis Max.) = %s[mV]" % vmax)
				Log("		(Y-axis Min.) = %s[mV]" % vmin)

				# Get Group List
				Group = []
				for row in sub_DB.Net_Form._DataGridView.Rows:
					if row.Cells[0].Value:
						if not row.Cells[4].Value in Group:
							Group.append(row.Cells[4].Value)

				# Get Plot List
				Plot_list = {}
				for key in Group:
					Plot_list[key] = []
					for row in sub_DB.Net_Form._DataGridView.Rows:
						if row.Cells[0].Value:
							if key == row.Cells[4].Value:
								Plot_list[key].append(row.Cells[1].Value)

				# Plot
				key_list = Plot_list.keys()
				key_list.sort()
				Log("		(Report Name)")
				for key in key_list:						
					if key == "None":
						for net in Plot_list[key]:								
							for row in sub_DB.Net_Form._DataGridView.Rows:
								if net == row.Cells[1].Value:
									Report_Name = row.Cells[3].Value
									break
							sub_DB.Cal_Form._Label_Vref.Text = "Plotting Eye in AEDT - %s" % Report_Name
							sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
							Log("			= %s" % Report_Name)
							Plot_Eye(Report_Name, [net], vmin, vmax, Eye_Measure_Results, sub_DB.Option_Form._CheckBox_ExportExcelReport.Checked)
								
					else:
						sub_DB.Cal_Form._Label_Vref.Text = "Plotting Eye in AEDT - %s" % key
						sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
						Log("			= %s" % key)
						Plot_Eye(key, Plot_list[key], vmin, vmax, Eye_Measure_Results, sub_DB.Option_Form._CheckBox_ExportExcelReport.Checked)

				#sub_ScriptEnv.Release()
				#sub_ScriptEnv.Shutdown()
				#sub_DB.AEDT = {}
					
			# *.csv input
			elif sub_DB.InputFile_Flag == 2: # *.csv input
				sub_DB.Excel_Img_File = []

				AEDT_File = sub_DB.result_dir + "\\" + sub_DB.Input_File.split(".")[0] + ".aedt"
				MessageBox.Show("The eye diagram will plot in Ansys Electronics Desktop.\n\n"+
				AEDT_File ,"Information",MessageBoxButtons.OK, MessageBoxIcon.Information)

				# Find min./max. voltage value for Y-axis setup
				vol_max = []
				vol_min = []
				for key in sub_DB.Waveform:
					vol_max.append(max(sub_DB.Waveform[key]))
					vol_min.append(min(sub_DB.Waveform[key]))
				vmax = (max(vol_max)//100 + 1)*100
				if min(vol_min) < 0:
					vmin = (min(vol_min)//100)*100
				else:
					vmin = (min(vol_min)//100-1)*100
				Log("		(Y-axis Max.) = %s[mV]" % vmax)
				Log("		(Y-axis Min.) = %s[mV]" % vmin)

				self.TopMost = True
				sub_DB.Cal_Form.TopMost = True
				sub_AEDT.Set_AEDT_PlotTemplate()
				Log("		(Plot Template) = Done")
				self.TopMost = False
				sub_DB.Cal_Form.TopMost = False

				# Get Group List
				Group = []
				for row in sub_DB.Net_Form._DataGridView.Rows:
					if row.Cells[0].Value:
						if not row.Cells[4].Value in Group:
							Group.append(row.Cells[4].Value)

				# Get Plot List
				Plot_list = {}
				for key in Group:
					Plot_list[key] = []
					for row in sub_DB.Net_Form._DataGridView.Rows:
						if row.Cells[0].Value:
							if key == row.Cells[4].Value:
								Plot_list[key].append(row.Cells[1].Value)

				# Plot
				key_list = Plot_list.keys()
				key_list.sort()
				Log("		(Report Name)")
				for key in key_list:
					if key == "None":
						AEDT_File = AEDT_File.split(".")[0] + "_NonGroup." + AEDT_File.split(".")[-1]										
						for net in Plot_list[key]:								
							for row in sub_DB.Net_Form._DataGridView.Rows:
								if net == row.Cells[1].Value:
									Report_Name = row.Cells[3].Value
									break
							sub_DB.Cal_Form._Label_Vref.Text = "Plotting Eye in AEDT - %s" % Report_Name
							sub_DB.Cal_Form._ProgressBar_Vref.Value += 1											
							Import_file = Gen_waveform_file(self._TextBox_InputFile.Text, net, False)
							Log("			= %s" % Report_Name)
							Plot_Eye_Import(Report_Name, Import_file, [net], vmin, vmax, Eye_Measure_Results, sub_DB.Option_Form._CheckBox_ExportExcelReport.Checked)
							os.remove(Import_file)
								
					else:
						AEDT_File = AEDT_File.split(".")[0] + "_Group." + AEDT_File.split(".")[-1]										
						sub_DB.Cal_Form._Label_Vref.Text = "Plotting Eye in AEDT - %s" % key
						sub_DB.Cal_Form._ProgressBar_Vref.Value += 1										
						Import_file = Gen_waveform_file(self._TextBox_InputFile.Text, Plot_list[key], True)
						Log("			= %s" % key)
						Plot_Eye_Import(key, Import_file, Plot_list[key], vmin, vmax, Eye_Measure_Results, sub_DB.Option_Form._CheckBox_ExportExcelReport.Checked)
						os.remove(Import_file)

				if os.path.isfile(AEDT_File):									
					prj_name = AEDT_File.split("\\")[-1].split(".")[0]
					if prj_name in sub_DB.AEDT["Desktop"].GetProjectList():
						sub_DB.AEDT["Desktop"].CloseProject(prj_name)
					os.remove(AEDT_File)
					if os.path.isfile(AEDT_File + ".lock"):
						os.remove(AEDT_File + ".lock")
					sub_DB.AEDT["Project"].SaveAs(AEDT_File, True)
					sub_ScriptEnv.Release()									
					sub_DB.AEDT = {}
				else:
					sub_DB.AEDT["Project"].SaveAs(AEDT_File, True)
					sub_ScriptEnv.Release()
					sub_DB.AEDT = {}

				#sub_ScriptEnv.Release()
				#sub_ScriptEnv.Shutdown()								
			Log("	<Eye Plot> = Done")

		else:
			Log("	<Eye Plot> = False")

	except Exception as e:						
		Log("	<Launch Eye Plot> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to launch Eye Plot","Warning")						
		EXIT()

	#########################
	#  Create Excel Report  #
	#########################
	try:						
		sub_DB.Cal_Form.Text = "Creating Report..."	
		sub_DB.Cal_Form._Label_Vref.Text = "Creating Excel Report - %s" % sub_DB.Option_Form._TextBox_OutputExcelFile.Text.split("\\")[-1]
		sub_DB.Cal_Form._ProgressBar_Vref.Value += 1				

		if sub_DB.Option_Form._CheckBox_ExportExcelReport.Checked:
			Log("	<Create Excel Report> = Start")
			Log("		(Report Format) = %s" % sub_DB.Option_Form._ComboBox_ReportFormat.Text)
			# AEDT Input
			if sub_DB.InputFile_Flag == 1:
				# Default
				if sub_DB.Option_Form._ComboBox_ReportFormat.SelectedIndex == 0:
					Create_Excel_Report()
				elif sub_DB.Option_Form._ComboBox_ReportFormat.SelectedIndex == 1:
					Create_Setup_Hold_Excel_Report()

			# CSV Input
			elif sub_DB.InputFile_Flag == 2:
				# Default
				if sub_DB.Option_Form._ComboBox_ReportFormat.SelectedIndex == 0:
					Create_Excel_Report_Imported()
				#elif sub_DB.Option_Form._ComboBox_ReportFormat.SelectedIndex == 1:
				#	Create_Setup_Hold_Excel_Report_Imported()

			Log("	<Create Excel Report> = Done")

		else:
			Log("	<Create Excel Report> = False")

	except Exception as e:						
		Log("	<Launch Create Excel Report> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to launch create excel report","Warning")
		EXIT()
					
	#########################
	#  Save Log File        #
	#########################
	try:
		Log("[Eye Analyze End] = %s" % time.strftime('%Y.%m.%d, %H:%M:%S'))
		Log("[Save Log] = Done")
		LogSave()

	except Exception as e:						
		Log("[Save Log] = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to save log file","Warning")
		EXIT()


###############
# for Old Eye #
###############

# Default Eye Analyze
def Old_Default(self):
	###############################
	#   Cal. Max. Progress Number #
	###############################
	Location = Cal_Max_Process(self, 0)

	#########################
	#   Vref Calculation    #
	#########################
	try:						
		sub_DB.Cal_Form.Text = "Check Vref"
		sub_DB.Cal_Form._Label_Vref.Text = "Checking Vref"
		sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
		Vref = float(self._TextBox_Vref.Text)
		Log("	<Get Vref> = Done")

	except Exception as e:						
		Log("	<Get Vref> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to get Vref value","Warning")						
		EXIT()

	#########################
	#   Eye Analyze         #
	#########################
	try:
		sub_DB.Cal_Form.Text = "Analyzing Eye Diagram"
		sub_DB.Cal_Form._Label_Vref.Text = "Analyzing Eye Diagram..."
		sub_DB.Cal_Form._ProgressBar_Vref.Value += 1	

		#TODO : Eye analyze for old eye
		#Eye_Measure_Results = Measure_Eye(self, Location)

		#	Close Progress Form and change mouse cursor from defualt to wait
		sub_DB.Cal_Form._Label_Vref.Text = "Wrapping up eye measurement results"
		sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
			
		self._Button_ViewNet.BackColor = System.Drawing.SystemColors.Control			
		self._Button_Analyze.Enabled = True
		self._Button_Analyze.BackColor = System.Drawing.SystemColors.Info

		# View Analyze Result
		if sub_DB.Eye_Analyze_Flag:
			sub_DB.Net_Form._DataGridView.Columns.Add(sub_DB.Net_Form._Col_Width)
			sub_DB.Net_Form._DataGridView.Columns.Add(sub_DB.Net_Form._Col_Margin)
			sub_DB.Eye_Analyze_Flag = False
		else:
			for row in sub_DB.Net_Form._DataGridView.Rows:
				row.Cells[5].Value = ""
				row.Cells[6].Value = ""
				
		sub_DB.Net_Form._DataGridView.Columns[5].DisplayIndex = 2
		sub_DB.Net_Form._DataGridView.Columns[6].DisplayIndex = 3
		sub_DB.Net_Form._DataGridView.Columns[4].DisplayIndex = 4

		#TODO : Show eye analyze results
		#for row in sub_DB.Net_Form._DataGridView.Rows:
		#	if row.Cells[0].Value:								
		#		row.Cells[5].Value = str(Eye_Measure_Results[row.Cells[1].Value][0])
		#		row.Cells[6].Value = str(Eye_Measure_Results[row.Cells[1].Value][2])
		sub_DB.Net_Form.Init_Flag = False

		sub_DB.Net_Form.Text = "Eye Analyze Results"
		Log("	<Eye Analyze> = Done")

	except Exception as e:						
		Log("	<Launch Eye Analyze> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to launch Eye Analyze","Warning")						
		EXIT()

	#########################
	#   Eye Plot            #
	#########################
	try:						
		sub_DB.Cal_Form.Text = "Plotting Eye..."	
		sub_DB.Cal_Form._Label_Vref.Text = "Plotting Eye in AEDT"
		sub_DB.Cal_Form._ProgressBar_Vref.Value += 1

		if sub_DB.Option_Form._CheckBox_PlotEye.Checked:
			Log("	<Eye Plot> = Start")
			# *.aedt input
			if sub_DB.InputFile_Flag == 1:
				#TODO : AEDT Eye Plot
				sub_DB.Excel_Img_File = []

				# Find min./max. voltage value for Y-axis setup
				#TODO : AEDT Eye Plot - Find min./max. voltage value for Y-axis setup
				#vol_max = []
				#vol_min = []
				#for key in sub_DB.Waveform:
				#	vol_max.append(max(sub_DB.Waveform[key]))
				#	vol_min.append(min(sub_DB.Waveform[key]))
				#vmax = (max(vol_max)//100 + 1)*100
				#if min(vol_min) < 0:
				#	vmin = (min(vol_min)//100)*100
				#else:
				#	vmin = (min(vol_min)//100-1)*100
				#Log("		(Y-axis Max.) = %s[mV]" % vmax)
				#Log("		(Y-axis Min.) = %s[mV]" % vmin)

				# Get Group List
				#TODO : AEDT Eye Plot - Get Group List
				#Group = []
				#for row in sub_DB.Net_Form._DataGridView.Rows:
				#	if row.Cells[0].Value:
				#		if not row.Cells[4].Value in Group:
				#			Group.append(row.Cells[4].Value)

				# Get Plot List
				#TODO : AEDT Eye Plot - Get Plot List
				#Plot_list = {}
				#for key in Group:
				#	Plot_list[key] = []
				#	for row in sub_DB.Net_Form._DataGridView.Rows:
				#		if row.Cells[0].Value:
				#			if key == row.Cells[4].Value:
				#				Plot_list[key].append(row.Cells[1].Value)

				# Plot
				#TODO : AEDT Eye Plot - Plot Eye Diagram
				#key_list = Plot_list.keys()
				#key_list.sort()
				#Log("		(Report Name)")
				#for key in key_list:						
				#	if key == "None":
				#		for net in Plot_list[key]:								
				#			for row in sub_DB.Net_Form._DataGridView.Rows:
				#				if net == row.Cells[1].Value:
				#					Report_Name = row.Cells[3].Value
				#					break
				#			sub_DB.Cal_Form._Label_Vref.Text = "Plotting Eye in AEDT - %s" % Report_Name
				#			sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
				#			Log("			= %s" % Report_Name)
				#			Plot_Eye(Report_Name, [net], vmin, vmax, Eye_Measure_Results, sub_DB.Option_Form._CheckBox_ExportExcelReport.Checked)
								
				#	else:
				#		sub_DB.Cal_Form._Label_Vref.Text = "Plotting Eye in AEDT - %s" % key
				#		sub_DB.Cal_Form._ProgressBar_Vref.Value += 1
				#		Log("			= %s" % key)
				#		Plot_Eye(key, Plot_list[key], vmin, vmax, Eye_Measure_Results, sub_DB.Option_Form._CheckBox_ExportExcelReport.Checked)

			# *.csv input
			elif sub_DB.InputFile_Flag == 2: # *.csv input
				#TODO : CSV Eye Plot
				sub_DB.Excel_Img_File = []

				# Generate AEDT project
				#TODO : CSV Eye Plot - Generate AEDT project
				#AEDT_File = sub_DB.result_dir + "\\" + sub_DB.Input_File.split(".")[0] + ".aedt"
				#MessageBox.Show("The eye diagram will plot in Ansys Electronics Desktop.\n\n"+
				#AEDT_File ,"Information",MessageBoxButtons.OK, MessageBoxIcon.Information)

				# Find min./max. voltage value for Y-axis setup
				#TODO : CSV Eye Plot - Find min./max. voltage value for Y-axis setup
				#vol_max = []
				#vol_min = []
				#for key in sub_DB.Waveform:
				#	vol_max.append(max(sub_DB.Waveform[key]))
				#	vol_min.append(min(sub_DB.Waveform[key]))
				#vmax = (max(vol_max)//100 + 1)*100
				#if min(vol_min) < 0:
				#	vmin = (min(vol_min)//100)*100
				#else:
				#	vmin = (min(vol_min)//100-1)*100
				#Log("		(Y-axis Max.) = %s[mV]" % vmax)
				#Log("		(Y-axis Min.) = %s[mV]" % vmin)
				#self.TopMost = True
				#sub_DB.Cal_Form.TopMost = True
				#sub_AEDT.Set_AEDT_PlotTemplate()
				#Log("		(Plot Template) = Done")
				#self.TopMost = False
				#sub_DB.Cal_Form.TopMost = False

				# Get Group List
				#TODO : CSV Eye Plot - Get Group List
				#Group = []
				#for row in sub_DB.Net_Form._DataGridView.Rows:
				#	if row.Cells[0].Value:
				#		if not row.Cells[4].Value in Group:
				#			Group.append(row.Cells[4].Value)

				# Get Plot List
				#TODO : CSV Eye Plot - Get Plot List
				#Plot_list = {}
				#for key in Group:
				#	Plot_list[key] = []
				#	for row in sub_DB.Net_Form._DataGridView.Rows:
				#		if row.Cells[0].Value:
				#			if key == row.Cells[4].Value:
				#				Plot_list[key].append(row.Cells[1].Value)

				# Plot
				#TODO : CSV Eye Plot - Plot Eye Diagram
				#key_list = Plot_list.keys()
				#key_list.sort()
				#Log("		(Report Name)")
				#for key in key_list:
				#	if key == "None":
				#		AEDT_File = AEDT_File.split(".")[0] + "_NonGroup." + AEDT_File.split(".")[-1]										
				#		for net in Plot_list[key]:								
				#			for row in sub_DB.Net_Form._DataGridView.Rows:
				#				if net == row.Cells[1].Value:
				#					Report_Name = row.Cells[3].Value
				#					break
				#			sub_DB.Cal_Form._Label_Vref.Text = "Plotting Eye in AEDT - %s" % Report_Name
				#			sub_DB.Cal_Form._ProgressBar_Vref.Value += 1											
				#			Import_file = Gen_waveform_file(self._TextBox_InputFile.Text, net, False)
				#			Log("			= %s" % Report_Name)
				#			Plot_Eye_Import(Report_Name, Import_file, [net], vmin, vmax, Eye_Measure_Results, sub_DB.Option_Form._CheckBox_ExportExcelReport.Checked)
				#			os.remove(Import_file)
								
				#	else:
				#		AEDT_File = AEDT_File.split(".")[0] + "_Group." + AEDT_File.split(".")[-1]										
				#		sub_DB.Cal_Form._Label_Vref.Text = "Plotting Eye in AEDT - %s" % key
				#		sub_DB.Cal_Form._ProgressBar_Vref.Value += 1										
				#		Import_file = Gen_waveform_file(self._TextBox_InputFile.Text, Plot_list[key], True)
				#		Log("			= %s" % key)
				#		Plot_Eye_Import(key, Import_file, Plot_list[key], vmin, vmax, Eye_Measure_Results, sub_DB.Option_Form._CheckBox_ExportExcelReport.Checked)
				#		os.remove(Import_file)

				# Delete AEDT Project File and *.lock File + Release AEDT for Initialization
				#TODO : CSV Eye Plot - Initialization
				#if os.path.isfile(AEDT_File):									
				#	sub_DB.AEDT["Desktop"].CloseProject(AEDT_File.split("\\")[-1].split(".")[0])
				#	os.remove(AEDT_File)
				#	if os.path.isfile(AEDT_File + ".lock"):
				#		os.remove(AEDT_File + ".lock")
				#	sub_DB.AEDT["Project"].SaveAs(AEDT_File, True)
				#	sub_ScriptEnv.Release()									
				#	sub_DB.AEDT = {}
				#else:
				#	sub_DB.AEDT["Project"].SaveAs(AEDT_File, True)
				#	sub_ScriptEnv.Release()
				#	sub_DB.AEDT = {}

			Log("	<Eye Plot> = Done")

		else:
			Log("	<Eye Plot> = False")

	except Exception as e:						
		Log("	<Launch Eye Plot> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to launch Eye Plot","Warning")						
		EXIT()

	#########################
	#  Create Excel Report  #
	#########################
	try:						
		sub_DB.Cal_Form.Text = "Creating Report..."	
		sub_DB.Cal_Form._Label_Vref.Text = "Creating Excel Report - %s" % sub_DB.Option_Form._TextBox_OutputExcelFile.Text.split("\\")[-1]
		sub_DB.Cal_Form._ProgressBar_Vref.Value += 1				

		if sub_DB.Option_Form._CheckBox_ExportExcelReport.Checked:
			#TODO : Create Excel Report
			Log("	<Create Excel Report> = Start")
			#if sub_DB.InputFile_Flag == 1:
			#	Create_Excel_Report()
			#elif sub_DB.InputFile_Flag == 2:
			#	Create_Excel_Report_Imported()
			Log("	<Create Excel Report> = Done")

		else:
			Log("	<Create Excel Report> = False")

	except Exception as e:						
		Log("	<Launch Create Excel Report> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to launch create excel report","Warning")
		EXIT()

	#########################
	#  Save Log File        #
	#########################
	try:
		Log("[Eye Analyze End] = %s" % time.strftime('%Y.%m.%d, %H:%M:%S'))
		Log("[Save Log] = Done")
		LogSave()

	except Exception as e:						
		Log("[Save Log] = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to save log file","Warning")
		EXIT()



#################
# sub functions #
#################

# Calculate Max. process number and position
def Cal_Max_Process(self, prog_offset):
	''' ''''''''''''''''''''''''''''''''''''
	# Calculate Maximum Process Value
	''''''''''''''''''''''''''''''''''''' '''
	try:
		iter = 0
		iter1 = 0
		Group = []
		for row in sub_DB.Net_Form._DataGridView.Rows:
			if row.Cells[0].Value:
				iter1 += 1
				if row.Cells[4].Value.lower() == "none":
					iter += 1
				else:
					if not row.Cells[4].Value in Group:
						Group.append(row.Cells[4].Value)
						iter += 1

		# *.aedt Input
		if sub_DB.InputFile_Flag == 1:
			max_val = 5 + 4 + iter1 + prog_offset
			if sub_DB.Option_Form._CheckBox_PlotEye.Checked:
				max_val = max_val + iter				

		# *.csv Input
		elif sub_DB.InputFile_Flag == 2:
			max_val = 5 + 3 + iter1
			if sub_DB.Option_Form._CheckBox_PlotEye.Checked:
				max_val = max_val + iter

		# for compliance test
		if sub_DB.Option_Form._CheckBox_Compiance.Checked:						
			max_val += sub_DB.Compliance_Form.Checked_Num + 3 # 3 = Export waveform, Get waveform, Load spec.

		Log("	<Calculate Max. Progress number> = Done, Max. Pogress Num. = %s" % max_val)

	except Exception as e:						
		Log("	<Calculate Max. Progress number> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to calculate maximum progress number","Warning")						
		EXIT()

	''' '''''''''''''''''''''''''''''''''''''
	# Show Option Form for Eye Analyzer		
	''''''''''''''''''''''''''''''''''''' '''	
	self._Options_ToolStripMenuItem.Enabled = True

	#	Get Location for Progress Form
	x_axis = self.Location.X + self.Size.Width/2
	y_axis = self.Location.Y + self.Size.Height/2
	Location = [x_axis, y_axis]

	#	Show Progress Form and change mouse cursor from defualt to wait
	try:
		Log("	<Progress Form Launch> = Done, Max. Pogress Num. = %s" % max_val)
		import GUI_subforms
		sub_DB.Cal_Form = GUI_subforms.CalForm(Location)
		sub_DB.Cal_Form._ProgressBar_Vref.Maximum = max_val				
		sub_DB.Cal_Form.Show()				
		self.Cursor = Cursors.WaitCursor
		sub_DB.Cal_Form.Cursor = Cursors.WaitCursor

	except Exception as e:						
		Log("	<Progress Form Launch> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to launch Progress Form","Warning")						
		EXIT()

	return Location

# Get strobe waveform for setup/hold - New Eye
def Get_Strobe(self):
	# Initialize
	Log("		(AEDT Launch) = Done")
	oProject = sub_DB.AEDT["Project"]
	oDesign = sub_DB.AEDT["Design"]
	oModule = oDesign.GetModule("ReportSetup")
	Report_Name = []
	Report_Name = self._CheckedListBox_ReportName.CheckedItems
	for report in Report_Name:	
		oModule.UpdateReports([report])

	oModule.CopyReportsData(["Voltage Waveforms at Receivers"])
	oModule.PasteReports()
	oModule.DeleteTraces(
		[
			"Voltage Waveforms at Receivers_1:=", ["V(M_DQ_6__D2_G83568-001_U1B5)","V(M_DQ_3__C8_G83568-001_U1B5)","V(M_DQ_7__E7_G83568-001_U1B5)","V(M_DQ_0__B3_G83568-001_U1B5)","V(M_DQ_4__E3_G83568-001_U1B5)","V(M_DQ_1__C7_G83568-001_U1B5)","V(M_DQ_5__E8_G83568-001_U1B5)","V(M_DQ_2__C2_G83568-001_U1B5)"]
		])
	oModule.ChangeProperty(
	[
		"NAME:AllTabs",
		[
			"NAME:Report",
			[
				"NAME:PropServers", 
				"Voltage Waveforms at Receivers_1"
			],
			[
				"NAME:ChangedProps",
				[
					"NAME:Name",
					"Value:="		, "temp_eye"
				]
			]
		]
	])
	#TODO : Fix this Code using real example AEDT input w/ strobe
	#########################################################################################################################################################################################################################################################################################	
	## Get Plot List
	#PlotList = []
	#for row in sub_DB.Net_Form._DataGridView.Rows:
	#	if "DQS" in row.Cells[2].Value:
	#		PlotList.append(row.Cells[1].Value.replace("\"","").split("[")[0].strip())
	#Log("		(Get plot list) = Done")

	## Create Variable List	
	#Var_list = []
	#Var_list.append("Time:=")
	#Var_list.append(["All"])
	#Sim_type = oDesign.GetDesignType()			
	#if Sim_type == "Circuit Netlist":
	#	pass
	#else:
	#	Global_Varlist = oProject.GetVariables()
	#	Local_Varlist = oDesign.GetVariables()					
	#	for var in Global_Varlist:
	#		Var_list.append(var + ":=")
	#		Var_list.append(["All"])
	#Log("		(Get variable list) = Done")
	
	## Create temp eye diagram		
	#oModule.CreateReport("temp_eye", "Eye Diagram", "Rectangular Plot", self._ComboBox_SolutionName.Text, 
	#[
	#	"NAME:Context",
	#	"SimValueContext:="	, [1,0,2,0,False,False,-1,1,0,1,1,"",0,0,"DE",False,"0","DP",False,"500000000","DT",False,"0.001","NUMLEVELS",False,"0","WE",False,sub_DB.total_waveform_length,"WM",False,sub_DB.total_waveform_length,"WN",False,"0ps","WS",False,"0ps"]
	#], 
	#Var_list, 
	#[
	#	"Component:="		, PlotList
	#], 
	#[
	#	"Unit Interval:="	, str(1/(float(sub_DB.Eye_Form._ComboBox_DataRate.Text)*1000000))+"s",
	#	"Offset:="		, str(sub_DB.Option_Form._TextBox_EyeOffset.Text) + "ns",
	#	"Auto Delay:="		, True,
	#	"Manual Delay:="	, "0ps",
	#	"AutoCompCrossAmplitude:=", True,
	#	"CrossingAmplitude:="	, "0mV",
	#	"AutoCompEyeMeasurementPoint:=", True,
	#	"EyeMeasurementPoint:="	, (1/(float(self._ComboBox_DataRate.Text)*1000000))/2		
	#])
	#Log("		(Create temp eye-diagram) = Done")
	#########################################################################################################################################################################################################################################################################################
	

	# Export Uniform Report	
	File = sub_DB.result_dir + "\\Waveforms_Strobe.csv"		
	oModule.UpdateReports(["temp_eye"])
	oModule.ExportUniformPointsToFile("temp_eye", File, "0ns", sub_DB.total_waveform_length, "1ps", False)	
	Log("		(Export Uniform Strobe Wavefrom File) = Done")

	# Delete temp Report	
	oModule.DeleteReports(["temp_eye"])
	Log("		(Delete temp eye-diagram) = Done")

	# Get Strobe Waveform
	Waveform = {}
	with open(File) as fp:
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

	# Check voltage unit
	if sub_DB.Unit["Voltage"].lower() == "mv":
		pass
	elif sub_DB.Unit["Voltage"].lower() == "v":
		for key in Waveform:
			for i in range(0, len(Waveform[key])):
				Waveform[key][i] = Waveform[key][i]*1000
	else:
		MessageBox.Show("The voltage unit in the input csv file is not supported.","Warning",MessageBoxButtons.OK, MessageBoxIcon.Warning)
		
	sub_DB.Strobe_Waveform = Waveform

# Measure Setup/Hold Margin - New Eye
def Setup_Hold(self):
	#####################################
    # 1. Load Compliance Specifications #
    #####################################
	try:
		Log("		(Load Data setup & hold spec.) = Start")		
		File = path + r'\Resources\Compliance_Spec_DDR4.xlsx'
		# Open Excel spec. file and set Excel instances		
		try:
			xlApp = Excel.ApplicationClass()
			xlApp.Visible = False
			xlApp.DisplayAlerts = False
			xlbook = xlApp.Workbooks.Open(File)

			xlsheet = xlbook.Worksheets["tDS & tDH"]
			Log("            = Open spec. file : Done")

		except Exception as e:
			Log("            = Open spec. file : Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Eye setup/hold - Open spec. file failed","Warning")
			EXIT()

		# Load Setup + Hold spec.		
		sub_DB.Spec["Setup + Hold"]={}
		try:
			start_row = 3
			end_row = 9
			start_col = 9
			end_col = 9
			
			for row in range(start_row, end_row+1):
				Datarate_key = str(int(xlsheet.Cells[row, start_col-7].Value2))
				for col in range(start_col, end_col+1):
					if not xlsheet.Cells[row, col].Value2 == "-":						
						sub_DB.Spec["Setup + Hold"][Datarate_key] = xlsheet.Cells[row, col].Value2        
			Log("            = Load data setup base Value : Done")

		except Exception as e:
			Log("            = Load data setup base Value : Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Compliance test - Loading data setup base value failed","Warning")
			EXIT()


		xlbook.Close()
		xlApp.Quit()
		ReleaseObject(xlsheet)
		ReleaseObject(xlbook)
		ReleaseObject(xlApp)

		Log("            = Load Data setup & hold spec. : Done")
		
	except Exception as e:
		Log("            = Load Data setup & hold spec. : Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Compliance test - Loading data setup & hold spec. failed","Warning")
		EXIT()

	#########################
	# 2. Measure Setup/Hold #
	#########################	
	try:
		Log("	    (Measure Setup/Hold) = Start")
		Result = {}
		Result["Data Setup Time"] = {}
		Result["Data Hold Time"] = {}
		checking_item = "data setup & hold time"
		sub_DB.Cal_Form._Label_Vref.Text = "Checking %s" % checking_item
		sub_DB.Cal_Form._ProgressBar_Vref.Value += 2
		sub_DB.Cal_Form.Refresh()
		Log("            = Check %s : Start" % checking_item)

		#############
		# Set Spec. #
		#############
		V_high = float(self._TextBox_VcentDQ.Text) + 0.5*float(self._TextBox_VdIVW.Text)
		V_low = float(self._TextBox_VcentDQ.Text) - 0.5*float(self._TextBox_VdIVW.Text)
		Vref = float(self._TextBox_VcentDQ.Text)

		Spec = sub_DB.Spec["Setup + Hold"][self._ComboBox_DataRate.Text]

		###########################################
		# Set Target Net & Reference Net Wavefrom #
		###########################################
		Target_net = sub_DB.Waveform
		Ref_net = sub_DB.Strobe_Waveform
		for net in Ref_net.keys():
			Group_idx, Match = Net_Identify(net.strip(), sub_DB.Uenv) # Match = "Group prefix / Net Number prefix"				
			if Group_idx == 2: # DQS_P
				pos = sub_DB.Strobe_Waveform[net]
				Ref_key = Match
			elif Group_idx == 3: # DQS_N
				neg = sub_DB.Strobe_Waveform[net]
		Ref_net[Ref_key] = [i-j for i, j in zip(pos,neg)]

		######################################################
		# Find Zero Crossing Points and Slew Rate for Strobe #
		######################################################
		Zero_crossing = []
		for time_idx in range(int(float(sub_DB.Option_Form._TextBox_EyeOffset.Text)*1000), len(Ref_net[Ref_key]) - 1):
			if float(Ref_net[Ref_key][time_idx]) * float(Ref_net[Ref_key][time_idx+1]) < 0:
				# Get Zero crossing point
				Zero_crossing.append(time_idx)

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

					# Find zero crossing point
					while(1):
						if Zero_crossing[zero_idx] > time_idx:
							if zero_idx == 0:
								zero_idx = 1
							t0_s = Zero_crossing[zero_idx]								
							t0_h = Zero_crossing[zero_idx-1]								
							break
						zero_idx += 1
					temp_setup_result.append(t0_s) #[1] - Reference time
					temp_hold_result.append(t0_h) #[1] - Reference time

					# Find Hold Time                
					temp_idx = t0_h
					while(1):
						temp_idx += 1
						if float(net[temp_idx-1]) < V_low and float(net[temp_idx]) > V_low:
							t_h = temp_idx - t0_h
							temp_hold_result.append(temp_idx) #[2] - Sampled time
							temp_hold_result.append(t_h) #[3] - Measured hold time
							break

						if temp_idx == len(net) - 1:
							break

					# Find Setup Time                
					temp_idx = time_idx
					while(1):
						temp_idx += 1
						if float(net[temp_idx-1]) < V_high and float(net[temp_idx]) > V_high:
							t_s = t0_s - temp_idx
							temp_setup_result.append(temp_idx) #[2] - Sampled time
							temp_setup_result.append(t_s) #[3] - Measured setup time
							break

						if temp_idx == len(net) - 1:
							break
						

					Setup_Result[key].append(temp_setup_result)
					Hold_Result[key].append(temp_hold_result)

				# Detect Transition - Falling
				elif float(net[time_idx-1]) > Vref and float(net[time_idx]) < Vref:
					# Initialize Spec., default = False
					temp_setup_result = []
					temp_hold_result = []                
					temp_setup_result.append(False) #[0] - Spec. In/Out
					temp_hold_result.append(False) #[0] - Spec. In/Out

					# Find zero crossing point
					while(1):
						if Zero_crossing[zero_idx] > time_idx:
							if zero_idx == 0:
								zero_idx = 1
							t0_s = Zero_crossing[zero_idx]								
							t0_h = Zero_crossing[zero_idx-1]								
							break
						zero_idx += 1
					temp_setup_result.append(t0_s) #[1] - Reference time
					temp_hold_result.append(t0_h) #[1] - Reference time

					# Find Hold Time                
					temp_idx = t0_h						
					while(1):
						temp_idx += 1
						if float(net[temp_idx-1]) > V_high and float(net[temp_idx]) < V_high:
							t_h = temp_idx - t0_h
							temp_hold_result.append(temp_idx) #[2] - Sampled time
							temp_hold_result.append(t_h) #[3] - Measured hold time
							break

						if temp_idx == len(net) - 1:
							break

					# Find Setup Time                
					temp_idx = time_idx						
					while(1):
						temp_idx += 1
						if float(net[temp_idx-1]) > V_low and float(net[temp_idx]) < V_low:
							t_s = t0_s - temp_idx
							temp_setup_result.append(temp_idx) #[2] - Sampled time
							temp_setup_result.append(t_s) #[3] - Measured setup time
							break

						if temp_idx == len(net) - 1:
							break

					Setup_Result[key].append(temp_setup_result)
					Hold_Result[key].append(temp_hold_result)

				time_idx += 1

				# quit while
				if time_idx >= Zero_crossing[len(Zero_crossing)-1]:                
					break

		Log("            = Check %s : Done" % checking_item)
		Log("	    (Compliance Test) = Done")

		return Setup_Result, Hold_Result
			
	except Exception as e:
		Log("            = Check %s : Failed" % checking_item)
		Log(traceback.format_exc())
		print sub_DB.Log
		MessageBox.Show("(Measure Setup/Hold) - Check %s failed" % checking_item,"Warning")
		EXIT()	

# Eye Measure for Default Eye Analyze - New Eye
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

		sub_DB.Eye_Measure_Results = Eye_Measure_Results
		Log("		(Eye Measure) = Done")
		return Eye_Measure_Results

	except Exception as e:		
		Log("	<Eye Analyze> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to analyze eye","Warning")						
		EXIT()