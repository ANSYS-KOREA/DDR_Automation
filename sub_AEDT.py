import os
import sub_ScriptEnv
import sub_DB
import time
import traceback

from sub_functions import *

def Get_AEDT_Version():	
	for row in sub_DB.Var_Form._dataGridView.Rows:
		if row.Cells[0].Value:
			version = row.Cells[1].Value	
	return version

def Get_AEDT_Dir():
	for row in sub_DB.Var_Form._dataGridView.Rows:
		if row.Cells[0].Value:
			ansysEmInstallDirectory = row.Cells[3].Value	
	return ansysEmInstallDirectory

def Get_AEDT_Info(self, File):
	try:
		Delete_LockFile(File)
		Version = Get_AEDT_Version()		
		Log("[AEDT Version] : %s" % Version)
		try:
			oApp, oDesktop = sub_ScriptEnv.Initialize("Ansoft.ElectronicsDesktop." + Version)			

		except:
			MessageBox.Show("AEDT %s is not installed. Run as default version." % Version.replace('.', ' R'),"Warning")
			oApp, oDesktop = sub_ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")

		oDesktop.RestoreWindow()

		Project_list = oDesktop.GetProjectList()
		Input_Project_Name = File.split("\\")[-1].split(".")[0]
		if not Input_Project_Name in Project_list:		
			oDesktop.OpenProject(File)

		oProject = oDesktop.SetActiveProject(Input_Project_Name)
		
		sub_DB.AEDT["App"] = oApp
		sub_DB.AEDT["Desktop"] = oDesktop
		sub_DB.AEDT["Project"] = oProject

		# Add Designs into ComboBox
		design_name = []
		for design in oProject.GetDesigns():
			design_name.append(design.GetName().split(";")[-1])

		design_name.sort()
		for design in design_name:
			self._ComboBox_Design.Items.Add(design)
		#self.Init_Flag = True
		#self._ComboBox_Design.SelectedIndex = 0		
		#oDesign = oProject.SetActiveDesign(self._ComboBox_Design.Items[0])		
		if self._ComboBox_Design.Text == "":
			oDesign = oProject.SetActiveDesign(self._ComboBox_Design.Items[0])
		else:
			oDesign = oProject.SetActiveDesign(self._ComboBox_Design.Text)
		oModule = oDesign.GetModule("ReportSetup")
		sub_DB.AEDT["Design"] = oDesign
		sub_DB.AEDT["Module"] = oModule		

		# Set Active Design
		if "(Design)<Setup>[EYE]" in sub_DB.Uenv:		
			for item in self._ComboBox_Design.Items:						
				if item == sub_DB.Uenv["(Design)<Setup>[EYE]"][0]:
					self._ComboBox_Design.SelectedItem = item
					break
			oDesign = oProject.SetActiveDesign(self._ComboBox_Design.Text)
			
			# Add reports into ComboBox
			oModule = oDesign.GetModule("ReportSetup")
			report_name = []
			for report in oModule.GetAllReportNames():
				report_name.append(report)

			report_name.sort()
			for report in report_name:
				self._CheckedListBox_ReportName.Items.Add(report)

			# Set Active Report
			if "(Report)<Setup>[EYE]" in sub_DB.Uenv:
				for i in range(0, self._CheckedListBox_ReportName.Items.Count):
					if self._CheckedListBox_ReportName.Items[i] == sub_DB.Uenv["(Report)<Setup>[EYE]"][0]:
						self._CheckedListBox_ReportName.SetItemChecked(i, True)

	except Exception as e:		
		Log("[AEDT Launch] : Failed")
		Log(traceback.format_exc())
		print traceback.format_exc()
		MessageBox.Show("Fail to run AEDT","Warning")
		EXIT()

