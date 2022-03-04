import os
import time
import sys
import System.Drawing
import System.Windows.Forms
import sub_DB

from GUI_subforms import *
from sub_functions import *
from System.Drawing import *
from System.Windows.Forms import *

class StartForm(Form):
	def __init__(self):

		self.InitializeComponent()

	''' StartForm - GUI '''	
	def InitializeComponent(self):		
		global path
		path = os.path.dirname(os.path.abspath(__file__))
		self._PictureBox_EM = System.Windows.Forms.PictureBox()
		self._PictureBox_Tran = System.Windows.Forms.PictureBox()
		self._PictureBox_Eye = System.Windows.Forms.PictureBox()
		self._PictureBox_Comp = System.Windows.Forms.PictureBox()

		self._Button_Start = System.Windows.Forms.Button()
		self._Button_Debug = System.Windows.Forms.Button()

		self._MenuStrip = System.Windows.Forms.MenuStrip()
		self._File_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._DDRConf_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._DDRConf_Load_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._DDRConf_Edit_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._UserConf_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._UserConf_Load_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._UserConf_Edit_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._Exit_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._Help_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._Help_DDRHelp_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._Help_DDRGuid_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._Help_DDRNew_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._Help_DDRAbout_ToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()

		self._toolStripSeparator1 = System.Windows.Forms.ToolStripSeparator()
		self._toolStripSeparator2 = System.Windows.Forms.ToolStripSeparator()
		
		self._openFileDialog1 = System.Windows.Forms.OpenFileDialog()

		self._MenuStrip.SuspendLayout()
		self._PictureBox_EM.BeginInit()
		self._PictureBox_Tran.BeginInit()
		self._PictureBox_Eye.BeginInit()
		self._PictureBox_Comp.BeginInit()
		self.SuspendLayout()
		# 
		# PictureBox_EM
		#
		LogoFile = path + "\\Resources\\Main1_off.bmp"
		self._PictureBox_EM.BackgroundImage = Bitmap(LogoFile)
		self._PictureBox_EM.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch
		self._PictureBox_EM.Location = System.Drawing.Point(5, 34)
		self._PictureBox_EM.Name = "PictureBox_EM"
		self._PictureBox_EM.Size = System.Drawing.Size(850, 100)
		self._PictureBox_EM.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage
		self._PictureBox_EM.TabIndex = 1
		self._PictureBox_EM.TabStop = False
		self._PictureBox_EM.Click += self.PictureBox_EMClick
		# 
		# PictureBox_Tran
		# 
		LogoFile = path + "\\Resources\\Main2_off.bmp"
		self._PictureBox_Tran.BackgroundImage = Bitmap(LogoFile)
		self._PictureBox_Tran.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch
		self._PictureBox_Tran.Location = System.Drawing.Point(5, 134)
		self._PictureBox_Tran.Name = "PictureBox_Tran"
		self._PictureBox_Tran.Size = System.Drawing.Size(850, 100)
		self._PictureBox_Tran.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage
		self._PictureBox_Tran.TabIndex = 4
		self._PictureBox_Tran.TabStop = False
		self._PictureBox_Tran.Click += self.PictureBox_TranClick
		# 
		# PictureBox_Eye
		# 
		LogoFile = path + "\\Resources\\Main3_off.bmp"
		self._PictureBox_Eye.BackgroundImage = Bitmap(LogoFile)
		self._PictureBox_Eye.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch		
		self._PictureBox_Eye.Location = System.Drawing.Point(5, 234)
		self._PictureBox_Eye.Name = "PictureBox_Eye"
		self._PictureBox_Eye.Size = System.Drawing.Size(850, 100)
		self._PictureBox_Eye.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage
		self._PictureBox_Eye.TabIndex = 14
		self._PictureBox_Eye.TabStop = False
		self._PictureBox_Eye.Click += self.PictureBox_EyeClick
		# 
		# PictureBox_Comp
		# 
		LogoFile = path + "\\Resources\\Main4_off.bmp"
		self._PictureBox_Comp.BackgroundImage = Bitmap(LogoFile)
		self._PictureBox_Comp.BackgroundImageLayout = System.Windows.Forms.ImageLayout.Stretch				
		self._PictureBox_Comp.Location = System.Drawing.Point(5, 334)
		self._PictureBox_Comp.Name = "PictureBox_Comp"
		self._PictureBox_Comp.Size = System.Drawing.Size(850, 100)
		self._PictureBox_Comp.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage
		self._PictureBox_Comp.TabIndex = 15
		self._PictureBox_Comp.TabStop = False
		self._PictureBox_Comp.Click += self.PictureBox_CompClick
		# 
		# Button_Start
		# 
		self._Button_Start.Font = System.Drawing.Font("Century Gothic", 18, System.Drawing.FontStyle.Bold)
		self._Button_Start.Location = System.Drawing.Point(19, 436)
		self._Button_Start.Name = "Button_Start"
		self._Button_Start.Size = System.Drawing.Size(817, 50)
		self._Button_Start.TabIndex = 13
		self._Button_Start.Text = "Start DDR Wizard"
		self._Button_Start.UseVisualStyleBackColor = True
		self._Button_Start.Click += self.Button_StartClick
		# 
		# Button_Debug
		# 
		self._Button_Debug.Location = System.Drawing.Point(749, 4)
		self._Button_Debug.Name = "Button_Debug"
		self._Button_Debug.Size = System.Drawing.Size(87, 24)
		self._Button_Debug.TabIndex = 16
		self._Button_Debug.Text = "Debug"
		self._Button_Debug.UseVisualStyleBackColor = True
		self._Button_Debug.Visible = sub_DB.Debug_Mode
		self._Button_Debug.Click += self.Button_DebugClick
		# 
		# MenuStrip
		#
		self._MenuStrip.BackColor = System.Drawing.Color.FromArgb(240, 240, 240)
		self._MenuStrip.Font = System.Drawing.Font("Arial", 10)
		self._MenuStrip.Items.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._File_ToolStripMenuItem,
			self._Help_ToolStripMenuItem]))
		self._MenuStrip.Location = System.Drawing.Point(0, 0)
		self._MenuStrip.Name = "MenuStrip"
		self._MenuStrip.Size = System.Drawing.Size(578, 24)
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
		# openFileDialog1
		# 
		self._openFileDialog1.FileName = "openFileDialog1"
		# 
		# StartForm
		# 
		self.ClientSize = System.Drawing.Size(878, 539)
		self.MaximumSize = System.Drawing.Size(878, 539)
		self.MinimumSize = System.Drawing.Size(878, 539)
		self.Controls.Add(self._Button_Debug)
		self.Controls.Add(self._PictureBox_Comp)
		self.Controls.Add(self._PictureBox_Eye)
		self.Controls.Add(self._Button_Start)
		self.Controls.Add(self._PictureBox_EM)
		self.Controls.Add(self._PictureBox_Tran)
		self.Controls.Add(self._MenuStrip)
		self.Font = System.Drawing.Font("Arial", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
		IconFile = path + "\\Resources\\LOGO.ico"
		self.Icon = Icon(IconFile)
		self.MainMenuStrip = self._MenuStrip		
		self.Name = "StartForm"
		self.Text = "ANSYS DDR Wizard"
		self.Load += self.StartFormLoad
		self._MenuStrip.ResumeLayout(False)
		self._MenuStrip.PerformLayout()
		self._PictureBox_EM.EndInit()
		self._PictureBox_Tran.EndInit()
		self._PictureBox_Eye.EndInit()
		self._PictureBox_Comp.EndInit()
		self.ResumeLayout(False)
		self.PerformLayout()

		# Variables				
		self.EM_flag = False
		self.Tran_flag = False
		self.Eye_flag = False
		self.Comp_flag = False
	''' StartForm - Events '''
	def StartFormLoad(self, sender, e):
		# Load Preserved Definition File		
		File = path + "\\Resources\\Ref.def"		
		Cenv = Load_env(File)
		Cenv["File"] = File		
		sub_DB.Cenv = Cenv
		
		# Load Preserved Configuration File
		if sub_DB.Debug_Mode:
			File = path + "\\Resources\\Test_0215.cnf"
		else:
			File = path + "\\Resources\\Ref.cnf"
		Uenv = Load_env(File)
		Uenv["File"] = File		
		sub_DB.Uenv = Uenv

	def PictureBox_EMClick(self, sender, e):
		if self.EM_flag:
			LogoFile = path + "\\Resources\\Main1_off.bmp"
			self._PictureBox_EM.BackgroundImage = Bitmap(LogoFile)
		else:
			LogoFile = path + "\\Resources\\Main1_on.bmp"
			self._PictureBox_EM.BackgroundImage = Bitmap(LogoFile)
		self.EM_flag = not self.EM_flag		

	def PictureBox_TranClick(self, sender, e):
		if self.Tran_flag:
			LogoFile = path + "\\Resources\\Main2_off.bmp"
			self._PictureBox_Tran.BackgroundImage = Bitmap(LogoFile)
		else:
			LogoFile = path + "\\Resources\\Main2_on.bmp"
			self._PictureBox_Tran.BackgroundImage = Bitmap(LogoFile)
		self.Tran_flag = not self.Tran_flag

	def PictureBox_EyeClick(self, sender, e):
		if self.Eye_flag:
			LogoFile = path + "\\Resources\\Main3_off.bmp"
			self._PictureBox_Eye.BackgroundImage = Bitmap(LogoFile)
		else:
			LogoFile = path + "\\Resources\\Main3_on.bmp"
			self._PictureBox_Eye.BackgroundImage = Bitmap(LogoFile)
		self.Eye_flag = not self.Eye_flag

	def PictureBox_CompClick(self, sender, e):
		if self.Comp_flag:
			LogoFile = path + "\\Resources\\Main4_off.bmp"
			self._PictureBox_Comp.BackgroundImage = Bitmap(LogoFile)
		else:
			LogoFile = path + "\\Resources\\Main4_on.bmp"
			self._PictureBox_Comp.BackgroundImage = Bitmap(LogoFile)
		self.Comp_flag = not self.Comp_flag

	def DDRConf_Load_ToolStripMenuItemClick(self, sender, e):
		# Select DDR Definition File		
		dialog = OpenFileDialog()
		dialog.InitialDirectory = path + "\\Resources"
		dialog.Filter = "DDR wizard definition file|*.def"
		dialog.Title = "Select ANSYS DDR Wizard Definition File"
		if dialog.ShowDialog(self) == DialogResult.OK:
			File = dialog.FileName			
		else:
			MessageBox.Show("Please Select the DDR wizard definition file(*.def)","Warning")

		# Parse DDR Definition File
		# Get Defined Data
		Cenv = Load_env(File)
		Cenv["File"] = File		
		sub_DB.Cenv = Cenv

		MessageBox.Show("DDR wizard definition file \"%s\" is loaded" % File.split("\\")[-1], "Load")

	def DDRConf_Edit_ToolStripMenuItemClick(self, sender, e):		
		## Select DDR Definition File		
		#dialog = OpenFileDialog()
		#dialog.InitialDirectory = path + "\\Resources"
		#dialog.Filter = "DDR wizard definition file|*.def"
		#dialog.Title = "Select ANSYS DDR Wizard Definition File"
		#if dialog.ShowDialog(self) == DialogResult.OK:
		#	File = dialog.FileName
		#	#if File.split("\\")[-1] == "Ref.def":
		#	#	MessageBox.Show("The reference definition file \"Ref.def\" cannot be edited", "Warning")
		#	#else:			
		#	sub_DB.Env_Form = EnvEditor(File)
		#	sub_DB.Env_Form.ShowDialog()
			
		#else:
		#	MessageBox.Show("Please Select the DDR wizard definition file(*.def)","Warning")
		sub_DB.Env_Form = EnvEditor(sub_DB.Cenv["File"])
		sub_DB.Env_Form.ShowDialog()

	def UserConf_Load_ToolStripMenuItemClick(self, sender, e):
		# Select DDR Configuration File		
		dialog = OpenFileDialog()
		dialog.InitialDirectory = path + "\\Resources"
		dialog.Filter = "DDR wizard configuration file|*.cnf"
		dialog.Title = "Select ANSYS DDR Wizard Configuration File"
		if dialog.ShowDialog(self) == DialogResult.OK:
			File = dialog.FileName			
		else:
			MessageBox.Show("Please Select the DDR wizard configuration file(*.cnf)","Warning")

		# Parse DDR Configuration File
		# Get Defined Data
		Uenv = Load_env(File)
		Uenv["File"] = File
		sub_DB.Uenv = Uenv

		MessageBox.Show("DDR wizard configuration file \"%s\" is loaded" % File.split("\\")[-1], "Load")

	def UserConf_Edit_ToolStripMenuItemClick(self, sender, e):		
		## Select DDR Configuration File		
		#dialog = OpenFileDialog()
		#dialog.InitialDirectory = path + "\\Resources"
		#dialog.Filter = "DDR wizard configuration file|*.cnf"
		#dialog.Title = "Select ANSYS DDR Wizard configuration File"
		#if dialog.ShowDialog(self) == DialogResult.OK:
		#	File = dialog.FileName
		#	#if File.split("\\")[-1] == "Ref.cnf":
		#	#	MessageBox.Show("The reference configuration file \"Ref.cnf\" cannot be edited", "Warning")
		#	#else:			
		#	sub_DB.Env_Form = EnvEditor(File)
		#	sub_DB.Env_Form.ShowDialog()
		#else:
		#	MessageBox.Show("Please Select the DDR wizard configuration file(*.cnf)","Warning")
		sub_DB.Env_Form = EnvEditor(sub_DB.Uenv["File"])
		sub_DB.Env_Form.ShowDialog()

	def Exit_ToolStripMenuItemClick(self, sender, e):		
		os._exit(0)
		pass

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

	def Button_StartClick(self, sender, e):
		# Back-up Configuration
		#	for EM		
		if "[EM]" in sub_DB.Uenv:
			sub_DB.Uenv["[EM]"][0] = str(self.EM_flag)
		else:
			sub_DB.Uenv["[EM]"] = [str(self.EM_flag)]

		#	for Tran
		if "[Tran]" in sub_DB.Uenv:
			sub_DB.Uenv["[Tran]"][0] = str(self.Tran_flag)
		else:
			sub_DB.Uenv["[Tran]"] = [str(self.Tran_flag)]

		#	for Eye
		if "[Eye]" in sub_DB.Uenv:
			sub_DB.Uenv["[Eye]"][0] = str(self.Eye_flag)
		else:
			sub_DB.Uenv["[Eye]"] = [str(self.Eye_flag)]

		#	for Comp
		if "[Comp]" in sub_DB.Uenv:
			sub_DB.Uenv["[Comp]"][0] = str(self.Comp_flag)
		else:
			sub_DB.Uenv["[Comp]"] = [str(self.Comp_flag)]

		# Close Form
		self.Close()

	def Button_DebugClick(self, sender, e):
		self.StartFormLoad(self, sender)
		self.PictureBox_EyeClick(self, sender)
		self.Button_StartClick(self, sender)