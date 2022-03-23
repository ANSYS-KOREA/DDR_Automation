import os
import sub_ScriptEnv
import sub_DB
import time

from sub_functions import *



def Get_AEDT_Version():
	import os
	max = 0.0
	ANSYSEM_Env_Var = [s for s in os.environ.keys() if 'ANSYSEM' in s]
	if 'ANSYSEM_INSTALL_DIR' in ANSYSEM_Env_Var:
		ansysEmInstallDirectory = os.environ['ANSYSEM_INSTALL_DIR']        
		version = "20" + ansysEmInstallDirectory.split("\\")[-2].replace("AnsysEM","")

	else:
		for var in ANSYSEM_Env_Var:
			version = float(var.replace('ANSYSEM_ROOT','').replace('.',''))
			if version > max:
				max = version
				ansysEmInstallDirectory = os.environ[var]
		max = max/10
		version = "20" + str(max)

	return version

def Get_AEDT_Dir():    
    max = 0.0
    ANSYSEM_Env_Var = [s for s in os.environ.keys() if 'ANSYSEM' in s]
    if 'ANSYSEM_INSTALL_DIR' in ANSYSEM_Env_Var:
        ansysEmInstallDirectory = os.environ['ANSYSEM_INSTALL_DIR']
    else:
        for var in ANSYSEM_Env_Var:
            version = float(var.replace('ANSYSEM_ROOT','').replace('.',''))
            if version > max:
                max = version
                ansysEmInstallDirectory = os.environ[var]
                
    return ansysEmInstallDirectory

def Get_AEDT_Info(self, File):
	try:
		Version = Get_AEDT_Version()
		Log("[AEDT Version] : %s" % Version)
		oApp, oDesktop = sub_ScriptEnv.Initialize("Ansoft.ElectronicsDesktop." + Version)
		oDesktop.RestoreWindow()

		Project_list = oDesktop.GetProjectList()
		Input_Project_Name = File.split("\\")[-1].split(".")[0]
		if not Input_Project_Name in Project_list:		
			oDesktop.OpenProject(File)

		oProject = oDesktop.SetActiveProject(Input_Project_Name)
				
		# Add Designs into ComboBox
		design_name = []
		for design in oProject.GetDesigns():
			design_name.append(design.GetName().split(";")[-1])

		design_name.sort()
		for design in design_name:
			self._ComboBox_Design.Items.Add(design)

		#self._ComboBox_Design.SelectedIndex = 0

		sub_DB.AEDT["App"] = oApp
		sub_DB.AEDT["Desktop"] = oDesktop
		sub_DB.AEDT["Project"] = oProject

		# Set Active Design
		if "(Design)<Setup>[EYE]" in sub_DB.Uenv:		
			for item in self._ComboBox_Design.Items:						
				if item == sub_DB.Uenv["(Design)<Setup>[EYE]"][0]:
					self._ComboBox_Design.SelectedItem = item
					break
			oDesign = oProject.SetActiveDesign(self._ComboBox_Design.SelectedItem)

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
		Log(str(e))
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
