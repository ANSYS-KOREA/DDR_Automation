import os
import time
import sys

import System.Drawing
import System.Windows.Forms
import sub_ScriptEnv
import sub_AEDT
import sub_DB
import traceback

from GUI_subforms import *
from sub_functions import *
from System.Drawing import *
from System.Windows.Forms import *

class Eye_Form(Form):
	def __init__(self):
		self.InitializeComponent()
		pass
	
	''' Eye_Form - GUI '''	
	def InitializeComponent(self):		
		global path
		path = os.path.dirname(os.path.abspath(__file__))

		self._PictureBox_Logo = System.Windows.Forms.PictureBox()
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

		self._CheckedListBox_ReportName = System.Windows.Forms.CheckedListBox()

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
		self._Button_ImgShow = System.Windows.Forms.Button()
		self._Button_Debug = System.Windows.Forms.Button()

		self._openFileDialog1 = System.Windows.Forms.OpenFileDialog()

		self._CheckBox_AnalyzeDQ = System.Windows.Forms.CheckBox()
		self._CheckBox_AnalyzeADDR = System.Windows.Forms.CheckBox()
		self._CheckBox_EditEnable_NewEye = System.Windows.Forms.CheckBox()
		self._CheckBox_EditEnable_OldEye = System.Windows.Forms.CheckBox()

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

		self._toolStripSeparator1 = System.Windows.Forms.ToolStripSeparator()
		self._toolStripSeparator2 = System.Windows.Forms.ToolStripSeparator()

		self._PictureBox_Logo.BeginInit()
		self._PictureBox_OldEye.BeginInit()
		self._PictureBox_NewEye.BeginInit()
		self._MenuStrip.SuspendLayout()
		self._GroupBox_Setup.SuspendLayout()
		self._GroupBox_OldEye.SuspendLayout()		
		self._GroupBox_NewEye.SuspendLayout()
		self._GroupBox_UnitOld.SuspendLayout()
		self._GroupBox_UnitNew.SuspendLayout()		
		self.SuspendLayout()
		# 
		# MenuStrip
		#
		self._MenuStrip.BackColor = System.Drawing.Color.FromArgb(240, 240, 240)
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
		self._UserConf_Load_ToolStripMenuItem.Text = "Load"
		self._UserConf_Load_ToolStripMenuItem.Click += self.UserConf_Load_ToolStripMenuItemClick
		# 
		# UserConf_Save_ToolStripMenuItem
		# 
		self._UserConf_Save_ToolStripMenuItem.Name = "UserConf_Save_ToolStripMenuItem"
		self._UserConf_Save_ToolStripMenuItem.Size = System.Drawing.Size(100, 22)
		self._UserConf_Save_ToolStripMenuItem.Text = "Save"
		self._UserConf_Save_ToolStripMenuItem.Click += self.UserConf_Save_ToolStripMenuItemClick
		# 
		# UserConf_Edit_ToolStripMenuItem
		# 
		self._UserConf_Edit_ToolStripMenuItem.Name = "UserConf_Edit_ToolStripMenuItem"
		self._UserConf_Edit_ToolStripMenuItem.Size = System.Drawing.Size(100, 22)
		self._UserConf_Edit_ToolStripMenuItem.Text = "Edit"
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
			[self._Options_ToolStripMenuItem]))
		self._Tool_ToolStripMenuItem.Name = "Tool_ToolStripMenuItem"
		self._Tool_ToolStripMenuItem.Size = System.Drawing.Size(46, 20)
		self._Tool_ToolStripMenuItem.Text = "Tool"
		# 
		# Options_ToolStripMenuItem
		# 
		self._Options_ToolStripMenuItem.Name = "Options_ToolStripMenuItem"
		self._Options_ToolStripMenuItem.Size = System.Drawing.Size(152, 22)
		self._Options_ToolStripMenuItem.Text = "Options"
		#self._Options_ToolStripMenuItem.Enabled = False
		self._Options_ToolStripMenuItem.Click += self.Options_ToolStripMenuItemClick
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
		self._Help_DDRHelp_ToolStripMenuItem.Text = "Ansys DDR Wizard Help"
		self._Help_DDRHelp_ToolStripMenuItem.Click += self.Help_DDRHelp_ToolStripMenuItemClick
		# 
		# Help_DDRGuid_ToolStripMenuItem
		# 
		self._Help_DDRGuid_ToolStripMenuItem.Name = "Help_DDRGuid_ToolStripMenuItem"
		self._Help_DDRGuid_ToolStripMenuItem.Size = System.Drawing.Size(300, 22)
		self._Help_DDRGuid_ToolStripMenuItem.Text = "Ansys DDR Wizard Getting Started Guides"
		self._Help_DDRGuid_ToolStripMenuItem.Click += self.Help_DDRGuid_ToolStripMenuItemClick
		# 
		# Help_DDRNew_ToolStripMenuItem
		# 
		self._Help_DDRNew_ToolStripMenuItem.Name = "Help_DDRNew_ToolStripMenuItem"
		self._Help_DDRNew_ToolStripMenuItem.Size = System.Drawing.Size(300, 22)
		self._Help_DDRNew_ToolStripMenuItem.Text = "What's New in this Release"
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
		# PictureBox_Logo
		# 
		File = path + "\\Resources\\Eye_Analyzer_Logo.bmp"
		self._PictureBox_Logo.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch
		self._PictureBox_Logo.ErrorImage = None
		self._PictureBox_Logo.Image = Bitmap(File)
		self._PictureBox_Logo.Location = System.Drawing.Point(12, 22)
		self._PictureBox_Logo.Name = "PictureBox_Logo"
		self._PictureBox_Logo.Size = System.Drawing.Size(685, 76)
		self._PictureBox_Logo.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage
		self._PictureBox_Logo.TabIndex = 25
		self._PictureBox_Logo.TabStop = False
		# 
		# PictureBox_OldEye
		# 
		File = path + "\\Resources\\EYE_Measuer_Old.bmp"
		self._PictureBox_OldEye.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch
		self._PictureBox_OldEye.ErrorImage = None
		self._PictureBox_OldEye.Image = Bitmap(File)
		self._PictureBox_OldEye.Location = System.Drawing.Point(6, 17)
		self._PictureBox_OldEye.Name = "PictureBox_OldEye"
		self._PictureBox_OldEye.Size = System.Drawing.Size(867, 457)
		self._PictureBox_OldEye.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage
		self._PictureBox_OldEye.TabIndex = 26
		self._PictureBox_OldEye.TabStop = False		
		# 
		# PictureBox_NewEye
		#
		File = path + "\\Resources\\EYE_Measuer_New.bmp"
		self._PictureBox_NewEye.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch
		self._PictureBox_NewEye.ErrorImage = None
		self._PictureBox_NewEye.Image = Bitmap(File)
		self._PictureBox_NewEye.Location = System.Drawing.Point(6, 17)
		self._PictureBox_NewEye.Name = "PictureBox_NewEye"
		self._PictureBox_NewEye.Size = System.Drawing.Size(867, 457)
		self._PictureBox_NewEye.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage
		self._PictureBox_NewEye.TabIndex = 26
		self._PictureBox_NewEye.TabStop = False
		# 
		# GroupBox_Setup
		# 
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
		self._GroupBox_Setup.Location = System.Drawing.Point(12, 104)
		self._GroupBox_Setup.Name = "GroupBox_Setup"
		self._GroupBox_Setup.Size = System.Drawing.Size(685, 150)
		self._GroupBox_Setup.TabIndex = 8
		self._GroupBox_Setup.TabStop = False
		self._GroupBox_Setup.Text = "DDR Eye Analyzer Setup"		
		# 
		# GroupBox_OldEye
		# 
		self._GroupBox_OldEye.Controls.Add(self._Button_ImgShow)
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
		self._GroupBox_OldEye.Location = System.Drawing.Point(12, 260)
		self._GroupBox_OldEye.Name = "GroupBox_OldEye"
		self._GroupBox_OldEye.Size = System.Drawing.Size(879, 510)
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
		self._GroupBox_UnitOld.Location = System.Drawing.Point(18, 27)		
		self._GroupBox_UnitOld.Name = "GroupBox_UnitOld"
		self._GroupBox_UnitOld.Size = System.Drawing.Size(106, 66)
		self._GroupBox_UnitOld.TabIndex = 38
		self._GroupBox_UnitOld.TabStop = False
		self._GroupBox_UnitOld.Text = "Unit"
		# 
		# GroupBox_NewEye
		#		
		self._GroupBox_NewEye.Controls.Add(self._Button_ImgShow)		
		self._GroupBox_NewEye.Controls.Add(self._Label_Info)
		self._GroupBox_NewEye.Controls.Add(self._CheckBox_EditEnable_NewEye)
		self._GroupBox_NewEye.Controls.Add(self._TextBox_TdIVW)
		self._GroupBox_NewEye.Controls.Add(self._GroupBox_UnitNew)
		self._GroupBox_NewEye.Controls.Add(self._TextBox_VcentDQ)
		self._GroupBox_NewEye.Controls.Add(self._TextBox_VdIVW)
		self._GroupBox_NewEye.Controls.Add(self._PictureBox_NewEye)
		self._GroupBox_NewEye.Font = System.Drawing.Font("Arial", 11, System.Drawing.FontStyle.Bold)
		self._GroupBox_NewEye.Location = System.Drawing.Point(12, 260)
		self._GroupBox_NewEye.Name = "GroupBox_NewEye"
		self._GroupBox_NewEye.Size = System.Drawing.Size(879, 510)
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
		self._GroupBox_UnitNew.Location = System.Drawing.Point(18, 27)		
		self._GroupBox_UnitNew.Name = "GroupBox_UnitNew"
		self._GroupBox_UnitNew.Size = System.Drawing.Size(150, 66)
		self._GroupBox_UnitNew.TabIndex = 38
		self._GroupBox_UnitNew.TabStop = False
		self._GroupBox_UnitNew.Text = "Unit"
		# 
		# Label_Datarate
		# 
		self._Label_Datarate.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_Datarate.Location = System.Drawing.Point(339, 115)
		self._Label_Datarate.Name = "Label_Datarate"
		self._Label_Datarate.Size = System.Drawing.Size(106, 28)
		self._Label_Datarate.TabIndex = 11
		self._Label_Datarate.Text = "Data Rate :"
		self._Label_Datarate.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_DDRGen
		# 
		self._Label_DDRGen.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_DDRGen.Location = System.Drawing.Point(6, 115)
		self._Label_DDRGen.Name = "Label_DDRGen"
		self._Label_DDRGen.Size = System.Drawing.Size(125, 28)
		self._Label_DDRGen.TabIndex = 10
		self._Label_DDRGen.Text = "DDR Generation :"
		self._Label_DDRGen.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_Mbps
		# 
		self._Label_Mbps.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_Mbps.Location = System.Drawing.Point(613, 115)
		self._Label_Mbps.Name = "Label_Mbps"
		self._Label_Mbps.Size = System.Drawing.Size(45, 28)
		self._Label_Mbps.TabIndex = 21
		self._Label_Mbps.Text = "Mbps"
		self._Label_Mbps.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_Version
		# 
		self._Label_Version.Font = System.Drawing.Font("Swis721 Blk BT", 20.25, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_Version.Location = System.Drawing.Point(692, 60)
		self._Label_Version.Name = "Label_Version"
		self._Label_Version.Size = System.Drawing.Size(104, 28)
		self._Label_Version.TabIndex = 24
		self._Label_Version.Text = "v0.0"
		self._Label_Version.TextAlign = System.Drawing.ContentAlignment.MiddleLeft		
		# 
		# Label_Design
		# 
		self._Label_Design.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_Design.Location = System.Drawing.Point(25, 55)
		self._Label_Design.Name = "Label_Design"
		self._Label_Design.Size = System.Drawing.Size(106, 28)
		self._Label_Design.TabIndex = 22
		self._Label_Design.Text = "Design :"
		self._Label_Design.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_InputFile
		# 
		self._Label_InputFile.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_InputFile.Location = System.Drawing.Point(25, 17)
		self._Label_InputFile.Name = "Label_InputFile"
		self._Label_InputFile.Size = System.Drawing.Size(106, 28)
		self._Label_InputFile.TabIndex = 9
		self._Label_InputFile.Text = "Input File :"
		self._Label_InputFile.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_ReportName
		# 
		self._Label_ReportName.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_ReportName.Location = System.Drawing.Point(339, 55)
		self._Label_ReportName.Name = "Label_ReportName"
		self._Label_ReportName.Size = System.Drawing.Size(106, 28)
		self._Label_ReportName.TabIndex = 26
		self._Label_ReportName.Text = "Report Name :"
		self._Label_ReportName.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_SolutionName
		# 
		self._Label_SolutionName.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_SolutionName.Location = System.Drawing.Point(25, 85)
		self._Label_SolutionName.Name = "Label_ReportName"
		self._Label_SolutionName.Size = System.Drawing.Size(106, 28)
		self._Label_SolutionName.TabIndex = 26
		self._Label_SolutionName.Text = "Setup Name :"
		self._Label_SolutionName.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_DQ
		# 
		self._Label_DQ.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_DQ.Location = System.Drawing.Point(345, 448)
		self._Label_DQ.Name = "Label_DQ"
		self._Label_DQ.Size = System.Drawing.Size(40, 28)
		self._Label_DQ.TabIndex = 29
		self._Label_DQ.Text = "DQ :"
		self._Label_DQ.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_ADDR
		# 
		self._Label_ADDR.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_ADDR.Location = System.Drawing.Point(308, 478)
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
		self._Label_AC_DQ.Location = System.Drawing.Point(82, 200)
		self._Label_AC_DQ.Name = "Label_AC_DQ"
		self._Label_AC_DQ.Size = System.Drawing.Size(40, 28)
		self._Label_AC_DQ.TabIndex = 40
		self._Label_AC_DQ.Text = "DQ :"
		self._Label_AC_DQ.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_AC_ADDR
		# 
		self._Label_AC_ADDR.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_AC_ADDR.Location = System.Drawing.Point(48, 228)
		self._Label_AC_ADDR.Name = "Label_AC_ADDR"
		self._Label_AC_ADDR.Size = System.Drawing.Size(74, 28)
		self._Label_AC_ADDR.TabIndex = 41
		self._Label_AC_ADDR.Text = "Address :"
		self._Label_AC_ADDR.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_DC_ADDR
		# 
		self._Label_DC_ADDR.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_DC_ADDR.Location = System.Drawing.Point(645, 244)
		self._Label_DC_ADDR.Name = "Label_DC_ADDR"
		self._Label_DC_ADDR.Size = System.Drawing.Size(74, 28)
		self._Label_DC_ADDR.TabIndex = 44
		self._Label_DC_ADDR.Text = "Address :"
		self._Label_DC_ADDR.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_DC_DQ
		# 
		self._Label_DC_DQ.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_DC_DQ.Location = System.Drawing.Point(680, 216)
		self._Label_DC_DQ.Name = "Label_DC_DQ"
		self._Label_DC_DQ.Size = System.Drawing.Size(40, 28)
		self._Label_DC_DQ.TabIndex = 43
		self._Label_DC_DQ.Text = "DQ :"
		self._Label_DC_DQ.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_Info
		# 
		self._Label_Info.Font = System.Drawing.Font("Arial", 9)
		self._Label_Info.Location = System.Drawing.Point(10, 485)
		self._Label_Info.Name = "Label_Info"
		self._Label_Info.Size = System.Drawing.Size(860, 23)
		self._Label_Info.TabIndex = 41
		self._Label_Info.Text = "* Vcent_DQ will be automatically calculated after Target Net Setup. To use manual Vcent_DQ, check \"Edit enable\" and enter the value for Vcent_DQ."
		self._Label_Info.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# CheckedListBox_ReportName
		# 
		self._CheckedListBox_ReportName.FormattingEnabled = True
		self._CheckedListBox_ReportName.Font = System.Drawing.Font("Arial", 9)
		self._CheckedListBox_ReportName.Location = System.Drawing.Point(451, 57)
		self._CheckedListBox_ReportName.Name = "CheckedListBox_ReportName"
		self._CheckedListBox_ReportName.Size = System.Drawing.Size(198, 52)
		self._CheckedListBox_ReportName.TabIndex = 31
		self._CheckedListBox_ReportName.SelectedIndexChanged += self.CheckedListBox_ReportNameSelectedIndexChanged
		# 
		# ComboBox_DDRGen
		# 
		self._ComboBox_DDRGen.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._ComboBox_DDRGen.FormattingEnabled = True
		self._ComboBox_DDRGen.Location = System.Drawing.Point(137, 117)
		self._ComboBox_DDRGen.Name = "ComboBox_DDRGen"
		self._ComboBox_DDRGen.Size = System.Drawing.Size(198, 24)
		self._ComboBox_DDRGen.TabIndex = 14
		self._ComboBox_DDRGen.Enabled = False
		self._ComboBox_DDRGen.SelectedIndexChanged += self.ComboBox_DDRGenSelectedIndexChanged
		# 
		# ComboBox_DataRate
		# 
		self._ComboBox_DataRate.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._ComboBox_DataRate.FormattingEnabled = True
		self._ComboBox_DataRate.Location = System.Drawing.Point(451, 117)
		self._ComboBox_DataRate.Name = "ComboBox_DataRate"
		self._ComboBox_DataRate.Size = System.Drawing.Size(156, 24)
		self._ComboBox_DataRate.TabIndex = 20
		self._ComboBox_DataRate.Enabled = False
		self._ComboBox_DataRate.SelectedIndexChanged += self.ComboBox_DataRateSelectedIndexChanged		
		# 
		# ComboBox_SolutionName
		# 
		self._ComboBox_SolutionName.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._ComboBox_SolutionName.FormattingEnabled = True
		self._ComboBox_SolutionName.Location = System.Drawing.Point(137, 87)
		self._ComboBox_SolutionName.Name = "ComboBox_SolutionName"
		self._ComboBox_SolutionName.Size = System.Drawing.Size(198, 24)
		self._ComboBox_SolutionName.TabIndex = 27		
		# 
		# ComboBox_Design
		# 
		self._ComboBox_Design.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._ComboBox_Design.FormattingEnabled = True
		self._ComboBox_Design.Location = System.Drawing.Point(137, 57)
		self._ComboBox_Design.Name = "ComboBox_Design"
		self._ComboBox_Design.Size = System.Drawing.Size(198, 24)
		self._ComboBox_Design.TabIndex = 28
		self._ComboBox_Design.SelectedIndexChanged += self.ComboBox_DesignSelectedIndexChanged
		# 
		# ComboBox_AC_DQ
		# 
		self._ComboBox_AC_DQ.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._ComboBox_AC_DQ.FormattingEnabled = True
		self._ComboBox_AC_DQ.Location = System.Drawing.Point(128, 201)
		self._ComboBox_AC_DQ.Name = "ComboBox_AC_DQ"
		self._ComboBox_AC_DQ.Size = System.Drawing.Size(73, 24)
		self._ComboBox_AC_DQ.TabIndex = 46
		self._ComboBox_AC_DQ.Visible = False
		self._ComboBox_AC_DQ.SelectedIndexChanged += self.ComboBox_AC_DQSelectedIndexChanged
		# 
		# ComboBox_AC_ADDR
		# 
		self._ComboBox_AC_ADDR.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._ComboBox_AC_ADDR.FormattingEnabled = True
		self._ComboBox_AC_ADDR.Location = System.Drawing.Point(128, 230)
		self._ComboBox_AC_ADDR.Name = "ComboBox_AC_ADDR"
		self._ComboBox_AC_ADDR.Size = System.Drawing.Size(73, 24)
		self._ComboBox_AC_ADDR.TabIndex = 48
		self._ComboBox_AC_ADDR.Visible = False
		self._ComboBox_AC_ADDR.SelectedIndexChanged += self.ComboBox_AC_ADDRSelectedIndexChanged
		# 
		# TextBox_InputFile
		# 
		self._TextBox_InputFile.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_InputFile.Location = System.Drawing.Point(137, 22)
		self._TextBox_InputFile.Name = "TextBox_InputFile"
		self._TextBox_InputFile.Size = System.Drawing.Size(470, 23)
		self._TextBox_InputFile.TabIndex = 13
		# 
		# TextBox_AC_DQ
		#
		self._TextBox_AC_DQ.BackColor = System.Drawing.Color.WhiteSmoke
		self._TextBox_AC_DQ.ReadOnly = True
		self._TextBox_AC_DQ.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_AC_DQ.Location = System.Drawing.Point(128, 201)
		self._TextBox_AC_DQ.Name = "TextBox_AC_DQ"
		self._TextBox_AC_DQ.Size = System.Drawing.Size(71, 23)
		self._TextBox_AC_DQ.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
		self._TextBox_AC_DQ.TabIndex = 27
		# 
		# TextBox_AC_ADDR
		# 
		self._TextBox_AC_ADDR.BackColor = System.Drawing.Color.WhiteSmoke
		self._TextBox_AC_ADDR.ReadOnly = True
		self._TextBox_AC_ADDR.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_AC_ADDR.Location = System.Drawing.Point(128, 230)
		self._TextBox_AC_ADDR.Name = "TextBox_AC_ADDR"
		self._TextBox_AC_ADDR.Size = System.Drawing.Size(71, 23)
		self._TextBox_AC_ADDR.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
		self._TextBox_AC_ADDR.TabIndex = 39
		# 
		# TextBox_DC_DQ
		# 
		self._TextBox_DC_DQ.BackColor = System.Drawing.Color.WhiteSmoke
		self._TextBox_DC_DQ.ReadOnly = True
		self._TextBox_DC_DQ.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_DC_DQ.Location = System.Drawing.Point(722, 219)
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
		self._TextBox_DC_ADDR.Location = System.Drawing.Point(722, 248)
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
		self._TextBox_Vref.Location = System.Drawing.Point(164, 267)
		self._TextBox_Vref.Name = "TextBox_Vref"
		self._TextBox_Vref.Size = System.Drawing.Size(57, 23)
		self._TextBox_Vref.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
		self._TextBox_Vref.TabIndex = 34		
		# 
		# TextBox_DQSetup
		# 
		self._TextBox_DQSetup.BackColor = System.Drawing.Color.WhiteSmoke
		self._TextBox_DQSetup.ReadOnly = True
		self._TextBox_DQSetup.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_DQSetup.Location = System.Drawing.Point(386, 452)
		self._TextBox_DQSetup.Name = "TextBox_DQSetup"
		self._TextBox_DQSetup.Size = System.Drawing.Size(50, 23)
		self._TextBox_DQSetup.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
		self._TextBox_DQSetup.TabIndex = 28
		# 
		# TextBox_DQHold
		# 
		self._TextBox_DQHold.BackColor = System.Drawing.Color.WhiteSmoke
		self._TextBox_DQHold.ReadOnly = True
		self._TextBox_DQHold.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_DQHold.Location = System.Drawing.Point(447, 452)
		self._TextBox_DQHold.Name = "TextBox_DQHold"
		self._TextBox_DQHold.Size = System.Drawing.Size(58, 23)
		self._TextBox_DQHold.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
		self._TextBox_DQHold.TabIndex = 29
		# 
		# TextBox_ADDRSetup
		# 
		self._TextBox_ADDRSetup.BackColor = System.Drawing.Color.WhiteSmoke
		self._TextBox_ADDRSetup.ReadOnly = True
		self._TextBox_ADDRSetup.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_ADDRSetup.Location = System.Drawing.Point(386, 481)
		self._TextBox_ADDRSetup.Name = "TextBox_ADDRSetup"
		self._TextBox_ADDRSetup.Size = System.Drawing.Size(50, 23)
		self._TextBox_ADDRSetup.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
		self._TextBox_ADDRSetup.TabIndex = 30
		# 
		# TextBox_ADDRHold
		# 
		self._TextBox_ADDRHold.BackColor = System.Drawing.Color.WhiteSmoke
		self._TextBox_ADDRHold.ReadOnly = True
		self._TextBox_ADDRHold.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_ADDRHold.Location = System.Drawing.Point(447, 481)
		self._TextBox_ADDRHold.Name = "TextBox_ADDRHold"
		self._TextBox_ADDRHold.Size = System.Drawing.Size(58, 23)
		self._TextBox_ADDRHold.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
		self._TextBox_ADDRHold.TabIndex = 31
		# 
		# TextBox_VdIVW
		# 
		self._TextBox_VdIVW.BackColor = System.Drawing.Color.WhiteSmoke
		self._TextBox_VdIVW.ReadOnly = True
		self._TextBox_VdIVW.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_VdIVW.Location = System.Drawing.Point(132, 271)
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
		self._TextBox_TdIVW.Location = System.Drawing.Point(425, 346)
		self._TextBox_TdIVW.Name = "TextBox_TdIVW"
		self._TextBox_TdIVW.Size = System.Drawing.Size(59, 23)
		self._TextBox_TdIVW.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
		self._TextBox_TdIVW.TabIndex = 39
		# 
		# TextBox_VcentDQ
		# 
		self._TextBox_VcentDQ.BackColor = System.Drawing.Color.WhiteSmoke
		self._TextBox_VcentDQ.ReadOnly = True
		self._TextBox_VcentDQ.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_VcentDQ.Location = System.Drawing.Point(698, 262)
		self._TextBox_VcentDQ.Name = "TextBox_VcentDQ"
		self._TextBox_VcentDQ.Size = System.Drawing.Size(59, 23)
		self._TextBox_VcentDQ.TextAlign = System.Windows.Forms.HorizontalAlignment.Right
		self._TextBox_VcentDQ.TabIndex = 34
		# 
		# Button_Import
		# 
		self._Button_Import.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_Import.Location = System.Drawing.Point(613, 22)
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
		self._Button_ViewNet.Location = System.Drawing.Point(703, 111)
		self._Button_ViewNet.Name = "Button_ViewNet"
		self._Button_ViewNet.Size = System.Drawing.Size(188, 42)
		self._Button_ViewNet.TabIndex = 27
		self._Button_ViewNet.Text = "Target Net Setup"
		self._Button_ViewNet.UseVisualStyleBackColor = True
		self._Button_ViewNet.Enabled = False
		self._Button_ViewNet.Click += self.Button_ViewNetClick		
		# 
		# Button_Analyze
		# 
		self._Button_Analyze.Font = System.Drawing.Font("Arial", 12, System.Drawing.FontStyle.Bold)
		self._Button_Analyze.Location = System.Drawing.Point(703, 161)
		self._Button_Analyze.Name = "Button_Analyze"
		self._Button_Analyze.Size = System.Drawing.Size(188, 42)
		self._Button_Analyze.TabIndex = 35
		self._Button_Analyze.Text = "Analyze"
		self._Button_Analyze.UseVisualStyleBackColor = True
		self._Button_Analyze.Enabled = False
		self._Button_Analyze.Click += self.Button_AnalyzeClick
		# 
		# Button_ViewResult
		# 
		self._Button_ViewResult.Font = System.Drawing.Font("Arial", 12, System.Drawing.FontStyle.Bold)
		self._Button_ViewResult.Location = System.Drawing.Point(703, 211)
		self._Button_ViewResult.Name = "Button_ViewResult"
		self._Button_ViewResult.Size = System.Drawing.Size(188, 42)
		self._Button_ViewResult.TabIndex = 35
		self._Button_ViewResult.Text = "View Result"
		self._Button_ViewResult.UseVisualStyleBackColor = True
		self._Button_ViewResult.Enabled = False
		self._Button_ViewResult.Click += self.Button_ViewResultClick
		# 
		# Button_ImgShow
		#
		self._Button_ImgShow.FlatStyle = System.Windows.Forms.FlatStyle.Standard
		self._Button_ImgShow.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_ImgShow.Location = System.Drawing.Point(818, 8)
		self._Button_ImgShow.Name = "Button_ImgShow"
		self._Button_ImgShow.Size = System.Drawing.Size(60, 28)
		self._Button_ImgShow.TabIndex = 43
		self._Button_ImgShow.Text = 'Hide'
		self._Button_ImgShow.UseVisualStyleBackColor = True
		self._Button_ImgShow.Click += self.Button_ImgShowClick
		# 
		# Button_Debug
		# 
		self._Button_Debug.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_Debug.Location = System.Drawing.Point(811, 12)
		self._Button_Debug.Name = "Button_Debug"
		self._Button_Debug.Size = System.Drawing.Size(80, 38)
		self._Button_Debug.TabIndex = 29
		self._Button_Debug.Text = "Debug"
		self._Button_Debug.UseVisualStyleBackColor = True
		self._Button_Debug.Visible = sub_DB.Debug_Mode
		self._Button_Debug.Click += self.Button_DebugClick
		# 
		# CheckBox_AnalyzeDQ
		# 
		self._CheckBox_AnalyzeDQ.Font = System.Drawing.Font("Arial", 10)
		self._CheckBox_AnalyzeDQ.Location = System.Drawing.Point(716, 29)
		self._CheckBox_AnalyzeDQ.Name = "CheckBox_AnalyzeDQ"
		self._CheckBox_AnalyzeDQ.Size = System.Drawing.Size(138, 29)
		self._CheckBox_AnalyzeDQ.TabIndex = 36
		self._CheckBox_AnalyzeDQ.Text = "Analyze DQ"
		self._CheckBox_AnalyzeDQ.UseVisualStyleBackColor = True
		# 
		# CheckBox_AnalyzeADDR
		# 
		self._CheckBox_AnalyzeADDR.Font = System.Drawing.Font("Arial", 10)
		self._CheckBox_AnalyzeADDR.Location = System.Drawing.Point(716, 55)
		self._CheckBox_AnalyzeADDR.Name = "CheckBox_AnalyzeADDR"
		self._CheckBox_AnalyzeADDR.Size = System.Drawing.Size(138, 29)
		self._CheckBox_AnalyzeADDR.TabIndex = 37
		self._CheckBox_AnalyzeADDR.Text = "Analyze Address"
		self._CheckBox_AnalyzeADDR.UseVisualStyleBackColor = True
		# 
		# CheckBox_EditEnable_NewEye
		# 
		self._CheckBox_EditEnable_NewEye.Font = System.Drawing.Font("Arial", 10)
		self._CheckBox_EditEnable_NewEye.Location = System.Drawing.Point(775, 458)
		self._CheckBox_EditEnable_NewEye.Name = "CheckBox_EditEnable_NewEye"
		self._CheckBox_EditEnable_NewEye.Size = System.Drawing.Size(100, 29)
		self._CheckBox_EditEnable_NewEye.TabIndex = 40
		self._CheckBox_EditEnable_NewEye.Text = "Edit enable"
		self._CheckBox_EditEnable_NewEye.UseVisualStyleBackColor = True
		self._CheckBox_EditEnable_NewEye.CheckedChanged += self.CheckBox_EditEnable_NewEyeCheckedChanged
		# 
		# CheckBox_EditEnable_OldEye
		# 
		self._CheckBox_EditEnable_OldEye.Font = System.Drawing.Font("Arial", 10)
		self._CheckBox_EditEnable_OldEye.Location = System.Drawing.Point(775, 458)
		self._CheckBox_EditEnable_OldEye.Name = "CheckBox_EditEnable_OldEye"
		self._CheckBox_EditEnable_OldEye.Size = System.Drawing.Size(100, 29)
		self._CheckBox_EditEnable_OldEye.TabIndex = 40
		self._CheckBox_EditEnable_OldEye.Text = "Edit enable"
		self._CheckBox_EditEnable_OldEye.UseVisualStyleBackColor = True
		self._CheckBox_EditEnable_OldEye.CheckedChanged += self.CheckBox_EditEnable_OldEyeCheckedChanged
		# 
		# openFileDialog1
		# 
		self._openFileDialog1.FileName = "openFileDialog1"
		# 
		# Eye_Form
		# 
		self.ClientSize = System.Drawing.Size(904, 780)
		self.MinimumSize = System.Drawing.Size(self.Size.Width, self.Size.Height)
		#self.MaximumSize = System.Drawing.Size(self.Size.Width, self.Size.Height)
		self.FormSize_W = self.Size.Width
		self.FormSize_H = self.Size.Height
		self.Image_flag = False
		self.Controls.Add(self._Button_Debug)
		self.Controls.Add(self._GroupBox_NewEye)
		self.Controls.Add(self._Button_Analyze)
		self.Controls.Add(self._Button_ViewNet)
		self.Controls.Add(self._Button_ViewResult)
		self.Controls.Add(self._GroupBox_OldEye)
		self.Controls.Add(self._PictureBox_Logo)
		self.Controls.Add(self._Label_Version)
		self.Controls.Add(self._GroupBox_Setup)
		self.Controls.Add(self._MenuStrip)
		self.MainMenuStrip = self._MenuStrip
		IconFile = path + "\\Resources\\LOGO.ico"
		self.Icon = Icon(IconFile)
		self.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen		
		self.Name = "Eye_Form"
		self.Text = "ANSYS DDR Eye Analyzer"
		self.Load += self.Eye_FormLoad
		self.ResizeEnd += self.Eye_FormResizeEnd
		self.FormClosing += self.Eye_FormFormClosing
		self._MenuStrip.ResumeLayout(False)
		self._MenuStrip.PerformLayout()
		self._GroupBox_Setup.ResumeLayout(False)
		self._GroupBox_Setup.PerformLayout()
		self._PictureBox_Logo.EndInit()
		self._GroupBox_OldEye.ResumeLayout(False)
		self._GroupBox_OldEye.PerformLayout()
		self._PictureBox_OldEye.EndInit()
		self._GroupBox_UnitOld.ResumeLayout(False)
		self._GroupBox_NewEye.ResumeLayout(False)
		self._GroupBox_NewEye.PerformLayout()
		self._GroupBox_UnitNew.ResumeLayout(False)
		self._PictureBox_NewEye.EndInit()
		self.ResumeLayout(False)

	''' Eye_Form - Events '''	
	def Eye_FormLoad(self, sender, e):
		try:
			# initialization
			self._TextBox_InputFile.BackColor = System.Drawing.SystemColors.Info

			# Setup the Common Env. Info.		
			#	Add DDR Type into ComboBox
			DDR_Gen = []
			for key in sub_DB.Cenv:
				if "[DDR Info]" in key:
					DDR_Gen.append(key.split("<")[-1].split(">")[0])

			DDR_Gen.sort()
			for ddr in DDR_Gen:
				self._ComboBox_DDRGen.Items.Add(ddr)

			# Setup the User Env. Info.
			if "(Input File)<Setup>[EYE]" in sub_DB.Uenv:
				self._TextBox_InputFile.Text = sub_DB.Uenv["(Input File)<Setup>[EYE]"][0]
			
				# for *.aedt Input File
				if sub_DB.Uenv["(Input File)<Setup>[EYE]"][0].strip().split("\\")[-1].split(".")[-1] == "aedt":				
					sub_AEDT.Get_AEDT_Info(self, sub_DB.Uenv["(Input File)<Setup>[EYE]"][0])

				# for *.csv Input File
				elif sub_DB.Uenv["(Input File)<Setup>[EYE]"][0].strip().split("\\")[-1].split(".")[-1] == "csv":
					pass
				#elif sub_DB.Uenv["(Input File)<Setup>[EYE]"][0].strip().split("\\")[-1].split(".")[-1] == "tr0":
			else:	
				pass

		except Exception as e:			
			Log("[Eye_FormLoad] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to load Eye Analyzer main GUI","Warning")			
			EXIT()

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
			self._ComboBox_DataRate.Size = System.Drawing.Size(self._ComboBox_DataRate.Width + Gap_W/2, self._ComboBox_DataRate.Height)
			self._CheckedListBox_ReportName.Size = System.Drawing.Size(self._CheckedListBox_ReportName.Width + Gap_W/2, self._CheckedListBox_ReportName.Height)

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

		except Exception as e:			
			Log("[Eye_FormResizeEnd] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to resize Eye Analyzer main GUI","Warning")			
			EXIT()

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
			dialog.InitialDirectory = path + "\\Resources"
			dialog.Filter = "DDR wizard configuration file|*.cnf"
			dialog.Title = "Select ANSYS DDR Wizard Configuration File"
			if dialog.ShowDialog(self) == DialogResult.OK:
				File = dialog.FileName
				# Parse DDR Configuration File
				# Get Defined Data
				Uenv = Load_env(File)
				Uenv["File"] = File
				sub_DB.Uenv = Uenv
				Log("[Load Configuration File] = %s" % File)
				sub_DB.Net_Form.Init_Flag = True
				sub_DB.Net_Form._DataGridView.Rows.Clear()
				MessageBox.Show("DDR wizard configuration file \"%s\" is loaded" % File.split("\\")[-1], "Load")

			else:
				MessageBox.Show("Please Select the DDR wizard configuration file(*.cnf)","Warning")

		except Exception as e:			
			Log("[Load Configuration File] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to load DDR Wizard configuration file","Warning")
			EXIT()

	def UserConf_Save_ToolStripMenuItemClick(self, sender, e):
		# TBD
		pass

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

	def Help_DDRHelp_ToolStripMenuItemClick(self, sender, e):
		MessageBox.Show("ANSYS DDR Wizard Help", "To Be Done")
		pass

	def Help_DDRGuid_ToolStripMenuItemClick(self, sender, e):
		MessageBox.Show("ANSYS DDR Wizard User Guide", "To be done")
		pass

	def Help_DDRNew_ToolStripMenuItemClick(self, sender, e):
		MessageBox.Show("ANSYS DDR Wizard What's New", "To be done")
		pass

	def Help_DDRAbout_ToolStripMenuItemClick(self, sender, e):
		MessageBox.Show("About ANSYS DDR Wizard", "To be done")
		pass

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

		self._TextBox_AC_DQ.ReadOnly = not self._CheckBox_EditEnable_OldEye.Checked
		self._TextBox_AC_ADDR.ReadOnly = not self._CheckBox_EditEnable_OldEye.Checked
		self._TextBox_DC_DQ.ReadOnly = not self._CheckBox_EditEnable_OldEye.Checked
		self._TextBox_DC_ADDR.ReadOnly = not self._CheckBox_EditEnable_OldEye.Checked
		self._TextBox_Vref.ReadOnly = not self._CheckBox_EditEnable_OldEye.Checked
		self._TextBox_DQSetup.ReadOnly = not self._CheckBox_EditEnable_OldEye.Checked
		self._TextBox_DQHold.ReadOnly = not self._CheckBox_EditEnable_OldEye.Checked
		self._TextBox_ADDRSetup.ReadOnly = not self._CheckBox_EditEnable_OldEye.Checked
		self._TextBox_ADDRHold.ReadOnly = not self._CheckBox_EditEnable_OldEye.Checked

	def ComboBox_AC_DQSelectedIndexChanged(self, sender, e):		
		keyword = "<" + self._ComboBox_DDRGen.Text + "-" + self._ComboBox_DataRate.Text + ">" + "[Eye Spec]"
		for key in sub_DB.Cenv:
			if keyword in key:
				if "DQ Setup" in key and self._ComboBox_AC_DQ.Text in key:
					self._TextBox_DQSetup.Text = sub_DB.Cenv[key][0]

	def ComboBox_AC_ADDRSelectedIndexChanged(self, sender, e):		
		keyword = "<" + self._ComboBox_DDRGen.Text + "-" + self._ComboBox_DataRate.Text + ">" + "[Eye Spec]"
		for key in sub_DB.Cenv:
			if keyword in key:
				if "ADDR Setup" in key and self._ComboBox_AC_ADDR.Text in key:
					self._TextBox_ADDRSetup.Text = sub_DB.Cenv[key][0]

	def Button_ImportClick(self, sender, e):
		try:
			dialog = OpenFileDialog()
			dialog.InitialDirectory = sub_DB.Uenv["(Initial Input File Directory)<Setup>[Eye]"][0]
			dialog.Filter = "AEDT Project file|*.aedt|Comma delimited data file|*.csv"

			if dialog.ShowDialog(self) == DialogResult.OK:
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

				Initial()

				# for *.aedt File
				if extension == "aedt":
					Log("[Input File Type] = AEDT")
					Log("	<Input File> = %s" % File)
					self.TopMost = True
					self.Cursor = Cursors.WaitCursor				
					sub_AEDT.Get_AEDT_Info(self, File)
					self.Cursor = Cursors.Default
					self.TopMost = False

					self._ComboBox_Design.Enabled = True
					self._CheckedListBox_ReportName.Enabled = True
					self._ComboBox_SolutionName.Enabled = True
					self._CheckedListBox_ReportName.BackColor = System.Drawing.SystemColors.Window

					self._TextBox_InputFile.BackColor = System.Drawing.SystemColors.Window
					self._ComboBox_Design.BackColor = System.Drawing.SystemColors.Info				
					self._ComboBox_Design.SelectedIndex = 0
					sub_DB.InputFile_Flag = 1

				# for *.csv File
				elif extension == "csv":
					Log("[Input File Type] = CSV")
					Log("	<Input File> = %s" % File)
					# Disable unnecessary component
					self._TextBox_InputFile.BackColor = System.Drawing.SystemColors.Window
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

				# for *.tr0 File
				elif extension == "tr0":

					pass

			else:
				MessageBox.Show("Please Select the Input File(*.aedt or *.csv)","Warning")

		except Exception as e:			
			Log("[Input File Import] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to import Input File\n%s" % File,"Warning")			
			EXIT()

	def ComboBox_DesignSelectedIndexChanged(self, sender, e):
		try:
			# Initialization 
			sub_DB.Net_Form.Init_Flag = True
			self._CheckedListBox_ReportName.Items.Clear()		

			oProject = sub_DB.AEDT["Project"]
			oDesign = oProject.SetActiveDesign(self._ComboBox_Design.SelectedItem)
			Log("[AEDT Design] = %s" % self._ComboBox_Design.Text)

			# Get Solutions
			self._ComboBox_SolutionName.Items.Clear()
			Sim_type = oDesign.GetDesignType()			
			if Sim_type == "Circuit Netlist":
				self._ComboBox_SolutionName.Items.Add("TRAN")
				self._ComboBox_SolutionName.SelectedIndex = 0
			else:
				oModule = oDesign.GetModule("SimSetup")
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
			self._CheckedListBox_ReportName.SetItemChecked(0, True)

			# Set Next Step
			self._ComboBox_Design.BackColor = System.Drawing.SystemColors.Window
			self._ComboBox_DDRGen.BackColor = System.Drawing.SystemColors.Info
			self._ComboBox_DDRGen.Enabled = True
		
			# Back-up the AEDT Info
			sub_DB.AEDT["Design"] = oDesign
			sub_DB.AEDT["Module"] = oModule

		except Exception as e:			
			Log("[AEDT Design] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to set AEDT Design","Warning")
			EXIT()

	def CheckedListBox_ReportNameSelectedIndexChanged(self, sender, e):

		sub_DB.Net_Form.Init_Flag = True		

	def ComboBox_DDRGenSelectedIndexChanged(self, sender, e):
		try:
			# Initialization
			sub_DB.Net_Form.Init_Flag = True
			self._ComboBox_DDRGen.BackColor = System.Drawing.SystemColors.Window
			self._ComboBox_DataRate.BackColor = System.Drawing.SystemColors.Info
			self._ComboBox_DataRate.Enabled = True
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

			# Set Eye Vaildation Type according to DDR Gen.
			DDR_Gen = self._ComboBox_DDRGen.Text
			if DDR_Gen.find("DDR4") != -1 or DDR_Gen.find("DDR5") != -1:
				self._GroupBox_NewEye.Visible = True
				self._GroupBox_OldEye.Visible = False			
				sub_DB.Eyeflag = True
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

			# Clear Eye Spec.
			if sub_DB.Eyeflag:
				self._TextBox_VdIVW.Text = ""
				self._TextBox_TdIVW.Text = ""
				self._TextBox_VcentDQ.Text = ""			
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
			self._ComboBox_AC_DQ.Items.Clear()
			self._ComboBox_AC_ADDR.Items.Clear()		
			self._ComboBox_DataRate.BackColor = System.Drawing.SystemColors.Window
			self._Button_ViewNet.Enabled = True
			self._Button_ViewNet.BackColor = System.Drawing.SystemColors.Info

			# Get Keywork
			#	ex) <DDR3-800>
			keyword = "<" + self._ComboBox_DDRGen.Text + "-" + self._ComboBox_DataRate.Text + ">" + "[Eye Spec]"
			Log("[DDR datarate] = %s" % self._ComboBox_DataRate.Text)

			# Set Eye Specifications
			#	for New Eye		
			if sub_DB.Eyeflag: 
				if self._ComboBox_DDRGen.Text == "DDR4":
					for key in sub_DB.Cenv:
						if keyword in key:
							if "Rx Mask Voltage" in key:
								if "!" in sub_DB.Cenv[key][0]:									
									MessageBox.Show("The JEDEC specification, ""VdIVW"" for the %s-%s you chose has not been decided yet, so the DDR Wizard has set the value arbitrarily based on the specification of the commercial DDR product." % (self._ComboBox_DDRGen.Text, self._ComboBox_DataRate.Text),"Warning")
									self._TextBox_VdIVW.BackColor = System.Drawing.Color.PeachPuff
									self._TextBox_VdIVW.Text = sub_DB.Cenv[key][0].replace("!","")
								else:									
									self._TextBox_VdIVW.Text = sub_DB.Cenv[key][0]
								Log("	<VdIVW> : %s" % self._TextBox_VdIVW.Text)

							elif "Rx Timing Window Total" in key:
								if "!" in sub_DB.Cenv[key][0]:
									MessageBox.Show("The JEDEC specification, ""TdIVW"" for the ""%s-%s"" you chose has not been decided yet, so the DDR Wizard has set the value arbitrarily based on the specification of the commercial DDR product." % (self._ComboBox_DDRGen.Text,	self._ComboBox_DataRate.Text),"Warning")
									self._TextBox_TdIVW.BackColor = System.Drawing.Color.PeachPuff
									self._TextBox_TdIVW.Text = sub_DB.Cenv[key][0].replace("!","")
								else:
									self._TextBox_TdIVW.Text = sub_DB.Cenv[key][0]
								Log("	<TdIVW> : %s" % self._TextBox_TdIVW.Text)

				elif self._ComboBox_DDRGen.Text == "DDR5":
					pass

				elif self._ComboBox_DDRGen.Text == "LPDDR4":
					pass

				elif self._ComboBox_DDRGen.Text == "LPDDR5":
					pass

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
							
							elif "DC Th" in key and "DQ" in key:
								self._TextBox_DC_DQ.Text = sub_DB.Cenv[key][0]

							elif "AC Th" in key and "CA" in key:
								for val in sub_DB.Cenv[key]:
									self._ComboBox_AC_ADDR.Items.Add(val)
								self._ComboBox_AC_ADDR.SelectedIndex = 0
							
							elif "DC Th" in key and "CA" in key:
								self._TextBox_DC_ADDR.Text = sub_DB.Cenv[key][0]

							elif "DQ Setup" in key and self._ComboBox_AC_DQ.Text in key:
								self._TextBox_DQSetup.Text = sub_DB.Cenv[key][0]
							
							elif "DQ Hold" in key and self._TextBox_DC_DQ.Text in key:
								self._TextBox_DQHold.Text = sub_DB.Cenv[key][0]

							elif "ADDR Setup" in key and self._ComboBox_AC_ADDR.Text in key:
								self._TextBox_ADDRSetup.Text = sub_DB.Cenv[key][0]
							
							elif "ADDR Hold" in key and self._TextBox_DC_ADDR.Text in key:
								self._TextBox_ADDRHold.Text = sub_DB.Cenv[key][0]
							
							elif "VREF" in key:
								self._TextBox_Vref.Text = sub_DB.Cenv[key][0]

				elif self._ComboBox_DDRGen.Text == "LPDDR2":
					pass
				elif self._ComboBox_DDRGen.Text == "LPDDR3":
					pass

		except Exception as e:			
			Log("[DDR datarate] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to set DDR datarate","Warning")
			EXIT()

	def Button_ViewNetClick(self, sender, e):
		try:
			# Target Net Setup			
			Check_spec()
			sub_DB.Net_Form.StartPosition = System.Windows.Forms.FormStartPosition.Manual
			sub_DB.Net_Form.Location = System.Drawing.Point(sub_DB.Eye_Form.Location.X + sub_DB.Eye_Form.Size.Width, sub_DB.Eye_Form.Location.Y)
			sub_DB.Net_Form.Text = "Target Net Setup - " + sub_DB.Uenv["File"].split("\\")[-1]
			if sub_DB.Net_Form._DataGridView.Columns.Count > 5:			
				sub_DB.Net_Form._DataGridView.Columns[6].DisplayIndex = 6
				sub_DB.Net_Form._DataGridView.Columns[5].DisplayIndex = 5
				sub_DB.Net_Form._DataGridView.Columns[4].DisplayIndex = 4
			sub_DB.Net_Form.ShowDialog()

			self._Button_ViewNet.BackColor = System.Drawing.SystemColors.Control
			self._Button_Analyze.Enabled = True
			self._Button_Analyze.BackColor = System.Drawing.SystemColors.Info

		except Exception as e:			
			Log("[Net Form Launch] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to launch Net Classification Form","Warning")			
			EXIT()

	def Button_AnalyzeClick(self, sender, e):
		try:			
			Log("[Eye Analyze Start] = %s" % time.strftime('%Y.%m.%d, %H:%M:%S'))
			# Initiallization
			sub_DB.Excel_Img_File = []

			''' '''''''''''''''''''''''''''''''''''''
			# Calculate Maximum Process Value
			''''''''''''''''''''''''''''''''''''' '''
			# New Eye
			if sub_DB.Eyeflag:
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
					#if sub_DB.AEDT == {}:
					#	self.TopMost = True
					#	self.Cursor = Cursors.WaitCursor
					#	sub_AEDT.Get_AEDT_Info(self, sub_DB.File)
					#	self.Cursor = Cursors.Default
					#	self.TopMost = False
					#	sub_DB.AEDT["Design"] = sub_DB.AEDT["Project"].SetActiveDesign(self._ComboBox_Design.SelectedItem)

					max_val = 5 + 4 + iter1
					if sub_DB.Option_Form._CheckBox_PlotEye.Checked:
						max_val = max_val + iter				

				# *.csv Input
				elif sub_DB.InputFile_Flag == 2:
					max_val = 5 + 3 + iter1
					if sub_DB.Option_Form._CheckBox_PlotEye.Checked:
						max_val = max_val + iter
			# Old Eye
			else:
				pass

			''' '''''''''''''''''''''''''''''''''''''
			# Show Option Form for Eye Analyzer		
			''''''''''''''''''''''''''''''''''''' '''
			result = sub_DB.Option_Form.ShowDialog()		
			self._Options_ToolStripMenuItem.Enabled = True

			# Press OK Button in Option Form
			if result == DialogResult.OK:
				# for New Eye		
				if sub_DB.Eyeflag:
					
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

					#########################
					#   Vref Calculation    #
					#########################
					try:
						sub_DB.Cal_Form.Text = "Calculating Vcent_DQ"
						sub_DB.Cal_Form._Label_Vref.Text = "Calculating Vcent_DQ..."
						sub_DB.Cal_Form._ProgressBar_Vref.Value += 1	

						if sub_DB.InputFile_Flag == 1: # *.aedt input
							Vref = Cal_Vref_AEDT(self, Location)
						
						elif sub_DB.InputFile_Flag == 2: # *.csv input					
							Vref = Cal_Vref_WaveForm()

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
									sub_DB.AEDT["Desktop"].CloseProject(AEDT_File.split("\\")[-1].split(".")[0])
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
							if sub_DB.InputFile_Flag == 1:
								Create_Excel_Report()
							elif sub_DB.InputFile_Flag == 2:
								Create_Excel_Report_Imported()
							Log("	<Create Excel Report> = Done")

						else:
							Log("	<Create Excel Report> = False")

						sub_DB.Cal_Form.Close()
						self.Cursor = Cursors.Default			
						sub_DB.Cal_Form.Cursor = Cursors.Default

						os.startfile(sub_DB.result_dir)
						sub_DB.Result_Flag = True
						sub_DB.Net_Form.ShowDialog()
						sub_DB.Result_Flag = False
						#sub_DB.Net_Form.Init_Flag = True						

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

				# for Old Eye
				else:
					pass

				self._Button_Analyze.BackColor = System.Drawing.SystemColors.Control
				self._Button_ViewResult.Enabled = True

			# Press Cancel Button in Option Form
			else:
				pass

		except Exception as e:			
			Log("[Eye Analyze Start] = Fail")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to start Eye Analyze","Warning")			
			EXIT()
		
	def Button_ViewResultClick(self, sender, e):
		try:
			Log("[View Eye Analyze Result]")
			sub_DB.Result_Flag = True
			sub_DB.Net_Form._DataGridView.Columns[5].DisplayIndex = 2
			sub_DB.Net_Form._DataGridView.Columns[6].DisplayIndex = 3
			sub_DB.Net_Form._DataGridView.Columns[4].DisplayIndex = 4
			sub_DB.Net_Form.ShowDialog()
			sub_DB.Result_Flag = False

		except Exception as e:			
			Log("[View Eye Analyze Result] = Fail")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to View Eye Analyze Result","Warning")			
			EXIT()

	def Button_ImgShowClick(self, sender, e):
		# TODO : Button Image Show Click Event
		self.Image_flag = not self.Image_flag
		if self.Image_flag:
			self._Button_ImgShow.Text = "Show"
		else:
			self._Button_ImgShow.Text = "Hide"

	def Eye_FormFormClosing(self, sender, e):
		sub_ScriptEnv.Release()		
		os._exit(0)

	''' For Debuggin '''
	def Button_DebugClick(self, sender, e):
		File = "D:\\1_Work\\20220106_DDR_Compliance\\0_DB\\LPDDR4_20220203\\Examples\\Galileo_R21_DDR_SSN_siwave.aedt"		
		self._TextBox_InputFile.Text = File
		extension = File.split("\\")[-1].split(".")[-1] # Get File Extension
		# for *.aedt File
		if extension == "aedt":				
			self.Cursor = Cursors.WaitCursor				
			sub_AEDT.Get_AEDT_Info(self, File)
			self.Cursor = Cursors.Default

			self._TextBox_InputFile.BackColor = System.Drawing.SystemColors.Window
			self._ComboBox_Design.BackColor = System.Drawing.SystemColors.Info
		self._ComboBox_Design.SelectedIndex = 0
		self._CheckedListBox_ReportName.SetItemChecked(0, True)
		self._ComboBox_DDRGen.SelectedIndex = 2
		self._ComboBox_DataRate.SelectedIndex = 2
		self.Button_ViewNetClick(self, sender)		
		self.Button_AnalyzeClick(self, sender)