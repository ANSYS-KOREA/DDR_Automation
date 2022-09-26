import os
import time
import sys

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
from sub_IBIS import *
from System.Drawing import *
from System.Windows.Forms import *

class Eye_Form(Form):
	def __init__(self):

		self.InitializeComponent()
	
	''' Eye_Form - GUI '''
	def InitializeComponent(self):		
		global path
		path = os.path.dirname(os.path.abspath(__file__))

		self._PictureBox_OldEye = System.Windows.Forms.PictureBox()
		self._PictureBox_NewEye = System.Windows.Forms.PictureBox()

		self._GroupBox_Setup = System.Windows.Forms.GroupBox()
		self._GroupBox_OldEye = System.Windows.Forms.GroupBox()
		self._GroupBox_UnitOld = System.Windows.Forms.GroupBox()
		self._GroupBox_NewEye = System.Windows.Forms.GroupBox()
		self._GroupBox_UnitNew = System.Windows.Forms.GroupBox()		

		self._ComboBox_DDRGen = System.Windows.Forms.ComboBox()
		self._ComboBox_DataRate = System.Windows.Forms.ComboBox()		
		self._ComboBox_SolutionName = System.Windows.Forms.ComboBox()
		self._ComboBox_Design = System.Windows.Forms.ComboBox()
		self._ComboBox_AC_DQ = System.Windows.Forms.ComboBox()
		self._ComboBox_AC_ADDR = System.Windows.Forms.ComboBox()
		self._ComboBox_AEDT = System.Windows.Forms.ComboBox()

		self._CheckedListBox_ReportName = System.Windows.Forms.CheckedListBox()

		self._Label_ns = System.Windows.Forms.Label()
		self._Label_Offset = System.Windows.Forms.Label()		
		self._Label_Version = System.Windows.Forms.Label()		
		self._Label_InputFile = System.Windows.Forms.Label()
		self._Label_Design = System.Windows.Forms.Label()
		self._Label_ReportName = System.Windows.Forms.Label()
		self._Label_SolutionName = System.Windows.Forms.Label()
		self._Label_DDRGen = System.Windows.Forms.Label()
		self._Label_Datarate = System.Windows.Forms.Label()		
		self._Label_Mbps = System.Windows.Forms.Label()		
		self._Label_AC_DQ = System.Windows.Forms.Label()
		self._Label_AC_ADDR = System.Windows.Forms.Label()
		self._Label_DC_DQ = System.Windows.Forms.Label()
		self._Label_DC_ADDR = System.Windows.Forms.Label()
		self._Label_DQ = System.Windows.Forms.Label()
		self._Label_ADDR = System.Windows.Forms.Label()
		self._Label_VoltageUnitOld = System.Windows.Forms.Label()
		self._Label_TimeUnitOld = System.Windows.Forms.Label()		
		self._Label_VoltageUnitNew = System.Windows.Forms.Label()
		self._Label_TimeUnitNew = System.Windows.Forms.Label()
		self._Label_Info = System.Windows.Forms.Label()
		self._Label_VdIVW = System.Windows.Forms.Label()
		self._Label_TimingSpec = System.Windows.Forms.Label()
		self._Label_VoltageSpec = System.Windows.Forms.Label()
		self._Label_TdIVW = System.Windows.Forms.Label()
		self._Label_VcentDQ = System.Windows.Forms.Label()
		self._Label_Vac = System.Windows.Forms.Label()
		self._Label_Vdc = System.Windows.Forms.Label()
		self._Label_Setup = System.Windows.Forms.Label()
		self._Label_Hold = System.Windows.Forms.Label()
		self._Label_Vref = System.Windows.Forms.Label()
		self._Label_dq = System.Windows.Forms.Label()
		self._Label_addr = System.Windows.Forms.Label()
		self._Label_AEDT = System.Windows.Forms.Label()

		self._H_Border_1 = System.Windows.Forms.Label()
		self._H_Border_2 = System.Windows.Forms.Label()
		self._H_Border_3 = System.Windows.Forms.Label()
		self._V_Border_0 = System.Windows.Forms.Label()
		self._V_Border_1 = System.Windows.Forms.Label()
		self._V_Border_2 = System.Windows.Forms.Label()
		self._V_Border_3 = System.Windows.Forms.Label()
		self._V_Border_4 = System.Windows.Forms.Label()
		self._V_Border_5 = System.Windows.Forms.Label()
		self._V_Border_6 = System.Windows.Forms.Label()
		
		self._TextBox_Offset = System.Windows.Forms.TextBox()
		self._TextBox_InputFile = System.Windows.Forms.TextBox()
		self._TextBox_AC_DQ = System.Windows.Forms.TextBox()
		self._TextBox_AC_ADDR = System.Windows.Forms.TextBox()
		self._TextBox_DC_DQ = System.Windows.Forms.TextBox()
		self._TextBox_DC_ADDR = System.Windows.Forms.TextBox()
		self._TextBox_DQSetup = System.Windows.Forms.TextBox()
		self._TextBox_DQHold = System.Windows.Forms.TextBox()
		self._TextBox_ADDRHold = System.Windows.Forms.TextBox()
		self._TextBox_ADDRSetup = System.Windows.Forms.TextBox()		
		self._TextBox_Vref = System.Windows.Forms.TextBox()		
		self._TextBox_VcentDQ = System.Windows.Forms.TextBox()
		self._TextBox_VdIVW = System.Windows.Forms.TextBox()
		self._TextBox_TdIVW = System.Windows.Forms.TextBox()

		self._Button_Import = System.Windows.Forms.Button()
		self._Button_ViewNet = System.Windows.Forms.Button()
		self._Button_Analyze = System.Windows.Forms.Button()
		self._Button_ViewResult = System.Windows.Forms.Button()
		self._Button_ImgShow_New = System.Windows.Forms.Button()
		self._Button_ImgShow_Old = System.Windows.Forms.Button()
		self._Button_Add_New = System.Windows.Forms.Button()
		self._Button_Add_Old = System.Windows.Forms.Button()
		self._Button_LoadCnf = System.Windows.Forms.Button()
		self._Button_Debug = System.Windows.Forms.Button()

		self._openFileDialog1 = System.Windows.Forms.OpenFileDialog()
		self._saveFileDialog1 = System.Windows.Forms.SaveFileDialog()

		self._CheckBox_VcentDQ = System.Windows.Forms.CheckBox()
		self._CheckBox_Vref = System.Windows.Forms.CheckBox()
		self._CheckBox_AnalyzeDQ = System.Windows.Forms.CheckBox()
		self._CheckBox_AnalyzeADDR = System.Windows.Forms.CheckBox()
		self._CheckBox_EditEnable_NewEye = System.Windows.Forms.CheckBox()
		self._CheckBox_EditEnable_OldEye = System.Windows.Forms.CheckBox()
		self._CheckBox_Debug = System.Windows.Forms.CheckBox()

		self._TextBox_InputFile_ToopTip = System.Windows.Forms.ToolTip()		
		self._ComboBox_Design_ToopTip = System.Windows.Forms.ToolTip()
		self._ComboBox_SolutionName_ToopTip = System.Windows.Forms.ToolTip()

		self._MenuStrip = System.Windows.Forms.MenuStrip()
		self._File_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._DDRConf_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._DDRConf_Load_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._DDRConf_Edit_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._UserConf_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._UserConf_Load_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._UserConf_Save_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._UserConf_Edit_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._Exit_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()		
		self._Help_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._Help_DDRHelp_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._Help_DDRGuid_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._Help_DDRNew_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._Help_DDRAbout_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._Tool_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._Options_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._Options_IBISStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._Options_BatchStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._toolStripSeparator1 = System.Windows.Forms.ToolStripSeparator()
		self._toolStripSeparator2 = System.Windows.Forms.ToolStripSeparator()

		self._toolStrip1 = System.Windows.Forms.ToolStrip()
		self._toolStrip_Input_Button = System.Windows.Forms.ToolStripButton()		
		self._toolStrip_DefLoad_Button = System.Windows.Forms.ToolStripButton()
		self._toolStrip_DefEdit_Button = System.Windows.Forms.ToolStripButton()		
		self._toolStrip_CnfLoad_Button = System.Windows.Forms.ToolStripButton()
		self._toolStrip_CnfSave_Button = System.Windows.Forms.ToolStripButton()		
		self._toolStrip_CnfEdit_Button = System.Windows.Forms.ToolStripButton()
		self._toolStrip_Option_Button = System.Windows.Forms.ToolStripButton()
		self._toolStrip_Batch_Button = System.Windows.Forms.ToolStripButton()
		self._toolStrip_IBIS_Button = System.Windows.Forms.ToolStripButton()
		
		self._toolStripSplit_IBIS_Button = System.Windows.Forms.ToolStripSplitButton()
		self._IBISToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._ADEAQuickGuideToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()		

		self._toolStripSplit_Help_Button = System.Windows.Forms.ToolStripSplitButton()
		self._ADEAHelpToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._ADEAQuickGuideToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()		
		self._WhatsNewInThisReleaseToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._AboutAnsysDDREyeAnalyzerToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._toolStripSeparator3 = System.Windows.Forms.ToolStripSeparator()
		self._toolStripSeparator4 = System.Windows.Forms.ToolStripSeparator()
		self._toolStripSeparator5 = System.Windows.Forms.ToolStripSeparator()
		self._toolStripSeparator6 = System.Windows.Forms.ToolStripSeparator()
		self._toolStripSeparator7 = System.Windows.Forms.ToolStripSeparator()

		self._PictureBox_OldEye.BeginInit()
		self._PictureBox_NewEye.BeginInit()
		self._MenuStrip.SuspendLayout()
		self._GroupBox_Setup.SuspendLayout()
		self._GroupBox_OldEye.SuspendLayout()		
		self._GroupBox_NewEye.SuspendLayout()
		self._GroupBox_UnitOld.SuspendLayout()
		self._GroupBox_UnitNew.SuspendLayout()
		self._toolStrip1.SuspendLayout()
		self.SuspendLayout()
		# 
		# MenuStrip
		#
		self._MenuStrip.BackColor = System.Drawing.SystemColors.Window
		self._MenuStrip.Font = System.Drawing.Font("Arial", 10)
		self._MenuStrip.Items.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._File_ToolStripMenuItem,
			self._Tool_ToolStripMenuItem,
			self._Help_ToolStripMenuItem]))
		self._MenuStrip.Location = System.Drawing.Point(0, 0)
		self._MenuStrip.Name = "MenuStrip"
		self._MenuStrip.Size = System.Drawing.Size(1000, 24)
		self._MenuStrip.TabIndex = 0
		self._MenuStrip.Text = "menuStrip1"
		# 
		# File_ToolStripMenuItem
		# 
		self._File_ToolStripMenuItem.DropDownItems.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._DDRConf_ToolStripMenuItem,
			self._UserConf_ToolStripMenuItem,
			self._toolStripSeparator1,
			self._Exit_ToolStripMenuItem]))
		self._File_ToolStripMenuItem.Name = "File_ToolStripMenuItem"
		self._File_ToolStripMenuItem.Size = System.Drawing.Size(37, 20)
		self._File_ToolStripMenuItem.Text = "File"
		# 
		# DDRConf_ToolStripMenuItem
		# 
		self._DDRConf_ToolStripMenuItem.DropDownItems.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._DDRConf_Load_ToolStripMenuItem,			
			self._DDRConf_Edit_ToolStripMenuItem]))
		self._DDRConf_ToolStripMenuItem.Name = "DDRConf_ToolStripMenuItem"
		self._DDRConf_ToolStripMenuItem.Size = System.Drawing.Size(177, 22)
		self._DDRConf_ToolStripMenuItem.Text = "DDR Definition"
		# 
		# DDRConf_Load_ToolStripMenuItem
		# 
		self._DDRConf_Load_ToolStripMenuItem.Name = "DDRConf_Load_ToolStripMenuItem"
		self._DDRConf_Load_ToolStripMenuItem.Size = System.Drawing.Size(100, 22)
		self._DDRConf_Load_ToolStripMenuItem.Text = "Load"
		self._DDRConf_Load_ToolStripMenuItem.Click += self.DDRConf_Load_ToolStripMenuItemClick		
		# 
		# DDRConf_Edit_ToolStripMenuItem
		# 
		self._DDRConf_Edit_ToolStripMenuItem.Name = "DDRConf_Edit_ToolStripMenuItem"
		self._DDRConf_Edit_ToolStripMenuItem.Size = System.Drawing.Size(100, 22)
		self._DDRConf_Edit_ToolStripMenuItem.Text = "Edit"
		self._DDRConf_Edit_ToolStripMenuItem.Click += self.DDRConf_Edit_ToolStripMenuItemClick
		# 
		# UserConf_ToolStripMenuItem
		# 
		self._UserConf_ToolStripMenuItem.DropDownItems.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._UserConf_Load_ToolStripMenuItem,
			self._UserConf_Save_ToolStripMenuItem,
			self._UserConf_Edit_ToolStripMenuItem]))
		self._UserConf_ToolStripMenuItem.Name = "UserConf_ToolStripMenuItem"
		self._UserConf_ToolStripMenuItem.Size = System.Drawing.Size(177, 22)
		self._UserConf_ToolStripMenuItem.Text = "User Configuration"		
		# 
		# UserConf_Load_ToolStripMenuItem
		# 
		self._UserConf_Load_ToolStripMenuItem.Name = "UserConf_Load_ToolStripMenuItem"
		self._UserConf_Load_ToolStripMenuItem.Size = System.Drawing.Size(100, 22)
		self._UserConf_Load_ToolStripMenuItem.Text = "Load                 Ctrl+L"
		self._UserConf_Load_ToolStripMenuItem.Click += self.UserConf_Load_ToolStripMenuItemClick
		# 
		# UserConf_Save_ToolStripMenuItem
		# 
		self._UserConf_Save_ToolStripMenuItem.Name = "UserConf_Save_ToolStripMenuItem"
		self._UserConf_Save_ToolStripMenuItem.Size = System.Drawing.Size(100, 22)
		self._UserConf_Save_ToolStripMenuItem.Text = "Save                 Ctrl+S"
		self._UserConf_Save_ToolStripMenuItem.Click += self.UserConf_Save_ToolStripMenuItemClick
		# 
		# UserConf_Edit_ToolStripMenuItem
		# 
		self._UserConf_Edit_ToolStripMenuItem.Name = "UserConf_Edit_ToolStripMenuItem"
		self._UserConf_Edit_ToolStripMenuItem.Size = System.Drawing.Size(100, 22)
		self._UserConf_Edit_ToolStripMenuItem.Text = "Edit                   Ctrl+E"
		self._UserConf_Edit_ToolStripMenuItem.Click += self.UserConf_Edit_ToolStripMenuItemClick
		# 
		# Exit_ToolStripMenuItem
		# 
		self._Exit_ToolStripMenuItem.Name = "Exit_ToolStripMenuItem"
		self._Exit_ToolStripMenuItem.Size = System.Drawing.Size(177, 22)
		self._Exit_ToolStripMenuItem.Text = "Exit"
		self._Exit_ToolStripMenuItem.Click += self.Exit_ToolStripMenuItemClick
		# 
		# Tool_ToolStripMenuItem
		# 
		self._Tool_ToolStripMenuItem.DropDownItems.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._Options_ToolStripMenuItem,
			 self._Options_IBISStripMenuItem,
			 self._Options_BatchStripMenuItem]))
		self._Tool_ToolStripMenuItem.Name = "Tool_ToolStripMenuItem"
		self._Tool_ToolStripMenuItem.Size = System.Drawing.Size(46, 20)
		self._Tool_ToolStripMenuItem.Text = "Tool"
		# 
		# Options_ToolStripMenuItem
		# 
		self._Options_ToolStripMenuItem.Name = "Options_ToolStripMenuItem"
		self._Options_ToolStripMenuItem.Size = System.Drawing.Size(152, 22)
		self._Options_ToolStripMenuItem.Text = "Options"
		self._Options_ToolStripMenuItem.Click += self.Options_ToolStripMenuItemClick
		# 
		# Options_IBIShStripMenuItem
		# 
		self._Options_IBISStripMenuItem.Name = "Options_IBIShStripMenuItem"
		self._Options_IBISStripMenuItem.Size = System.Drawing.Size(152, 22)
		self._Options_IBISStripMenuItem.Text = "IBIS Optimization"
		self._Options_IBISStripMenuItem.Click += self.Options_IBISStripMenuItemClick
		# 
		# Options_BatchStripMenuItem
		# 
		self._Options_BatchStripMenuItem.Name = "Options_BatchStripMenuItem"
		self._Options_BatchStripMenuItem.Size = System.Drawing.Size(152, 22)
		self._Options_BatchStripMenuItem.Text = "Batch"
		self._Options_BatchStripMenuItem.Visible = False
		self._Options_BatchStripMenuItem.Click += self.Options_BatchStripMenuItemClick
		# 
		# Help_ToolStripMenuItem
		# 
		self._Help_ToolStripMenuItem.DropDownItems.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._Help_DDRHelp_ToolStripMenuItem,
			self._Help_DDRGuid_ToolStripMenuItem,
			self._toolStripSeparator2,
			self._Help_DDRNew_ToolStripMenuItem,
			self._Help_DDRAbout_ToolStripMenuItem]))
		self._Help_ToolStripMenuItem.Name = "Help_ToolStripMenuItem"
		self._Help_ToolStripMenuItem.Size = System.Drawing.Size(44, 20)
		self._Help_ToolStripMenuItem.Text = "Help"
		# 
		# Help_DDRHelp_ToolStripMenuItem
		# 
		self._Help_DDRHelp_ToolStripMenuItem.Name = "Help_DDRHelp_ToolStripMenuItem"
		self._Help_DDRHelp_ToolStripMenuItem.Size = System.Drawing.Size(300, 22)
		self._Help_DDRHelp_ToolStripMenuItem.Text = "Ansys DDR Eye Analyzer User Guide"
		self._Help_DDRHelp_ToolStripMenuItem.Click += self.Help_DDRHelp_ToolStripMenuItemClick
		# 
		# Help_DDRGuid_ToolStripMenuItem
		# 
		self._Help_DDRGuid_ToolStripMenuItem.Name = "Help_DDRGuid_ToolStripMenuItem"
		self._Help_DDRGuid_ToolStripMenuItem.Size = System.Drawing.Size(300, 22)
		self._Help_DDRGuid_ToolStripMenuItem.Text = "Ansys DDR Eye Analyzer Quick Guide"
		self._Help_DDRGuid_ToolStripMenuItem.Click += self.Help_DDRGuid_ToolStripMenuItemClick
		# 
		# Help_DDRNew_ToolStripMenuItem
		# 
		self._Help_DDRNew_ToolStripMenuItem.Name = "Help_DDRNew_ToolStripMenuItem"
		self._Help_DDRNew_ToolStripMenuItem.Size = System.Drawing.Size(300, 22)
		self._Help_DDRNew_ToolStripMenuItem.Text = "What's New in this Release"
		self._Help_DDRNew_ToolStripMenuItem.Visible = False
		self._Help_DDRNew_ToolStripMenuItem.Click += self.Help_DDRNew_ToolStripMenuItemClick
		# 
		# Help_DDRAbout_ToolStripMenuItem
		# 
		self._Help_DDRAbout_ToolStripMenuItem.Name = "Help_DDRAbout_ToolStripMenuItem"
		self._Help_DDRAbout_ToolStripMenuItem.Size = System.Drawing.Size(300, 22)
		self._Help_DDRAbout_ToolStripMenuItem.Text = "About Ansys DDR Wizard"		
		self._Help_DDRAbout_ToolStripMenuItem.Click += self.Help_DDRAbout_ToolStripMenuItemClick
		# 
		# toolStripSeparator1
		# 
		self._toolStripSeparator1.Name = "toolStripSeparator1"
		self._toolStripSeparator1.Size = System.Drawing.Size(174, 6)
		# 
		# toolStripSeparator2
		#
		self._toolStripSeparator2.Name = "toolStripSeparator2"
		self._toolStripSeparator2.Size = System.Drawing.Size(297, 6)		
		# 
		# toolStrip1
		#
		self._toolStrip1.GripStyle = System.Windows.Forms.ToolStripGripStyle.Hidden
		self._toolStrip1.BackColor = System.Drawing.SystemColors.Control
		self._toolStrip1.Items.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._toolStrip_Input_Button,
			self._toolStripSeparator3,
			self._toolStrip_DefLoad_Button,
			self._toolStrip_DefEdit_Button,
			self._toolStripSeparator4,
			self._toolStrip_CnfLoad_Button,
			self._toolStrip_CnfSave_Button,
			self._toolStrip_CnfEdit_Button,
			self._toolStripSeparator5,
			self._toolStrip_Option_Button,			
			self._toolStrip_IBIS_Button,
			self._toolStrip_Batch_Button,
			self._toolStripSeparator6,
			self._toolStripSplit_Help_Button]))
		self._toolStrip1.Location = System.Drawing.Point(0, 0)
		self._toolStrip1.Name = "toolStrip1"
		self._toolStrip1.AutoSize = False
		self._toolStrip1.Size = System.Drawing.Size(1802, 35)
		self._toolStrip1.TabIndex = 45
		self._toolStrip1.Visible = True
		self._toolStrip1.Text = "toolStrip1"
		self._toolStrip1.ImageScalingSize = System.Drawing.Size(15, 20)
		# 
		# toolStrip_Input_Button
		#
		#File = path + r'\Resources\open-folder.png'
		File = path + r'\Resources\fig\folder.png'
		self._toolStrip_Input_Button.AutoToolTip = False
		self._toolStrip_Input_Button.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch
		self._toolStrip_Input_Button.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.ImageAndText
		self._toolStrip_Input_Button.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageAboveText
		self._toolStrip_Input_Button.Font = System.Drawing.Font("Calibri", 8.25, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._toolStrip_Input_Button.Image = Bitmap(File)
		self._toolStrip_Input_Button.ImageTransparentColor = System.Drawing.Color.Magenta
		self._toolStrip_Input_Button.Margin = System.Windows.Forms.Padding(11, 3, 0, 2)
		self._toolStrip_Input_Button.Name = "toolStrip_Input_Button"		
		self._toolStrip_Input_Button.Text = "Open"
		self._toolStrip_Input_Button.ToolTipText = "[Crtl+I] : Open Input File"
		self._toolStrip_Input_Button.Click += self.toolStrip_Input_ButtonClick
		# 
		# toolStripSeparator3
		# 
		self._toolStripSeparator3.Name = "toolStripSeparator1"
		self._toolStripSeparator3.Size = System.Drawing.Size(6, 25)
		#
		# toolStrip_DefLoad_Button
		#
		File = path + r'\Resources\fig\import.png'
		self._toolStrip_DefLoad_Button.AutoToolTip = False
		self._toolStrip_DefLoad_Button.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch
		self._toolStrip_DefLoad_Button.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.ImageAndText
		self._toolStrip_DefLoad_Button.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageAboveText
		self._toolStrip_DefLoad_Button.Font = System.Drawing.Font("Calibri", 8.25, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._toolStrip_DefLoad_Button.Image = Bitmap(File)
		self._toolStrip_DefLoad_Button.ImageTransparentColor = System.Drawing.Color.Magenta
		self._toolStrip_DefLoad_Button.Margin = System.Windows.Forms.Padding(0, 4, 0, 2)
		self._toolStrip_DefLoad_Button.Name = "toolStrip_DefLoad_Button"		
		self._toolStrip_DefLoad_Button.Text = "Load Def"
		self._toolStrip_DefLoad_Button.ToolTipText = "Load Definition File"
		self._toolStrip_DefLoad_Button.Click += self.toolStrip_DefLoad_ButtonClick		
		#
		# toolStrip_DefEdit_Button
		#
		File = path + r'\Resources\fig\edit.png'
		self._toolStrip_DefEdit_Button.AutoToolTip = False
		self._toolStrip_DefEdit_Button.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch
		self._toolStrip_DefEdit_Button.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.ImageAndText
		self._toolStrip_DefEdit_Button.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageAboveText
		self._toolStrip_DefEdit_Button.Font = System.Drawing.Font("Calibri", 8.25, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._toolStrip_DefEdit_Button.Image = Bitmap(File)
		self._toolStrip_DefEdit_Button.ImageTransparentColor = System.Drawing.Color.Magenta
		self._toolStrip_DefEdit_Button.Margin = System.Windows.Forms.Padding(0, 4, 0, 2)
		self._toolStrip_DefEdit_Button.Name = "toolStrip_DefEdit_Button"		
		self._toolStrip_DefEdit_Button.Text = "Edit Def"
		self._toolStrip_DefEdit_Button.ToolTipText = "Edit Definition File"
		self._toolStrip_DefEdit_Button.Click += self.toolStrip_DefEdit_ButtonClick
		# 
		# toolStripSeparator4
		# 
		self._toolStripSeparator4.Name = "toolStripSeparator4"
		self._toolStripSeparator4.Size = System.Drawing.Size(6, 25)
		#
		# toolStrip_CnfLoad_Button
		#
		File = path + r'\Resources\fig\import.png'
		self._toolStrip_CnfLoad_Button.AutoToolTip = False
		self._toolStrip_CnfLoad_Button.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch
		self._toolStrip_CnfLoad_Button.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.ImageAndText
		self._toolStrip_CnfLoad_Button.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageAboveText
		self._toolStrip_CnfLoad_Button.Font = System.Drawing.Font("Calibri", 8.25, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._toolStrip_CnfLoad_Button.Image = Bitmap(File)
		self._toolStrip_CnfLoad_Button.ImageTransparentColor = System.Drawing.Color.Magenta
		self._toolStrip_CnfLoad_Button.Margin = System.Windows.Forms.Padding(0, 4, 0, 2)
		self._toolStrip_CnfLoad_Button.Name = "toolStrip_CnfLoad_Button"		
		self._toolStrip_CnfLoad_Button.Text = "Load Cnf"
		self._toolStrip_CnfLoad_Button.ToolTipText = "[Crtl+L] : Load Configuration File"
		self._toolStrip_CnfLoad_Button.Click += self.toolStrip_CnfLoad_ButtonClick
		#
		# toolStrip_CnfSave_Button
		#
		File = path + r'\Resources\fig\save.png'
		self._toolStrip_CnfSave_Button.AutoToolTip = False
		self._toolStrip_CnfSave_Button.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch
		self._toolStrip_CnfSave_Button.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.ImageAndText
		self._toolStrip_CnfSave_Button.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageAboveText
		self._toolStrip_CnfSave_Button.Font = System.Drawing.Font("Calibri", 8.25, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._toolStrip_CnfSave_Button.Image = Bitmap(File)
		self._toolStrip_CnfSave_Button.ImageTransparentColor = System.Drawing.Color.Magenta
		self._toolStrip_CnfSave_Button.Margin = System.Windows.Forms.Padding(0, 4, 0, 2)
		self._toolStrip_CnfSave_Button.Name = "toolStrip_CnfSave_Button"
		self._toolStrip_CnfSave_Button.Text = "Save Cnf"
		self._toolStrip_CnfSave_Button.ToolTipText = "[Crtl+S] : Soad Configuration File"
		self._toolStrip_CnfSave_Button.Click += self.toolStrip_CnfSave_ButtonClick
		#
		# toolStrip_CnfEdit_Button
		#
		File = path + r'\Resources\fig\edit.png'
		self._toolStrip_CnfEdit_Button.AutoToolTip = False
		self._toolStrip_CnfEdit_Button.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch
		self._toolStrip_CnfEdit_Button.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.ImageAndText
		self._toolStrip_CnfEdit_Button.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageAboveText
		self._toolStrip_CnfEdit_Button.Font = System.Drawing.Font("Calibri", 8.25, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._toolStrip_CnfEdit_Button.Image = Bitmap(File)
		self._toolStrip_CnfEdit_Button.ImageTransparentColor = System.Drawing.Color.Magenta
		self._toolStrip_CnfEdit_Button.Margin = System.Windows.Forms.Padding(0, 4, 0, 2)
		self._toolStrip_CnfEdit_Button.Name = "toolStrip_CnfEdit_Button"
		self._toolStrip_CnfEdit_Button.Text = "Edit Cnf"
		self._toolStrip_CnfEdit_Button.ToolTipText = "[Crtl+E] : Load Configuration File"
		self._toolStrip_CnfEdit_Button.Click += self.toolStrip_CnfEdit_ButtonClick
		# 
		# toolStripSeparator5
		# 
		self._toolStripSeparator5.Name = "toolStripSeparator5"
		self._toolStripSeparator5.Size = System.Drawing.Size(6, 25)				
		#
		# toolStrip_Option_Button
		#
		File = path + r'\Resources\fig\options.png'
		self._toolStrip_Option_Button.AutoToolTip = False
		self._toolStrip_Option_Button.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch
		self._toolStrip_Option_Button.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.ImageAndText
		self._toolStrip_Option_Button.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageAboveText
		self._toolStrip_Option_Button.Font = System.Drawing.Font("Calibri", 8.25, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._toolStrip_Option_Button.Image = Bitmap(File)
		self._toolStrip_Option_Button.ImageTransparentColor = System.Drawing.Color.Magenta
		self._toolStrip_Option_Button.Margin = System.Windows.Forms.Padding(0, 4, 0, 2)
		self._toolStrip_Option_Button.Name = "toolStrip_Option_Button"
		self._toolStrip_Option_Button.Text = "Option"
		self._toolStrip_Option_Button.ToolTipText = "[Crtl+O] : Set Eye Analysis Options"
		self._toolStrip_Option_Button.Click += self.toolStrip_Option_ButtonClick		
		#
		# toolStrip_IBIS_Button
		#
		File = path + r'\Resources\fig\IBIS.png'
		self._toolStrip_IBIS_Button.AutoToolTip = False
		self._toolStrip_IBIS_Button.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch
		self._toolStrip_IBIS_Button.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.ImageAndText
		self._toolStrip_IBIS_Button.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageAboveText
		self._toolStrip_IBIS_Button.Font = System.Drawing.Font("Calibri", 8.25, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._toolStrip_IBIS_Button.Image = Bitmap(File)
		self._toolStrip_IBIS_Button.ImageTransparentColor = System.Drawing.Color.Magenta
		self._toolStrip_IBIS_Button.Margin = System.Windows.Forms.Padding(0, 4, 0, 2)
		self._toolStrip_IBIS_Button.Name = "toolStrip_IBIS_Button"
		self._toolStrip_IBIS_Button.Text = "IBIS Opt."
		self._toolStrip_IBIS_Button.ToolTipText = "[Crtl+B] : DDR IBIS Optimization"
		self._toolStrip_IBIS_Button.Click += self.toolStrip_IBIS_ButtonClick		
		#
		# toolStrip_Batch_Button
		#
		File = path + r'\Resources\fig\batch.png'
		self._toolStrip_Batch_Button.AutoToolTip = False
		self._toolStrip_Batch_Button.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch
		self._toolStrip_Batch_Button.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.ImageAndText
		self._toolStrip_Batch_Button.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageAboveText
		self._toolStrip_Batch_Button.Font = System.Drawing.Font("Calibri", 8.25, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._toolStrip_Batch_Button.Image = Bitmap(File)
		self._toolStrip_Batch_Button.ImageTransparentColor = System.Drawing.Color.Magenta
		self._toolStrip_Batch_Button.Margin = System.Windows.Forms.Padding(0, 4, 0, 2)
		self._toolStrip_Batch_Button.Name = "toolStrip_Batch_Button"
		self._toolStrip_Batch_Button.Text = "Batch"
		self._toolStrip_Batch_Button.ToolTipText = "[Crtl+C] : Batch Process for ADEA"
		self._toolStrip_Batch_Button.Visible = False
		self._toolStrip_Batch_Button.Click += self.toolStrip_Batch_ButtonClick		
		# 
		# toolStripSeparator6
		# 
		self._toolStripSeparator6.Name = "toolStripSeparator4"
		self._toolStripSeparator6.Size = System.Drawing.Size(6, 25)
		# 
		# toolStripSplit_Help_Button
		# 
		File = path + r'\Resources\fig\help.png'
		self._toolStripSplit_Help_Button.AutoToolTip = False
		self._toolStripSplit_Help_Button.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch
		self._toolStripSplit_Help_Button.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.ImageAndText
		self._toolStripSplit_Help_Button.DropDownItems.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._ADEAHelpToolStripMenuItem,
			self._ADEAQuickGuideToolStripMenuItem,
			self._toolStripSeparator7,
			self._WhatsNewInThisReleaseToolStripMenuItem,
			self._AboutAnsysDDREyeAnalyzerToolStripMenuItem]))
		self._toolStripSplit_Help_Button.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageAboveText
		self._toolStripSplit_Help_Button.Font = System.Drawing.Font("Calibri", 8.25, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._toolStripSplit_Help_Button.Image = Bitmap(File)
		self._toolStripSplit_Help_Button.ImageTransparentColor = System.Drawing.Color.Magenta
		self._toolStripSplit_Help_Button.Margin = System.Windows.Forms.Padding(0, 4, 0, 2)
		self._toolStripSplit_Help_Button.Name = "toolStrip_Help_Button"
		self._toolStripSplit_Help_Button.Text = "Help"
		self._toolStripSplit_Help_Button.ToolTipText = "Help for ADEA"	
		# 
		# ADEAHelpToolStripMenuItem
		# 
		self._ADEAHelpToolStripMenuItem.Name = "ADEAHelpToolStripMenuItem"
		self._ADEAHelpToolStripMenuItem.Size = System.Drawing.Size(243, 22)
		self._ADEAHelpToolStripMenuItem.Text = "ADEA User Guide"
		self._ADEAHelpToolStripMenuItem.Click += self.ADEAHelpToolStripMenuItemClick
		# 
		# ADEAQuickGuideToolStripMenuItem
		# 
		self._ADEAQuickGuideToolStripMenuItem.Name = "ADEAQuickGuideToolStripMenuItem"
		self._ADEAQuickGuideToolStripMenuItem.Size = System.Drawing.Size(243, 22)
		self._ADEAQuickGuideToolStripMenuItem.Text = "ADEA Quick Guide"
		self._ADEAQuickGuideToolStripMenuItem.Click += self.ADEAQuickGuideToolStripMenuItemClick
		# 
		# toolStripSeparator7
		# 
		self._toolStripSeparator7.Name = "toolStripSeparator1"		
		self._toolStripSeparator7.Size = System.Drawing.Size(240, 6)
		# 
		# WhatsNewInThisReleaseToolStripMenuItem
		# 
		self._WhatsNewInThisReleaseToolStripMenuItem.Name = "WhatsNewInThisReleaseToolStripMenuItem"
		self._WhatsNewInThisReleaseToolStripMenuItem.Size = System.Drawing.Size(243, 22)
		self._WhatsNewInThisReleaseToolStripMenuItem.Text = "What's New in this Release"
		self._WhatsNewInThisReleaseToolStripMenuItem.Visible = False
		self._WhatsNewInThisReleaseToolStripMenuItem.Click += self.WhatsNewInThisReleaseToolStripMenuItemClick
		# 
		# AboutAnsysDDREyeAnalyzerToolStripMenuItem
		# 
		self._AboutAnsysDDREyeAnalyzerToolStripMenuItem.Name = "AboutAnsysDDREyeAnalyzerToolStripMenuItem"
		self._AboutAnsysDDREyeAnalyzerToolStripMenuItem.Size = System.Drawing.Size(243, 22)
		self._AboutAnsysDDREyeAnalyzerToolStripMenuItem.Text = "About Ansys DDR Eye Analyzer"		
		self._AboutAnsysDDREyeAnalyzerToolStripMenuItem.Click += self.AboutAnsysDDREyeAnalyzerToolStripMenuItemClick
		# 
		# PictureBox_OldEye
		# 
		File = path + "\\Resources\\fig\\EYE_Measuer_Old.jpg"
		self._PictureBox_OldEye.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch
		self._PictureBox_OldEye.ErrorImage = None
		self._PictureBox_OldEye.Image = Bitmap(File)
		self._PictureBox_OldEye.Location = System.Drawing.Point(6, 17)
		self._PictureBox_OldEye.Name = "PictureBox_OldEye"
		self._PictureBox_OldEye.Size = System.Drawing.Size(678, 397)
		self._PictureBox_OldEye.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage
		self._PictureBox_OldEye.TabIndex = 26
		self._PictureBox_OldEye.TabStop = False		
		# 
		# PictureBox_NewEye
		#
		File = path + "\\Resources\\fig\\EYE_Measuer_New.jpg"
		self._PictureBox_NewEye.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch
		self._PictureBox_NewEye.ErrorImage = None
		self._PictureBox_NewEye.Image = Bitmap(File)
		self._PictureBox_NewEye.Location = System.Drawing.Point(6, 17)
		self._PictureBox_NewEye.Name = "PictureBox_NewEye"
		self._PictureBox_NewEye.Size = System.Drawing.Size(678, 397)
		self._PictureBox_NewEye.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage
		self._PictureBox_NewEye.TabIndex = 26
		self._PictureBox_NewEye.TabStop = False
		# 
		# GroupBox_Setup
		#
		self._GroupBox_Setup.Controls.Add(self._TextBox_Offset)
		self._GroupBox_Setup.Controls.Add(self._Label_ns)
		self._GroupBox_Setup.Controls.Add(self._Label_Offset)
		self._GroupBox_Setup.Controls.Add(self._ComboBox_AEDT)
		self._GroupBox_Setup.Controls.Add(self._CheckedListBox_ReportName)
		self._GroupBox_Setup.Controls.Add(self._ComboBox_Design)
		self._GroupBox_Setup.Controls.Add(self._ComboBox_SolutionName)		
		self._GroupBox_Setup.Controls.Add(self._Label_SolutionName)
		self._GroupBox_Setup.Controls.Add(self._Label_ReportName)
		self._GroupBox_Setup.Controls.Add(self._Label_Design)
		self._GroupBox_Setup.Controls.Add(self._Label_Mbps)
		self._GroupBox_Setup.Controls.Add(self._ComboBox_DataRate)
		self._GroupBox_Setup.Controls.Add(self._Button_Import)
		self._GroupBox_Setup.Controls.Add(self._ComboBox_DDRGen)
		self._GroupBox_Setup.Controls.Add(self._TextBox_InputFile)
		self._GroupBox_Setup.Controls.Add(self._Label_Datarate)
		self._GroupBox_Setup.Controls.Add(self._Label_DDRGen)
		self._GroupBox_Setup.Controls.Add(self._Label_InputFile)
		self._GroupBox_Setup.Font = System.Drawing.Font("Arial", 11, System.Drawing.FontStyle.Bold)		
		self._GroupBox_Setup.Location = System.Drawing.Point(5, 56)
		self._GroupBox_Setup.Name = "GroupBox_Setup"
		self._GroupBox_Setup.Size = System.Drawing.Size(586, 138)
		self._GroupBox_Setup.TabIndex = 8
		self._GroupBox_Setup.TabStop = False
		self._GroupBox_Setup.Text = "DDR Eye Analyzer Setup"		
		# 
		# GroupBox_OldEye
		#
		self._GroupBox_OldEye.Controls.Add(self._Button_Add_Old)
		self._GroupBox_OldEye.Controls.Add(self._CheckBox_Vref)
		self._GroupBox_OldEye.Controls.Add(self._Label_Vac)
		self._GroupBox_OldEye.Controls.Add(self._Label_Vdc)
		self._GroupBox_OldEye.Controls.Add(self._Label_Setup)
		self._GroupBox_OldEye.Controls.Add(self._Label_Hold)
		self._GroupBox_OldEye.Controls.Add(self._Label_Vref)
		self._GroupBox_OldEye.Controls.Add(self._Label_addr)
		self._GroupBox_OldEye.Controls.Add(self._Label_dq)
		self._GroupBox_OldEye.Controls.Add(self._H_Border_1)
		self._GroupBox_OldEye.Controls.Add(self._H_Border_2)
		self._GroupBox_OldEye.Controls.Add(self._H_Border_3)
		self._GroupBox_OldEye.Controls.Add(self._V_Border_0)
		self._GroupBox_OldEye.Controls.Add(self._V_Border_1)
		self._GroupBox_OldEye.Controls.Add(self._V_Border_2)
		self._GroupBox_OldEye.Controls.Add(self._V_Border_3)
		self._GroupBox_OldEye.Controls.Add(self._V_Border_4)
		self._GroupBox_OldEye.Controls.Add(self._V_Border_5)
		self._GroupBox_OldEye.Controls.Add(self._V_Border_6)
		self._GroupBox_OldEye.Controls.Add(self._Button_ImgShow_Old)
		self._GroupBox_OldEye.Controls.Add(self._ComboBox_AC_ADDR)
		self._GroupBox_OldEye.Controls.Add(self._ComboBox_AC_ADDR)
		self._GroupBox_OldEye.Controls.Add(self._ComboBox_AC_DQ)
		self._GroupBox_OldEye.Controls.Add(self._GroupBox_UnitOld)
		self._GroupBox_OldEye.Controls.Add(self._CheckBox_AnalyzeADDR)
		self._GroupBox_OldEye.Controls.Add(self._CheckBox_AnalyzeDQ)
		self._GroupBox_OldEye.Controls.Add(self._CheckBox_EditEnable_OldEye)
		self._GroupBox_OldEye.Controls.Add(self._Label_ADDR)
		self._GroupBox_OldEye.Controls.Add(self._Label_DQ)
		self._GroupBox_OldEye.Controls.Add(self._Label_AC_ADDR)
		self._GroupBox_OldEye.Controls.Add(self._Label_AC_DQ)
		self._GroupBox_OldEye.Controls.Add(self._Label_DC_ADDR)
		self._GroupBox_OldEye.Controls.Add(self._Label_DC_DQ)
		self._GroupBox_OldEye.Controls.Add(self._TextBox_Vref)
		self._GroupBox_OldEye.Controls.Add(self._TextBox_DC_DQ)
		self._GroupBox_OldEye.Controls.Add(self._TextBox_DC_ADDR)
		self._GroupBox_OldEye.Controls.Add(self._TextBox_ADDRHold)
		self._GroupBox_OldEye.Controls.Add(self._TextBox_ADDRSetup)
		self._GroupBox_OldEye.Controls.Add(self._TextBox_DQHold)
		self._GroupBox_OldEye.Controls.Add(self._TextBox_DQSetup)
		self._GroupBox_OldEye.Controls.Add(self._TextBox_AC_DQ)
		self._GroupBox_OldEye.Controls.Add(self._TextBox_AC_ADDR)
		self._GroupBox_OldEye.Controls.Add(self._PictureBox_OldEye)		
		self._GroupBox_OldEye.Font = System.Drawing.Font("Arial", 11, System.Drawing.FontStyle.Bold)
		self._GroupBox_OldEye.Location = System.Drawing.Point(5, 197)
		self._GroupBox_OldEye.Name = "GroupBox_OldEye"
		self._GroupBox_OldEye.Size = System.Drawing.Size(690, 455)		
		self._GroupBox_OldEye.TabIndex = 26
		self._GroupBox_OldEye.TabStop = False
		self._GroupBox_OldEye.Text = "Eye Analysis"		
		self._GroupBox_OldEye.Visible = False
		# 
		# GroupBox_UnitOld
		# 
		self._GroupBox_UnitOld.Controls.Add(self._Label_TimeUnitOld)
		self._GroupBox_UnitOld.Controls.Add(self._Label_VoltageUnitOld)
		self._GroupBox_UnitOld.Font = System.Drawing.Font("Arial", 9)
		self._GroupBox_UnitOld.Location = System.Drawing.Point(11, 22)		
		self._GroupBox_UnitOld.Name = "GroupBox_UnitOld"
		self._GroupBox_UnitOld.Size = System.Drawing.Size(106, 66)
		self._GroupBox_UnitOld.TabIndex = 38
		self._GroupBox_UnitOld.TabStop = False
		self._GroupBox_UnitOld.Text = "Unit"
		# 
		# GroupBox_NewEye
		#
		self._GroupBox_NewEye.Controls.Add(self._Button_Add_New)
		self._GroupBox_NewEye.Controls.Add(self._CheckBox_VcentDQ)
		self._GroupBox_NewEye.Controls.Add(self._Label_VoltageSpec)
		self._GroupBox_NewEye.Controls.Add(self._Label_TimingSpec)
		self._GroupBox_NewEye.Controls.Add(self._Label_VdIVW)
		self._GroupBox_NewEye.Controls.Add(self._Label_TdIVW)
		self._GroupBox_NewEye.Controls.Add(self._Label_VcentDQ)
		self._GroupBox_NewEye.Controls.Add(self._Button_ImgShow_New)
		self._GroupBox_NewEye.Controls.Add(self._Label_Info)
		self._GroupBox_NewEye.Controls.Add(self._CheckBox_EditEnable_NewEye)
		self._GroupBox_NewEye.Controls.Add(self._TextBox_TdIVW)
		self._GroupBox_NewEye.Controls.Add(self._GroupBox_UnitNew)
		self._GroupBox_NewEye.Controls.Add(self._TextBox_VcentDQ)
		self._GroupBox_NewEye.Controls.Add(self._TextBox_VdIVW)
		self._GroupBox_NewEye.Controls.Add(self._PictureBox_NewEye)
		self._GroupBox_NewEye.Font = System.Drawing.Font("Arial", 11, System.Drawing.FontStyle.Bold)
		self._GroupBox_NewEye.Location = System.Drawing.Point(5, 197)
		self._GroupBox_NewEye.Name = "GroupBox_NewEye"
		self._GroupBox_NewEye.Size = System.Drawing.Size(690, 455)
		self._GroupBox_NewEye.TabIndex = 36
		self._GroupBox_NewEye.TabStop = False
		self._GroupBox_NewEye.Text = "Eye Analysis"
		self._GroupBox_NewEye.Visible = True
		# 
		# GroupBox_UnitNew
		# 
		self._GroupBox_UnitNew.Controls.Add(self._Label_TimeUnitNew)
		self._GroupBox_UnitNew.Controls.Add(self._Label_VoltageUnitNew)
		self._GroupBox_UnitNew.Font = System.Drawing.Font("Arial", 9)
		self._GroupBox_UnitNew.Location = System.Drawing.Point(11, 22)		
		self._GroupBox_UnitNew.Name = "GroupBox_UnitNew"
		self._GroupBox_UnitNew.Size = System.Drawing.Size(150, 66)
		self._GroupBox_UnitNew.TabIndex = 38
		self._GroupBox_UnitNew.TabStop = False
		self._GroupBox_UnitNew.Text = "Unit"
		# 
		# Label_Datarate
		# 
		self._Label_Datarate.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_Datarate.Location = System.Drawing.Point(268, 104)
		self._Label_Datarate.Name = "Label_Datarate"
		self._Label_Datarate.Size = System.Drawing.Size(106, 28)
		self._Label_Datarate.TabIndex = 11
		self._Label_Datarate.Text = "Data-rate :"
		self._Label_Datarate.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_DDRGen
		# 
		self._Label_DDRGen.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)		
		self._Label_DDRGen.Location = System.Drawing.Point(2, 104)
		self._Label_DDRGen.Name = "Label_DDRGen"
		self._Label_DDRGen.Size = System.Drawing.Size(115, 28)		
		self._Label_DDRGen.TabIndex = 10
		self._Label_DDRGen.Text = "DDR Generation :"
		self._Label_DDRGen.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_Mbps
		# 
		self._Label_Mbps.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_Mbps.Location = System.Drawing.Point(535, 104)
		self._Label_Mbps.Name = "Label_Mbps"
		self._Label_Mbps.Size = System.Drawing.Size(45, 28)
		self._Label_Mbps.TabIndex = 21
		self._Label_Mbps.Text = "Mbps"
		self._Label_Mbps.Visible = False
		self._Label_Mbps.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_Offset
		# 
		self._Label_Offset.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_Offset.Location = System.Drawing.Point(446, 104)
		self._Label_Offset.Name = "Label_Offset"
		self._Label_Offset.Size = System.Drawing.Size(55, 25)
		self._Label_Offset.TabIndex = 21
		self._Label_Offset.Text = "Offset :"
		self._Label_Offset.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_ns
		# 
		self._Label_ns.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_ns.Location = System.Drawing.Point(558, 104)
		self._Label_ns.Name = "Label_ns"
		self._Label_ns.Size = System.Drawing.Size(20, 25)
		self._Label_ns.TabIndex = 21
		self._Label_ns.Text = "ns"
		self._Label_ns.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_Version
		# 
		self._Label_Version.Font = System.Drawing.Font("Swis721 Blk BT", 15, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_Version.Location = System.Drawing.Point(352, 34)
		self._Label_Version.Name = "Label_Version"
		self._Label_Version.Size = System.Drawing.Size(104, 28)
		self._Label_Version.TabIndex = 24
		self._Label_Version.Text = sub_DB.Version
		self._Label_Version.Visible = False
		self._Label_Version.TextAlign = System.Drawing.ContentAlignment.MiddleLeft		
		# 
		# Label_Design
		# 
		self._Label_Design.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)		
		self._Label_Design.Location = System.Drawing.Point(11, 47)
		self._Label_Design.Name = "Label_Design"
		self._Label_Design.Size = System.Drawing.Size(106, 28)
		self._Label_Design.TabIndex = 22
		self._Label_Design.Text = "Design :"
		self._Label_Design.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_InputFile
		# 
		self._Label_InputFile.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_InputFile.Location = System.Drawing.Point(6, 19)
		self._Label_InputFile.Name = "Label_InputFile"
		self._Label_InputFile.Size = System.Drawing.Size(110, 28)
		self._Label_InputFile.TabIndex = 9
		self._Label_InputFile.Text = "Ver. && Input File :"
		self._Label_InputFile.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_ReportName
		# 
		self._Label_ReportName.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_ReportName.Location = System.Drawing.Point(270, 48)
		self._Label_ReportName.Name = "Label_ReportName"
		self._Label_ReportName.Size = System.Drawing.Size(106, 28)
		self._Label_ReportName.TabIndex = 26
		self._Label_ReportName.Text = "Report Name :"
		self._Label_ReportName.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_SolutionName
		# 
		self._Label_SolutionName.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_SolutionName.Location = System.Drawing.Point(11, 76)
		self._Label_SolutionName.Name = "Label_ReportName"
		self._Label_SolutionName.Size = System.Drawing.Size(106, 28)
		self._Label_SolutionName.TabIndex = 26
		self._Label_SolutionName.Text = "Setup Name :"
		self._Label_SolutionName.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_DQ
		# 
		self._Label_DQ.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_DQ.Location = System.Drawing.Point(258, 395)
		self._Label_DQ.Name = "Label_DQ"
		self._Label_DQ.Size = System.Drawing.Size(40, 28)
		self._Label_DQ.TabIndex = 29
		self._Label_DQ.Text = "DQ :"
		self._Label_DQ.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_ADDR
		# 
		self._Label_ADDR.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_ADDR.Location = System.Drawing.Point(221, 421)
		self._Label_ADDR.Name = "Label_ADDR"
		self._Label_ADDR.Size = System.Drawing.Size(77, 28)
		self._Label_ADDR.TabIndex = 35
		self._Label_ADDR.Text = "Address :"
		self._Label_ADDR.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_VoltageUnitOld
		# 
		self._Label_VoltageUnitOld.Font = System.Drawing.Font("Arial", 9)
		self._Label_VoltageUnitOld.Location = System.Drawing.Point(6, 15)
		self._Label_VoltageUnitOld.Name = "Label_VoltageUnitOld"
		self._Label_VoltageUnitOld.Size = System.Drawing.Size(94, 28)
		self._Label_VoltageUnitOld.TabIndex = 29
		self._Label_VoltageUnitOld.Text = "* Voltage : [mV]"
		self._Label_VoltageUnitOld.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_TimeUnitOld
		# 
		self._Label_TimeUnitOld.Font = System.Drawing.Font("Arial", 9)
		self._Label_TimeUnitOld.Location = System.Drawing.Point(6, 36)
		self._Label_TimeUnitOld.Name = "Label_TimeUnitOld"
		self._Label_TimeUnitOld.Size = System.Drawing.Size(94, 28)
		self._Label_TimeUnitOld.TabIndex = 30
		self._Label_TimeUnitOld.Text = "* Time : [ps]"
		self._Label_TimeUnitOld.TextAlign = System.Drawing.ContentAlignment.MiddleLeft		
		# 
		# Label_TimeUnitNew
		# 
		self._Label_TimeUnitNew.Font = System.Drawing.Font("Arial", 9)
		self._Label_TimeUnitNew.Location = System.Drawing.Point(6, 36)
		self._Label_TimeUnitNew.Name = "Label_TimeUnitNew"
		self._Label_TimeUnitNew.Size = System.Drawing.Size(140, 28)
		self._Label_TimeUnitNew.TabIndex = 30
		self._Label_TimeUnitNew.Text = "* Time : UI(Unit-Interval)"
		self._Label_TimeUnitNew.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_VoltageUnitNew
		# 
		self._Label_VoltageUnitNew.Font = System.Drawing.Font("Arial", 9)
		self._Label_VoltageUnitNew.Location = System.Drawing.Point(6, 15)
		self._Label_VoltageUnitNew.Name = "Label_VoltageUnitNew"
		self._Label_VoltageUnitNew.Size = System.Drawing.Size(94, 28)
		self._Label_VoltageUnitNew.TabIndex = 29
		self._Label_VoltageUnitNew.Text = "* Voltage : [mV]"
		self._Label_VoltageUnitNew.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_AC_DQ
		# 
		self._Label_AC_DQ.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_AC_DQ.Location = System.Drawing.Point(45, 169)
		self._Label_AC_DQ.Name = "Label_AC_DQ"
		self._Label_AC_DQ.Size = System.Drawing.Size(40, 28)
		self._Label_AC_DQ.TabIndex = 40
		self._Label_AC_DQ.Text = "DQ :"
		self._Label_AC_DQ.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_AC_ADDR
		# 
		self._Label_AC_ADDR.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_AC_ADDR.Location = System.Drawing.Point(11, 195)
		self._Label_AC_ADDR.Name = "Label_AC_ADDR"
		self._Label_AC_ADDR.Size = System.Drawing.Size(74, 28)
		self._Label_AC_ADDR.TabIndex = 41
		self._Label_AC_ADDR.Text = "Address :"
		self._Label_AC_ADDR.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_DC_ADDR
		# 
		self._Label_DC_ADDR.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_DC_ADDR.Location = System.Drawing.Point(487, 246)
		self._Label_DC_ADDR.Name = "Label_DC_ADDR"
		self._Label_DC_ADDR.Size = System.Drawing.Size(63, 20)
		self._Label_DC_ADDR.TabIndex = 44
		self._Label_DC_ADDR.Text = "Address :"
		self._Label_DC_ADDR.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_DC_DQ
		# 
		self._Label_DC_DQ.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_DC_DQ.Location = System.Drawing.Point(511, 216)
		self._Label_DC_DQ.Name = "Label_DC_DQ"
		self._Label_DC_DQ.Size = System.Drawing.Size(40, 28)
		self._Label_DC_DQ.TabIndex = 43
		self._Label_DC_DQ.Text = "DQ :"
		self._Label_DC_DQ.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_Info
		# 
		self._Label_Info.Font = System.Drawing.Font("Arial", 9)
		self._Label_Info.Location = System.Drawing.Point(10, 423)
		self._Label_Info.Name = "Label_Info"
		self._Label_Info.Size = System.Drawing.Size(460, 26)
		self._Label_Info.TabIndex = 41
		self._Label_Info.Text = "* Vcent_DQ will be automatically calculated after Target Net Setup.\n* To use manual values, check \"Edit enable\" and enter the values."
		self._Label_Info.Visible = False
		self._Label_Info.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_VdIVW
		# 
		self._Label_VdIVW.Font = System.Drawing.Font("Arial", 10)
		self._Label_VdIVW.Location = System.Drawing.Point(170, 26)
		self._Label_VdIVW.Name = "Label_VdIVW"
		self._Label_VdIVW.Size = System.Drawing.Size(55, 26)
		self._Label_VdIVW.TabIndex = 41
		self._Label_VdIVW.Text = "VdIVW :"
		self._Label_VdIVW.Visible = False
		self._Label_VdIVW.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_TdIVW
		# 
		self._Label_TdIVW.Font = System.Drawing.Font("Arial", 10)
		self._Label_TdIVW.Location = System.Drawing.Point(310, 26)
		self._Label_TdIVW.Name = "Label_TdIVW"
		self._Label_TdIVW.Size = System.Drawing.Size(55, 26)
		self._Label_TdIVW.TabIndex = 41
		self._Label_TdIVW.Text = "TdIVW :"
		self._Label_TdIVW.Visible = False
		self._Label_TdIVW.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_TimingSpec
		# 
		self._Label_TimingSpec.Font = System.Drawing.Font("Arial", 8)
		self._Label_TimingSpec.Location = System.Drawing.Point(298, 285)
		self._Label_TimingSpec.Name = "Label_Timing_Spec"
		self._Label_TimingSpec.Size = System.Drawing.Size(88, 16)
		self._Label_TimingSpec.TabIndex = 41
		self._Label_TimingSpec.Text = "Timing Spec.[UI]"
		self._Label_TimingSpec.Visible = True
		self._Label_TimingSpec.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_VoltageSpec
		# 
		self._Label_VoltageSpec.Font = System.Drawing.Font("Arial", 8)
		self._Label_VoltageSpec.Location = System.Drawing.Point(60, 261)
		self._Label_VoltageSpec.Name = "Label_Voltage_Spec"
		self._Label_VoltageSpec.Size = System.Drawing.Size(97, 16)
		self._Label_VoltageSpec.TabIndex = 41
		self._Label_VoltageSpec.Text = "Voltage Spec.[mV]"
		self._Label_VoltageSpec.Visible = True
		self._Label_VoltageSpec.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_VcentDQ
		# 
		self._Label_VcentDQ.Font = System.Drawing.Font("Arial", 10)
		self._Label_VcentDQ.Location = System.Drawing.Point(450, 26)
		self._Label_VcentDQ.Name = "Label_VcentDQ"
		self._Label_VcentDQ.Size = System.Drawing.Size(76, 26)
		self._Label_VcentDQ.TabIndex = 41
		self._Label_VcentDQ.Text = "Vcent_DQ :"
		self._Label_VcentDQ.Visible = False
		self._Label_VcentDQ.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_Vac
		# 
		self._Label_Vac.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Bold)
		self._Label_Vac.Location = System.Drawing.Point(210, 9)
		self._Label_Vac.Name = "Label_Vac"
		self._Label_Vac.Size = System.Drawing.Size(35, 20)
		self._Label_Vac.TabIndex = 41
		self._Label_Vac.Text = "Vac"
		self._Label_Vac.Visible = False
		self._Label_Vac.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_Vdc
		# 
		self._Label_Vdc.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Bold)
		self._Label_Vdc.Location = System.Drawing.Point(300, 9)
		self._Label_Vdc.Name = "Label_Vdc"
		self._Label_Vdc.Size = System.Drawing.Size(35, 20)
		self._Label_Vdc.TabIndex = 41
		self._Label_Vdc.Text = "Vdc"
		self._Label_Vdc.Visible = False
		self._Label_Vdc.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_Setup
		# 
		self._Label_Setup.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Bold)
		self._Label_Setup.Location = System.Drawing.Point(380, 9)
		self._Label_Setup.Name = "Label_Setup"
		self._Label_Setup.Size = System.Drawing.Size(55, 20)
		self._Label_Setup.TabIndex = 41
		self._Label_Setup.Text = "Setup"
		self._Label_Setup.Visible = False
		self._Label_Setup.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_Hold
		# 
		self._Label_Hold.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Bold)
		self._Label_Hold.Location = System.Drawing.Point(470, 9)
		self._Label_Hold.Name = "Label_Hold"
		self._Label_Hold.Size = System.Drawing.Size(55, 20)
		self._Label_Hold.TabIndex = 41
		self._Label_Hold.Text = "Hold"
		self._Label_Hold.Visible = False
		self._Label_Hold.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_Vref
		# 
		self._Label_Vref.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Bold)
		self._Label_Vref.Location = System.Drawing.Point(560, 9)
		self._Label_Vref.Name = "Label_Vref"
		self._Label_Vref.Size = System.Drawing.Size(55, 20)
		self._Label_Vref.TabIndex = 41
		self._Label_Vref.Text = "Vref"
		self._Label_Vref.Visible = False
		self._Label_Vref.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_dq
		# 
		self._Label_dq.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Bold)
		self._Label_dq.Location = System.Drawing.Point(120, 31)
		self._Label_dq.Name = "Label_dq"
		self._Label_dq.Size = System.Drawing.Size(55, 26)
		self._Label_dq.TabIndex = 41
		self._Label_dq.Text = "DQ"
		self._Label_dq.Visible = False
		self._Label_dq.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_addr
		# 
		self._Label_addr.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Bold)
		self._Label_addr.Location = System.Drawing.Point(120, 61)
		self._Label_addr.Name = "Label_dq"
		self._Label_addr.Size = System.Drawing.Size(60, 26)
		self._Label_addr.TabIndex = 41
		self._Label_addr.Text = "Address"
		self._Label_addr.Visible = False
		self._Label_addr.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# H_Border_1
		# 
		self._H_Border_1.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
		self._H_Border_1.Location = System.Drawing.Point(120, 29)
		self._H_Border_1.Name = "H_Border_1"
		self._H_Border_1.Size = System.Drawing.Size(504, 2)
		self._H_Border_1.Visible = False
		self._H_Border_1.TabIndex = 18
		# 
		# H_Border_2
		# 
		self._H_Border_2.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
		self._H_Border_2.Location = System.Drawing.Point(120, 58)
		self._H_Border_2.Name = "H_Border_2"
		self._H_Border_2.Size = System.Drawing.Size(414, 2)
		self._H_Border_2.Visible = False
		self._H_Border_2.TabIndex = 18
		# 
		# H_Border_3
		# 
		self._H_Border_3.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
		self._H_Border_3.Location = System.Drawing.Point(120, 87)
		self._H_Border_3.Name = "H_Border_3"
		self._H_Border_3.Size = System.Drawing.Size(505, 2)
		self._H_Border_3.Visible = False
		self._H_Border_3.TabIndex = 18
		# 
		# V_Border_0
		# 
		self._V_Border_0.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
		self._V_Border_0.Location = System.Drawing.Point(118, 8)
		self._V_Border_0.Name = "V_Border_0"
		self._V_Border_0.Size = System.Drawing.Size(2, 80)
		self._V_Border_0.Visible = False
		self._V_Border_0.TabIndex = 165		
		# 
		# V_Border_1
		# 
		self._V_Border_1.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
		self._V_Border_1.Location = System.Drawing.Point(180, 8)
		self._V_Border_1.Name = "V_Border_1"
		self._V_Border_1.Size = System.Drawing.Size(2, 80)
		self._V_Border_1.Visible = False
		self._V_Border_1.TabIndex = 165
		# 
		# V_Border_2
		# 
		self._V_Border_2.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
		self._V_Border_2.Location = System.Drawing.Point(268, 8)
		self._V_Border_2.Name = "V_Border_2"
		self._V_Border_2.Size = System.Drawing.Size(2, 80)
		self._V_Border_2.Visible = False
		self._V_Border_2.TabIndex = 165
		# 
		# V_Border_3
		# 
		self._V_Border_3.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
		self._V_Border_3.Location = System.Drawing.Point(356, 8)
		self._V_Border_3.Name = "V_Border_3"
		self._V_Border_3.Size = System.Drawing.Size(2, 80)
		self._V_Border_3.Visible = False
		self._V_Border_3.TabIndex = 165
		# 
		# V_Border_4
		# 
		self._V_Border_4.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
		self._V_Border_4.Location = System.Drawing.Point(444, 8)
		self._V_Border_4.Name = "V_Border_4"
		self._V_Border_4.Size = System.Drawing.Size(2, 80)
		self._V_Border_4.Visible = False
		self._V_Border_4.TabIndex = 165
		# 
		# V_Border_5
		# 
		self._V_Border_5.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
		self._V_Border_5.Location = System.Drawing.Point(532, 8)
		self._V_Border_5.Name = "V_Border_5"
		self._V_Border_5.Size = System.Drawing.Size(2, 80)
		self._V_Border_5.Visible = False
		self._V_Border_5.TabIndex = 165
		# 
		# V_Border_6
		# 
		self._V_Border_6.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
		self._V_Border_6.Location = System.Drawing.Point(624, 8)
		self._V_Border_6.Name = "V_Border_6"
		self._V_Border_6.Size = System.Drawing.Size(2, 80)
		self._V_Border_6.Visible = False
		self._V_Border_6.TabIndex = 165
		# 
		# CheckedListBox_ReportName
		# 
		self._CheckedListBox_ReportName.FormattingEnabled = True
		self._CheckedListBox_ReportName.Font = System.Drawing.Font("Arial", 9)
		self._CheckedListBox_ReportName.Location = System.Drawing.Point(377, 50)
		self._CheckedListBox_ReportName.Name = "CheckedListBox_ReportName"
		self._CheckedListBox_ReportName.Size = System.Drawing.Size(198, 52)
		self._CheckedListBox_ReportName.TabIndex = 31		
		self._CheckedListBox_ReportName.ItemCheck += self.CheckedListBox_ReportNameItemCheck
		# 
		# ComboBox_DDRGen
		# 
		self._ComboBox_DDRGen.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._ComboBox_DDRGen.FormattingEnabled = True
		self._ComboBox_DDRGen.Location = System.Drawing.Point(120, 106)
		self._ComboBox_DDRGen.Name = "ComboBox_DDRGen"
		self._ComboBox_DDRGen.Size = System.Drawing.Size(150, 24)
		self._ComboBox_DDRGen.TabIndex = 14
		self._ComboBox_DDRGen.Enabled = False
		self._ComboBox_DDRGen.SelectedIndexChanged += self.ComboBox_DDRGenSelectedIndexChanged
		# 
		# ComboBox_DataRate
		# 
		self._ComboBox_DataRate.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._ComboBox_DataRate.FormattingEnabled = True
		self._ComboBox_DataRate.Location = System.Drawing.Point(377, 106)
		self._ComboBox_DataRate.Name = "ComboBox_DataRate"
		self._ComboBox_DataRate.Size = System.Drawing.Size(60, 24)
		self._ComboBox_DataRate.TabIndex = 20
		self._ComboBox_DataRate.Enabled = False
		self._ComboBox_DataRate.SelectedIndexChanged += self.ComboBox_DataRateSelectedIndexChanged		
		# 
		# ComboBox_SolutionName
		# 
		self._ComboBox_SolutionName.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._ComboBox_SolutionName.FormattingEnabled = True
		self._ComboBox_SolutionName.Location = System.Drawing.Point(120, 78)
		self._ComboBox_SolutionName.Name = "ComboBox_SolutionName"
		self._ComboBox_SolutionName.Size = System.Drawing.Size(150, 24)
		self._ComboBox_SolutionName.TabIndex = 27
		self._ComboBox_SolutionName.SelectedIndexChanged += self.ComboBox_SolutionNameSelectedIndexChanged

		self._ComboBox_SolutionName_ToopTip
		# 
		# ComboBox_Design
		# 
		self._ComboBox_Design.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._ComboBox_Design.FormattingEnabled = True		
		self._ComboBox_Design.Location = System.Drawing.Point(120, 50)
		self._ComboBox_Design.Name = "ComboBox_Design"
		self._ComboBox_Design.Size = System.Drawing.Size(150, 24)
		self._ComboBox_Design.TabIndex = 28		
		self._ComboBox_Design.SelectedIndexChanged += self.ComboBox_DesignSelectedIndexChanged
		# 
		# ComboBox_AEDT
		# 
		self._ComboBox_AEDT.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._ComboBox_AEDT.FormattingEnabled = True
		self._ComboBox_AEDT.Location = System.Drawing.Point(120, 22)
		self._ComboBox_AEDT.Name = "ComboBox_AEDT"
		self._ComboBox_AEDT.Size = System.Drawing.Size(80, 24)
		self._ComboBox_AEDT.TabIndex = 14
		self._ComboBox_AEDT.Text = 'Default'
		self._ComboBox_AEDT.Items.Add('2022 R2')
		self._ComboBox_AEDT.Items.Add('2022 R1')
		self._ComboBox_AEDT.Items.Add('2021 R2')
		self._ComboBox_AEDT.Items.Add('2021 R1')
		self._ComboBox_AEDT.Items.Add('2020 R2')
		self._ComboBox_AEDT.Items.Add('2020 R1')
		# 
		# ComboBox_AC_DQ
		# 
		self._ComboBox_AC_DQ.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._ComboBox_AC_DQ.FormattingEnabled = True
		self._ComboBox_AC_DQ.Location = System.Drawing.Point(88, 173)		
		self._ComboBox_AC_DQ.Name = "ComboBox_AC_DQ"
		self._ComboBox_AC_DQ.Size = System.Drawing.Size(73, 24)		
		self._ComboBox_AC_DQ.TabIndex = 46
		self._ComboBox_AC_DQ.Visible = True
		self._ComboBox_AC_DQ.SelectedIndexChanged += self.ComboBox_AC_DQSelectedIndexChanged
		# 
		# ComboBox_AC_ADDR
		# 
		self._ComboBox_AC_ADDR.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._ComboBox_AC_ADDR.FormattingEnabled = True
		self._ComboBox_AC_ADDR.Location = System.Drawing.Point(88, 200)		
		self._ComboBox_AC_ADDR.Name = "ComboBox_AC_ADDR"
		self._ComboBox_AC_ADDR.Size = System.Drawing.Size(73, 24)		
		self._ComboBox_AC_ADDR.TabIndex = 48
		self._ComboBox_AC_ADDR.Visible = True		
		self._ComboBox_AC_ADDR.SelectedIndexChanged += self.ComboBox_AC_ADDRSelectedIndexChanged
		# 
		# TextBox_InputFile
		# 
		self._TextBox_InputFile.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_InputFile.Location = System.Drawing.Point(204, 22)
		self._TextBox_InputFile.Name = "TextBox_InputFile"
		self._TextBox_InputFile.Size = System.Drawing.Size(330, 23)
		self._TextBox_InputFile.TabIndex = 13
		# 
		# TextBox_Offset
		# 
		self._TextBox_Offset.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_Offset.Location = System.Drawing.Point(498, 106)
		self._TextBox_Offset.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
		self._TextBox_Offset.Name = "TextBox_InputFile"
		self._TextBox_Offset.Size = System.Drawing.Size(60, 23)
		self._TextBox_Offset.Text = "5"
		self._TextBox_Offset.TabIndex = 50
		self._TextBox_Offset.TextChanged += self.TextBox_OffsetTextChanged
		# 
		# TextBox_AC_DQ
		#
		self._TextBox_AC_DQ.BackColor = System.Drawing.Color.WhiteSmoke
		self._TextBox_AC_DQ.ReadOnly = True
		self._TextBox_AC_DQ.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_AC_DQ.Location = System.Drawing.Point(88, 173)		
		self._TextBox_AC_DQ.Name = "TextBox_AC_DQ"
		self._TextBox_AC_DQ.Size = System.Drawing.Size(71, 23)
		self._TextBox_AC_DQ.Visible = False
		self._TextBox_AC_DQ.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
		self._TextBox_AC_DQ.TabIndex = 27
		# 
		# TextBox_AC_ADDR
		# 
		self._TextBox_AC_ADDR.BackColor = System.Drawing.Color.WhiteSmoke
		self._TextBox_AC_ADDR.ReadOnly = True
		self._TextBox_AC_ADDR.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_AC_ADDR.Location = System.Drawing.Point(88, 200)		
		self._TextBox_AC_ADDR.Name = "TextBox_AC_ADDR"
		self._TextBox_AC_ADDR.Size = System.Drawing.Size(71, 23)		
		self._TextBox_AC_ADDR.Visible = False
		self._TextBox_AC_ADDR.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
		self._TextBox_AC_ADDR.TabIndex = 39
		# 
		# TextBox_DC_DQ
		# 
		self._TextBox_DC_DQ.BackColor = System.Drawing.Color.WhiteSmoke
		self._TextBox_DC_DQ.ReadOnly = True
		self._TextBox_DC_DQ.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_DC_DQ.Location = System.Drawing.Point(553, 219)
		self._TextBox_DC_DQ.Name = "TextBox_DC_DQ"
		self._TextBox_DC_DQ.Size = System.Drawing.Size(71, 23)		
		self._TextBox_DC_DQ.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
		self._TextBox_DC_DQ.TabIndex = 33
		# 
		# TextBox_DC_ADDR
		# 
		self._TextBox_DC_ADDR.BackColor = System.Drawing.Color.WhiteSmoke
		self._TextBox_DC_ADDR.ReadOnly = True
		self._TextBox_DC_ADDR.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_DC_ADDR.Location = System.Drawing.Point(553, 246)		
		self._TextBox_DC_ADDR.Name = "TextBox_DC_ADDR"
		self._TextBox_DC_ADDR.Size = System.Drawing.Size(71, 23)		
		self._TextBox_DC_ADDR.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
		self._TextBox_DC_ADDR.TabIndex = 42
		# 
		# TextBox_Vref
		# 
		self._TextBox_Vref.BackColor = System.Drawing.Color.WhiteSmoke
		self._TextBox_Vref.ReadOnly = True
		self._TextBox_Vref.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_Vref.Location = System.Drawing.Point(130, 232)		
		self._TextBox_Vref.Name = "TextBox_Vref"
		self._TextBox_Vref.Size = System.Drawing.Size(52, 23)		
		self._TextBox_Vref.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
		self._TextBox_Vref.TextChanged += self.TextBox_VrefTextChanged
		self._TextBox_Vref.TabIndex = 34		
		# 
		# TextBox_DQSetup
		# 
		self._TextBox_DQSetup.BackColor = System.Drawing.Color.WhiteSmoke
		self._TextBox_DQSetup.ReadOnly = True
		self._TextBox_DQSetup.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_DQSetup.Location = System.Drawing.Point(299, 398)		
		self._TextBox_DQSetup.Name = "TextBox_DQSetup"
		self._TextBox_DQSetup.Size = System.Drawing.Size(45, 23)
		self._TextBox_DQSetup.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
		self._TextBox_DQSetup.TabIndex = 28
		# 
		# TextBox_DQHold
		# 
		self._TextBox_DQHold.BackColor = System.Drawing.Color.WhiteSmoke
		self._TextBox_DQHold.ReadOnly = True
		self._TextBox_DQHold.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_DQHold.Location = System.Drawing.Point(347, 398)		
		self._TextBox_DQHold.Name = "TextBox_DQHold"
		self._TextBox_DQHold.Size = System.Drawing.Size(56, 23)		
		self._TextBox_DQHold.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
		self._TextBox_DQHold.TabIndex = 29
		# 
		# TextBox_ADDRSetup
		# 
		self._TextBox_ADDRSetup.BackColor = System.Drawing.Color.WhiteSmoke
		self._TextBox_ADDRSetup.ReadOnly = True
		self._TextBox_ADDRSetup.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_ADDRSetup.Location = System.Drawing.Point(299, 425)
		self._TextBox_ADDRSetup.Name = "TextBox_ADDRSetup"
		self._TextBox_ADDRSetup.Size = System.Drawing.Size(45, 23)
		self._TextBox_ADDRSetup.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
		self._TextBox_ADDRSetup.TabIndex = 30
		# 
		# TextBox_ADDRHold
		# 
		self._TextBox_ADDRHold.BackColor = System.Drawing.Color.WhiteSmoke
		self._TextBox_ADDRHold.ReadOnly = True
		self._TextBox_ADDRHold.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_ADDRHold.Location = System.Drawing.Point(347, 425)		
		self._TextBox_ADDRHold.Name = "TextBox_ADDRHold"
		self._TextBox_ADDRHold.Size = System.Drawing.Size(56, 23)		
		self._TextBox_ADDRHold.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
		self._TextBox_ADDRHold.TabIndex = 31
		# 
		# TextBox_VdIVW
		# 
		self._TextBox_VdIVW.BackColor = System.Drawing.Color.WhiteSmoke
		self._TextBox_VdIVW.ReadOnly = True
		self._TextBox_VdIVW.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_VdIVW.Location = System.Drawing.Point(97, 238)
		self._TextBox_VdIVW.Name = "TextBox_VdIVW"
		self._TextBox_VdIVW.Size = System.Drawing.Size(59, 23)
		self._TextBox_VdIVW.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
		self._TextBox_VdIVW.TabIndex = 27
		# 
		# TextBox_TdIVW
		# 
		self._TextBox_TdIVW.BackColor = System.Drawing.Color.WhiteSmoke
		self._TextBox_TdIVW.ReadOnly = True
		self._TextBox_TdIVW.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_TdIVW.Location = System.Drawing.Point(333, 303)		
		self._TextBox_TdIVW.Name = "TextBox_TdIVW"
		self._TextBox_TdIVW.Size = System.Drawing.Size(52, 23)
		self._TextBox_TdIVW.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
		self._TextBox_TdIVW.TabIndex = 39
		# 
		# TextBox_VcentDQ
		# 
		self._TextBox_VcentDQ.BackColor = System.Drawing.Color.WhiteSmoke
		self._TextBox_VcentDQ.ReadOnly = True
		self._TextBox_VcentDQ.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_VcentDQ.Location = System.Drawing.Point(548, 231)		
		self._TextBox_VcentDQ.Name = "TextBox_VcentDQ"
		self._TextBox_VcentDQ.Size = System.Drawing.Size(59, 23)
		self._TextBox_VcentDQ.Text = "Auto"			
		self._TextBox_VcentDQ.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
		self._TextBox_VcentDQ.TextChanged += self.TextBox_VcentDQTextChanged
		self._TextBox_VcentDQ.TabIndex = 34
		# 
		# Button_Import
		# 
		self._Button_Import.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_Import.Location = System.Drawing.Point(539, 22)
		self._Button_Import.Name = "Button_Import"
		self._Button_Import.Size = System.Drawing.Size(36, 23)
		self._Button_Import.TabIndex = 19
		self._Button_Import.Text = "..."
		self._Button_Import.UseVisualStyleBackColor = True
		self._Button_Import.Click += self.Button_ImportClick
		# 
		# Button_ViewNet
		# 
		self._Button_ViewNet.Font = System.Drawing.Font("Arial", 11)
		self._Button_ViewNet.Location = System.Drawing.Point(595, 64)
		self._Button_ViewNet.Name = "Button_ViewNet"
		self._Button_ViewNet.Size = System.Drawing.Size(100, 37)
		self._Button_ViewNet.TabIndex = 27
		self._Button_ViewNet.Text = "Net Setup"
		self._Button_ViewNet.UseVisualStyleBackColor = True
		self._Button_ViewNet.Enabled = True
		self._Button_ViewNet.Click += self.Button_ViewNetClick		
		# 
		# Button_Analyze
		# 
		self._Button_Analyze.Font = System.Drawing.Font("Arial", 12, System.Drawing.FontStyle.Bold)
		self._Button_Analyze.Location = System.Drawing.Point(595, 110)
		self._Button_Analyze.Name = "Button_Analyze"
		self._Button_Analyze.Size = System.Drawing.Size(100, 37)
		self._Button_Analyze.TabIndex = 35
		self._Button_Analyze.Text = "Analyze"
		self._Button_Analyze.UseVisualStyleBackColor = True
		self._Button_Analyze.Enabled = False
		self._Button_Analyze.Click += self.Button_AnalyzeClick
		# 
		# Button_ViewResult
		# 
		self._Button_ViewResult.Font = System.Drawing.Font("Arial", 12, System.Drawing.FontStyle.Bold)
		self._Button_ViewResult.Location = System.Drawing.Point(595, 156)
		self._Button_ViewResult.Name = "Button_ViewResult"
		self._Button_ViewResult.Size = System.Drawing.Size(100, 37)
		self._Button_ViewResult.TabIndex = 35
		self._Button_ViewResult.Text = "Result"
		self._Button_ViewResult.UseVisualStyleBackColor = True
		self._Button_ViewResult.Enabled = False
		self._Button_ViewResult.Click += self.Button_ViewResultClick
		# 
		# Button_ImgShow_New
		#
		self._Button_ImgShow_New.FlatStyle = System.Windows.Forms.FlatStyle.Standard
		self._Button_ImgShow_New.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_ImgShow_New.Location = System.Drawing.Point(629, 8)
		self._Button_ImgShow_New.Name = "Button_ImgShow_New"
		self._Button_ImgShow_New.Size = System.Drawing.Size(60, 28)
		self._Button_ImgShow_New.TabIndex = 43
		self._Button_ImgShow_New.Text = 'Hide'
		self._Button_ImgShow_New.UseVisualStyleBackColor = True
		self._Button_ImgShow_New.Click += self.Button_ImgShow_NewClick
		# 
		# Button_ImgShow_Old
		#
		self._Button_ImgShow_Old.FlatStyle = System.Windows.Forms.FlatStyle.Standard
		self._Button_ImgShow_Old.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_ImgShow_Old.Location = System.Drawing.Point(629, 8)
		self._Button_ImgShow_Old.Name = "Button_ImgShow_Old"
		self._Button_ImgShow_Old.Size = System.Drawing.Size(60, 28)
		self._Button_ImgShow_Old.TabIndex = 43
		self._Button_ImgShow_Old.Text = 'Hide'
		self._Button_ImgShow_Old.UseVisualStyleBackColor = True
		self._Button_ImgShow_Old.Click += self.Button_ImgShow_OldClick
		# 
		# Button_Add_New
		#
		self._Button_Add_New.FlatStyle = System.Windows.Forms.FlatStyle.Standard
		self._Button_Add_New.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_Add_New.Location = System.Drawing.Point(629, 36)
		self._Button_Add_New.Name = "Button_Add_New"
		self._Button_Add_New.Size = System.Drawing.Size(60, 28)
		self._Button_Add_New.TabIndex = 43
		self._Button_Add_New.Text = 'Add'
		self._Button_Add_New.UseVisualStyleBackColor = True
		self._Button_Add_New.Visible = False
		#self._Button_Add_New.Click += self.Button_Add_NewClick
		# 
		# Button_Add_Old
		#
		self._Button_Add_Old.FlatStyle = System.Windows.Forms.FlatStyle.Standard
		self._Button_Add_Old.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_Add_Old.Location = System.Drawing.Point(629, 36)
		self._Button_Add_Old.Name = "Button_Add_Old"
		self._Button_Add_Old.Size = System.Drawing.Size(60, 28)
		self._Button_Add_Old.TabIndex = 43
		self._Button_Add_Old.Text = 'Add'
		self._Button_Add_Old.UseVisualStyleBackColor = True
		self._Button_Add_Old.Visible = False
		#self._Button_Add_Old.Click += self.Button_Old_NewClick
		# 
		# Button_LoadCnf
		#
		self._Button_LoadCnf.FlatStyle = System.Windows.Forms.FlatStyle.Standard
		self._Button_LoadCnf.Font = System.Drawing.Font("Arial", 8, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_LoadCnf.Location = System.Drawing.Point(595, 5)
		self._Button_LoadCnf.Name = "Button_LoadCnf"
		self._Button_LoadCnf.Size = System.Drawing.Size(100, 20)
		self._Button_LoadCnf.TabIndex = 43
		self._Button_LoadCnf.Text = 'Load Latest Cnf'
		self._Button_LoadCnf.UseVisualStyleBackColor = True
		self._Button_LoadCnf.Visible = False
		self._Button_LoadCnf.Click += self.Button_LoadCnfClick
		# 
		# Button_Debug
		# 
		self._Button_Debug.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_Debug.Location = System.Drawing.Point(530, 1)
		self._Button_Debug.Name = "Button_Debug"
		self._Button_Debug.Size = System.Drawing.Size(80, 25)
		self._Button_Debug.TabIndex = 29
		self._Button_Debug.Text = "Debug"
		self._Button_Debug.UseVisualStyleBackColor = True
		self._Button_Debug.Visible = False
		self._Button_Debug.Click += self.Button_DebugClick		
		# 
		# CheckBox_Debug
		# 
		self._CheckBox_Debug.Font = System.Drawing.Font("Arial", 10)
		self._CheckBox_Debug.Location = System.Drawing.Point(620, 1)
		self._CheckBox_Debug.Name = "CheckBox_AnalyzeDQ"
		self._CheckBox_Debug.Size = System.Drawing.Size(138, 29)
		self._CheckBox_Debug.TabIndex = 36
		self._CheckBox_Debug.Text = "Debug"
		self._CheckBox_Debug.Visible = sub_DB.Debug_Mode
		self._CheckBox_Debug.UseVisualStyleBackColor = True
		self._CheckBox_Debug.CheckedChanged += self.CheckBox_DebugCheckedChanged
		# 
		# CheckBox_VcentDQ
		# 
		self._CheckBox_VcentDQ.Font = System.Drawing.Font("Arial", 9)
		self._CheckBox_VcentDQ.Location = System.Drawing.Point(548, 254)
		self._CheckBox_VcentDQ.Name = "CheckBox_VcentDQ"
		self._CheckBox_VcentDQ.Size = System.Drawing.Size(110, 18)
		self._CheckBox_VcentDQ.TabIndex = 36
		self._CheckBox_VcentDQ.Text = "Auto VcentDQ"
		self._CheckBox_VcentDQ.Visible = True
		self._CheckBox_VcentDQ.Checked = True
		self._CheckBox_VcentDQ.UseVisualStyleBackColor = True
		self._CheckBox_VcentDQ.CheckedChanged += self.CheckBox_VcentDQCheckedChanged
		# 
		# CheckBox_Vref
		# 
		self._CheckBox_Vref.Font = System.Drawing.Font("Arial", 9)
		self._CheckBox_Vref.Location = System.Drawing.Point(103, 254)		
		self._CheckBox_Vref.Name = "CheckBox_Vref"
		self._CheckBox_Vref.Size = System.Drawing.Size(75, 18)
		self._CheckBox_Vref.TabIndex = 36
		self._CheckBox_Vref.Text = "Auto Vref"
		self._CheckBox_Vref.Visible = True
		self._CheckBox_Vref.Checked = True
		self._CheckBox_Vref.UseVisualStyleBackColor = True
		self._CheckBox_Vref.CheckedChanged += self.CheckBox_VrefCheckedChanged
		# 
		# CheckBox_AnalyzeDQ
		# 
		self._CheckBox_AnalyzeDQ.Font = System.Drawing.Font("Arial", 10)
		self._CheckBox_AnalyzeDQ.Location = System.Drawing.Point(552, 19)
		self._CheckBox_AnalyzeDQ.Name = "CheckBox_AnalyzeDQ"
		self._CheckBox_AnalyzeDQ.Size = System.Drawing.Size(138, 29)
		self._CheckBox_AnalyzeDQ.TabIndex = 36
		self._CheckBox_AnalyzeDQ.Text = "Analyze DQ"
		self._CheckBox_AnalyzeDQ.Visible = False
		self._CheckBox_AnalyzeDQ.UseVisualStyleBackColor = True
		# 
		# CheckBox_AnalyzeADDR
		# 
		self._CheckBox_AnalyzeADDR.Font = System.Drawing.Font("Arial", 10)
		self._CheckBox_AnalyzeADDR.Location = System.Drawing.Point(552, 45)
		self._CheckBox_AnalyzeADDR.Name = "CheckBox_AnalyzeADDR"
		self._CheckBox_AnalyzeADDR.Size = System.Drawing.Size(138, 29)
		self._CheckBox_AnalyzeADDR.TabIndex = 37
		self._CheckBox_AnalyzeADDR.Text = "Analyze Address"
		self._CheckBox_AnalyzeADDR.Visible = False
		self._CheckBox_AnalyzeADDR.UseVisualStyleBackColor = True
		# 
		# CheckBox_EditEnable_NewEye
		# 
		self._CheckBox_EditEnable_NewEye.Font = System.Drawing.Font("Arial", 10)
		self._CheckBox_EditEnable_NewEye.Location = System.Drawing.Point(590, 423)
		self._CheckBox_EditEnable_NewEye.Name = "CheckBox_EditEnable_NewEye"
		self._CheckBox_EditEnable_NewEye.Size = System.Drawing.Size(93, 29)
		self._CheckBox_EditEnable_NewEye.TabIndex = 40
		self._CheckBox_EditEnable_NewEye.Text = "Edit enable"
		self._CheckBox_EditEnable_NewEye.UseVisualStyleBackColor = True
		self._CheckBox_EditEnable_NewEye.Visible = False
		self._CheckBox_EditEnable_NewEye.CheckedChanged += self.CheckBox_EditEnable_NewEyeCheckedChanged
		# 
		# CheckBox_EditEnable_OldEye
		# 
		self._CheckBox_EditEnable_OldEye.Font = System.Drawing.Font("Arial", 10)
		self._CheckBox_EditEnable_OldEye.Location = System.Drawing.Point(590, 423)		
		self._CheckBox_EditEnable_OldEye.Name = "CheckBox_EditEnable_OldEye"
		self._CheckBox_EditEnable_OldEye.Size = System.Drawing.Size(95, 29)
		self._CheckBox_EditEnable_OldEye.TabIndex = 40
		self._CheckBox_EditEnable_OldEye.Text = "Edit enable"
		self._CheckBox_EditEnable_OldEye.UseVisualStyleBackColor = True		
		self._CheckBox_EditEnable_OldEye.Visible = False
		self._CheckBox_EditEnable_OldEye.CheckedChanged += self.CheckBox_EditEnable_OldEyeCheckedChanged
		# 
		# openFileDialog1
		# 
		self._openFileDialog1.FileName = "openFileDialog1"
		# 
		# Eye_Form
		# 
		self.ClientSize = System.Drawing.Size(700, 657)
		self.MinimumSize = System.Drawing.Size(self.Size.Width, self.Size.Height)
		self.FormSize_W = self.Size.Width
		self.FormSize_H = self.Size.Height
		self.Image_flag_New = False
		self.Image_flag_Old = False
		self.Full_Size_flag = True
		self.Init_Flag = True		
		self.Controls.Add(self._toolStrip1)
		self.Controls.Add(self._CheckBox_Debug)
		self.Controls.Add(self._Button_LoadCnf)
		self.Controls.Add(self._Button_Debug)
		self.Controls.Add(self._GroupBox_NewEye)
		self.Controls.Add(self._Button_Analyze)
		self.Controls.Add(self._Button_ViewNet)
		self.Controls.Add(self._Button_ViewResult)
		self.Controls.Add(self._GroupBox_OldEye)
		self.Controls.Add(self._Label_Version)
		self.Controls.Add(self._GroupBox_Setup)
		
		self.Controls.Add(self._MenuStrip)
		self.MainMenuStrip = self._MenuStrip
		IconFile = path + "\\Resources\\fig\\LOGO.ico"
		self.Icon = Icon(IconFile)
		self.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen		
		self.Name = "Eye_Form"
		self.Text = sub_DB.Title[0]
		self.Load += self.Eye_FormLoad
		self.ResizeEnd += self.Eye_FormResizeEnd		
		self.FormClosing += self.Eye_FormFormClosing
		self.KeyPreview = True
		self.KeyPress += self.Eye_FormKeyPress
		self._MenuStrip.ResumeLayout(False)
		self._MenuStrip.PerformLayout()
		self._GroupBox_Setup.ResumeLayout(False)
		self._GroupBox_Setup.PerformLayout()		
		self._GroupBox_OldEye.ResumeLayout(False)
		self._GroupBox_OldEye.PerformLayout()
		self._PictureBox_OldEye.EndInit()
		self._GroupBox_UnitOld.ResumeLayout(False)
		self._GroupBox_NewEye.ResumeLayout(False)
		self._GroupBox_NewEye.PerformLayout()
		self._GroupBox_UnitNew.ResumeLayout(False)
		self._toolStrip1.ResumeLayout(False)
		self._toolStrip1.PerformLayout()
		self._PictureBox_NewEye.EndInit()
		self.ResumeLayout(False)

	''' Eye_Form - Events '''
	def Eye_FormLoad(self, sender, e):
		try:			
			# initialization
			self._TextBox_InputFile.BackColor = System.Drawing.SystemColors.Info
			self._TextBox_Offset.Text = "7.5"

			# Setup the Common Env. Info.		
			#	Add DDR Type into ComboBox
			DDR_Gen = []
			for key in sub_DB.Cenv:
				if "[DDR Info]" in key:
					DDR_Gen.append(key.split("<")[-1].split(">")[0])

			DDR_Gen.sort()
			for ddr in DDR_Gen:
				self._ComboBox_DDRGen.Items.Add(ddr)

			if os.path.isfile(sub_DB.user_dir + r'\latest.cnf'):				
				CnfAutoLoad(self)
				sub_DB.AutoLoad_flag = True

			# Setup the User Env. Info.
			if "(Input File)<Setup>[EYE]" in sub_DB.Uenv:
				self._TextBox_InputFile.Text = sub_DB.Uenv["(Input File)<Setup>[EYE]"][0]
			
				# for *.aedt Input File
				if sub_DB.Uenv["(Input File)<Setup>[EYE]"][0].strip().split("\\")[-1].split(".")[-1] == "aedt":				
					sub_AEDT.Get_AEDT_Info(self, sub_DB.Uenv["(Input File)<Setup>[EYE]"][0])

				# for *.csv Input File
				elif sub_DB.Uenv["(Input File)<Setup>[EYE]"][0].strip().split("\\")[-1].split(".")[-1] == "csv":
					pass

				# for *.tr0 Input File
				#elif sub_DB.Uenv["(Input File)<Setup>[EYE]"][0].strip().split("\\")[-1].split(".")[-1] == "tr0":
			else:	
				pass

			self._CheckBox_EditEnable_NewEye.Checked = True
			self._CheckBox_EditEnable_OldEye.Checked = True

		except Exception as e:			
			Log("[Eye_FormLoad] = Failed")
			Log(traceback.format_exc())
			print traceback.format_exc()
			MessageBox.Show("Fail to load Eye Analyzer main GUI","Warning")			
			EXIT()

	def Eye_FormKeyPress(self, sender, e):		
		# Save Cnf - Ctrl + S
		if e.KeyChar == chr(19):
			self.UserConf_Save_ToolStripMenuItemClick(self, sender)

		# Load Cnf - Ctrl + L
		elif e.KeyChar == chr(12):		
			self.UserConf_Load_ToolStripMenuItemClick(self, sender)

		# Edit Cnf - Ctrl + E
		elif e.KeyChar == chr(5):
			self.UserConf_Edit_ToolStripMenuItemClick(self, sender)

		# Open Input File - Ctrl + I
		elif e.KeyChar == chr(9):
			self.Button_ImportClick(self, sender)

		# Open Option Form - Ctrl + O
		elif e.KeyChar == chr(15):
			sub_DB.Option_Form.ShowDialog()

		# DDR IBIS Optimization - Ctrl + B
		elif e.KeyChar == chr(2):
			pass

		# ESC
		#elif e.KeyChar == chr(27):
		#	self.Close()

		# Batch - Ctrl + C
		elif e.KeyChar == chr(3):
			pass		

	def Eye_FormResizeEnd(self, sender, e):
		try:
			# Get previous Eye_Form width/height and resized Eye_Form width/height
			# Calculate Gap betweent previous and resized width/height		
			Gap_W = self.Size.Width - self.FormSize_W
			Gap_H = self.Size.Height - self.FormSize_H

			# Backup the resized Eye_Form width/height as previous MainFomr width/height
			self.FormSize_W = self.Size.Width
			self.FormSize_H = self.Size.Height

			# Resize
			self._GroupBox_Setup.Size = System.Drawing.Size(self._GroupBox_Setup.Width + Gap_W, self._GroupBox_Setup.Height)
			self._TextBox_InputFile.Size = System.Drawing.Size(self._TextBox_InputFile.Width + Gap_W, self._TextBox_InputFile.Height)
			self._ComboBox_Design.Size = System.Drawing.Size(self._ComboBox_Design.Width + Gap_W/2, self._ComboBox_Design.Height)
			self._ComboBox_SolutionName.Size = System.Drawing.Size(self._ComboBox_SolutionName.Width + Gap_W/2, self._ComboBox_SolutionName.Height)
			self._ComboBox_DDRGen.Size = System.Drawing.Size(self._ComboBox_DDRGen.Width + Gap_W/2, self._ComboBox_DDRGen.Height)
			self._ComboBox_DataRate.Size = System.Drawing.Size(self._ComboBox_DataRate.Width + Gap_W/4, self._ComboBox_DataRate.Height)
			self._CheckedListBox_ReportName.Size = System.Drawing.Size(self._CheckedListBox_ReportName.Width + Gap_W/2, self._CheckedListBox_ReportName.Height)
			self._TextBox_Offset.Size = System.Drawing.Size(self._TextBox_Offset.Width + Gap_W/4, self._TextBox_Offset.Height)
			

			# Relocate
			self._Button_Import.Location = System.Drawing.Point(self._Button_Import.Location.X + Gap_W, self._Button_Import.Location.Y)
			self._Label_ReportName.Location = System.Drawing.Point(self._Label_ReportName.Location.X + Gap_W/2, self._Label_ReportName.Location.Y)
			self._Label_Datarate.Location = System.Drawing.Point(self._Label_Datarate.Location.X + Gap_W/2, self._Label_Datarate.Location.Y)
			self._Label_Mbps.Location = System.Drawing.Point(self._Label_Mbps.Location.X + Gap_W, self._Label_Mbps.Location.Y)
			self._CheckedListBox_ReportName.Location = System.Drawing.Point(self._CheckedListBox_ReportName.Location.X + Gap_W/2, self._CheckedListBox_ReportName.Location.Y)
			self._ComboBox_DataRate.Location = System.Drawing.Point(self._ComboBox_DataRate.Location.X + Gap_W/2, self._ComboBox_DataRate.Location.Y)
			self._Button_ViewNet.Location = System.Drawing.Point(self._Button_ViewNet.Location.X + Gap_W, self._Button_ViewNet.Location.Y)
			self._Button_Analyze.Location = System.Drawing.Point(self._Button_Analyze.Location.X + Gap_W, self._Button_Analyze.Location.Y)
			self._Button_ViewResult.Location = System.Drawing.Point(self._Button_ViewResult.Location.X + Gap_W, self._Button_ViewResult.Location.Y)
			self._Label_Offset.Location = System.Drawing.Point(self._Label_Offset.Location.X + Gap_W*3/4, self._Label_Offset.Location.Y)
			self._TextBox_Offset.Location = System.Drawing.Point(self._TextBox_Offset.Location.X + Gap_W*3/4, self._TextBox_Offset.Location.Y)
			
			self._Label_ns.Location = System.Drawing.Point(self._Label_ns.Location.X + Gap_W, self._Label_ns.Location.Y)

		except Exception as e:			
			Log("[Eye_FormResizeEnd] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to resize Eye Analyzer main GUI","Warning")			
			EXIT()

	########################################################################
	def DDRConf_Load_ToolStripMenuItemClick(self, sender, e):
		try:
			# Select DDR Definition File		
			dialog = OpenFileDialog()
			dialog.InitialDirectory = path + "\\Resources"
			dialog.Filter = "DDR wizard definition file|*.def"
			dialog.Title = "Select ANSYS DDR Wizard Definition File"
			if dialog.ShowDialog(self) == DialogResult.OK:
				File = dialog.FileName
				# Parse DDR Definition File
				# Get Defined Data
				Cenv = Load_env(File)
				Cenv["File"] = File
				sub_DB.Cenv = Cenv
				Initial(True)
				self._ComboBox_DDRGen.Items.Clear()
				self._ComboBox_DataRate.Items.Clear()
				
				# Setup the Common Env. Info.		
				#	Add DDR Type into ComboBox
				DDR_Gen = []
				for key in sub_DB.Cenv:
					if "[DDR Info]" in key:
						DDR_Gen.append(key.split("<")[-1].split(">")[0])

				DDR_Gen.sort()
				for ddr in DDR_Gen:
					self._ComboBox_DDRGen.Items.Add(ddr)

				self._ComboBox_DDRGen.Text = ""
				self._ComboBox_DataRate.Text = ""
				self._ComboBox_DDRGen.BackColor = System.Drawing.SystemColors.Info
				self._ComboBox_DataRate.BackColor = System.Drawing.SystemColors.Info
				
				Log("[Load Definition File] = %s" % File)
				MessageBox.Show("DDR wizard definition file \"%s\" is loaded" % File.split("\\")[-1], "Load")
				

			else:
				MessageBox.Show("Please Select the DDR wizard definition file(*.def)","Warning")

		except Exception as e:			
			Log("[Load Definition File] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to load DDR Wizard definition file","Warning")
			EXIT()

	def DDRConf_Edit_ToolStripMenuItemClick(self, sender, e):
		try:
			Log("[Edit Definition File] = %s" % sub_DB.Cenv["File"])
			File = sub_DB.Cenv["File"]
			sub_DB.Env_Form = EnvEditor(File)
			sub_DB.Env_Form.ShowDialog()

		except Exception as e:			
			Log("[Edit Definition File] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to edit DDR Wizard definition file","Warning")
			EXIT()

	def UserConf_Load_ToolStripMenuItemClick(self, sender, e):
		try:
			# Select DDR Configuration File		
			dialog = OpenFileDialog()
			dialog.Title = "Load Configuration File"
			dialog.Filter = "Configuration File|*.cnf"			
			if dialog.ShowDialog(self) == DialogResult.OK:
				File = dialog.FileName
				CnfLoad(self, File)

				# for AEDT Input
				if sub_DB.InputFile_Flag == 1:
					sub_AEDT.Set_AEDT_Info(self, self._TextBox_InputFile.Text)
					flag, show_msg_flag, msg = Check_Input(self)
					if flag:				
						sub_DB.Net_Form.NetFormLoad(self, sender)						
						for row in sub_DB.Net_Form._DataGridView.Rows:
							if row.Cells[0].Value:
								self._Button_Analyze.Enabled = True
								self._Button_Analyze.BackColor = System.Drawing.SystemColors.Info
								break

					#if Check_Setup(self):				
					#	self.Cursor = Cursors.WaitCursor					
					#	sub_AEDT.Set_AEDT_Info(self, self._TextBox_InputFile.Text)
					#	self.Cursor = Cursors.Default
					#	self.Button_ViewNetClick(self, sender)

				# for CSV Input
				elif sub_DB.InputFile_Flag == 2:
					self._ComboBox_Design.Text = "N/A"
					self._ComboBox_Design.Enabled = False
					self._CheckedListBox_ReportName.Items.Clear()
					self._CheckedListBox_ReportName.Enabled = False
					self._CheckedListBox_ReportName.BackColor = System.Drawing.SystemColors.Control
					self._ComboBox_SolutionName.Text = "N/A"
					self._ComboBox_SolutionName.Enabled = False

					# Read Input csv file, Backup Netlist and Waveforms
					try:
						Waveform = {}
						with open(sub_DB.Eye_Form._TextBox_InputFile.Text) as fp:
							# Read the fist line
							temp_data = fp.readline().replace("\"","").replace(" ","").replace("-","_").strip().split(",")
							temp_data = list(filter(None,temp_data))							

							# Delete global & local variable data
							for i in range(0, len(temp_data)):
								if not "Time" in temp_data[i]:
									del temp_data[i]
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
							Time = []
							for line in fp:
								Time.append(float(line.split(",")[0]))
								for i in range(0, len(temp_data)):					
									data[i].append(float(line.split(",")[i+1]))
								
						fp.close()

						Log("	<Read WaveFrom>")
						for cell in data:
							key = cell[0].split("[")[0].replace("-","_")
							del cell[0]
							Waveform[key] = cell
							Log("		= %s" % key)

						# Check time unit
						if sub_DB.Unit["Time"].lower() == "ps":
							pass
						elif sub_DB.Unit["Time"].lower() == "ns":
							for i in range(0, len(Time)):
								Time[i] = Time[i]*1000
						else:
							MessageBox.Show("The time unit in the input csv file is not supported.","Warning",MessageBoxButtons.OK, MessageBoxIcon.Warning)
						sub_DB.Time = Time

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
						
						# Create Netlist
						Netlist = []
						for i in range(0, len(temp_data)):
							Netlist.append(temp_data[i].split("[")[0].replace("-","_"))
						sub_DB.Netlist = Netlist

						# Check input csv file time resolution
						# Non uniform time resolution
						if not sub_DB.Time[1] - sub_DB.Time[0] == 1:
							sub_DB.CSV_flag = False
							Log("	<Time Resolution> = Un-uniform")
							# OK Click, keep going
							if MessageBox.Show(							
								"The most appropriate format of Eye Analyzer's input csv file is voltage waveform extracted uniformly in 1ps.\n\n"+
								"\"%s\" does not meet this condition, which may result in inaccurate results.\n\n" % File.split("\\")[-1]+
								"Will you continue?","Warning",MessageBoxButtons.OKCancel, MessageBoxIcon.Warning) == DialogResult.OK:

								# Enable Next Step
								self._ComboBox_DDRGen.BackColor = System.Drawing.SystemColors.Info
								self._ComboBox_DDRGen.Enabled = True
								sub_DB.InputFile_Flag = 2

							# Cancel Click, re-select input file
							else:
								self._TextBox_InputFile.Text = ""

						# Uniform time resolution
						else:
							Log("	<Time Resolution> = Uniform")
							sub_DB.CSV_flag = True
							self._ComboBox_DDRGen.BackColor = System.Drawing.SystemColors.Info
							self._ComboBox_DDRGen.Enabled = True
							sub_DB.InputFile_Flag = 2

					except Exception as e:
						Log("[Input CSV File Parsing] = Failed")
						Log(traceback.format_exc())
						MessageBox.Show("Input csv file parsing has been failed.\n\nPlease check the input file,\n\t%s." % File.split("\\")[-1],"Warning",MessageBoxButtons.OK, MessageBoxIcon.Warning)
						self._TextBox_InputFile.Text = ""
						EXIT()

			else:
				MessageBox.Show("Loading configuration file has been canceled.","Warning")

		except Exception as e:			
			Log("[Load Configuration File] = Failed")
			Log(traceback.format_exc())
			print traceback.format_exc()
			MessageBox.Show("Fail to load configuration file","Warning")
			EXIT()

	def UserConf_Save_ToolStripMenuItemClick(self, sender, e):
		try:
			dialog = SaveFileDialog()
			dialog.Title = "Saving Configuration File"
			dialog.Filter = "Configuration file|*.cnf"
			if dialog.ShowDialog(self) == DialogResult.OK:
				File = dialog.FileName
				CnfSave(File)

			else:
				MessageBox.Show("Saving configuration file has been canceled.","Warning")

		except Exception as e:			
			Log("[Save Configuration File] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to save configuration file","Warning")
			EXIT()

	def UserConf_Edit_ToolStripMenuItemClick(self, sender, e):
		try:
			Log("[Edit Configuration File] = %s" % sub_DB.Uenv["File"])
			File = sub_DB.Uenv["File"]
			sub_DB.Env_Form = EnvEditor(File)
			sub_DB.Env_Form.ShowDialog()

		except Exception as e:			
			Log("[Edit Configuration File] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to edit DDR Wizard configuration file","Warning")
			EXIT()

	def Exit_ToolStripMenuItemClick(self, sender, e):
		CnfAutoSave()
		Log("[Save Log] = Done")
		LogSave(sub_DB.exit_iter)
		sub_ScriptEnv.Release()		
		os._exit(0)

	def Options_ToolStripMenuItemClick(self, sender, e):
		try:
			Log("[Option Form Launch]")
			sub_DB.Option_Form.ShowDialog()

		except Exception as e:			
			Log("[Option Form Launch] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to load Option Form","Warning")
			EXIT()

	def Options_IBISStripMenuItemClick(self, sender, e):
		try:
			if sub_DB.IBIS_Result_Init_Flag:
				IBIS_Init()			
			self.Cursor = Cursors.WaitCursor
			Log("[IBIS Form Launch]")
			flag, show_msg_flag, msg = Check_Input(self)
			if flag:
				# for *.aedt Input File
				if sub_DB.InputFile_Flag == 1:
					Sim_type = sub_DB.AEDT["Design"].GetDesignType()
					if Sim_type == "Circuit Netlist":
						MessageBox.Show("IBIS Optimization is not Supported for AEDT Circuit Netlist Input Files.", "Warning")

					else:
						File = self._TextBox_InputFile.Text
						sub_DB.IBIS_Form._ComboBox_IBIS_Tx.Text = "Select"
						sub_DB.IBIS_Form._ComboBox_IBIS_Rx.Text = "Select"
						sub_DB.IBIS_Form._ComboBox_IBIS_Tx.BackColor = System.Drawing.SystemColors.Info
						sub_DB.IBIS_Form._ComboBox_IBIS_Rx.BackColor = System.Drawing.SystemColors.Info

						#for item in sub_DB.Parsing_data['IBIS_File']:
						#	#print ''
						#	#print item
						#	#IBIS = IBIS_Parsing(File)
						#	#print IBIS
						#	#print ''
						#	#for key in IBIS.keys():
						#	#	print ''
						#	#	print key
						#	#	for item in IBIS[key]:
						#	#		print item

						#	#print JH

						#	IBIS_File_name = item.split('\\')[-1]
						#	sub_DB.IBIS_Form._ComboBox_IBIS_Tx.Items.Add(IBIS_File_name)
						#	sub_DB.IBIS_Form._ComboBox_IBIS_Rx.Items.Add(IBIS_File_name)										
						#	Group, Match = IBIS_Identify(IBIS_File_name, sub_DB.Cenv)
						#	if Group == "Tx":								
						#		sub_DB.IBIS_Form._ComboBox_IBIS_Tx.Text = IBIS_File_name
						#		sub_DB.IBIS_Form._ComboBox_IBIS_Tx.BackColor = System.Drawing.SystemColors.Window
						#	elif Group == "Rx":								
						#		sub_DB.IBIS_Form._ComboBox_IBIS_Rx.Text = IBIS_File_name
						#		sub_DB.IBIS_Form._ComboBox_IBIS_Rx.BackColor = System.Drawing.SystemColors.Window
						
						sub_DB.IBIS_Form.StartPosition = System.Windows.Forms.FormStartPosition.Manual
						sub_DB.IBIS_Form.Location = System.Drawing.Point(sub_DB.Eye_Form.Location.X + sub_DB.Eye_Form.Size.Width, sub_DB.Eye_Form.Location.Y)						
						sub_DB.IBIS_Form.ShowDialog()

				# for *.csv Input File
				else:
					MessageBox.Show("IBIS Optimization is not Supported for CSV Input Files.", "Warning")

			else:
				if show_msg_flag:
					MessageBox.Show("The following entries are missing :\n\n" + msg + "\nPlease enter so that nothing is missing","Warning")

			self.Cursor = Cursors.Default

		except Exception as e:			
			Log("[IBIS Form Launch] = Failed")
			Log(traceback.format_exc())
			print traceback.format_exc()
			MessageBox.Show("Fail to Launch IBIS Opt Form","Warning")
			EXIT()

	def Options_BatchStripMenuItemClick(self, sender, e):

		pass

	def Help_DDRHelp_ToolStripMenuItemClick(self, sender, e):		
		os.startfile(path + r'\Resources\help\User_Guide_EN.pdf')
		pass

	def Help_DDRGuid_ToolStripMenuItemClick(self, sender, e):
		os.startfile(path + r'\Resources\help\Quick_Guide_EN.pdf')
		pass

	def Help_DDRNew_ToolStripMenuItemClick(self, sender, e):
		MessageBox.Show("ANSYS DDR Wizard What's New", "To be done")
		pass

	def Help_DDRAbout_ToolStripMenuItemClick(self, sender, e):
		os.startfile(path + r'\Resources\help\Readme.html')
		pass

	########################################################################
	def toolStrip_Input_ButtonClick(self, sender, e):

		self.Button_ImportClick(self, sender)

	def toolStrip_DefLoad_ButtonClick(self, sender, e):

		self.DDRConf_Load_ToolStripMenuItemClick(self, sender)

	def toolStrip_DefEdit_ButtonClick(self, sender, e):

		self.DDRConf_Edit_ToolStripMenuItemClick(self, sender)

	def toolStrip_CnfLoad_ButtonClick(self, sender, e):

		self.UserConf_Load_ToolStripMenuItemClick(self, sender)

	def toolStrip_CnfSave_ButtonClick(self, sender, e):

		self.UserConf_Save_ToolStripMenuItemClick(self, sender)

	def toolStrip_CnfEdit_ButtonClick(self, sender, e):

		self.UserConf_Edit_ToolStripMenuItemClick(self, sender)
	
	def toolStrip_Option_ButtonClick(self, sender, e):

		self.Options_ToolStripMenuItemClick(self, sender)
		
	def toolStrip_IBIS_ButtonClick(self, sender, e):
		
		self.Options_IBISStripMenuItemClick(self, sender)

	def toolStrip_Batch_ButtonClick(self, sender, e):

		pass

	def ADEAHelpToolStripMenuItemClick(self, sender, e):

		self.Help_DDRHelp_ToolStripMenuItemClick(self, sender)

	def ADEAQuickGuideToolStripMenuItemClick(self, sender, e):

		self.Help_DDRGuid_ToolStripMenuItemClick(self, sender)

	def WhatsNewInThisReleaseToolStripMenuItemClick(self, sender, e):

		print "What's New"

	def AboutAnsysDDREyeAnalyzerToolStripMenuItemClick(self, sender, e):

		self.Help_DDRAbout_ToolStripMenuItemClick(self, sender)

	########################################################################
	def TextBox_OffsetTextChanged(self, sender, e):		
		sub_DB.Option_Form._TextBox_EyeOffset.Text = self._TextBox_Offset.Text
		pass

	def TextBox_VcentDQTextChanged(self, sender, e):
		if self._TextBox_VcentDQ.Text == "Auto":
			self._CheckBox_VcentDQ.Checked = True
			sub_DB.Option_Form._ComboBox_Vref.SelectedIndex = 0
		else:
			self._CheckBox_VcentDQ.Checked = False
			sub_DB.Option_Form._ComboBox_Vref.SelectedIndex = 1
			sub_DB.Option_Form._TextBox_Vref.Text = self._TextBox_VcentDQ.Text

	def TextBox_VrefTextChanged(self, sender, e):		
		if self._TextBox_Vref.Text == "Auto":
			self._CheckBox_Vref.Checked = True
			sub_DB.Option_Form._ComboBox_Vref.SelectedIndex = 0
		else:
			self._CheckBox_Vref.Checked = False
			sub_DB.Option_Form._ComboBox_Vref.SelectedIndex = 1
			sub_DB.Option_Form._TextBox_Vref.Text = self._TextBox_Vref.Text

	########################################################################
	def CheckBox_EditEnable_NewEyeCheckedChanged(self, sender, e):		
		if self._CheckBox_EditEnable_NewEye.Checked:
			color = System.Drawing.SystemColors.Info
		else:
			color = System.Drawing.Color.WhiteSmoke

		self._TextBox_VdIVW.BackColor = color
		self._TextBox_TdIVW.BackColor = color
		self._TextBox_VcentDQ.BackColor = color

		self._TextBox_VdIVW.ReadOnly = not self._CheckBox_EditEnable_NewEye.Checked
		self._TextBox_TdIVW.ReadOnly = not self._CheckBox_EditEnable_NewEye.Checked
		self._TextBox_VcentDQ.ReadOnly = not self._CheckBox_EditEnable_NewEye.Checked

	def CheckBox_EditEnable_OldEyeCheckedChanged(self, sender, e):
		if self._CheckBox_EditEnable_OldEye.Checked:
			color = System.Drawing.SystemColors.Info
		else:
			color = System.Drawing.Color.WhiteSmoke

		self._TextBox_AC_DQ.BackColor = color
		self._TextBox_AC_ADDR.BackColor = color
		self._TextBox_DC_DQ.BackColor = color
		self._TextBox_DC_ADDR.BackColor = color
		self._TextBox_Vref.BackColor = color
		self._TextBox_DQSetup.BackColor = color
		self._TextBox_DQHold.BackColor = color
		self._TextBox_ADDRSetup.BackColor = color
		self._TextBox_ADDRHold.BackColor = color
		self._ComboBox_AC_DQ.BackColor = color
		self._ComboBox_AC_ADDR.BackColor = color

		self._TextBox_AC_DQ.ReadOnly = not self._CheckBox_EditEnable_OldEye.Checked
		self._TextBox_AC_ADDR.ReadOnly = not self._CheckBox_EditEnable_OldEye.Checked
		self._TextBox_DC_DQ.ReadOnly = not self._CheckBox_EditEnable_OldEye.Checked
		self._TextBox_DC_ADDR.ReadOnly = not self._CheckBox_EditEnable_OldEye.Checked
		self._TextBox_Vref.ReadOnly = not self._CheckBox_EditEnable_OldEye.Checked
		self._TextBox_DQSetup.ReadOnly = not self._CheckBox_EditEnable_OldEye.Checked
		self._TextBox_DQHold.ReadOnly = not self._CheckBox_EditEnable_OldEye.Checked
		self._TextBox_ADDRSetup.ReadOnly = not self._CheckBox_EditEnable_OldEye.Checked
		self._TextBox_ADDRHold.ReadOnly = not self._CheckBox_EditEnable_OldEye.Checked

	def CheckBox_VcentDQCheckedChanged(self, sender, e):
		if sender.Checked:
			self._TextBox_VcentDQ.Text = "Auto"
			
		else:
			if self._TextBox_VcentDQ.Text == "Auto":
				self._TextBox_VcentDQ.Text = ""
				
		sub_DB.Title[2] = sub_DB.Option_Form._ComboBox_Vref.Text
		self.Text = " : ".join(sub_DB.Title)

	def CheckBox_VrefCheckedChanged(self, sender, e):		
		if sender.Checked:
			self._TextBox_Vref.Text = "Auto"
		else:
			if self._TextBox_Vref.Text == "Auto":
				self._TextBox_Vref.Text = ""

		sub_DB.Title[2] = sub_DB.Option_Form._ComboBox_Vref.Text
		self.Text = " : ".join(sub_DB.Title)

	########################################################################
	def ComboBox_AC_DQSelectedIndexChanged(self, sender, e):		
		keyword = "<" + self._ComboBox_DDRGen.Text + "-" + self._ComboBox_DataRate.Text + ">" + "[Eye Spec]"
		for key in sub_DB.Cenv:
			if keyword in key:
				if "DQ Setup" in key and self._ComboBox_AC_DQ.Text in key:
					if "!" in sub_DB.Cenv[key][0]:
						if sub_DB.TBD_flag:
							MessageBox.Show("Use undecied JEDEC specifications for %s-%s.\nCheck the specifications entered." % (self._ComboBox_DDRGen.Text, self._ComboBox_DataRate.Text),"Warning")
							sub_DB.TBD_flag = False
						self._TextBox_DQSetup.BackColor = System.Drawing.Color.PeachPuff
						self._TextBox_DQSetup.Text = sub_DB.Cenv[key][0].replace("!","")						
					else:
						self._TextBox_DQSetup.Text = sub_DB.Cenv[key][0]						
					Log("	<DQ Setup Time - AC%s> : %s[ps]" % (self._ComboBox_AC_DQ.Text, self._TextBox_DQSetup.Text))

	def ComboBox_AC_ADDRSelectedIndexChanged(self, sender, e):		
		keyword = "<" + self._ComboBox_DDRGen.Text + "-" + self._ComboBox_DataRate.Text + ">" + "[Eye Spec]"
		for key in sub_DB.Cenv:
			if keyword in key:
				if "ADDR Setup" in key and self._ComboBox_AC_ADDR.Text in key:
					self._TextBox_ADDRSetup.Text = sub_DB.Cenv[key][0]

	def ComboBox_DesignSelectedIndexChanged(self, sender, e):		
		try:
			# Set ToopTip
			self._ComboBox_Design_ToopTip.SetToolTip(self._ComboBox_Design, self._ComboBox_Design.Text)

			# Initialization 
			sub_DB.Eye_Form._CheckBox_VcentDQ.Checked = True
			sub_DB.Eye_Form._CheckBox_Vref.Checked = True
			sub_DB.Net_Form.Init_Flag = True
			self._CheckedListBox_ReportName.Items.Clear()

			oProject = sub_DB.AEDT["Project"]
			oDesign = oProject.SetActiveDesign(self._ComboBox_Design.SelectedItem)
			sub_DB.AEDT["Design"] = oDesign
			Log("[AEDT Design] = %s" % self._ComboBox_Design.Text)

			# Get Solutions
			self._ComboBox_SolutionName.Items.Clear()
			Sim_type = oDesign.GetDesignType()
			if Sim_type == "Circuit Netlist":
				self._ComboBox_SolutionName.Items.Add("TRAN")
				self._ComboBox_SolutionName.SelectedIndex = 0
			else:
				oModule = oDesign.GetModule("SimSetup")
				sub_DB.AEDT["Module"] = oModule
				for solution in oModule.GetAllSolutionSetups():
					self._ComboBox_SolutionName.Items.Add(solution)
				self._ComboBox_SolutionName.SelectedIndex = 0

			# Get Reports
			oModule = oDesign.GetModule("ReportSetup")
			report_name = []
			for report in oModule.GetAllReportNames():
				report_name.append(report)

			report_name.sort()
			for report in report_name:
				self._CheckedListBox_ReportName.Items.Add(report)
			self.Init_Flag = True
			self._CheckedListBox_ReportName.SetItemChecked(0, True)
	
			# Set Next Step
			self._ComboBox_Design.BackColor = System.Drawing.SystemColors.Window
			self._ComboBox_DDRGen.BackColor = System.Drawing.SystemColors.Info
			self._ComboBox_DDRGen.Enabled = True
		
			# Back-up the AEDT Info
			sub_DB.AEDT["Design"] = oDesign
			sub_DB.AEDT["Module"] = oModule

			flag, show_msg_flag, msg = Check_Input(self)
			if flag:
				sub_DB.Net_Form.NetFormLoad(self, sender)				
				for row in sub_DB.Net_Form._DataGridView.Rows:
					if row.Cells[0].Value:
						self._Button_Analyze.Enabled = True
						self._Button_Analyze.BackColor = System.Drawing.SystemColors.Info
						self._Button_ViewNet.BackColor = System.Drawing.SystemColors.Control
						break
				
		except Exception as e:			
			Log("[AEDT Design] = Failed")
			Log(traceback.format_exc())
			print traceback.format_exc()
			MessageBox.Show("Fail to set AEDT Design","Warning")
			EXIT()

	def ComboBox_SolutionNameSelectedIndexChanged(self, sender, e):
		# Set ToopTip		
		self._ComboBox_SolutionName_ToopTip.SetToolTip(self._ComboBox_SolutionName, self._ComboBox_SolutionName.Text)		

	def ComboBox_DDRGenSelectedIndexChanged(self, sender, e):
		try:			
			# Initialization
			if sub_DB.AutoLoad_flag:
				sub_DB.TBD_flag = True
			sub_DB.Net_Form.Init_Flag = True
			self._ComboBox_DDRGen.BackColor = System.Drawing.SystemColors.Window
			self._ComboBox_DataRate.BackColor = System.Drawing.SystemColors.Info
			self._ComboBox_DataRate.Enabled = True
			self._Button_Analyze.Enabled = False
			self._Button_Analyze.BackColor = System.Drawing.SystemColors.Control
			Log("[DDR type] = %s" % self._ComboBox_DDRGen.Text)
			
			# Add DDR Data-rate into ComboBox
			self._ComboBox_DataRate.Items.Clear()
			self._ComboBox_DataRate.Text = ""		
			Datarate = []
			for key in sub_DB.Cenv:
				if "[DDR Info]" in key:
					if "<" + self._ComboBox_DDRGen.Text + ">" in key:
						for speed in sub_DB.Cenv[key]:
							self._ComboBox_DataRate.Items.Add(speed)
			#self._Button_ViewNet.Enabled = False
			#self._Button_ViewNet.BackColor = System.Drawing.SystemColors.Control

			# Set Eye Vaildation Type according to DDR Gen.
			DDR_Gen = self._ComboBox_DDRGen.Text
			if DDR_Gen.find("DDR4") != -1 or DDR_Gen.find("DDR5") != -1:
				self._GroupBox_NewEye.Visible = True
				self._GroupBox_OldEye.Visible = False
				self.TextBox_VcentDQTextChanged(self, sender)
				sub_DB.Eyeflag = True
				
				if self.Full_Size_flag:
					if self.Image_flag_New:
						self.Button_ImgShow_NewClick(self, sender)
				else:
					if not self.Image_flag_New:
						self.Button_ImgShow_NewClick(self, sender)
					
			else:
				self._GroupBox_NewEye.Visible = False
				self._GroupBox_OldEye.Visible = True			
				sub_DB.Eyeflag = False
				if DDR_Gen == "DDR3":
					self._TextBox_AC_DQ.Visible = False
					self._TextBox_AC_ADDR.Visible = False
					self._ComboBox_AC_DQ.Visible = True
					self._ComboBox_AC_ADDR.Visible = True
					
				else:
					self._TextBox_AC_DQ.Visible = True
					self._TextBox_AC_ADDR.Visible = True
					self._ComboBox_AC_DQ.Visible = False
					self._ComboBox_AC_ADDR.Visible = False

				if self.Full_Size_flag:
					if self.Image_flag_Old:
						self.Button_ImgShow_OldClick(self, sender)
				else:
					if not self.Image_flag_Old:
						self.Button_ImgShow_OldClick(self, sender)

			# Clear Eye Spec.
			if sub_DB.Eyeflag:
				self._TextBox_VdIVW.Text = ""
				self._TextBox_TdIVW.Text = ""
				self._TextBox_VcentDQ.Text = "Auto"			
			else:
				self._TextBox_AC_DQ.Text = ""
				self._TextBox_AC_ADDR.Text = ""
				self._TextBox_DC_DQ.Text = ""
				self._TextBox_DC_ADDR.Text = ""
				self._TextBox_Vref.Text = ""
				self._TextBox_DQSetup.Text = ""
				self._TextBox_DQHold.Text = ""
				self._TextBox_ADDRSetup.Text = ""
				self._TextBox_ADDRHold.Text = ""

		except Exception as e:			
			Log("[DDR type] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to set DDR type","Warning")
			EXIT()

	def ComboBox_DataRateSelectedIndexChanged(self, sender, e):
		try:
			# Initialization
			if sub_DB.AutoLoad_flag:
				sub_DB.TBD_flag = True
			self._ComboBox_AC_DQ.Items.Clear()
			self._ComboBox_AC_ADDR.Items.Clear()		
			self._ComboBox_DataRate.BackColor = System.Drawing.SystemColors.Window
			self._Button_Analyze.Enabled = False
			self._Button_Analyze.BackColor = System.Drawing.SystemColors.Control
			if sub_DB.TBD_flag:
				self._Button_ViewNet.BackColor = System.Drawing.SystemColors.Info

			# Get Keywork
			#	ex) <DDR3-800>
			keyword = "<" + self._ComboBox_DDRGen.Text + "-" + self._ComboBox_DataRate.Text + ">" + "[Eye Spec]"			
			Log("[DDR datarate] = %s" % self._ComboBox_DataRate.Text)

			# Set Eye Specifications
			#	for New Eye		
			if sub_DB.Eyeflag:
				self._TextBox_VcentDQ.Text = "Auto"
				if self._ComboBox_DDRGen.Text == "DDR4":
					for key in sub_DB.Cenv:
						if keyword in key:
							if "Rx Mask Voltage" in key:
								if "!" in sub_DB.Cenv[key][0]:
									if sub_DB.TBD_flag:
										MessageBox.Show("Use undecied JEDEC specifications for %s-%s.\nCheck the specifications entered." % (self._ComboBox_DDRGen.Text, self._ComboBox_DataRate.Text),"Warning")
										sub_DB.TBD_flag = False
									self._TextBox_VdIVW.BackColor = System.Drawing.Color.PeachPuff
									self._TextBox_VdIVW.Text = sub_DB.Cenv[key][0].replace("!","")
								else:
									self._TextBox_VdIVW.BackColor = System.Drawing.SystemColors.Window
									self._TextBox_VdIVW.Text = sub_DB.Cenv[key][0]
								Log("	<VdIVW> : %s[mV]" % self._TextBox_VdIVW.Text)

							elif "Rx Timing Window Total" in key:
								if "!" in sub_DB.Cenv[key][0]:
									if sub_DB.TBD_flag:
										MessageBox.Show("Use undecied JEDEC specifications for %s-%s.\nCheck the specifications entered." % (self._ComboBox_DDRGen.Text, self._ComboBox_DataRate.Text),"Warning")
										sub_DB.TBD_flag = False
									self._TextBox_TdIVW.BackColor = System.Drawing.Color.PeachPuff
									self._TextBox_TdIVW.Text = sub_DB.Cenv[key][0].replace("!","")
								else:
									self._TextBox_TdIVW.BackColor = System.Drawing.SystemColors.Window
									self._TextBox_TdIVW.Text = sub_DB.Cenv[key][0]
								Log("	<TdIVW> : %s[UI]" % self._TextBox_TdIVW.Text)

				elif self._ComboBox_DDRGen.Text == "DDR5":
					for key in sub_DB.Cenv:
						if keyword in key:
							if "Rx Mask Voltage" in key:
								if "!" in sub_DB.Cenv[key][0]:
									if sub_DB.TBD_flag:
										MessageBox.Show("Use undecied JEDEC specifications for %s-%s.\nCheck the specifications entered." % (self._ComboBox_DDRGen.Text, self._ComboBox_DataRate.Text),"Warning")
										sub_DB.TBD_flag = False
									self._TextBox_VdIVW.BackColor = System.Drawing.Color.PeachPuff
									self._TextBox_VdIVW.Text = sub_DB.Cenv[key][0].replace("!","")
								else:
									self._TextBox_VdIVW.BackColor = System.Drawing.SystemColors.Window
									self._TextBox_VdIVW.Text = sub_DB.Cenv[key][0]
								Log("	<VdIVW> : %s[mV]" % self._TextBox_VdIVW.Text)

							elif "Rx Timing Window Total" in key:
								if "!" in sub_DB.Cenv[key][0]:
									if sub_DB.TBD_flag:
										MessageBox.Show("Use undecied JEDEC specifications for %s-%s.\nCheck the specifications entered." % (self._ComboBox_DDRGen.Text, self._ComboBox_DataRate.Text),"Warning")
										sub_DB.TBD_flag = False
									self._TextBox_TdIVW.BackColor = System.Drawing.Color.PeachPuff
									self._TextBox_TdIVW.Text = sub_DB.Cenv[key][0].replace("!","")
								else:
									self._TextBox_TdIVW.BackColor = System.Drawing.SystemColors.Window
									self._TextBox_TdIVW.Text = sub_DB.Cenv[key][0]
								Log("	<TdIVW> : %s[UI]" % self._TextBox_TdIVW.Text)

				elif self._ComboBox_DDRGen.Text == "LPDDR4":
					for key in sub_DB.Cenv:
						if keyword in key:
							if "Rx Mask Voltage" in key:
								if "!" in sub_DB.Cenv[key][0]:
									if sub_DB.TBD_flag:
										MessageBox.Show("Use undecied JEDEC specifications for %s-%s.\nCheck the specifications entered." % (self._ComboBox_DDRGen.Text, self._ComboBox_DataRate.Text),"Warning")
										sub_DB.TBD_flag = False
									self._TextBox_VdIVW.BackColor = System.Drawing.Color.PeachPuff
									self._TextBox_VdIVW.Text = sub_DB.Cenv[key][0].replace("!","")
								else:
									self._TextBox_VdIVW.BackColor = System.Drawing.SystemColors.Window
									self._TextBox_VdIVW.Text = sub_DB.Cenv[key][0]
								Log("	<VdIVW> : %s[mV]" % self._TextBox_VdIVW.Text)

							elif "Rx Timing Window Total" in key:
								if "!" in sub_DB.Cenv[key][0]:
									if sub_DB.TBD_flag:
										MessageBox.Show("Use undecied JEDEC specifications for %s-%s.\nCheck the specifications entered." % (self._ComboBox_DDRGen.Text, self._ComboBox_DataRate.Text),"Warning")
										sub_DB.TBD_flag = False
									self._TextBox_TdIVW.BackColor = System.Drawing.Color.PeachPuff
									self._TextBox_TdIVW.Text = sub_DB.Cenv[key][0].replace("!","")
								else:
									self._TextBox_TdIVW.BackColor = System.Drawing.SystemColors.Window
									self._TextBox_TdIVW.Text = sub_DB.Cenv[key][0]
								Log("	<TdIVW> : %s[UI]" % self._TextBox_TdIVW.Text)

				elif self._ComboBox_DDRGen.Text == "LPDDR5":					
					for key in sub_DB.Cenv:
						if keyword in key:
							if "Rx Mask Voltage" in key:
								if "!" in sub_DB.Cenv[key][0]:
									if sub_DB.TBD_flag:
										MessageBox.Show("Use undecied JEDEC specifications for %s-%s.\nCheck the specifications entered." % (self._ComboBox_DDRGen.Text, self._ComboBox_DataRate.Text),"Warning")
										sub_DB.TBD_flag = False
									self._TextBox_VdIVW.BackColor = System.Drawing.Color.PeachPuff
									self._TextBox_VdIVW.Text = sub_DB.Cenv[key][0].replace("!","")
								else:
									self._TextBox_VdIVW.BackColor = System.Drawing.SystemColors.Window
									self._TextBox_VdIVW.Text = sub_DB.Cenv[key][0]
								Log("	<VdIVW> : %s[mV]" % self._TextBox_VdIVW.Text)

							elif "Rx Timing Window Total" in key:
								if "!" in sub_DB.Cenv[key][0]:
									if sub_DB.TBD_flag:
										MessageBox.Show("Use undecied JEDEC specifications for %s-%s.\nCheck the specifications entered." % (self._ComboBox_DDRGen.Text, self._ComboBox_DataRate.Text),"Warning")
										sub_DB.TBD_flag = False
									self._TextBox_TdIVW.BackColor = System.Drawing.Color.PeachPuff
									self._TextBox_TdIVW.Text = sub_DB.Cenv[key][0].replace("!","")
								else:
									self._TextBox_TdIVW.BackColor = System.Drawing.SystemColors.Window
									self._TextBox_TdIVW.Text = sub_DB.Cenv[key][0]
								Log("	<TdIVW> : %s[UI]" % self._TextBox_TdIVW.Text)

			#	for Old Eye
			else: 
				if self._ComboBox_DDRGen.Text == "DDR2":
					for key in sub_DB.Cenv:
						if keyword in key:
							if "AC" in key:
								self._TextBox_AC_DQ.Text = sub_DB.Cenv[key][0]
								self._TextBox_AC_ADDR.Text = sub_DB.Cenv[key][0]
							elif "DC" in key:
								self._TextBox_DC_DQ.Text = sub_DB.Cenv[key][0]
								self._TextBox_DC_ADDR.Text = sub_DB.Cenv[key][0]
							elif "DQ Setup" in key:
								self._TextBox_DQSetup.Text = sub_DB.Cenv[key][0]
							elif "DQ Hold" in key:
								self._TextBox_DQHold.Text = sub_DB.Cenv[key][0]
							elif "ADDR Setup" in key:
								self._TextBox_ADDRSetup.Text = sub_DB.Cenv[key][0]
							elif "ADDR Hold" in key:
								self._TextBox_ADDRHold.Text = sub_DB.Cenv[key][0]
							elif "VREF" in key:
								self._TextBox_Vref.Text = sub_DB.Cenv[key][0]

				elif self._ComboBox_DDRGen.Text == "DDR3":				
					for key in sub_DB.Cenv:
						if keyword in key:							
							if "AC Th" in key and "DQ" in key:
								for val in sub_DB.Cenv[key]:
									self._ComboBox_AC_DQ.Items.Add(val)
								self._ComboBox_AC_DQ.SelectedIndex = 0
								Log("	<AC Threshold Voltage - DQ> : %s[mV]" % self._ComboBox_AC_DQ.Text)
							
							elif "DC Th" in key and "DQ" in key:
								self._TextBox_DC_DQ.Text = sub_DB.Cenv[key][0]
								Log("	<DC Threshold Voltage - DQ> : %s[mV]" % self._TextBox_DC_DQ.Text)

							elif "AC Th" in key and "CA" in key:
								for val in sub_DB.Cenv[key]:
									self._ComboBox_AC_ADDR.Items.Add(val)
								self._ComboBox_AC_ADDR.SelectedIndex = 0
								Log("	<AC Threshold Voltage - CA> : %s[mV]" % self._ComboBox_AC_ADDR.Text)
							
							elif "DC Th" in key and "CA" in key:
								self._TextBox_DC_ADDR.Text = sub_DB.Cenv[key][0]
								Log("	<DC Threshold Voltage - CA> : %s[mV]" % self._TextBox_DC_ADDR.Text)

					for key in sub_DB.Cenv:
						if keyword in key:
							if "DQ Setup" in key and self._ComboBox_AC_DQ.Text in key:
								if "!" in sub_DB.Cenv[key][0]:
									if sub_DB.TBD_flag:
										MessageBox.Show("Use undecied JEDEC specifications for %s-%s.\nCheck the specifications entered." % (self._ComboBox_DDRGen.Text, self._ComboBox_DataRate.Text),"Warning")
										sub_DB.TBD_flag = False
									self._TextBox_DQSetup.BackColor = System.Drawing.Color.PeachPuff
									self._TextBox_DQSetup.Text = sub_DB.Cenv[key][0].replace("!","")									
								else:
									self._TextBox_DQSetup.BackColor = System.Drawing.SystemColors.Window
									self._TextBox_DQSetup.Text = sub_DB.Cenv[key][0]									
								Log("	<DQ Setup Time - AC%s> : %s[ps]" % (self._ComboBox_AC_DQ.Text, self._TextBox_DQSetup.Text))
							
							elif "DQ Hold" in key and self._TextBox_DC_DQ.Text in key:
								if "!" in sub_DB.Cenv[key][0]:
									if sub_DB.TBD_flag:
										MessageBox.Show("Use undecied JEDEC specifications for %s-%s.\nCheck the specifications entered." % (self._ComboBox_DDRGen.Text, self._ComboBox_DataRate.Text),"Warning")
										sub_DB.TBD_flag = False
									self._TextBox_DQHold.BackColor = System.Drawing.Color.PeachPuff
									self._TextBox_DQHold.Text = sub_DB.Cenv[key][0].replace("!","")
								else:
									self._TextBox_DQHold.BackColor = System.Drawing.SystemColors.Window
									self._TextBox_DQHold.Text = sub_DB.Cenv[key][0]
								Log("	<DQ Hold Time - DC%s> : %s[ps]" % (self._TextBox_DC_DQ.Text, self._TextBox_DQHold.Text))

							elif "ADDR Setup" in key and self._ComboBox_AC_ADDR.Text in key:								
								if "!" in sub_DB.Cenv[key][0]:
									if sub_DB.TBD_flag:
										MessageBox.Show("Use undecied JEDEC specifications for %s-%s.\nCheck the specifications entered." % (self._ComboBox_DDRGen.Text, self._ComboBox_DataRate.Text),"Warning")
										sub_DB.TBD_flag = False
									self._TextBox_ADDRSetup.BackColor = System.Drawing.Color.PeachPuff
									self._TextBox_ADDRSetup.Text = sub_DB.Cenv[key][0].replace("!","")									
								else:
									self._TextBox_ADDRSetup.BackColor = System.Drawing.SystemColors.Window
									self._TextBox_ADDRSetup.Text = sub_DB.Cenv[key][0]									
								Log("	<ADDR Setup Time - AC%s> : %s[ps]" % (self._ComboBox_AC_ADDR.Text, self._TextBox_ADDRSetup.Text))

							elif "ADDR Hold" in key and self._TextBox_DC_ADDR.Text in key:
								if "!" in sub_DB.Cenv[key][0]:
									if sub_DB.TBD_flag:
										MessageBox.Show("Use undecied JEDEC specifications for %s-%s.\nCheck the specifications entered." % (self._ComboBox_DDRGen.Text, self._ComboBox_DataRate.Text),"Warning")
										sub_DB.TBD_flag = False
									self._TextBox_ADDRHold.BackColor = System.Drawing.Color.PeachPuff
									self._TextBox_ADDRHold.Text = sub_DB.Cenv[key][0].replace("!","")
								else:
									self._TextBox_ADDRHold.BackColor = System.Drawing.SystemColors.Window
									self._TextBox_ADDRHold.Text = sub_DB.Cenv[key][0]
								Log("	<ADDR Hold Time - DC%s> : %s[ps]" % (self._TextBox_DC_ADDR.Text, self._TextBox_ADDRHold.Text))
							
							elif "VREF" in key:
								self._TextBox_Vref.Text = sub_DB.Cenv[key][0]					

				elif self._ComboBox_DDRGen.Text == "LPDDR2":
					#TODO : Setup LPDDR2 Eye Spec.
					pass

				elif self._ComboBox_DDRGen.Text == "LPDDR3":
					#TODO : Setup LPDDR3 Eye Spec.
					pass

			flag, show_msg_flag, msg = Check_Input(self)
			if flag:				
				sub_DB.Net_Form.NetFormLoad(self, sender)				
				for row in sub_DB.Net_Form._DataGridView.Rows:
					if row.Cells[0].Value:
						self._Button_Analyze.Enabled = True
						self._Button_Analyze.BackColor = System.Drawing.SystemColors.Info
						break
			sub_DB.datarate = int(self._ComboBox_DataRate.Text)
			sub_DB.UI = 1.0/(sub_DB.datarate*1e6)*1e12

		except Exception as e:			
			Log("[DDR datarate] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to set DDR datarate","Warning")
			EXIT()

	def CheckedListBox_ReportNameItemCheck(self, sender, e):		
		try:
			if self.Init_Flag:
				self.Init_Flag = False
			
			else:			
				self.Init_Flag = True
				self._CheckedListBox_ReportName.SetItemChecked(e.Index, e.NewValue)

				Initial(True)				
				sub_AEDT.Get_AEDT_Info(self, self._TextBox_InputFile.Text)
				self._Button_ViewNet.BackColor = System.Drawing.SystemColors.Info

				flag, show_msg_flag, msg = Check_Input(self)			
				if flag:
					sub_DB.Net_Form.NetFormLoad(self, sender)										
					for row in sub_DB.Net_Form._DataGridView.Rows:
						if row.Cells[0].Value:
							self._Button_Analyze.Enabled = True
							self._Button_Analyze.BackColor = System.Drawing.SystemColors.Info
							self._Button_ViewNet.BackColor = System.Drawing.SystemColors.Control
							break

			sub_DB.Title[3] = sub_DB.Option_Form._ComboBox_Analyze.Text		
			self.Text = " : ".join(sub_DB.Title)

		except Exception as e:			
			print traceback.format_exc()			
			EXIT()

	########################################################################
	def Button_ImportClick(self, sender, e):
		try:
			sub_DB.TBD_flag = True
			self.Init_Flag = True
			dialog = OpenFileDialog()
			#dialog.Filter = "AEDT Project file|*.aedt|Comma Separated Values|*.csv"
			dialog.Filter = "AEDT Project file|*.aedt"

			if dialog.ShowDialog(self) == DialogResult.OK:
				self._ComboBox_Design.Text = ""
				File = dialog.FileName
				sub_DB.File = File
				result_dir = File.split(".")[0] + "_DDR_Results"
				sub_DB.Input_File = dialog.SafeFileName
				if os.path.isdir(result_dir):
					sub_DB.result_dir = result_dir
				else:
					os.makedirs(result_dir)
					sub_DB.result_dir = result_dir
				self._TextBox_InputFile.Text = File

				extension = File.split("\\")[-1].split(".")[-1] # Get File Extension				
				Initial(True)

				# for *.aedt File
				if extension == "aedt":					
					Log("[Input File Type] = AEDT")
					Log("	<Input File> = %s" % File)
					#self.TopMost = True
					self.Cursor = Cursors.WaitCursor					
					sub_AEDT.Get_AEDT_Info(self, File)
					self.Cursor = Cursors.Default
					#self.TopMost = False


					self._ComboBox_Design.Enabled = True
					self._CheckedListBox_ReportName.Enabled = True
					self._ComboBox_SolutionName.Enabled = True
					self._CheckedListBox_ReportName.BackColor = System.Drawing.SystemColors.Window

					self._TextBox_InputFile.BackColor = System.Drawing.SystemColors.Window
					self._ComboBox_Design.BackColor = System.Drawing.SystemColors.Info				
					self._ComboBox_DataRate.BackColor = System.Drawing.SystemColors.Info
					self._Button_ViewNet.BackColor = System.Drawing.SystemColors.Info
					self._ComboBox_Design.SelectedIndex = 0
					sub_DB.InputFile_Flag = 1

					# AEDT Parsing
					sim_type = sub_DB.AEDT["Design"].GetDesignType()
					if sim_type == 'Circuit Design':
						sub_DB.Parsing_data = AEDT_Parsing(File, self._ComboBox_Design.Text, True)

						#datarate_flag = False
						#for item in self._ComboBox_DataRate.Items:
						#	if item == str(sub_DB.Parsing_data['datarate']):
						#		datarate_flag = True
						#		break

						#if not datarate_flag:
						#	self._ComboBox_DataRate.Text = str(sub_DB.Parsing_data['datarate'])
						#	self._ComboBox_DataRate.BackColor = System.Drawing.SystemColors.Info

						#if self._ComboBox_DataRate.Text != str(sub_DB.Parsing_data['datarate']):
						#	self._ComboBox_DataRate.Text = str(sub_DB.Parsing_data['datarate'])
						#	self._ComboBox_DataRate.BackColor = System.Drawing.SystemColors.Info
					elif sim_type == 'Circuit Netlist':
						#TODO.220824 : AEDT parsing for circuit netlist input
						pass

				# for *.csv File
				elif extension == "csv":
					Log("[Input File Type] = CSV")
					Log("	<Input File> = %s" % File)
					# Disable unnecessary component
					self._TextBox_InputFile.BackColor = System.Drawing.SystemColors.Window
					self._ComboBox_Design.Text = "N/A"
					self._ComboBox_Design.Enabled = False
					self._CheckedListBox_ReportName.Items.Clear()
					self._CheckedListBox_ReportName.Items.Add("N/A")
					self._CheckedListBox_ReportName.SetItemChecked(0, True)
					self._CheckedListBox_ReportName.Enabled = False
					self._CheckedListBox_ReportName.BackColor = System.Drawing.SystemColors.Control
					self._ComboBox_SolutionName.Text = "N/A"
					self._ComboBox_SolutionName.Enabled = False

					# Read Input csv file, Backup Netlist and Waveforms
					try:
						Waveform = {}
						with open(sub_DB.Eye_Form._TextBox_InputFile.Text) as fp:
							# Read the fist line
							temp_data = fp.readline().replace("\"","").replace(" ","").replace("-","_").strip().split(",")
							temp_data = list(filter(None,temp_data))							

							# Delete global & local variable data
							for i in range(0, len(temp_data)):
								if not "Time" in temp_data[i]:
									del temp_data[i]
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
							Time = []
							for line in fp:
								Time.append(float(line.split(",")[0]))
								for i in range(0, len(temp_data)):					
									data[i].append(float(line.split(",")[i+1]))
								
						fp.close()

						Log("	<Read WaveFrom>")
						for cell in data:
							key = cell[0].split("[")[0].replace("-","_")
							del cell[0]
							Waveform[key] = cell
							Log("		= %s" % key)

						# Check time unit
						if sub_DB.Unit["Time"].lower() == "ps":
							pass
						elif sub_DB.Unit["Time"].lower() == "ns":
							for i in range(0, len(Time)):
								Time[i] = Time[i]*1000
						else:
							MessageBox.Show("The time unit in the input csv file is not supported.","Warning",MessageBoxButtons.OK, MessageBoxIcon.Warning)
						sub_DB.Time = Time

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
						
						# Create Netlist
						Netlist = []
						for i in range(0, len(temp_data)):
							Netlist.append(temp_data[i].split("[")[0].replace("-","_"))
						sub_DB.Netlist = Netlist

						# Check input csv file time resolution
						# Non uniform time resolution
						if not sub_DB.Time[1] - sub_DB.Time[0] == 1:
							sub_DB.CSV_flag = False
							Log("	<Time Resolution> = Un-uniform")
							# OK Click, keep going
							if MessageBox.Show(							
								"The most appropriate format of Eye Analyzer's input csv file is voltage waveform extracted uniformly in 1ps.\n\n"+
								"\"%s\" does not meet this condition, which may result in inaccurate results.\n\n" % File.split("\\")[-1]+
								"Will you continue?","Warning",MessageBoxButtons.OKCancel, MessageBoxIcon.Warning) == DialogResult.OK:

								# Enable Next Step
								self._ComboBox_DDRGen.BackColor = System.Drawing.SystemColors.Info
								self._ComboBox_DDRGen.Enabled = True
								self._ComboBox_DataRate.BackColor = System.Drawing.SystemColors.Info
								self._ComboBox_DataRate.Enabled = True
								self._Button_ViewNet.BackColor = System.Drawing.SystemColors.Info
								sub_DB.InputFile_Flag = 2

							# Cancel Click, re-select input file
							else:
								self._TextBox_InputFile.Text = ""

						# Uniform time resolution
						else:
							Log("	<Time Resolution> = Uniform")
							sub_DB.CSV_flag = True
							self._ComboBox_DDRGen.BackColor = System.Drawing.SystemColors.Info
							self._ComboBox_DDRGen.Enabled = True
							self._ComboBox_DataRate.BackColor = System.Drawing.SystemColors.Info
							self._ComboBox_DataRate.Enabled = True
							self._Button_ViewNet.BackColor = System.Drawing.SystemColors.Info
							sub_DB.InputFile_Flag = 2

					except Exception as e:
						Log("[Input CSV File Parsing] = Failed")
						Log(traceback.format_exc())
						MessageBox.Show("Input csv file parsing has been failed.\n\nPlease check the input file,\n\t%s." % File.split("\\")[-1],"Warning",MessageBoxButtons.OK, MessageBoxIcon.Warning)
						self._TextBox_InputFile.Text = ""
						EXIT()

					flag, show_msg_flag, msg = Check_Input(self)
					if flag:
						sub_DB.Net_Form.NetFormLoad(self, sender)						
						for row in sub_DB.Net_Form._DataGridView.Rows:
							if row.Cells[0].Value:
								self._Button_Analyze.Enabled = True
								self._Button_Analyze.BackColor = System.Drawing.SystemColors.Info
								self._Button_ViewNet.BackColor = System.Drawing.SystemColors.Control
								break

				# for *.tr0 File
				elif extension == "tr0":
					# TODO : Input Type for *.tr0
					pass

				sub_DB.Title[1] = File.split("\\")[-1]
				sub_DB.Title[2] = sub_DB.Option_Form._ComboBox_Vref.Text
				sub_DB.Title[3] = sub_DB.Option_Form._ComboBox_Analyze.Text
				sub_DB.Title[4] = str(sub_DB.Option_Form._CheckBox_PlotEye.Checked)

				if sub_DB.Option_Form._CheckBox_ExportExcelReport.Checked:
					sub_DB.Title[5] = "True-%s" % sub_DB.Option_Form._ComboBox_ReportFormat.Text
				else:
					sub_DB.Title[5] = "False"
				self.Text = " : ".join(sub_DB.Title)

			else:
				pass

			

			# Set ToopTip
			self._TextBox_InputFile_ToopTip.SetToolTip(self._TextBox_InputFile, self._TextBox_InputFile.Text)
			
		except Exception as e:
			Log("[Input File Import] = Failed")
			Log(traceback.format_exc())
			print traceback.format_exc()
			MessageBox.Show("Fail to import Input File\n%s" % File,"Warning")
			EXIT()

	def Button_ViewNetClick(self, sender, e):
		try:			
			# Check if any of report name has been checked
			flag, show_msg_flag, msg = Check_Input(self)

			if flag:				
				# Target Net Setup				
				sub_DB.Net_Form.StartPosition = System.Windows.Forms.FormStartPosition.Manual
				sub_DB.Net_Form.Location = System.Drawing.Point(sub_DB.Eye_Form.Location.X + sub_DB.Eye_Form.Size.Width, sub_DB.Eye_Form.Location.Y)
				sub_DB.Net_Form.Text = "Target Net Setup - " + sub_DB.Uenv["File"].split("\\")[-1]
				if sub_DB.Net_Form._DataGridView.Columns.Count > 5:			
					sub_DB.Net_Form._DataGridView.Columns[6].DisplayIndex = 6
					sub_DB.Net_Form._DataGridView.Columns[5].DisplayIndex = 5
					sub_DB.Net_Form._DataGridView.Columns[4].DisplayIndex = 4

				sub_DB.Net_Form._Label_GroupName.Visible = True
				sub_DB.Net_Form._ComboBox_AnalyzeGroup.Visible = True
				sub_DB.Net_Form._Button_Update.Visible = True
				sub_DB.Net_Form._Button_Auto.Visible = True
				sub_DB.Net_Form._Button_EditRule.Visible = True
				sub_DB.Net_Form._Button_Identify.Visible = True

				sub_DB.Net_Form._Label_ImageWidth.Visible = False
				sub_DB.Net_Form._Label_ImageWidth_Unit.Visible = False
				sub_DB.Net_Form._CheckBox_PlotEye.Visible = False
				sub_DB.Net_Form._TextBox_ImageWidth.Visible = False
				sub_DB.Net_Form._Label_ReportFormat.Visible = False
				sub_DB.Net_Form._ComboBox_Report.Visible = False
				sub_DB.Net_Form._Button_Export.Visible = False				
				sub_DB.Net_Form.ShowDialog()
				#sub_DB.Net_Form.Show()

				self._Button_ViewNet.BackColor = System.Drawing.SystemColors.Control
				self._Button_Analyze.Enabled = True
				self._Button_Analyze.BackColor = System.Drawing.SystemColors.Info

			else:
				if show_msg_flag:
					MessageBox.Show("The following entries are missing :\n\n" + msg + "\nPlease enter so that nothing is missing","Warning")
			
		except Exception as e:			
			Log("[Net Form Launch] = Failed")
			Log(traceback.format_exc())
			print traceback.format_exc()
			MessageBox.Show("Fail to launch Net Classification Form","Warning")			
			EXIT()

	def Button_AnalyzeClick(self, sender, e):
		try:			
			# Check if any of report name has been checked
			flag, show_msg_flag, msg = Check_Input(self)

			if flag:
				Log("[Eye Analyze Start] = %s" % time.strftime('%Y.%m.%d, %H:%M:%S'))
				# Initiallization
				sub_DB.Excel_Img_File = []

				# Compliacne Check Box Visibility Control in option form
				if self._ComboBox_DDRGen.Text in ["DDR2", "DDR3"]:				
					sub_DB.Option_Form._CheckBox_Compiance.Visible = True
					sub_DB.Option_Form._Button_Compliance.Visible = True

				else:				
					sub_DB.Option_Form._CheckBox_Compiance.Visible = False
					sub_DB.Option_Form._Button_Compliance.Visible = False
							
				#########################
				#      Eye Analyze      #
				#########################

				# for New Eye
				if sub_DB.Eyeflag:
					# Default
					if sub_DB.Option_Form._ComboBox_Analyze.SelectedIndex == 0:						
						sub_EyeAnalyze.New_Default(self)

					# +Setup/Hold
					elif sub_DB.Option_Form._ComboBox_Analyze.SelectedIndex == 1:
						sub_EyeAnalyze.New_SetupHold(self)

				# for Old Eye
				else:
					if sub_DB.Option_Form._ComboBox_Analyze.SelectedIndex == 0:						
						sub_EyeAnalyze.Old_Default(self)

					# +Setup/Hold
					elif sub_DB.Option_Form._ComboBox_Analyze.SelectedIndex == 1:
						sub_EyeAnalyze.Old_SetupHold(self)
					
				#############################
				#      Compliance Test      #
				#############################
				if sub_DB.Option_Form._CheckBox_Compiance.Checked:						
					Log("	<Compliance Test> = Start")
					sub_Compliance.Compliacne_Test(self)

				else:
					Log("	<Compliance Test> = Unchecked")

				#####################
				#      Closing      #
				#####################
				sub_DB.Cal_Form.Close()
				self.Cursor = Cursors.Default
				sub_DB.Cal_Form.Cursor = Cursors.Default

				#os.startfile(sub_DB.result_dir)
				sub_DB.Result_Flag = True
				sub_DB.Net_Form._Label_GroupName.Visible = False
				sub_DB.Net_Form._ComboBox_AnalyzeGroup.Visible = False
				sub_DB.Net_Form._Button_Update.Visible = False
				sub_DB.Net_Form._Button_Auto.Visible = False
				sub_DB.Net_Form._Button_EditRule.Visible = False
				sub_DB.Net_Form._Button_Identify.Visible = False

				sub_DB.Net_Form._CheckBox_PlotEye.Visible = True
				sub_DB.Net_Form._Label_ReportFormat.Visible = True
				sub_DB.Net_Form._ComboBox_Report.Visible = True
				sub_DB.Net_Form._Button_Export.Visible = True
				sub_DB.Net_Form.Text += ' - Vref = %s[mV]' % sub_DB.Vref
				sub_DB.Net_Form.ShowDialog()
				sub_DB.Result_Flag = False
				self._Button_Analyze.BackColor = System.Drawing.SystemColors.Control
				self._Button_ViewResult.Enabled = True

			else:
				if show_msg_flag:
					MessageBox.Show("The following entries are missing :\n\n" + msg + "\nPlease enter so that nothing is missing","Warning")

		except Exception as e:			
			Log("[Eye Analyze Start] = Fail")
			Log(traceback.format_exc())
			print traceback.format_exc()
			MessageBox.Show("Fail to start Eye Analyze","Warning")			
			EXIT()
		
	def Button_ViewResultClick(self, sender, e):
		try:
			Log("[View Eye Analyze Result]")
			sub_DB.Result_Flag = True
			sub_DB.Net_Form._DataGridView.Columns[5].DisplayIndex = 2
			sub_DB.Net_Form._DataGridView.Columns[6].DisplayIndex = 3
			sub_DB.Net_Form._DataGridView.Columns[4].DisplayIndex = 4
			sub_DB.Net_Form._Label_GroupName.Visible = False
			sub_DB.Net_Form._ComboBox_AnalyzeGroup.Visible = False
			sub_DB.Net_Form._Button_Update.Visible = False
			sub_DB.Net_Form._Button_Auto.Visible = False
			sub_DB.Net_Form._Button_EditRule.Visible = False
			sub_DB.Net_Form._Button_Identify.Visible = False

			sub_DB.Net_Form._CheckBox_PlotEye.Visible = True			
			sub_DB.Net_Form._Label_ReportFormat.Visible = True
			sub_DB.Net_Form._ComboBox_Report.Visible = True
			sub_DB.Net_Form._Button_Export.Visible = True			
			sub_DB.Net_Form.ShowDialog()
			sub_DB.Result_Flag = False

		except Exception as e:			
			Log("[View Eye Analyze Result] = Fail")
			Log(traceback.format_exc())
			print traceback.format_exc()
			MessageBox.Show("Fail to View Eye Analyze Result","Warning")			
			EXIT()

	def Button_ImgShow_NewClick(self, sender, e):		
		self.Image_flag_New = not self.Image_flag_New

		# Compact Size
		if self.Image_flag_New:
			self.Full_Size_flag = False
			self._Button_ImgShow_New.Text = "Show"
			self._PictureBox_NewEye.Visible = False
			
			self._Label_VdIVW.Visible = True
			self._TextBox_VdIVW.Location = System.Drawing.Point(225, 28)
			self._TextBox_VdIVW.Size = System.Drawing.Size(65, 23)

			self._Label_TdIVW.Visible = True
			self._TextBox_TdIVW.Location = System.Drawing.Point(365, 28)
			self._TextBox_TdIVW.Size = System.Drawing.Size(65, 23)

			self._Label_VcentDQ.Visible = True
			self._TextBox_VcentDQ.Location = System.Drawing.Point(527, 28)
			self._TextBox_VcentDQ.Size = System.Drawing.Size(65, 23)

			self._CheckBox_VcentDQ.Location = System.Drawing.Point(527, 51)
			self._CheckBox_EditEnable_NewEye.Location = System.Drawing.Point(595, 31)

			self._Label_Info.Location = System.Drawing.Point(170, 60)

			self._GroupBox_NewEye.Size = System.Drawing.Size(690, 95)

			self._Label_VoltageSpec.Location = System.Drawing.Point(223, 51)
			self._Label_TimingSpec.Location = System.Drawing.Point(363, 51)
			

			self.MinimumSize = System.Drawing.Size(self.Size.Width, 335)
			self.Height = 335
			
		# Full Size
		else:
			self.Full_Size_flag = True
			self._Button_ImgShow_New.Text = "Hide"
			self._PictureBox_NewEye.Visible = True

			self._Label_VdIVW.Visible = False
			self._TextBox_VdIVW.Location = System.Drawing.Point(97, 238)
			self._TextBox_VdIVW.Size = System.Drawing.Size(59, 23)

			self._Label_TdIVW.Visible = False
			self._TextBox_TdIVW.Location = System.Drawing.Point(333, 303)
			self._TextBox_TdIVW.Size = System.Drawing.Size(52, 23)

			self._Label_VcentDQ.Visible = False
			self._TextBox_VcentDQ.Location = System.Drawing.Point(548, 231)
			self._TextBox_VcentDQ.Size = System.Drawing.Size(59, 23)

			self._CheckBox_VcentDQ.Location = System.Drawing.Point(548, 254)
			self._CheckBox_EditEnable_NewEye.Location = System.Drawing.Point(590, 423)

			self._Label_Info.Location = System.Drawing.Point(10, 423)

			self._GroupBox_NewEye.Size = System.Drawing.Size(690, 420)

			self._Label_TimingSpec.Location = System.Drawing.Point(298, 285)
			self._Label_VoltageSpec.Location = System.Drawing.Point(60, 261)

			self.MinimumSize = System.Drawing.Size(self.Size.Width, 660)
			self.Height = 660
			 
	def Button_ImgShow_OldClick(self, sender, e):		
		self.Image_flag_Old = not self.Image_flag_Old

		# Compact Size
		if self.Image_flag_Old:
			self.Full_Size_flag = False
			self._Button_ImgShow_Old.Text = "Show"

			self._PictureBox_OldEye.Visible = False

			self._Label_AC_DQ.Visible = False
			self._Label_AC_ADDR.Visible = False
			self._Label_DC_DQ.Visible = False
			self._Label_DC_ADDR.Visible = False
			self._Label_DQ.Visible = False
			self._Label_ADDR.Visible = False

			self._Label_Vac.Visible = True
			self._Label_Vdc.Visible = True
			self._Label_Setup.Visible = True
			self._Label_Hold.Visible = True
			self._Label_Vref.Visible = True
			self._Label_dq.Visible = True
			self._Label_addr.Visible = True
			self._H_Border_1.Visible = True
			self._H_Border_2.Visible = True
			self._H_Border_3.Visible = True			
			self._V_Border_1.Visible = True
			self._V_Border_2.Visible = True
			self._V_Border_3.Visible = True
			self._V_Border_4.Visible = True
			self._V_Border_5.Visible = True
			self._V_Border_6.Visible = True

			self._ComboBox_AC_DQ.Location = System.Drawing.Point(185, 33)			
			self._ComboBox_AC_DQ.Size = System.Drawing.Size(80, 24)

			self._ComboBox_AC_ADDR.Location = System.Drawing.Point(185, 61)
			self._ComboBox_AC_ADDR.Size = System.Drawing.Size(80, 24)

			self._TextBox_AC_DQ.Location = System.Drawing.Point(185, 33)			
			self._TextBox_AC_DQ.Size = System.Drawing.Size(80, 23)
			
			self._TextBox_AC_ADDR.Location = System.Drawing.Point(185, 61)			
			self._TextBox_AC_ADDR.Size = System.Drawing.Size(80, 23)

			self._TextBox_DC_DQ.Location = System.Drawing.Point(273, 33)			
			self._TextBox_DC_DQ.Size = System.Drawing.Size(80, 23)
			
			self._TextBox_DC_ADDR.Location = System.Drawing.Point(273, 61)
			self._TextBox_DC_ADDR.Size = System.Drawing.Size(80, 23)

			self._TextBox_DQSetup.Location = System.Drawing.Point(361, 33)			
			self._TextBox_DQSetup.Size = System.Drawing.Size(80, 23)
			
			self._TextBox_ADDRSetup.Location = System.Drawing.Point(361, 61)
			self._TextBox_ADDRSetup.Size = System.Drawing.Size(80, 23)

			self._TextBox_DQHold.Location = System.Drawing.Point(449, 33)			
			self._TextBox_DQHold.Size = System.Drawing.Size(80, 23)

			self._TextBox_ADDRHold.Location = System.Drawing.Point(449, 61)			
			self._TextBox_ADDRHold.Size = System.Drawing.Size(80, 23)

			self._TextBox_Vref.Location = System.Drawing.Point(539, 42)			
			self._TextBox_Vref.Size = System.Drawing.Size(80, 23)

			self._CheckBox_Vref.Location = System.Drawing.Point(539, 66)
			self._CheckBox_EditEnable_OldEye.Location = System.Drawing.Point(537, 63)

			self._GroupBox_OldEye.Size = System.Drawing.Size(690, 95)

			self.MinimumSize = System.Drawing.Size(self.Size.Width, 335)
			self.Height = 335

		# Full Size
		else:
			self.Full_Size_flag = True
			self._Button_ImgShow_Old.Text = "Hide"

			self._PictureBox_OldEye.Visible = True

			self._Label_AC_DQ.Visible = True
			self._Label_AC_ADDR.Visible = True
			self._Label_DC_DQ.Visible = True
			self._Label_DC_ADDR.Visible = True
			self._Label_DQ.Visible = True
			self._Label_ADDR.Visible = True

			self._Label_Vac.Visible = False
			self._Label_Vdc.Visible = False
			self._Label_Setup.Visible = False
			self._Label_Hold.Visible = False
			self._Label_Vref.Visible = False
			self._Label_dq.Visible = False
			self._Label_addr.Visible = False
			self._H_Border_1.Visible = False
			self._H_Border_2.Visible = False
			self._H_Border_3.Visible = False			
			self._V_Border_1.Visible = False
			self._V_Border_2.Visible = False
			self._V_Border_3.Visible = False
			self._V_Border_4.Visible = False
			self._V_Border_5.Visible = False
			self._V_Border_6.Visible = False

			self._ComboBox_AC_DQ.Location = System.Drawing.Point(88, 173)
			self._ComboBox_AC_DQ.Size = System.Drawing.Size(73, 24)

			self._ComboBox_AC_ADDR.Location = System.Drawing.Point(88, 200)
			self._ComboBox_AC_ADDR.Size = System.Drawing.Size(73, 24)

			self._TextBox_AC_DQ.Location = System.Drawing.Point(88, 173)
			self._TextBox_AC_DQ.Size = System.Drawing.Size(71, 23)

			self._TextBox_AC_ADDR.Location = System.Drawing.Point(88, 200)
			self._TextBox_AC_ADDR.Size = System.Drawing.Size(71, 23)

			self._TextBox_DC_DQ.Location = System.Drawing.Point(553, 219)
			self._TextBox_DC_DQ.Size = System.Drawing.Size(71, 23)

			self._TextBox_DC_ADDR.Size = System.Drawing.Size(71, 23)
			self._TextBox_DC_ADDR.Location = System.Drawing.Point(553, 246)

			self._TextBox_DQSetup.Location = System.Drawing.Point(299, 398)
			self._TextBox_DQSetup.Size = System.Drawing.Size(45, 23)

			self._TextBox_ADDRSetup.Location = System.Drawing.Point(299, 425)			
			self._TextBox_ADDRSetup.Size = System.Drawing.Size(45, 23)

			self._TextBox_DQHold.Location = System.Drawing.Point(347, 398)
			self._TextBox_DQHold.Size = System.Drawing.Size(56, 23)
			
			self._TextBox_ADDRHold.Location = System.Drawing.Point(347, 425)
			self._TextBox_ADDRHold.Size = System.Drawing.Size(56, 23)

			self._TextBox_Vref.Location = System.Drawing.Point(130, 232)
			self._TextBox_Vref.Size = System.Drawing.Size(52, 23)

			self._CheckBox_Vref.Location = System.Drawing.Point(103, 254)		
			self._CheckBox_EditEnable_OldEye.Location = System.Drawing.Point(590, 423)

			self._GroupBox_OldEye.Size = System.Drawing.Size(690, 420)

			self.MinimumSize = System.Drawing.Size(self.Size.Width, 660)
			self.Height = 660

	def Button_LoadCnfClick(self, sender, e):
		CnfLoad(self)

		flag = True
		if self._TextBox_InputFile.Text == "":
			flag = False

		if self._ComboBox_Design.Text == "":
			flag = False
		
		if len(self._CheckedListBox_ReportName.CheckedItems) == 0:
			flag = False

		if self._ComboBox_SolutionName.Text == "":
			flag = False

		if self._ComboBox_DDRGen.Text == "":
			flag = False

		if self._ComboBox_DataRate.Text == "":
			flag = False

		if flag:
			#self.TopMost = True
			self.Cursor = Cursors.WaitCursor
			sub_AEDT.Set_AEDT_Info(self, self._TextBox_InputFile.Text)
			self.Cursor = Cursors.Default
			#self.TopMost = False

			self.Button_ViewNetClick(self, sender)

	########################################################################
	def Eye_FormFormClosing(self, sender, e):
		CnfAutoSave()
		Log("[Save Log] = Done")
		LogSave(sub_DB.exit_iter)
		sub_ScriptEnv.Release()		
		os._exit(0)

	''' For Debuggin '''
	def CheckBox_DebugCheckedChanged(self, sender, e):
		sub_DB.Debug_Mode = self._CheckBox_Debug.Checked
		self._Button_Debug.Visible = self._CheckBox_Debug.Checked

	def Button_DebugClick(self, sender, e):
		File = []
		File.append(r'D:\1_Work\20220106_DDR_Compliance\1_Work\CNF\1.cnf')
		File.append(r'D:\1_Work\20220106_DDR_Compliance\1_Work\CNF\2.cnf')
		File.append(r'D:\1_Work\20220106_DDR_Compliance\1_Work\CNF\3.cnf')
		File.append(r'D:\1_Work\20220106_DDR_Compliance\1_Work\CNF\4.cnf')

		for CNF_file in File:
			Initial(True)
			Debug_Load_CNF(self, sender, CNF_file)
			self.Button_ViewNetClick(self, sender)
			self.Button_AnalyzeClick(self, sender)						
			
		LogSave(iter, r'D:\1_Work\20220106_DDR_Compliance\1_Work\CNF\Test.log')

def Debug_Load_CNF(self, sender, File):
	try:		
		CnfLoad(self, File)

		# for AEDT Input
		if sub_DB.InputFile_Flag == 1:
			if Check_Setup(self):				
				self.Cursor = Cursors.WaitCursor					
				sub_AEDT.Set_AEDT_Info(self, self._TextBox_InputFile.Text)
				self.Cursor = Cursors.Default				
				
		# for CSV Input
		elif sub_DB.InputFile_Flag == 2:
			self._ComboBox_Design.Text = "N/A"
			self._ComboBox_Design.Enabled = False
			self._CheckedListBox_ReportName.Items.Clear()
			self._CheckedListBox_ReportName.Enabled = False
			self._CheckedListBox_ReportName.BackColor = System.Drawing.SystemColors.Control
			self._ComboBox_SolutionName.Text = "N/A"
			self._ComboBox_SolutionName.Enabled = False

			# Read Input csv file, Backup Netlist and Waveforms
			try:
				Waveform = {}
				with open(sub_DB.Eye_Form._TextBox_InputFile.Text) as fp:
					# Read the fist line
					temp_data = fp.readline().replace("\"","").replace(" ","").replace("-","_").strip().split(",")
					temp_data = list(filter(None,temp_data))							

					# Delete global & local variable data
					for i in range(0, len(temp_data)):
						if not "Time" in temp_data[i]:
							del temp_data[i]
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
					Time = []
					for line in fp:
						Time.append(float(line.split(",")[0]))
						for i in range(0, len(temp_data)):					
							data[i].append(float(line.split(",")[i+1]))
								
				fp.close()

				Log("	<Read WaveFrom>")
				for cell in data:
					key = cell[0].split("[")[0].replace("-","_")
					del cell[0]
					Waveform[key] = cell
					Log("		= %s" % key)

				# Check time unit
				if sub_DB.Unit["Time"].lower() == "ps":
					pass
				elif sub_DB.Unit["Time"].lower() == "ns":
					for i in range(0, len(Time)):
						Time[i] = Time[i]*1000
				else:
					MessageBox.Show("The time unit in the input csv file is not supported.","Warning",MessageBoxButtons.OK, MessageBoxIcon.Warning)
				sub_DB.Time = Time

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
						
				# Create Netlist
				Netlist = []
				for i in range(0, len(temp_data)):
					Netlist.append(temp_data[i].split("[")[0].replace("-","_"))
				sub_DB.Netlist = Netlist

				# Check input csv file time resolution
				# Non uniform time resolution
				if not sub_DB.Time[1] - sub_DB.Time[0] == 1:
					sub_DB.CSV_flag = False
					Log("	<Time Resolution> = Un-uniform")
					# OK Click, keep going
					if MessageBox.Show(							
						"The most appropriate format of Eye Analyzer's input csv file is voltage waveform extracted uniformly in 1ps.\n\n"+
						"\"%s\" does not meet this condition, which may result in inaccurate results.\n\n" % File.split("\\")[-1]+
						"Will you continue?","Warning",MessageBoxButtons.OKCancel, MessageBoxIcon.Warning) == DialogResult.OK:

						# Enable Next Step
						self._ComboBox_DDRGen.BackColor = System.Drawing.SystemColors.Info
						self._ComboBox_DDRGen.Enabled = True
						sub_DB.InputFile_Flag = 2

					# Cancel Click, re-select input file
					else:
						self._TextBox_InputFile.Text = ""

				# Uniform time resolution
				else:
					Log("	<Time Resolution> = Uniform")
					sub_DB.CSV_flag = True
					self._ComboBox_DDRGen.BackColor = System.Drawing.SystemColors.Info
					self._ComboBox_DDRGen.Enabled = True
					sub_DB.InputFile_Flag = 2

			except Exception as e:
				Log("[Input CSV File Parsing] = Failed")
				Log(traceback.format_exc())
				MessageBox.Show("Input csv file parsing has been failed.\n\nPlease check the input file,\n\t%s." % File.split("\\")[-1],"Warning",MessageBoxButtons.OK, MessageBoxIcon.Warning)
				self._TextBox_InputFile.Text = ""
				EXIT()

	except Exception as e:			
		Log("[Load Configuration File] = Failed")
		Log(traceback.format_exc())
		print traceback.format_exc()
		MessageBox.Show("Fail to load configuration file","Warning")
		EXIT()