def Set_AEDT_Info(self, File):
	try:
		Delete_LockFile(File)
		Version = Get_AEDT_Version()
		Log("[AEDT Version] : %s" % Version)
		oApp, oDesktop = sub_ScriptEnv.Initialize("Ansoft.ElectronicsDesktop." + Version)
		oDesktop.RestoreWindow()

		Project_list = oDesktop.GetProjectList()
		Input_Project_Name = File.split("\\")[-1].split(".")[0]
		if not Input_Project_Name in Project_list:		
			oDesktop.OpenProject(File)

		oProject = oDesktop.SetActiveProject(Input_Project_Name)
		oDesign = oProject.SetActiveDesign(self._ComboBox_Design.Text)
		oModule = oDesign.GetModule("ReportSetup")

		sub_DB.AEDT["App"] = oApp
		sub_DB.AEDT["Desktop"] = oDesktop
		sub_DB.AEDT["Project"] = oProject
		sub_DB.AEDT["Design"] = oDesign

	except Exception as e:		
		Log("[AEDT Launch] : Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to run AEDT","Warning")		
		EXIT()

def Set_AEDT_PlotTemplate():	
	oApp, oDesktop = sub_ScriptEnv.Initialize("Ansoft.ElectronicsDesktop." + Get_AEDT_Version())
	oDesktop.RestoreWindow()
	oProject = oDesktop.NewProject()
	oProject.InsertDesign("Circuit Design", "Circuit", "None", "")
	oDesign = oProject.SetActiveDesign("Circuit")
	oEditor = oDesign.SetActiveEditor("SchematicEditor")
	oEditor.CreateComponent(
		[
			"NAME:ComponentProps",
			"Name:="		, "Nexxim Circuit Elements\\Independent Sources:V_DC",
			"Id:="			, "1"
		], 
		[
			"NAME:Attributes",
			"Page:="		, 1,
			"X:="			, -0.01778,
			"Y:="			, 0.04826,
			"Angle:="		, 0,
			"Flip:="		, False
		])
	oEditor.CreateComponent(
		[
			"NAME:ComponentProps",
			"Name:="		, "Nexxim Circuit Elements\\Resistors:RES_",
			"Id:="			, "2"
		], 
		[
			"NAME:Attributes",
			"Page:="		, 1,
			"X:="			, -0.0127,
			"Y:="			, 0.05334,
			"Angle:="		, 0,
			"Flip:="		, False
		])
	oEditor.CreateGround(
		[
			"NAME:GroundProps",
			"Id:="			, 8
		], 
		[
			"NAME:Attributes",
			"Page:="		, 1,
			"X:="			, -0.01778,
			"Y:="			, 0.04064,
			"Angle:="		, 0,
			"Flip:="		, False
		])
	oEditor.CreateGround(
		[
			"NAME:GroundProps",
			"Id:="			, 13
		], 
		[
			"NAME:Attributes",
			"Page:="		, 1,
			"X:="			, -0.00762,
			"Y:="			, 0.0508,
			"Angle:="		, 0,
			"Flip:="		, False
		])
	oModule = oDesign.GetModule("SimSetup")
	oModule.AddTransient(
		[
			"NAME:SimSetup",
			"DataBlockID:="		, 10,
			"OptionName:="		, "(Default Options)",
			"AdditionalOptions:="	, "",
			"AlterBlockName:="	, "",
			"FilterText:="		, "",
			"AnalysisEnabled:="	, 1,
			[
				"NAME:OutputQuantities"
			],
			[
				"NAME:NoiseOutputQuantities"
			],
			"Name:="		, "NexximTransient",
			"TransientData:="	, ["0.1ns","10ns"],
			"TransientNoiseData:="	, [False,"","",0,1,0,False,1],
			"TransientOtherData:="	, ["default"]
		])
	oModule = oDesign.GetModule("ReportSetup")

	sub_DB.AEDT["App"] = oApp
	sub_DB.AEDT["Desktop"] = oDesktop
	sub_DB.AEDT["Project"] = oProject
	sub_DB.AEDT["Design"] = oDesign
	sub_DB.AEDT["Editor"] = oEditor
	sub_DB.AEDT["Module"] = oModule

def Delete_LockFile(File):
	File = File + ".lock"
	if os.path.isfile(File):		
		os.remove(File)