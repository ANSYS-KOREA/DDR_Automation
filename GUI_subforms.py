import os
import time
import re
import traceback
import System.Drawing
import System.Windows.Forms
import sub_ScriptEnv
import sub_AEDT
import sub_DB

from sub_functions import *
from sub_IBIS import *
from System.Drawing import *
from System.Windows.Forms import *
from sub_Report_Excel import *

class EnvEditor(Form):
	def __init__(self, File):
		self.InitializeComponent(File)
		pass

	''' Env Editor - GUI '''	
	def InitializeComponent(self, File):		
		path = os.path.dirname(os.path.abspath(__file__))
		self._TreeView = System.Windows.Forms.TreeView()
		self._RichTextBox = System.Windows.Forms.RichTextBox()
		self._Button_SaveAs = System.Windows.Forms.Button()
		self._Button_Close = System.Windows.Forms.Button()
		self._Button_Save = System.Windows.Forms.Button()
		self._components = System.ComponentModel.Container()
		self._contextMenuStrip1 = System.Windows.Forms.ContextMenuStrip(self._components)
		self._expandAllToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._collapseAllToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._saveFileDialog1 = System.Windows.Forms.SaveFileDialog()
		self._CheckBox = System.Windows.Forms.CheckBox()
		self._contextMenuStrip1.SuspendLayout()
		
		self.SuspendLayout()
		# 
		# TreeView
		# 
		self._TreeView.BackColor = System.Drawing.Color.White
		self._TreeView.ContextMenuStrip = self._contextMenuStrip1
		self._TreeView.Font = System.Drawing.Font("Arial", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TreeView.Location = System.Drawing.Point(12, 12)
		self._TreeView.Name = "TreeView"
		self._TreeView.Size = System.Drawing.Size(318, 711)
		self._TreeView.TabIndex = 262
		self._TreeView.NodeMouseClick += self.TreeViewNodeMouseClick
		# 
		# RichTextBox
		# 
		self._RichTextBox.Font = System.Drawing.Font("Arial", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._RichTextBox.Location = System.Drawing.Point(336, 12)		
		self._RichTextBox.Name = "RichTextBox"
		self._RichTextBox.Size = System.Drawing.Size(843, 711)
		self._RichTextBox.TabIndex = 264
		self._RichTextBox.Text = ""
		self._RichTextBox.ReadOnly = True
		self._RichTextBox.BackColor  = System.Drawing.Color.WhiteSmoke
		self._RichTextBox.KeyPress += self.RichTextBoxKeyPress
		# 
		# Button_SaveAs
		# 
		self._Button_SaveAs.Font = System.Drawing.Font("Arial", 12, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_SaveAs.Location = System.Drawing.Point(916, 729)
		self._Button_SaveAs.Name = "Button_SaveAs"
		self._Button_SaveAs.Size = System.Drawing.Size(158, 38)
		self._Button_SaveAs.TabIndex = 265
		self._Button_SaveAs.Text = "Save As"
		self._Button_SaveAs.UseVisualStyleBackColor = True
		self._Button_SaveAs.Click += self.Button_SaveAsClick
		# 
		# Button_Close
		# 
		self._Button_Close.Font = System.Drawing.Font("Arial", 12, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_Close.Location = System.Drawing.Point(1084, 729)
		self._Button_Close.Name = "Button_Close"
		self._Button_Close.Size = System.Drawing.Size(95, 38)
		self._Button_Close.TabIndex = 266
		self._Button_Close.Text = "Close"
		self._Button_Close.UseVisualStyleBackColor = True
		self._Button_Close.Click += self.Button_CloseClick
		# 
		# Button_Save
		# 
		self._Button_Save.Font = System.Drawing.Font("Arial", 12, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_Save.Location = System.Drawing.Point(812, 729)
		self._Button_Save.Name = "Button_Save"
		self._Button_Save.Size = System.Drawing.Size(95, 38)
		self._Button_Save.TabIndex = 267
		self._Button_Save.Text = "Save"
		self._Button_Save.UseVisualStyleBackColor = True
		self._Button_Save.Click += self.Button_SaveClick
		# 
		# contextMenuStrip1
		# 
		self._contextMenuStrip1.Items.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._expandAllToolStripMenuItem,
			self._collapseAllToolStripMenuItem]))
		self._contextMenuStrip1.Name = "contextMenuStrip1"
		self._contextMenuStrip1.Size = System.Drawing.Size(138, 48)
		# 
		# expandAllToolStripMenuItem
		# 
		self._expandAllToolStripMenuItem.Name = "expandAllToolStripMenuItem"
		self._expandAllToolStripMenuItem.Size = System.Drawing.Size(137, 22)
		self._expandAllToolStripMenuItem.Text = "Expand All"
		self._expandAllToolStripMenuItem.Click += self.ExpandAllToolStripMenuItemClick
		# 
		# collapseAllToolStripMenuItem
		# 
		self._collapseAllToolStripMenuItem.Name = "collapseAllToolStripMenuItem"
		self._collapseAllToolStripMenuItem.Size = System.Drawing.Size(137, 22)
		self._collapseAllToolStripMenuItem.Text = "Collapse All"
		self._collapseAllToolStripMenuItem.Click += self.CollapseAllToolStripMenuItemClick
		# 
		# CheckBox
		# 
		self._CheckBox.BackColor = System.Drawing.SystemColors.Control
		self._CheckBox.Font = System.Drawing.Font("Arial", 10)
		self._CheckBox.Location = System.Drawing.Point(336, 729)
		self._CheckBox.Name = "CheckBox"
		self._CheckBox.Size = System.Drawing.Size(101, 25)
		self._CheckBox.TabIndex = 269
		self._CheckBox.Text = "Edit enable"		
		self._CheckBox.UseVisualStyleBackColor = False
		self._CheckBox.CheckedChanged += self.CheckBoxCheckedChanged
		# 
		# Env_Editor
		# 
		self.ClientSize = System.Drawing.Size(1191, 773)
		self.MinimumSize = System.Drawing.Size(self.Size.Width/2, self.Size.Height/2)
		self.FormSize_W = self.Size.Width
		self.FormSize_H = self.Size.Height
		self.Controls.Add(self._CheckBox)
		self.Controls.Add(self._Button_Save)
		self.Controls.Add(self._Button_Close)
		self.Controls.Add(self._Button_SaveAs)
		self.Controls.Add(self._RichTextBox)
		self.Controls.Add(self._TreeView)
		IconFile = path + "\\Resources\\LOGO.ico"
		self.Icon = Icon(IconFile)
		self.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent		
		self.Name = "Env_Editor"
		self.Text = "Ansys DDR Wizard Env. File Editor"
		self.Load += self.EnvEditorLoad
		self.ResizeEnd += self.EnvEditorResizeEnd
		self._contextMenuStrip1.ResumeLayout(False)
		self.ResumeLayout(False)

		# Variables
		self.File = File
		self.SaveFlag = False		

	''' Env Editor - Events '''	
	def EnvEditorResizeEnd(self, sender, e):
		try:
			# Get previous Start_Form width/height and resized Start_Form width/height
			# Calculate Gap betweent previous and resized width/height
			Gap_W = self.Size.Width - self.FormSize_W
			Gap_H = self.Size.Height - self.FormSize_H

			# Backup the resized Start_Form width/height as previous MainFomr width/height
			self.FormSize_W = self.Size.Width
			self.FormSize_H = self.Size.Height

			# Resize RichTextBox
			self._RichTextBox.Size = System.Drawing.Size(self._RichTextBox.Width + Gap_W, self._RichTextBox.Height + Gap_H)		
			self._TreeView.Size = System.Drawing.Size(self._TreeView.Width, self._TreeView.Height + Gap_H)		

			# Relocate Buttons based on the Gap_W
			self._Button_Save.Location = System.Drawing.Point(self._Button_Save.Location.X + Gap_W, self._Button_Save.Location.Y + Gap_H)
			self._Button_SaveAs.Location = System.Drawing.Point(self._Button_SaveAs.Location.X + Gap_W, self._Button_SaveAs.Location.Y + Gap_H)
			self._Button_Close.Location = System.Drawing.Point(self._Button_Close.Location.X + Gap_W, self._Button_Close.Location.Y + Gap_H)
			self._CheckBox.Location = System.Drawing.Point(self._CheckBox.Location.X, self._CheckBox.Location.Y + Gap_H)

		except Exception as e:
			Log("[EnvEditor ResizeEnd] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to resize Editor GUI","Warning")			
			EXIT()

	def EnvEditorLoad(self, sender, e):
		try:
			# Open *.cenv or *.uenv File		
			with open(self.File) as fp:
				# Parent node index for treeview
				ParentNode_idx = -1
				# Load Input File
				for line in fp:				
					if line.strip() != "":						
						if line.lstrip()[0]=="#":
							# Set the color of the comment line to "Green", Note that the symbol for the comment is "#"
							self._RichTextBox.SelectionColor = Color.Green						
							self._RichTextBox.SelectionFont = Font("Segoe UI", 9, FontStyle.Italic)
						else:
							# Set the color of the other line to "Black"
							self._RichTextBox.SelectionColor = Color.Black
							# Add parent node
							# The keyword of the parent node is defined between the symbol "[" and "]".
							if line.find("[") != -1:
								#level = 0
								Node = self._TreeView.Nodes.Add(line.split("[")[1].split("]")[0])							
								ParentNode_idx += 1
								ChildNode_idx = -1							
							# Add child node
							# The keyword of the child node is defined between the symbol "<" and ">".
							elif line.find("<") != -1:
								#level = 1
								Node = self._TreeView.Nodes[ParentNode_idx].Nodes.Add(line.split("<")[1].split(">")[0])							
								ChildNode_idx += 1
								GrandChildNode_idx = -1							
							# Add grandchild node
							# The keyword of the grandchild node is defined between the symbol "(" and ")".
							elif line.find("(") != -1:
								#level = 2
								Node = self._TreeView.Nodes[ParentNode_idx].Nodes[ChildNode_idx].Nodes.Add(line.split("(")[1].split(")")[0])							
								GrandChildNode_idx += 1
					self._RichTextBox.AppendText(line)
			fp.close()
			self._CheckBox.Checked = True
			if self.File.find(".def") != -1:
				self.Text = "Ansys DDR Wizard %s File Editor - %s" % ("Definition", self.File.split("\\")[-1])			
			else:
				self.Text = "Ansys DDR Wizard %s File Editor - %s" % ("Configuration", self.File.split("\\")[-1])

		except Exception as e:		
			Log("[EnvEditor Load] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to load Editor","Warning")			
			EXIT()

	def ExpandAllToolStripMenuItemClick(self, sender, e):
		self._TreeView.ExpandAll()
		pass
		
	def CollapseAllToolStripMenuItemClick(self, sender, e):
		self._TreeView.CollapseAll()		
		pass

	def TreeViewNodeMouseClick(self, sender, e):
		try:
			key = []
			current_node = e.Node
			for i in range(0, e.Node.Level+1):		
				if current_node.Level == 0:
					left = "["
					right = "]"
				elif current_node.Level == 1:
					left = "<"
					right = ">"
				elif current_node.Level == 2:
					left = "("
					right = ")"

				key.insert(0, left + current_node.Text + right)
				current_node = current_node.Parent

			HighLight(key, self._RichTextBox)

		except Exception as e:		
			Log("[EnvEditor Treeview Node Mouse Click] = Failed")
			Log(traceback.format_exc())
			print traceback.format_exc()
			MessageBox.Show("Fail to Select node in Editor","Warning")			
			EXIT()

	def RichTextBoxKeyPress(self, sender, e):
		try:
			if not self._RichTextBox.ReadOnly:
				# Enable save if there is any change in the file.
				self.SaveFlag = True

				# Keyboard Shortcut for Save
				# chr(19) = Ctrl + S 
				if e.KeyChar == chr(19):
					self.Button_SaveClick(self, sender)				

		except Exception as e:		
			Log("[EnvEditor Key Press] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to Press Key in Editor","Warning")			
			EXIT()

	def CheckBoxCheckedChanged(self, sender, e):
		try:
			if self._CheckBox.Checked:
				self._RichTextBox.ReadOnly = False
				self._RichTextBox.AcceptsTab = True
				self._RichTextBox.BackColor  = System.Drawing.Color.FloralWhite

			else:
				self._RichTextBox.ReadOnly = True
				self._RichTextBox.AcceptsTab = False
				self._RichTextBox.BackColor  = System.Drawing.Color.WhiteSmoke

		except Exception as e:
			Log("[Enable EnvEditor] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to make EnvEditor editable","Warning")			
			EXIT()

	def Button_SaveClick(self, sender, e):
		try:
			if self.SaveFlag:
				# File Save
				temp_text = self._RichTextBox.Text.split("\n")
				System.IO.File.WriteAllLines(self.File, temp_text)
				self.SaveFlag = False
				Log("[Save EnvEditor] = %s" % self.File)

				# The mouse cursor is changed to the wait cursor for 1 second
				# to inform the user that file has been saved.			
				self._RichTextBox.Cursor = Cursors.WaitCursor
				self.Cursor = Cursors.WaitCursor			
				time.sleep(1)
				self._RichTextBox.Cursor = Cursors.IBeam
				self.Cursor = Cursors.Default

		except Exception as e:		
			Log("[Save EnvEditor] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to save EnvEditor","Warning")			
			EXIT()

	def Button_SaveAsClick(self, sender, e):
		try:
			dialog = SaveFileDialog()
			dialog.InitialDirectory = os.path.dirname(os.path.abspath(__file__)) + "\\Resources"

			# for Common Env. Case
			if self.File.split("\\")[-1].split(".")[-1] == "def":
				dialog.Title = "Save ANSYS DDR Wizard Definition File"
				dialog.Filter = "DDR wizard definition file|*.def"
			
			# for User Env. Case
			else:
				dialog.Title = "Save ANSYS DDR Wizard Configuration File"
				dialog.Filter = "DDr wizard configuration file|*.cnf"
		
			# File Save
			if dialog.ShowDialog(self) == DialogResult.OK:
				File = dialog.FileName
				temp_text = self._RichTextBox.Text.split("\n")
				System.IO.File.WriteAllLines(File, temp_text)
				self.SaveFlag = False
				self.File = File
				Log("[Save As EnvEditor] = %s" % self.File)

			if self.File.find(".def") != -1:
				self.Text = "Ansys DDR Wizard %s File Editor - %s" % ("Definition", self.File.split("\\")[-1])			
			else:
				self.Text = "Ansys DDR Wizard %s File Editor - %s" % ("Configuration", self.File.split("\\")[-1])

		except Exception as e:		
			Log("[Save As EnvEditor] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to save as EnvEditor","Warning")			
			EXIT()

	def Button_CloseClick(self, sender, e):
		try:
			Log("[Close EnvEditor]")
			Cenv = {}
			Uenv = {}
			# Get Defined Data
			if self.File.find(".def") != -1:			
				Cenv = Load_env(self.File)
				Cenv["File"] = self.File				
				sub_DB.Cenv = Cenv
			
			else:			
				Uenv = Load_env(self.File)
				Uenv["File"] = self.File				
				sub_DB.Uenv = Uenv

			# if there is any change in the file, 
			if self.SaveFlag:
				dialogResult = MessageBox.Show("Want to save your changes to " + self.File.split("\\")[-1] + " ?" , "Save", MessageBoxButtons.YesNoCancel)
				# Save and Close
				if dialogResult == DialogResult.Yes:
					self.Button_SaveClick(self, sender)
					self.Close()
				# Close w/o save
				elif dialogResult == DialogResult.No:
					self.Close()
				# Cancel
		
			# if there is no change in the file, 
			else:
				# Close file
				self.Close()

		except Exception as e:		
			Log("[Close EnvEditor] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to close EnvEditor","Warning")			
			EXIT()

class NetForm(Form):
	def __init__(self):

		self.InitializeComponent()
	
	def InitializeComponent(self):
		path = os.path.dirname(os.path.abspath(__file__))
		self._DataGridView = System.Windows.Forms.DataGridView()
		self._Col_TargetNet = System.Windows.Forms.DataGridViewCheckBoxColumn()
		self._Col_NetName = System.Windows.Forms.DataGridViewTextBoxColumn()
		self._Col_Group = System.Windows.Forms.DataGridViewComboBoxColumn()		
		self._Col_MatchedString = System.Windows.Forms.DataGridViewTextBoxColumn()
		self._Col_AnalyzeGroup = System.Windows.Forms.DataGridViewComboBoxColumn()
		self._Col_Width = System.Windows.Forms.DataGridViewTextBoxColumn()
		self._Col_Margin = System.Windows.Forms.DataGridViewTextBoxColumn()
		self._Col_Setup = System.Windows.Forms.DataGridViewTextBoxColumn()
		self._Col_Hold = System.Windows.Forms.DataGridViewTextBoxColumn()
		self._Label_GroupName = System.Windows.Forms.Label()
		self._Label_ReportFormat = System.Windows.Forms.Label()
		self._Label_H_Border1 = System.Windows.Forms.Label()
		self._Label_ImageWidth = System.Windows.Forms.Label()
		self._Label_ImageWidth_Unit = System.Windows.Forms.Label()
		self._ComboBox_AnalyzeGroup = System.Windows.Forms.ComboBox()
		self._ComboBox_Report = System.Windows.Forms.ComboBox()
		self._CheckBox_PlotEye = System.Windows.Forms.CheckBox()
		self._TextBox_ImageWidth = System.Windows.Forms.TextBox()		
		self._Button_Update = System.Windows.Forms.Button()
		self._Button_Auto = System.Windows.Forms.Button()
		self._Button_EditRule = System.Windows.Forms.Button()		
		self._Button_Identify = System.Windows.Forms.Button()
		self._Button_Export = System.Windows.Forms.Button()
		self._Button_Close = System.Windows.Forms.Button()
		self.SuspendLayout()
		# 
		# DataGridView
		# 
		self._DataGridView.AllowUserToAddRows = False
		self._DataGridView.AllowUserToDeleteRows = False
		self._DataGridView.AllowUserToOrderColumns = True
		self._DataGridView.AllowUserToResizeRows = False
		self._DataGridView.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize
		self._DataGridView.Columns.AddRange(System.Array[System.Windows.Forms.DataGridViewColumn](
			[self._Col_TargetNet,
			self._Col_NetName,
			self._Col_Group,
			self._Col_MatchedString,
			self._Col_AnalyzeGroup]))
		self._DataGridView.EditMode = System.Windows.Forms.DataGridViewEditMode.EditOnF2
		self._DataGridView.Location = System.Drawing.Point(12, 12)
		self._DataGridView.Name = "DataGridView"
		self._DataGridView.RowHeadersVisible = False
		self._DataGridView.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect
		self._DataGridView.Size = System.Drawing.Size(459, 777)
		self._DataGridView.TabIndex = 36
		self._DataGridView.Columns[1].ReadOnly = True
		self._DataGridView.Columns[3].ReadOnly = False
		self._DataGridView.KeyPress += self.DataGridViewKeyPress
		self._DataGridView.ColumnHeaderMouseClick += self.DataGridViewColumnHeaderMouseClick
		self._DataGridView.CellMouseClick += self.DataGridViewCellMouseClick
		# 
		# Col_TargetNet
		# 
		self._Col_TargetNet.HeaderText = ""
		self._Col_TargetNet.Name = "Col_TargetNet"
		self._Col_TargetNet.Width = 26
		# 
		# Col_NetName
		# 
		self._Col_NetName.HeaderText = "Net Name"
		self._Col_NetName.Name = "Col_NetName"
		self._Col_NetName.Width = 130
		# 
		# Col_Group
		# 
		self._Col_Group.HeaderText = "Group"
		self._Col_Group.Items.AddRange(System.Array[System.Object](["DM","DQ","DQS_P","DQS_N","CLK_P","CLK_N","ADDR","OTHER"]))
		self._Col_Group.Name = "Col_Group"
		self._Col_Group.Width = 100	
		# 
		# Col_MatchedString
		# 
		self._Col_MatchedString.HeaderText = "Matched String"
		self._Col_MatchedString.Name = "Col_MatchedString"
		self._Col_MatchedString.Width = 100
		self._Col_MatchedString.SortMode = System.Windows.Forms.DataGridViewColumnSortMode.Programmatic
		# 
		# Col_AnalyzeGroup
		# 
		self._Col_AnalyzeGroup.HeaderText = "Analyze Group"
		self._Col_AnalyzeGroup.Name = "Col_AnalyzeGroup"
		self._Col_AnalyzeGroup.Items.AddRange(System.Array[System.Object](["None","Byte0","Byte1","Byte2","Byte3"]))
		self._Col_AnalyzeGroup.Width = 100
		# 
		# Col_Width
		# 
		self._Col_Width.HeaderText = "Width [ps]"
		self._Col_Width.Name = "Eye_Width"
		self._Col_Width.Width = 80
		# 
		# Col_Margin
		# 
		self._Col_Margin.HeaderText = "Margin [ps]"
		self._Col_Margin.Name = "Eye_Margin"
		self._Col_Margin.Width = 85
		# 
		# Col_Setup
		# 
		self._Col_Setup.HeaderText = "Setup [ps]"
		self._Col_Setup.Name = "Eye_Setup"
		self._Col_Setup.Width = 80
		# 
		# Col_Hold
		# 
		self._Col_Hold.HeaderText = "Hold [ps]"
		self._Col_Hold.Name = "Eye_Hold"
		self._Col_Hold.Width = 80
		# 
		# Label_GroupName
		# 
		self._Label_GroupName.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_GroupName.Location = System.Drawing.Point(12, 797)
		self._Label_GroupName.Name = "Label_GroupName"
		self._Label_GroupName.Size = System.Drawing.Size(109, 28)
		self._Label_GroupName.TabIndex = 30
		self._Label_GroupName.Text = "Analyze Group :"
		self._Label_GroupName.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_H_Border1
		# 
		self._Label_H_Border1.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
		self._Label_H_Border1.Location = System.Drawing.Point(12, 829)
		self._Label_H_Border1.Name = "Label_H_Border1"
		self._Label_H_Border1.Size = System.Drawing.Size(458, 2)
		self._Label_H_Border1.TabIndex = 39
		# 
		# Label_ReportFormat
		# 
		self._Label_ReportFormat.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_ReportFormat.Location = System.Drawing.Point(12, 837)
		self._Label_ReportFormat.Name = "Label_ReportFormat"
		self._Label_ReportFormat.Size = System.Drawing.Size(109, 28)
		self._Label_ReportFormat.TabIndex = 30
		self._Label_ReportFormat.Text = "Report Format :"
		self._Label_ReportFormat.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_ImageWidth
		# 
		self._Label_ImageWidth.Font = System.Drawing.Font("Arial", 9)
		self._Label_ImageWidth.Location = System.Drawing.Point(73, 152)
		self._Label_ImageWidth.Name = "Label_ImageWidth"
		self._Label_ImageWidth.Size = System.Drawing.Size(85, 28)
		self._Label_ImageWidth.TabIndex = 47
		self._Label_ImageWidth.Text = "Image Width :"
		self._Label_ImageWidth.Visible = False
		self._Label_ImageWidth.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_ImageWidth_Unit
		# 
		self._Label_ImageWidth_Unit.Font = System.Drawing.Font("Arial", 9)
		self._Label_ImageWidth_Unit.Location = System.Drawing.Point(249, 152)
		self._Label_ImageWidth_Unit.Name = "Label_ImageWidth_Unit"
		self._Label_ImageWidth_Unit.Size = System.Drawing.Size(51, 28)
		self._Label_ImageWidth_Unit.TabIndex = 49
		self._Label_ImageWidth_Unit.Text = "[pixel]"
		self._Label_ImageWidth_Unit.Visible = False
		self._Label_ImageWidth_Unit.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# ComboBox_AnalyzeGroup
		# 
		self._ComboBox_AnalyzeGroup.FormattingEnabled = True
		self._ComboBox_AnalyzeGroup.Location = System.Drawing.Point(121, 801)
		self._ComboBox_AnalyzeGroup.Name = "ComboBox_AnalyzeGroup"
		self._ComboBox_AnalyzeGroup.Items.AddRange(System.Array[System.Object](["None","Byte0","Byte1","Byte2","Byte3"]))
		self._ComboBox_AnalyzeGroup.Size = System.Drawing.Size(125, 21)
		self._ComboBox_AnalyzeGroup.TabIndex = 40		
		# 
		# ComboBox_Report
		# 
		self._ComboBox_Report.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._ComboBox_Report.FormattingEnabled = True
		self._ComboBox_Report.Location = System.Drawing.Point(121, 837)
		self._ComboBox_Report.Name = "ComboBox_Report"		
		self._ComboBox_Report.Size = System.Drawing.Size(125, 25)
		self._ComboBox_Report.TabIndex = 40
		# 
		# CheckBox_PlotEye
		# 
		self._CheckBox_PlotEye.Font = System.Drawing.Font("Arial", 9)
		self._CheckBox_PlotEye.Location = System.Drawing.Point(12, 797)
		self._CheckBox_PlotEye.Name = "CheckBox_PlotEye"
		self._CheckBox_PlotEye.Size = System.Drawing.Size(136, 29)
		self._CheckBox_PlotEye.TabIndex = 45
		self._CheckBox_PlotEye.Text = "Plot EYE with Mask"
		self._CheckBox_PlotEye.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		self._CheckBox_PlotEye.Checked = False
		self._CheckBox_PlotEye.UseVisualStyleBackColor = True
		self._CheckBox_PlotEye.CheckedChanged += self.CheckBox_PlotEyeCheckedChanged
		# 
		# TextBox_ImageWidth
		# 
		self._TextBox_ImageWidth.BackColor = System.Drawing.SystemColors.Window
		self._TextBox_ImageWidth.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_ImageWidth.Location = System.Drawing.Point(160, 155)
		self._TextBox_ImageWidth.Name = "TextBox_ImageWidth"
		self._TextBox_ImageWidth.Size = System.Drawing.Size(83, 23)
		self._TextBox_ImageWidth.Text = "200"
		self._TextBox_ImageWidth.Visible = False
		self._TextBox_ImageWidth.TabIndex = 48
		self._TextBox_ImageWidth.TextChanged += self.TextBox_ImageWidthTextChanged
		# 
		# Button_Update
		# 
		self._Button_Update.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_Update.Location = System.Drawing.Point(257, 799)
		self._Button_Update.Name = "Button_Update"
		self._Button_Update.Size = System.Drawing.Size(64, 25)
		self._Button_Update.TabIndex = 32
		self._Button_Update.Text = "Update"
		self._Button_Update.UseVisualStyleBackColor = True		
		self._Button_Update.Click += self.Button_UpdateClick		
		# 
		# Button_Auto
		# 
		self._Button_Auto.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_Auto.Location = System.Drawing.Point(327, 801)
		self._Button_Auto.Name = "Button_Auto"
		self._Button_Auto.Size = System.Drawing.Size(141, 25)
		self._Button_Auto.TabIndex = 38
		self._Button_Auto.Text = "Auto Grouping"
		self._Button_Auto.UseVisualStyleBackColor = True
		self._Button_Auto.Click += self.Button_AutoClick
		# 
		# Button_EditRule
		# 
		self._Button_EditRule.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_EditRule.Location = System.Drawing.Point(12, 837)
		self._Button_EditRule.Name = "Button_EditRule"
		self._Button_EditRule.Size = System.Drawing.Size(234, 35)
		self._Button_EditRule.TabIndex = 33
		self._Button_EditRule.Text = "Edit Net Classification Rules"
		self._Button_EditRule.UseVisualStyleBackColor = True
		self._Button_EditRule.Click += self.Button_EditRuleClick
		# 
		# Button_Identify
		# 
		self._Button_Identify.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_Identify.Location = System.Drawing.Point(257, 837)
		self._Button_Identify.Name = "Button_Identify"
		self._Button_Identify.Size = System.Drawing.Size(100, 35)
		self._Button_Identify.TabIndex = 35
		self._Button_Identify.Text = "Identify"
		self._Button_Identify.UseVisualStyleBackColor = True		
		self._Button_Identify.Click += self.Button_IdentifyClick
		# 
		# Button_Export
		# 
		self._Button_Export.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_Export.Location = System.Drawing.Point(257, 837)
		self._Button_Export.Name = "Button_Export"
		self._Button_Export.Size = System.Drawing.Size(100, 35)
		self._Button_Export.TabIndex = 35
		self._Button_Export.Text = "Export"
		self._Button_Export.UseVisualStyleBackColor = True		
		self._Button_Export.Click += self.Button_ExportClick
		# 
		# Button_Close
		# 
		self._Button_Close.Font = System.Drawing.Font("Arial", 12, System.Drawing.FontStyle.Bold)
		self._Button_Close.Location = System.Drawing.Point(368, 839)
		self._Button_Close.Name = "Button_Close"
		self._Button_Close.Size = System.Drawing.Size(100, 35)
		self._Button_Close.TabIndex = 37
		self._Button_Close.Text = "Close"
		self._Button_Close.UseVisualStyleBackColor = True
		self._Button_Close.Click += self.Button_CloseClick		
		# 
		# Net_Form
		#
		self.ClientSize = System.Drawing.Size(483, 882)
		#self.MaximumSize = System.Drawing.Size(499, 921)		
		self.FormSize_W = self.Size.Width
		self.FormSize_H = self.Size.Height
		self.Controls.Add(self._Label_ImageWidth)
		self.Controls.Add(self._Label_ImageWidth_Unit)
		self.Controls.Add(self._CheckBox_PlotEye)
		self.Controls.Add(self._TextBox_ImageWidth)
		self.Controls.Add(self._Label_ReportFormat)
		self.Controls.Add(self._ComboBox_Report)
		self.Controls.Add(self._Button_Export)
		self.Controls.Add(self._ComboBox_AnalyzeGroup)
		self.Controls.Add(self._Label_H_Border1)
		self.Controls.Add(self._Button_Auto)
		self.Controls.Add(self._Button_Update)
		self.Controls.Add(self._Button_EditRule)
		self.Controls.Add(self._Button_Identify)		
		self.Controls.Add(self._Button_Close)				
		self.Controls.Add(self._Label_GroupName)
		self.Controls.Add(self._DataGridView)
		IconFile = path + "\\Resources\\LOGO.ico"
		self.Icon = Icon(IconFile)
		self.StartPosition = System.Windows.Forms.FormStartPosition.Manual		
		self.Location = System.Drawing.Point(sub_DB.Eye_Form.Location.X + sub_DB.Eye_Form.Size.Width, sub_DB.Eye_Form.Location.Y)
		self.Name = "Net_Form"
		self.Text = "Target Net Setup"		
		self.Load += self.NetFormLoad
		self.ResizeEnd += self.NetFormResizeEnd
		self.MouseDoubleClick += self.NetFormMouseDoubleClick
		#self.FormClosing += self.Net_FormFormClosing
		self.ResumeLayout(False)
		self.PerformLayout()

		self.Init_Flag = True

	def NetFormResizeEnd(self, sender, e):
		try:
			# Get previous Eye_Form width/height and resized Eye_Form width/height
			# Calculate Gap betweent previous and resized width/height		
			Gap_W = self.Size.Width - self.FormSize_W
			Gap_H = self.Size.Height - self.FormSize_H

			# Backup the resized Eye_Form width/height as previous MainFomr width/height
			self.FormSize_W = self.Size.Width
			self.FormSize_H = self.Size.Height

			# Resize			
			self._DataGridView.Size = System.Drawing.Size(self._DataGridView.Width + Gap_W, self._DataGridView.Height + Gap_H)
			self._ComboBox_AnalyzeGroup.Size = System.Drawing.Size(self._ComboBox_AnalyzeGroup.Width + Gap_W, self._ComboBox_AnalyzeGroup.Height)
			self._Label_H_Border1.Size = System.Drawing.Size(self._Label_H_Border1.Width + Gap_W, self._Label_H_Border1.Height)
		

			# Relocate
			self._Label_GroupName.Location = System.Drawing.Point(self._Label_GroupName.Location.X, self._Label_GroupName.Location.Y + Gap_H)
			self._Label_ReportFormat.Location = System.Drawing.Point(self._Label_ReportFormat.Location.X, self._Label_ReportFormat.Location.Y + Gap_H)
			self._Label_H_Border1.Location = System.Drawing.Point(self._Label_H_Border1.Location.X, self._Label_H_Border1.Location.Y + Gap_H)
			self._ComboBox_AnalyzeGroup.Location = System.Drawing.Point(self._ComboBox_AnalyzeGroup.Location.X, self._ComboBox_AnalyzeGroup.Location.Y + Gap_H)
			self._ComboBox_Report.Location = System.Drawing.Point(self._ComboBox_Report.Location.X, self._ComboBox_Report.Location.Y + Gap_H)
			self._Button_Update.Location = System.Drawing.Point(self._Button_Update.Location.X + Gap_W, self._Button_Update.Location.Y + Gap_H)
			self._Button_Auto.Location = System.Drawing.Point(self._Button_Auto.Location.X + Gap_W, self._Button_Auto.Location.Y + Gap_H)
			self._Button_EditRule.Location = System.Drawing.Point(self._Button_EditRule.Location.X + Gap_W, self._Button_EditRule.Location.Y + Gap_H)
			self._Button_Identify.Location = System.Drawing.Point(self._Button_Identify.Location.X + Gap_W, self._Button_Identify.Location.Y + Gap_H)
			self._Button_Export.Location = System.Drawing.Point(self._Button_Export.Location.X + Gap_W, self._Button_Export.Location.Y + Gap_H)
			self._Button_Close.Location = System.Drawing.Point(self._Button_Close.Location.X + Gap_W, self._Button_Close.Location.Y + Gap_H)
			self._CheckBox_PlotEye.Location = System.Drawing.Point(self._CheckBox_PlotEye.Location.X, self._CheckBox_PlotEye.Location.Y + Gap_H)

		except Exception as e:		
			Log("[NetFrom ResizeEnd] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to resize Net Classification GUI","Warning")			
			EXIT()

	def NetFormLoad(self, sender, e):		
		try:
			if self.Init_Flag:
				self.Init_Flag = False
				# Get Simulated Waveform List
				if sub_DB.InputFile_Flag == 1: # for *.aedt input					
					oProject = sub_DB.AEDT["Project"]
					#oDesign = sub_DB.AEDT["Design"]
					#oModule = sub_DB.AEDT["Module"]
					#oDesign = oProject.SetActiveDesign(sub_DB.Eye_Form._ComboBox_Design.Items[0])
					oDesign = oProject.SetActiveDesign(sub_DB.Eye_Form._ComboBox_Design.Text)
					oModule = oDesign.GetModule("ReportSetup")					
					Report_Name = []
					iter = 0
					Report_Name = sub_DB.Eye_Form._CheckedListBox_ReportName.CheckedItems					
					Netlist = []
					for report in Report_Name:						
						for net in oModule.GetReportTraceNames(str(report)):
							Netlist.append(net)

					sub_DB.Netlist = Netlist

				elif sub_DB.InputFile_Flag == 2: # for *.csv input
					# Netlist and Waveforms are loaded at file import process
					Netlist = sub_DB.Netlist
		
				# Net Identify			
				file = sub_DB.Cenv["File"]
				Cenv = Load_env(sub_DB.Cenv["File"])
				Cenv["File"] = file
				sub_DB.Cenv = Cenv

				self._DataGridView.Rows.Clear()
				LVitem_List = []
				iter = 0
				for net in Netlist:			
					Group_idx, Match = Net_Identify(net.strip(), sub_DB.Cenv) # Match = "Group prefix / Net Number prefix"

					#if Group_idx == 1 or Group_idx == 2: # for DQ & DQS Group -> Check
					if Group_idx == 1: # for DQ Group -> Check
						self._DataGridView.Rows.Add(True, net, self._Col_Group.Items[Group_idx], Match, self._Col_AnalyzeGroup.Items[0])
					else: # Un-check
						self._DataGridView.Rows.Add(False, net, self._Col_Group.Items[Group_idx], Match, self._Col_AnalyzeGroup.Items[0])
				
				# Back-up the Current Displayed Row and Matched Name
				Backup_row = []
				Name = []
				for row in self._DataGridView.Rows:
					Backup_row.append(row)
					Name.append(row.Cells[3].Value)

				# "abc" -> [a, b, c] -> ord(a) + ord(b) + ord(c) = val
				# sort val and get index => Name_idx
				Name_idx = []
				for name in Name:
					temp_list = list(name)
					val = 0
					flag = True
					iter = len(temp_list)-1
					for text in temp_list:
						if 47 < ord(text) < 58:
							val += ord(text) + iter*10**int(text)
						else:
							if flag:
								val += ord(text)
								flag = False
							else:
								val += ord(text)
						iter -= 1					

					Name_idx.append(val)
				Name_idx = sorted(range(len(Name_idx)),key=lambda k: Name_idx[k], reverse=sub_DB.NetSort_Flag)

				# Clear row and add row as sorted sequentially
				self._DataGridView.Rows.Clear()
				for i in range(0, len(Name_idx)):
					self._DataGridView.Rows.Add(Backup_row[Name_idx[i]])

				# Add Report Format into Combo Box
				for item in sub_DB.Option_Form._ComboBox_ReportFormat.Items:
					self._ComboBox_Report.Items.Add(item)
				self._ComboBox_Report.SelectedIndex = 0

			for row in self._DataGridView.Rows:
				if row.Cells[0].Value:
					row.DefaultCellStyle.BackColor = System.Drawing.SystemColors.Info
				else:
					row.DefaultCellStyle.BackColor = System.Drawing.SystemColors.Window

			###################
			# Resize Net Form #
			###################
			# Data Grid View			
			self._DataGridView.Height = self._DataGridView.Rows.Count*self._DataGridView.Rows[0].Height + 50			
			self._DataGridView.Width = 459
			ref = self._DataGridView.Height

			# Label
			self._Label_GroupName.Location = System.Drawing.Point(10, ref+15)
			self._Label_GroupName.Size = System.Drawing.Size(109, 28)
			self._Label_ReportFormat.Location = System.Drawing.Point(10, ref+53)
			self._Label_ReportFormat.Size = System.Drawing.Size(109, 28)
			self._Label_ImageWidth.Location = System.Drawing.Point(200, ref+15)
			self._Label_ImageWidth_Unit.Location = System.Drawing.Point(370, ref+15)

			# Border
			self._Label_H_Border1.Location = System.Drawing.Point(12, ref+47)
			self._Label_H_Border1.Size = System.Drawing.Size(459, 2)

			# ComboBox
			self._ComboBox_AnalyzeGroup.Location = System.Drawing.Point(121, ref+19)
			self._ComboBox_AnalyzeGroup.Size = System.Drawing.Size(125, 21)
			self._ComboBox_Report.Location = System.Drawing.Point(121, ref+57)
			self._ComboBox_Report.Size = System.Drawing.Size(125, 21)

			# CheckBox
			self._CheckBox_PlotEye.Location = System.Drawing.Point(22, ref+15)

			# TextBox
			self._TextBox_ImageWidth.Location = System.Drawing.Point(284, ref+19)

			# Buttons
			self._Button_Update.Location = System.Drawing.Point(257, ref+16)
			self._Button_Update.Size = System.Drawing.Size(64, 25)
			self._Button_Auto.Location = System.Drawing.Point(330, ref+16)
			self._Button_Auto.Size = System.Drawing.Size(141, 25)
			self._Button_EditRule.Location = System.Drawing.Point(12, ref+55)
			self._Button_EditRule.Size = System.Drawing.Size(234, 35)
			self._Button_Identify.Location = System.Drawing.Point(257, ref+55)
			self._Button_Identify.Size = System.Drawing.Size(100, 35)
			self._Button_Export.Location = System.Drawing.Point(257, ref+55)
			self._Button_Export.Size = System.Drawing.Size(100, 35)
			self._Button_Close.Location = System.Drawing.Point(371, ref+55)
			self._Button_Close.Size = System.Drawing.Size(100, 35)

			# Main Form
			self.Height = ref+135	
			self.Width = 499			
			min_height = 200
			if self.Size.Height/2 >= min_height:
				min_height = self.Size.Height/2
			self.MinimumSize = System.Drawing.Size(self.Size.Width, min_height)
			self.FormSize_H = self.Height
			self.FormSize_W = self.Width			

			if sub_DB.Result_Flag:
				self._Label_ImageWidth.Visible = self._CheckBox_PlotEye.Checked
				self._Label_ImageWidth_Unit.Visible = self._CheckBox_PlotEye.Checked
				self._TextBox_ImageWidth.Visible = self._CheckBox_PlotEye.Checked
			else:
				self._Label_ImageWidth.Visible = False
				self._Label_ImageWidth_Unit.Visible = False
				self._TextBox_ImageWidth.Visible = False

			if sub_DB.Debug_Mode:
				self.Button_CloseClick(self, sender)

		except Exception as e:		
			Log("[Net Form Load] = Failed")
			Log(traceback.format_exc())
			print traceback.format_exc()
			MessageBox.Show("Fail to load Net Classification Form","Warning")
			EXIT()

	def NetFormMouseDoubleClick(self, sender, e):

		self.NetFormLoad(self, sender)

	def DataGridViewKeyPress(self, sender, e):
		try:
			# Spacebar = Check/Uncheck all the selected rows
			if e.KeyChar == chr(32):
				for row in self._DataGridView.SelectedRows:
					row.Cells[0].Value = not row.Cells[0].Value
					if row.Cells[0].Value:
						row.DefaultCellStyle.BackColor = System.Drawing.SystemColors.Info
					else:
						row.DefaultCellStyle.BackColor = System.Drawing.SystemColors.Window


		except Exception as e:		
			Log("[Net Form Key Press] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to press key in Net Classificiton Form","Warning")			
			EXIT()

	def DataGridViewColumnHeaderMouseClick(self, sender, e):
		try:
			if e.ColumnIndex == 3:
				# Back-up the Current Displayed Row and Matched Name
				Backup_row = []
				Name = []
				for row in sender.Rows:
					Backup_row.append(row)
					Name.append(row.Cells[3].Value)

				# "abc" -> [a, b, c] -> ord(a) + ord(b) + ord(c) = val
				# sort val and get index => Name_idx
				Name_idx = []
				for name in Name:
					temp_list = list(name)
					val = 0
					flag = True
					for text in temp_list:
						if 47 < ord(text) < 58:
							val += ord(text)							
						else:
							if flag:
								val += ord(text)*1000
								flag = False
							else:
								val += ord(text)

					Name_idx.append(val)
				Name_idx = sorted(range(len(Name_idx)),key=lambda k: Name_idx[k], reverse=sub_DB.NetSort_Flag)

				# Clear row and add row as sorted sequentially
				self._DataGridView.Rows.Clear()
				for i in range(0, len(Name_idx)):
					self._DataGridView.Rows.Add(Backup_row[Name_idx[i]])

				# Inverse the Sort Order : Ascending <-> Descending
				sub_DB.NetSort_Flag = not sub_DB.NetSort_Flag

		except Exception as e:		
			Log("[Net From Column Header Click] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to sort Column of Net Classificaion Form","Warning")			
			EXIT()

	def DataGridViewCellMouseClick(self, sender, e):
		if e.ColumnIndex == 0:
			if self._DataGridView.Rows[e.RowIndex].Cells[0].Value:
				self._DataGridView.Rows[e.RowIndex].DefaultCellStyle.BackColor = System.Drawing.SystemColors.Window
			else:
				self._DataGridView.Rows[e.RowIndex].DefaultCellStyle.BackColor = System.Drawing.SystemColors.Info

	def CheckBox_PlotEyeCheckedChanged(self, sender, e):		
		self._Label_ImageWidth.Visible = sender.Checked
		self._Label_ImageWidth_Unit.Visible = sender.Checked
		self._TextBox_ImageWidth.Visible = sender.Checked
		sub_DB.Option_Form._CheckBox_PlotEye.Checked = sender.Checked
		sub_DB.Option_Form._CheckBox_ExportExcelReport.Checked = sender.Checked

		sub_DB.Title[4] = str(sender.Checked)
		sub_DB.Eye_Form.Text = " : ".join(sub_DB.Title)

	def TextBox_ImageWidthTextChanged(self, sender, e):

		sub_DB.Option_Form._TextBox_ImageWidth.Text = sender.Text

	def Button_UpdateClick(self, sender, e):
		try:
			if self._ComboBox_AnalyzeGroup.Text == "":
				MessageBox.Show("Please enter or select the analyze group name","Warning")
			else:
				# Update Group
				if self._ComboBox_AnalyzeGroup.Text in self._ComboBox_AnalyzeGroup.Items:
					for row in self._DataGridView.SelectedRows:
						row.Cells[4].Value = self._ComboBox_AnalyzeGroup.Text

				# Add ComboBox Items in ComboBox_AnalyzeGroup and DataGridView
				else:
					self._ComboBox_AnalyzeGroup.Items.Add(self._ComboBox_AnalyzeGroup.Text)
					self._DataGridView.Columns[4].Items.Add(self._ComboBox_AnalyzeGroup.Text)
					for row in self._DataGridView.SelectedRows:
						row.Cells[4].Value = self._ComboBox_AnalyzeGroup.Text

		except Exception as e:		
			Log("[Net Update] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to updated net classify result","Warning")			
			EXIT()

	def Button_AutoClick(self, sender, e):
		try:
			# Analyze Grouping - "DM","DQ","DQS","CLK","ADDR","OTHER"
			for row in self._DataGridView.Rows:
				#  for DM Group
				if row.Cells[2].Value == "DM":
					pass

				#  for DQ Group - Byte0~3
				elif row.Cells[2].Value == "DQ":
					bit_num = int(re.sub(r'[^0-9]','',row.Cells[3].Value))
					if 0 <= bit_num <= 7: # Byte0
						row.Cells[4].Value = "Byte0"
					elif 8 <= bit_num <= 15: # Byte1
						row.Cells[4].Value = "Byte1"
					elif 16 <= bit_num <= 23: # Byte2
						row.Cells[4].Value = "Byte2"
					elif 24 <= bit_num <= 31: # Byte3
						row.Cells[4].Value = "Byte3"

				#  for DQS Group
				elif row.Cells[2].Value == "DQS":
					pass

				#  for CLK Group
				elif row.Cells[2].Value == "CLK":
					pass

				#  for ADDR Group
				elif row.Cells[2].Value == "ADDR":
					pass

				#  for OTHER Group
				elif row.Cells[2].Value == "OTHER":
					pass

		except Exception as e:		
			Log("[Auto Group] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to group target traces","Warning")			
			EXIT()
					
	def Button_EditRuleClick(self, sender, e):
		sub_DB.Env_Form = EnvEditor(sub_DB.Cenv["File"])
		sub_DB.Env_Form.ShowDialog()		

	def Button_IdentifyClick(self, sender, e):
		try:
			Cenv = {}
			File = sub_DB.Cenv["File"]
			with open(File) as fp:
				# Load Input File
				for line in fp:				
					if line.strip() != "":						
						if line.find("<DM>") != -1:
							key="<DM>"
							temp_data = []
							temp = line.strip().split("=")[-1].split(",")
							for cell in temp:
								if not cell == "":
									temp_data.append(cell.strip())
							Cenv[key+"[Net Identification]"] =  temp_data

						elif line.find("<DQ>") != -1:
							key="<DQ>"
							temp_data = []
							temp = line.strip().split("=")[-1].split(",")
							for cell in temp:
								if not cell == "":
									temp_data.append(cell.strip())
							Cenv[key+"[Net Identification]"] =  temp_data

						elif line.find("<DQS_P>") != -1:
							key="<DQS_P>"
							temp_data = []
							temp = line.strip().split("=")[-1].split(",")
							for cell in temp:
								if not cell == "":
									temp_data.append(cell.strip())
							Cenv[key+"[Net Identification]"] =  temp_data

						elif line.find("<DQS_N>") != -1:
							key="<DQS_N>"
							temp_data = []
							temp = line.strip().split("=")[-1].split(",")
							for cell in temp:
								if not cell == "":
									temp_data.append(cell.strip())
							Cenv[key+"[Net Identification]"] =  temp_data

						elif line.find("<CLK_P>") != -1:
							key="<CLK_P>"
							temp_data = []
							temp = line.strip().split("=")[-1].split(",")
							for cell in temp:
								if not cell == "":
									temp_data.append(cell.strip())
							Cenv[key+"[Net Identification]"] =  temp_data

						elif line.find("<CLK_N>") != -1:
							key="<CLK_N>"
							temp_data = []
							temp = line.strip().split("=")[-1].split(",")
							for cell in temp:
								if not cell == "":
									temp_data.append(cell.strip())
							Cenv[key+"[Net Identification]"] =  temp_data

						elif line.find("<ADDR>") != -1:
							key="<ADDR>"
							temp_data = []
							temp = line.strip().split("=")[-1].split(",")
							for cell in temp:
								if not cell == "":
									temp_data.append(cell.strip())
							Cenv[key+"[Net Identification]"] =  temp_data

						elif line.find("<Ignore>") != -1:
							key="<Ignore>"
							temp_data = []
							temp = line.strip().split("=")[-1].split(",")
							for cell in temp:
								if not cell == "":
									temp_data.append(cell.strip())
							Cenv[key+"[Net Identification]"] =  temp_data

			fp.close()
			self._DataGridView.Rows.Clear()
			sub_DB.Cenv = Cenv
			sub_DB.Cenv["File"] = File
			self.Text = "Target Net Setup - " + sub_DB.Cenv["File"].split("\\")[-1]

			LVitem_List = []
			iter = 0
			for net in sub_DB.Netlist:			
				Group_idx, Match = Net_Identify(net.strip(), sub_DB.Cenv)
				if Group_idx == 1: # for DQ Group -> Check
					self._DataGridView.Rows.Add(True, net, self._Col_Group.Items[Group_idx], Match, self._Col_AnalyzeGroup.Items[0])
				else: # Un-check
					self._DataGridView.Rows.Add(False, net, self._Col_Group.Items[Group_idx], Match, self._Col_AnalyzeGroup.Items[0])

			# Back-up the Current Displayed Row and Matched Name
			Backup_row = []
			Name = []
			for row in self._DataGridView.Rows:
				Backup_row.append(row)
				Name.append(row.Cells[3].Value)

			# "abc" -> [a, b, c] -> ord(a) + ord(b) + ord(c) = val
			# sort val and get index => Name_idx
			Name_idx = []
			for name in Name:
				temp_list = list(name)
				val = 0
				flag = True
				for text in temp_list:
					if 47 < ord(text) < 58:
						val += ord(text)							
					else:
						if flag:
							val += ord(text)*1000
							flag = False
						else:
							val += ord(text)

				Name_idx.append(val)
			Name_idx = sorted(range(len(Name_idx)),key=lambda k: Name_idx[k], reverse=sub_DB.NetSort_Flag)

			# Clear row and add row as sorted sequentially
			self._DataGridView.Rows.Clear()
			for i in range(0, len(Name_idx)):
				self._DataGridView.Rows.Add(Backup_row[Name_idx[i]])

			for row in self._DataGridView.Rows:
				if row.Cells[0].Value:
					row.DefaultCellStyle.BackColor = System.Drawing.SystemColors.Info

		except Exception as e:		
			Log("[Net Identify] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to identify target nets","Warning")			
			EXIT()

	def Button_ExportClick(self, sender, e):
		try:
			Log("	<Export Excel Report> = Start")
			Log("		(Report Format) = %s" % sub_DB.Option_Form._ComboBox_ReportFormat.Text)
			# AEDT Input
			if sub_DB.InputFile_Flag == 1:
				# Eye plot checked
				if self._CheckBox_PlotEye.Checked:
					# Eye diagrams were generated					
					if not len(sub_DB.Excel_Img_File) == 0:
						# Default
						if self._ComboBox_Report.SelectedIndex == 0:
							Create_Excel_Report()
						# +Setup/Hold
						elif self._ComboBox_Report.SelectedIndex == 1:
							Create_Setup_Hold_Excel_Report()

					# Eye diagrams were not generated
					else:
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
									Log("			= %s" % Report_Name)
									Plot_Eye(Report_Name, [net], vmin, vmax, sub_DB.Eye_Measure_Results, True)
								
							else:								
								Log("			= %s" % key)
								Plot_Eye(key, Plot_list[key], vmin, vmax, sub_DB.Eye_Measure_Results, True)

						# Default
						if self._ComboBox_Report.SelectedIndex == 0:
							Create_Excel_Report()
						# +Setup/Hold
						elif self._ComboBox_Report.SelectedIndex == 1:
							Create_Setup_Hold_Excel_Report()

				# Eye plot unchecked
				else:
					# Default w/o figure
					if self._ComboBox_Report.SelectedIndex == 0:
						Create_Excel_Report_wo_fig()
					# +Setup/Hold w/o figure
					elif self._ComboBox_Report.SelectedIndex == 1:
						Create_Setup_Hold_Excel_Report_wo_fig()

			# CSV Input
			elif sub_DB.InputFile_Flag == 2:
				# Eye plot checked
				if self._CheckBox_PlotEye.Checked:
					# Eye diagrams were generated
					if not len(sub_DB.Excel_Img_File) == 0:
						# Default
						if sub_DB.Option_Form._ComboBox_ReportFormat.SelectedIndex == 0:
							Create_Excel_Report_Imported()
						#elif sub_DB.Option_Form._ComboBox_ReportFormat.SelectedIndex == 1:
						#	Create_Setup_Hold_Excel_Report_Imported()

					# Eye diagrams were not generated
					else:
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

						#self.TopMost = True
						#sub_DB.Cal_Form.TopMost = True
						sub_AEDT.Set_AEDT_PlotTemplate()
						Log("		(Plot Template) = Done")
						#self.TopMost = False
						#sub_DB.Cal_Form.TopMost = False

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
									Import_file = Gen_waveform_file(sub_DB.Eye_Form._TextBox_InputFile.Text, net, False)
									Log("			= %s" % Report_Name)
									Plot_Eye_Import(Report_Name, Import_file, [net], vmin, vmax, sub_DB.Eye_Measure_Results, True)
									os.remove(Import_file)
								
							else:
								AEDT_File = AEDT_File.split(".")[0] + "_Group." + AEDT_File.split(".")[-1]																		
								Import_file = Gen_waveform_file(sub_DB.Eye_Form._TextBox_InputFile.Text, Plot_list[key], True)
								Log("			= %s" % key)
								Plot_Eye_Import(key, Import_file, Plot_list[key], vmin, vmax, sub_DB.Eye_Measure_Results, True)
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
						# Default
						if sub_DB.Option_Form._ComboBox_ReportFormat.SelectedIndex == 0:
							Create_Excel_Report_Imported()

				# Eye plot unchecked
				else:
					# Default w/o figure
					if sub_DB.Option_Form._ComboBox_ReportFormat.SelectedIndex == 0:
						Create_Excel_Report_Imported_wo_fig()					

			Log("	<Export Excel Report> = Done")

		except Exception as e:						
			Log("	<Export Excel Report> = Failed")
			Log(traceback.format_exc())			
			MessageBox.Show("Fail to export excel report","Warning")
			EXIT()

	def Button_CloseClick(self, sender, e):
		if sub_DB.Result_Flag:
			try:
				############################
				# Analyze Method : Default #
				############################
				if sub_DB.Option_Form._ComboBox_Analyze.SelectedIndex == 0:
					Log("	<Eye Analyze Results - %s>" % sub_DB.Option_Form._ComboBox_Analyze.Text)
					Log("		= Net Name, Eye Width[ps], Timing Margin[ps], Analyze Group, Signal Group, Matched String")
					for row in self._DataGridView.Rows:
						if row.Cells[0].Value:
							Log("		= %s, %s, %s, %s, %s, %s" % (row.Cells[1].Value, row.Cells[5].Value, row.Cells[6].Value, row.Cells[4].Value, row.Cells[2].Value, row.Cells[3].Value))

				#################################
				# Analyze Method : + Setup/Hold #
				#################################
				elif sub_DB.Option_Form._ComboBox_Analyze.SelectedIndex == 1:
					Log("	<Eye Analyze Results - %s>" % sub_DB.Option_Form._ComboBox_Analyze.Text)
					Log("		= Net Name, Eye Width[ps], Setup Margin[ps], Hold Margin[ps], Timing Margin[ps], Analyze Group, Signal Group, Matched String")
					for row in self._DataGridView.Rows:
						if row.Cells[0].Value:
							Log("		= %s, %s, %s, %s, %s, %s, %s, %s" % (row.Cells[1].Value, row.Cells[5].Value, row.Cells[7].Value, row.Cells[8].Value, row.Cells[6].Value, row.Cells[4].Value, row.Cells[2].Value, row.Cells[3].Value))

				sub_DB.Net_Form = self
				self.Close()

			except Exception as e:
				Log("	<Close Eye Analyze Results Form> = Failed")
				Log(traceback.format_exc())
				print traceback.format_exc()
				MessageBox.Show("Fail to Close Eye Analyze Results Form","Warning")			
				EXIT()

		else:
			try:
				Log("[Net Classification]")
				Log("	<Target Nets>")
				for row in self._DataGridView.Rows:
					if row.Cells[0].Value:
						Log("		= %s, %s, %s, %s" % (row.Cells[1].Value, row.Cells[2].Value, row.Cells[3].Value, row.Cells[4].Value))

				sub_DB.Net_Form = self				
				sub_DB.Eye_Form._ComboBox_DDRGen.BackColor = System.Drawing.SystemColors.Window
				sub_DB.Eye_Form._ComboBox_DataRate.BackColor = System.Drawing.SystemColors.Window
				self.Close()

			except Exception as e:
				Log("[Close Net Form] = Failed")
				Log(traceback.format_exc())
				MessageBox.Show("Fail to close Net Classification Form","Warning")			
				EXIT()

class CalForm(Form):
	def __init__(self, Location):

		self.InitializeComponent(Location)
	
	def InitializeComponent(self, Location):
		path = os.path.dirname(os.path.abspath(__file__))
		self._Label_Vref = System.Windows.Forms.Label()
		self._ProgressBar_Vref = System.Windows.Forms.ProgressBar()
		self.SuspendLayout()
		# 
		# Label_Vref
		# 
		self._Label_Vref.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_Vref.Location = System.Drawing.Point(12, 9)
		self._Label_Vref.Name = "Label_Vref"
		self._Label_Vref.Size = System.Drawing.Size(260, 28)
		self._Label_Vref.TabIndex = 10
		self._Label_Vref.Text = ""		
		self._Label_Vref.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# ProgressBar_Vref
		# 
		self._ProgressBar_Vref.BackColor = System.Drawing.SystemColors.Control
		self._ProgressBar_Vref.Location = System.Drawing.Point(12, 40)
		self._ProgressBar_Vref.Name = "ProgressBar_Vref"
		self._ProgressBar_Vref.Size = System.Drawing.Size(300, 22)
		self._ProgressBar_Vref.Style = System.Windows.Forms.ProgressBarStyle.Continuous
		self._ProgressBar_Vref.Minimum = 0
		self._ProgressBar_Vref.Maximum = 100
		self._ProgressBar_Vref.Value = 0
		self._ProgressBar_Vref.TabIndex = 42
		# 
		# Cal_Form
		# 
		self.AutoScaleMode = System.Windows.Forms.AutoScaleMode.None
		self.ClientSize = System.Drawing.Size(324, 74)
		self.Controls.Add(self._ProgressBar_Vref)
		self.Controls.Add(self._Label_Vref)
		IconFile = path + "\\Resources\\LOGO.ico"
		self.Icon = Icon(IconFile)
		self.StartPosition = System.Windows.Forms.FormStartPosition.Manual		
		self.Location = System.Drawing.Point(Location[0], Location[1])		
		self.Name = "Cal_Form"
		self.Text = ""
		self.ResumeLayout(False)

class OptionForm(Form):
	def __init__(self, idx):
		# Select DDR Wizard Process
		global process_idx
		process_idx = idx
		self.InitializeComponent()
	
	def InitializeComponent(self):
		global path
		path = os.path.dirname(os.path.abspath(__file__))
		TreeNode_EM = System.Windows.Forms.TreeNode("EM Extractor")
		TreeNode_Tran = System.Windows.Forms.TreeNode("Circuit Simulator")
		TreeNode_Eye = System.Windows.Forms.TreeNode("Eye Analyzer")
		#TreeNode_Comp = System.Windows.Forms.TreeNode("Compliance Test")
		self._TreeView = System.Windows.Forms.TreeView()

		self._GroupBox_General = System.Windows.Forms.GroupBox()
		self._GroupBox_Eye = System.Windows.Forms.GroupBox()
		self._GroupBox_EM = System.Windows.Forms.GroupBox()
		self._GroupBox_Tran = System.Windows.Forms.GroupBox()
		self._GroupBox_Comp = System.Windows.Forms.GroupBox()

		self._Button_Import_Resource = System.Windows.Forms.Button()
		self._Button_Import_Def = System.Windows.Forms.Button()
		self._Button_Import_Conf = System.Windows.Forms.Button()
		self._Button_OutputExcelFile = System.Windows.Forms.Button()
		self._Button_Compliance = System.Windows.Forms.Button()
		self._Button_Cancel = System.Windows.Forms.Button()
		self._Button_OK = System.Windows.Forms.Button()
		
		self._Label_Resource = System.Windows.Forms.Label()
		self._Label_Def = System.Windows.Forms.Label()
		self._Label_Conf = System.Windows.Forms.Label()
		self._Label_EyeOffset = System.Windows.Forms.Label()
		self._Label_EyeOffset_Unit = System.Windows.Forms.Label()
		self._Label_TotalWaveform = System.Windows.Forms.Label()
		self._Label_Vref = System.Windows.Forms.Label()		
		self._Label_mV = System.Windows.Forms.Label()
		self._Label_Analyze = System.Windows.Forms.Label()
		self._Label_ImageWidth = System.Windows.Forms.Label()
		self._Label_ImageWidth_Unit = System.Windows.Forms.Label()
		self._Label_ReportFormat = System.Windows.Forms.Label()
		self._Label_OutputExcelFile = System.Windows.Forms.Label()
		self._Label_V_Border1 = System.Windows.Forms.Label()
		self._Label_V_Border2 = System.Windows.Forms.Label()
		self._Label_V_Border3 = System.Windows.Forms.Label()		
				
		self._ComboBox_Vref = System.Windows.Forms.ComboBox()
		self._ComboBox_Analyze = System.Windows.Forms.ComboBox()
		self._ComboBox_ReportFormat = System.Windows.Forms.ComboBox()

		self._TextBox_Resource = System.Windows.Forms.TextBox()
		self._TextBox_Def = System.Windows.Forms.TextBox()
		self._TextBox_Conf = System.Windows.Forms.TextBox()
		self._TextBox_EyeOffset = System.Windows.Forms.TextBox()
		self._TextBox_Vref = System.Windows.Forms.TextBox()
		self._TextBox_ImageWidth = System.Windows.Forms.TextBox()		
		self._TextBox_OutputExcelFile = System.Windows.Forms.TextBox()

		self._CheckBox_PlotEye = System.Windows.Forms.CheckBox()
		self._CheckBox_ExportExcelReport = System.Windows.Forms.CheckBox()
		self._CheckBox_Compiance = System.Windows.Forms.CheckBox()
		
		self._folderBrowserDialog1 = System.Windows.Forms.FolderBrowserDialog()
		self._openFileDialog1 = System.Windows.Forms.OpenFileDialog()
		self._saveFileDialog1 = System.Windows.Forms.SaveFileDialog()

		self._GroupBox_General.SuspendLayout()
		self._GroupBox_Eye.SuspendLayout()
		self.SuspendLayout()
		# 
		# TreeView
		# 
		self._TreeView.Font = System.Drawing.Font("Arial", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TreeView.Location = System.Drawing.Point(12, 12)
		self._TreeView.Name = "TreeView"
		TreeNode_EM.Name = "EM Extractor"
		TreeNode_EM.Text = "EM Extractor"
		TreeNode_Tran.Name = "Circuit Simulator"
		TreeNode_Tran.Text = "Circuit Simulator"
		TreeNode_Eye.Name = "Eye Analyzer"
		TreeNode_Eye.Text = "Eye Analyzer"
		#TreeNode_Comp.Name = "Compliance Test"
		#TreeNode_Comp.Text = "Compliance Test"
		#self._TreeView.Nodes.AddRange(System.Array[System.Windows.Forms.TreeNode](
		#	[TreeNode_EM,
		#	TreeNode_Tran,
		#	TreeNode_Eye]))
		self._TreeView.Nodes.AddRange(System.Array[System.Windows.Forms.TreeNode](
			[TreeNode_Eye]))
		self._TreeView.Size = System.Drawing.Size(132, 269)
		self._TreeView.TabIndex = 0
		self._TreeView.NodeMouseClick += self.TreeViewNodeMouseClick
		# 
		# GroupBox_General
		# 
		self._GroupBox_General.Controls.Add(self._Button_Import_Conf)
		self._GroupBox_General.Controls.Add(self._Button_Import_Def)
		self._GroupBox_General.Controls.Add(self._TextBox_Conf)
		self._GroupBox_General.Controls.Add(self._TextBox_Def)
		self._GroupBox_General.Controls.Add(self._Button_Import_Resource)
		self._GroupBox_General.Controls.Add(self._TextBox_Resource)
		self._GroupBox_General.Controls.Add(self._Label_Conf)
		self._GroupBox_General.Controls.Add(self._Label_Def)
		self._GroupBox_General.Controls.Add(self._Label_Resource)
		self._GroupBox_General.Font = System.Drawing.Font("Arial", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._GroupBox_General.Location = System.Drawing.Point(255, 6)
		self._GroupBox_General.Name = "GroupBox_General"
		self._GroupBox_General.Size = System.Drawing.Size(543, 129)
		self._GroupBox_General.TabIndex = 33
		self._GroupBox_General.TabStop = False
		self._GroupBox_General.Visible = False
		self._GroupBox_General.Text = "General Directories"
		# 
		# GroupBox_EM
		# 
		self._GroupBox_EM.Font = System.Drawing.Font("Arial", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._GroupBox_EM.Location = System.Drawing.Point(155, 6)
		self._GroupBox_EM.Name = "GroupBox_EM"
		self._GroupBox_EM.Size = System.Drawing.Size(543, 275)
		self._GroupBox_EM.TabIndex = 35
		self._GroupBox_EM.TabStop = False
		self._GroupBox_EM.Visible = False
		self._GroupBox_EM.Text = "EM Extractor"
		# 
		# GroupBox_Tran
		# 
		self._GroupBox_Tran.Font = System.Drawing.Font("Arial", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._GroupBox_Tran.Location = System.Drawing.Point(155, 6)
		self._GroupBox_Tran.Name = "GroupBox_Tran"
		self._GroupBox_Tran.Size = System.Drawing.Size(543, 275)
		self._GroupBox_Tran.TabIndex = 36
		self._GroupBox_Tran.TabStop = False
		self._GroupBox_Tran.Visible = False
		self._GroupBox_Tran.Text = "Circuit Simulator"
		# 
		# GroupBox_Eye
		#
		self._GroupBox_Eye.Controls.Add(self._Label_OutputExcelFile)
		self._GroupBox_Eye.Controls.Add(self._Button_Compliance)
		self._GroupBox_Eye.Controls.Add(self._CheckBox_Compiance)
		self._GroupBox_Eye.Controls.Add(self._ComboBox_ReportFormat)
		self._GroupBox_Eye.Controls.Add(self._Label_ReportFormat)
		self._GroupBox_Eye.Controls.Add(self._Label_mV)
		self._GroupBox_Eye.Controls.Add(self._TextBox_Vref)
		self._GroupBox_Eye.Controls.Add(self._ComboBox_Analyze)
		self._GroupBox_Eye.Controls.Add(self._Label_Analyze)
		self._GroupBox_Eye.Controls.Add(self._ComboBox_Vref)
		self._GroupBox_Eye.Controls.Add(self._Label_Vref)
		self._GroupBox_Eye.Controls.Add(self._Label_V_Border3)
		self._GroupBox_Eye.Controls.Add(self._Label_V_Border2)		
		self._GroupBox_Eye.Controls.Add(self._Label_V_Border1)
		self._GroupBox_Eye.Controls.Add(self._Button_OutputExcelFile)
		self._GroupBox_Eye.Controls.Add(self._TextBox_OutputExcelFile)		
		self._GroupBox_Eye.Controls.Add(self._Label_ImageWidth_Unit)
		self._GroupBox_Eye.Controls.Add(self._TextBox_ImageWidth)				
		self._GroupBox_Eye.Controls.Add(self._Label_ImageWidth)
		self._GroupBox_Eye.Controls.Add(self._CheckBox_ExportExcelReport)		
		self._GroupBox_Eye.Controls.Add(self._CheckBox_PlotEye)
		self._GroupBox_Eye.Controls.Add(self._Label_TotalWaveform)
		self._GroupBox_Eye.Controls.Add(self._Label_EyeOffset_Unit)
		self._GroupBox_Eye.Controls.Add(self._TextBox_EyeOffset)
		self._GroupBox_Eye.Controls.Add(self._Label_EyeOffset)
		self._GroupBox_Eye.Font = System.Drawing.Font("Arial", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._GroupBox_Eye.Location = System.Drawing.Point(155, 6)
		self._GroupBox_Eye.Name = "GroupBox_Eye"
		self._GroupBox_Eye.Size = System.Drawing.Size(453, 275)
		self._GroupBox_Eye.TabIndex = 34
		self._GroupBox_Eye.TabStop = False
		self._GroupBox_Eye.Visible = False
		self._GroupBox_Eye.Text = "Eye Analyzer"
		# 
		# GroupBox_Comp
		# 
		self._GroupBox_Comp.Font = System.Drawing.Font("Arial", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._GroupBox_Comp.Location = System.Drawing.Point(255, 141)
		self._GroupBox_Comp.Name = "GroupBox_Comp"
		self._GroupBox_Comp.Size = System.Drawing.Size(543, 275)
		self._GroupBox_Comp.TabIndex = 36
		self._GroupBox_Comp.TabStop = False
		self._GroupBox_Comp.Visible = False
		self._GroupBox_Comp.Text = "Compliance Test"
		# 
		# Button_Import_Resource
		# 
		self._Button_Import_Resource.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_Import_Resource.Location = System.Drawing.Point(498, 22)
		self._Button_Import_Resource.Name = "Button_Import_Resource"
		self._Button_Import_Resource.Size = System.Drawing.Size(36, 23)
		self._Button_Import_Resource.TabIndex = 39
		self._Button_Import_Resource.Text = "..."
		self._Button_Import_Resource.UseVisualStyleBackColor = True
		self._Button_Import_Resource.Click += self.Button_Import_ResourceClick
		# 
		# Button_Import_Def
		# 
		self._Button_Import_Def.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_Import_Def.Location = System.Drawing.Point(498, 52)
		self._Button_Import_Def.Name = "Button_Import_Def"
		self._Button_Import_Def.Size = System.Drawing.Size(36, 23)
		self._Button_Import_Def.TabIndex = 42
		self._Button_Import_Def.Text = "..."
		self._Button_Import_Def.UseVisualStyleBackColor = True
		self._Button_Import_Def.Click += self.Button_Import_DefClick
		# 
		# Button_Import_Conf
		# 
		self._Button_Import_Conf.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_Import_Conf.Location = System.Drawing.Point(498, 84)
		self._Button_Import_Conf.Name = "Button_Import_Conf"
		self._Button_Import_Conf.Size = System.Drawing.Size(36, 23)
		self._Button_Import_Conf.TabIndex = 43
		self._Button_Import_Conf.Text = "..."
		self._Button_Import_Conf.UseVisualStyleBackColor = True
		self._Button_Import_Conf.Click += self.Button_Import_ConfClick
		# 
		# Button_OutputExcelFile
		# 
		self._Button_OutputExcelFile.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_OutputExcelFile.Location = System.Drawing.Point(498, 189)
		self._Button_OutputExcelFile.Name = "Button_OutputExcelFile"
		self._Button_OutputExcelFile.Size = System.Drawing.Size(36, 23)
		self._Button_OutputExcelFile.TabIndex = 55
		self._Button_OutputExcelFile.Text = "..."
		self._Button_OutputExcelFile.UseVisualStyleBackColor = True
		self._Button_OutputExcelFile.Visible = False
		self._Button_OutputExcelFile.Click += self.Button_OutputExcelFileClick
		# 
		# Button_Compliance
		# 
		self._Button_Compliance.Font = System.Drawing.Font("Arial", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_Compliance.Location = System.Drawing.Point(214, 192)
		self._Button_Compliance.Name = "Button_Compliance"
		self._Button_Compliance.Size = System.Drawing.Size(121, 23)
		self._Button_Compliance.TabIndex = 69
		self._Button_Compliance.Text = "Compliance Setup"
		self._Button_Compliance.UseVisualStyleBackColor = True
		self._Button_Compliance.Visible = False
		self._Button_Compliance.Click += self.Button_ComplianceClick
		# 
		# Button_OK
		# 
		self._Button_OK.Font = System.Drawing.Font("Arial", 9)
		self._Button_OK.Location = System.Drawing.Point(462, 287)
		self._Button_OK.Name = "Button_OK"
		self._Button_OK.Size = System.Drawing.Size(70, 28)
		self._Button_OK.TabIndex = 32
		self._Button_OK.Text = "OK"
		self._Button_OK.UseVisualStyleBackColor = True
		self._Button_OK.Click += self.Button_OKClick
		# 
		# Button_Cancel
		# 
		self._Button_Cancel.Font = System.Drawing.Font("Arial", 9)
		self._Button_Cancel.Location = System.Drawing.Point(538, 287)
		self._Button_Cancel.Name = "Button_Cancel"
		self._Button_Cancel.Size = System.Drawing.Size(70, 28)
		self._Button_Cancel.TabIndex = 29
		self._Button_Cancel.Text = "Cancel"
		self._Button_Cancel.UseVisualStyleBackColor = True		
		self._Button_Cancel.Click += self.Button_CancelClick
		# 
		# Label_Resource
		# 
		self._Label_Resource.Font = System.Drawing.Font("Arial", 9)
		self._Label_Resource.Location = System.Drawing.Point(6, 17)
		self._Label_Resource.Name = "Label_Resource"
		self._Label_Resource.Size = System.Drawing.Size(115, 28)
		self._Label_Resource.TabIndex = 34
		self._Label_Resource.Text = "Resources Folder :"
		self._Label_Resource.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_Def
		# 
		self._Label_Def.Font = System.Drawing.Font("Arial", 9)
		self._Label_Def.Location = System.Drawing.Point(6, 49)
		self._Label_Def.Name = "Label_Def"
		self._Label_Def.Size = System.Drawing.Size(115, 28)
		self._Label_Def.TabIndex = 35
		self._Label_Def.Text = "Definition File :"
		self._Label_Def.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_Conf
		# 
		self._Label_Conf.Font = System.Drawing.Font("Arial", 9)
		self._Label_Conf.Location = System.Drawing.Point(6, 81)
		self._Label_Conf.Name = "Label_Conf"
		self._Label_Conf.Size = System.Drawing.Size(115, 28)
		self._Label_Conf.TabIndex = 36
		self._Label_Conf.Text = "Configuration File :"
		self._Label_Conf.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_EyeOffset
		# 
		self._Label_EyeOffset.Font = System.Drawing.Font("Arial", 9)
		self._Label_EyeOffset.Location = System.Drawing.Point(6, 26)
		self._Label_EyeOffset.Name = "Label_EyeOffset"
		self._Label_EyeOffset.Size = System.Drawing.Size(115, 28)
		self._Label_EyeOffset.TabIndex = 37
		self._Label_EyeOffset.Text = "EYE Offset :"
		self._Label_EyeOffset.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_EyeOffset_Unit
		# 
		self._Label_EyeOffset_Unit.Font = System.Drawing.Font("Arial", 9)
		self._Label_EyeOffset_Unit.Location = System.Drawing.Point(216, 26)
		self._Label_EyeOffset_Unit.Name = "Label_EyeOffset_Unit"
		self._Label_EyeOffset_Unit.Size = System.Drawing.Size(36, 28)
		self._Label_EyeOffset_Unit.TabIndex = 43
		self._Label_EyeOffset_Unit.Text = "[ns]"
		self._Label_EyeOffset_Unit.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_TotalWaveform
		# 
		self._Label_TotalWaveform.Font = System.Drawing.Font("Arial", 9)
		self._Label_TotalWaveform.Location = System.Drawing.Point(245, 26)
		self._Label_TotalWaveform.Name = "Label_TotalWaveform"
		self._Label_TotalWaveform.Size = System.Drawing.Size(199, 28)
		self._Label_TotalWaveform.TabIndex = 44
		self._Label_TotalWaveform.Text = ", (Total Waveform Length = N/A)"
		self._Label_TotalWaveform.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_Vref
		# 
		self._Label_Vref.Font = System.Drawing.Font("Arial", 9)
		self._Label_Vref.Location = System.Drawing.Point(6, 72)
		self._Label_Vref.Name = "Label_Vref"
		self._Label_Vref.Size = System.Drawing.Size(115, 28)
		self._Label_Vref.TabIndex = 60
		self._Label_Vref.Text = "Vcent_DQ (Vref) :"
		self._Label_Vref.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# Label_mV
		# 
		self._Label_mV.Font = System.Drawing.Font("Arial", 9)
		self._Label_mV.Location = System.Drawing.Point(254, 72)
		self._Label_mV.Name = "Label_mV"
		self._Label_mV.Size = System.Drawing.Size(36, 28)
		self._Label_mV.TabIndex = 65
		self._Label_mV.Text = "[mV]"
		self._Label_mV.Visible = False
		self._Label_mV.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_Analyze
		# 
		self._Label_Analyze.Font = System.Drawing.Font("Arial", 9)
		self._Label_Analyze.Location = System.Drawing.Point(274, 72)
		self._Label_Analyze.Name = "Label_Analyze"
		self._Label_Analyze.Size = System.Drawing.Size(71, 28)
		self._Label_Analyze.TabIndex = 62
		self._Label_Analyze.Text = "Analyze :"
		self._Label_Analyze.TextAlign = System.Drawing.ContentAlignment.MiddleRight		
		# 
		# Label_ImageWidth
		# 
		self._Label_ImageWidth.Font = System.Drawing.Font("Arial", 9)
		self._Label_ImageWidth.Location = System.Drawing.Point(73, 152)
		self._Label_ImageWidth.Name = "Label_ImageWidth"
		self._Label_ImageWidth.Size = System.Drawing.Size(85, 28)
		self._Label_ImageWidth.TabIndex = 47
		self._Label_ImageWidth.Text = "Image Width :"
		self._Label_ImageWidth.Visible = False
		self._Label_ImageWidth.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_ImageWidth_Unit
		# 
		self._Label_ImageWidth_Unit.Font = System.Drawing.Font("Arial", 9)
		self._Label_ImageWidth_Unit.Location = System.Drawing.Point(219, 152)
		self._Label_ImageWidth_Unit.Name = "Label_ImageWidth_Unit"
		self._Label_ImageWidth_Unit.Size = System.Drawing.Size(51, 28)
		self._Label_ImageWidth_Unit.TabIndex = 49
		self._Label_ImageWidth_Unit.Text = "[pixel]"
		self._Label_ImageWidth_Unit.Visible = False
		self._Label_ImageWidth_Unit.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_ReportFormat
		# 		
		self._Label_ReportFormat.Font = System.Drawing.Font("Arial", 9)
		self._Label_ReportFormat.Location = System.Drawing.Point(276, 152)
		self._Label_ReportFormat.Name = "Label_ReportFormat"
		self._Label_ReportFormat.Size = System.Drawing.Size(52, 28)
		self._Label_ReportFormat.TabIndex = 66
		self._Label_ReportFormat.Text = "Format :"
		self._Label_ReportFormat.Visible = False
		self._Label_ReportFormat.TextAlign = System.Drawing.ContentAlignment.MiddleLeft		
		# 
		# Label_OutputExcelFile
		# 
		self._Label_OutputExcelFile.Font = System.Drawing.Font("Arial", 9)
		self._Label_OutputExcelFile.Location = System.Drawing.Point(73, 186)
		self._Label_OutputExcelFile.Name = "Label_OutputExcelFile"
		self._Label_OutputExcelFile.Size = System.Drawing.Size(313, 28)
		self._Label_OutputExcelFile.TabIndex = 53
		self._Label_OutputExcelFile.Text = "Result Directory : " + sub_DB.result_dir
		self._Label_OutputExcelFile.Visible = False
		self._Label_OutputExcelFile.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_V_Border1
		# 
		self._Label_V_Border1.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
		self._Label_V_Border1.Location = System.Drawing.Point(11, 62)
		self._Label_V_Border1.Name = "Label_V_Border1"
		self._Label_V_Border1.Size = System.Drawing.Size(432, 2)
		self._Label_V_Border1.TabIndex = 56		
		# 
		# Label_V_Border2
		# 
		self._Label_V_Border2.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
		self._Label_V_Border2.Location = System.Drawing.Point(11, 112)
		self._Label_V_Border2.Name = "Label_V_Border2"
		self._Label_V_Border2.Size = System.Drawing.Size(432, 2)
		self._Label_V_Border2.TabIndex = 58
		# 
		# Label_V_Border3
		# 
		self._Label_V_Border3.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
		self._Label_V_Border3.Location = System.Drawing.Point(11, 225)
		self._Label_V_Border3.Name = "Label_V_Border3"
		self._Label_V_Border3.Size = System.Drawing.Size(432, 2)
		self._Label_V_Border3.TabIndex = 59		
		# 
		# ComboBox_Vref
		# 
		self._ComboBox_Vref.FormattingEnabled = True
		self._ComboBox_Vref.Items.AddRange(System.Array[System.Object](
			["Auto",
			"Manual"]))
		self._ComboBox_Vref.Location = System.Drawing.Point(127, 76)
		self._ComboBox_Vref.Name = "ComboBox_Vref"
		self._ComboBox_Vref.Size = System.Drawing.Size(70, 23)
		self._ComboBox_Vref.TabIndex = 61
		self._ComboBox_Vref.SelectedIndex = 0
		self._ComboBox_Vref.SelectedIndexChanged += self.ComboBox_VrefSelectedIndexChanged
		# 
		# ComboBox_Analyze
		# 
		self._ComboBox_Analyze.FormattingEnabled = True
		#self._ComboBox_Analyze.Items.AddRange(System.Array[System.Object](
		#	["Default",
		#	"+ Setup/Hold"]))
		#self._ComboBox_Analyze.Items.AddRange(System.Array[System.Object](
		#	["Default",
		#	"Auto-delay",
		#	"Tr-by-Tr"]))
		self._ComboBox_Analyze.Items.AddRange(System.Array[System.Object](
			["Default"]))
		self._ComboBox_Analyze.Location = System.Drawing.Point(348, 76)
		self._ComboBox_Analyze.Name = "ComboBox_Analyze"
		self._ComboBox_Analyze.Size = System.Drawing.Size(84, 23)
		self._ComboBox_Analyze.TabIndex = 63
		self._ComboBox_Analyze.Text = "Default"
		self._ComboBox_Analyze.SelectedIndexChanged += self.ComboBox_AnalyzeSelectedIndexChanged
		# 
		# ComboBox_ReportFormat
		# 
		self._ComboBox_ReportFormat.FormattingEnabled = True
		self._ComboBox_ReportFormat.Items.AddRange(System.Array[System.Object](
			["Default"]))
		self._ComboBox_ReportFormat.Location = System.Drawing.Point(328, 156)
		self._ComboBox_ReportFormat.Name = "ComboBox_ReportFormat"
		self._ComboBox_ReportFormat.Size = System.Drawing.Size(104, 23)
		self._ComboBox_ReportFormat.TabIndex = 67
		self._ComboBox_ReportFormat.Text = "Default"
		self._ComboBox_ReportFormat.Visible = False
		# 
		# TextBox_Resource
		# 
		self._TextBox_Resource.BackColor = System.Drawing.SystemColors.Window
		self._TextBox_Resource.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_Resource.Location = System.Drawing.Point(127, 22)
		self._TextBox_Resource.Name = "TextBox_Resource"
		self._TextBox_Resource.Size = System.Drawing.Size(365, 23)
		self._TextBox_Resource.TabIndex = 38		
		# 
		# TextBox_Def
		# 
		self._TextBox_Def.BackColor = System.Drawing.SystemColors.Window
		self._TextBox_Def.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_Def.Location = System.Drawing.Point(127, 52)
		self._TextBox_Def.Name = "TextBox_Def"
		self._TextBox_Def.Size = System.Drawing.Size(365, 23)
		self._TextBox_Def.TabIndex = 40
		# 
		# TextBox_Conf
		# 
		self._TextBox_Conf.BackColor = System.Drawing.SystemColors.Window
		self._TextBox_Conf.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_Conf.Location = System.Drawing.Point(127, 84)
		self._TextBox_Conf.Name = "TextBox_Conf"
		self._TextBox_Conf.Size = System.Drawing.Size(365, 23)
		self._TextBox_Conf.TabIndex = 41
		# 
		# TextBox_EyeOffset
		# 
		self._TextBox_EyeOffset.BackColor = System.Drawing.SystemColors.Window
		self._TextBox_EyeOffset.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_EyeOffset.Location = System.Drawing.Point(127, 29)
		self._TextBox_EyeOffset.Name = "TextBox_EyeOffset"
		self._TextBox_EyeOffset.Size = System.Drawing.Size(83, 23)
		self._TextBox_EyeOffset.Text = "7.5"
		self._TextBox_EyeOffset.TabIndex = 42
		self._TextBox_EyeOffset.TextChanged += self.TextBox_EyeOffsetTextChanged
		# 
		# TextBox_Vref
		# 
		self._TextBox_Vref.BackColor = System.Drawing.SystemColors.Window
		self._TextBox_Vref.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_Vref.Location = System.Drawing.Point(203, 76)
		self._TextBox_Vref.Name = "TextBox_Vref"
		self._TextBox_Vref.Size = System.Drawing.Size(50, 23)
		self._TextBox_Vref.Visible = False
		self._TextBox_Vref.TextChanged += self.TextBox_VrefTextChanged
		self._TextBox_Vref.TabIndex = 64
		# 
		# TextBox_ImageWidth
		# 
		self._TextBox_ImageWidth.BackColor = System.Drawing.SystemColors.Window
		self._TextBox_ImageWidth.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_ImageWidth.Location = System.Drawing.Point(160, 155)
		self._TextBox_ImageWidth.Name = "TextBox_ImageWidth"
		self._TextBox_ImageWidth.Size = System.Drawing.Size(53, 23)
		self._TextBox_ImageWidth.Text = "200"
		self._TextBox_ImageWidth.Visible = False
		self._TextBox_ImageWidth.TabIndex = 48
		self._TextBox_ImageWidth.TextChanged += self.TextBox_ImageWidthTextChanged
		# 
		# TextBox_OutputExcelFile
		# 
		self._TextBox_OutputExcelFile.BackColor = System.Drawing.SystemColors.Window
		self._TextBox_OutputExcelFile.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_OutputExcelFile.Location = System.Drawing.Point(180, 189)
		self._TextBox_OutputExcelFile.Name = "TextBox_OutputExcelFile"
		self._TextBox_OutputExcelFile.Size = System.Drawing.Size(312, 23)
		self._TextBox_OutputExcelFile.Text = ""
		self._TextBox_OutputExcelFile.Visible = False
		self._TextBox_OutputExcelFile.TabIndex = 54
		# 
		# CheckBox_PlotEye
		# 
		self._CheckBox_PlotEye.Font = System.Drawing.Font("Arial", 9)
		self._CheckBox_PlotEye.Location = System.Drawing.Point(50, 232)
		self._CheckBox_PlotEye.Name = "CheckBox_PlotEye"
		self._CheckBox_PlotEye.Size = System.Drawing.Size(136, 29)
		self._CheckBox_PlotEye.TabIndex = 45
		self._CheckBox_PlotEye.Text = "Plot EYE with Mask"
		self._CheckBox_PlotEye.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		self._CheckBox_PlotEye.Checked = False
		self._CheckBox_PlotEye.UseVisualStyleBackColor = True
		self._CheckBox_PlotEye.CheckedChanged += self.CheckBox_PlotEyeCheckedChanged
		# 
		# CheckBox_ExportExcelReport
		# 
		self._CheckBox_ExportExcelReport.Font = System.Drawing.Font("Arial", 9)
		self._CheckBox_ExportExcelReport.Location = System.Drawing.Point(50, 120)
		self._CheckBox_ExportExcelReport.Name = "CheckBox_ExportExcelReport"
		self._CheckBox_ExportExcelReport.Size = System.Drawing.Size(136, 29)
		self._CheckBox_ExportExcelReport.TabIndex = 46
		self._CheckBox_ExportExcelReport.Text = "Export Excel Report"
		self._CheckBox_ExportExcelReport.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		self._CheckBox_ExportExcelReport.Checked = False
		self._CheckBox_ExportExcelReport.UseVisualStyleBackColor = True
		self._CheckBox_ExportExcelReport.CheckedChanged += self.CheckBox_ExportExcelReportCheckedChanged
		# 
		# CheckBox_Compiance
		# 
		self._CheckBox_Compiance.Font = System.Drawing.Font("Arial", 9)
		self._CheckBox_Compiance.Location = System.Drawing.Point(50, 190)
		self._CheckBox_Compiance.Name = "CheckBox_Compiance"
		self._CheckBox_Compiance.Size = System.Drawing.Size(162, 29)
		self._CheckBox_Compiance.TabIndex = 68
		self._CheckBox_Compiance.Text = "Check DDR Compliance"
		self._CheckBox_Compiance.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		self._CheckBox_Compiance.UseVisualStyleBackColor = True
		self._CheckBox_Compiance.Visible = False
		self._CheckBox_Compiance.CheckedChanged += self.CheckBox_CompianceCheckedChanged
		# 
		# openFileDialog1
		# 
		self._openFileDialog1.FileName = "openFileDialog1"		
		# 
		# Option_Form
		# 
		self.ClientSize = System.Drawing.Size(615, 322)
		self.MinimumSize = System.Drawing.Size(self.Size.Width, self.Size.Height)
		self.MaximumSize = System.Drawing.Size(1500, self.Size.Height)
		self.FormSize_W = self.Size.Width
		self.FormSize_H = self.Size.Height
		self.Controls.Add(self._TreeView)
		self.Controls.Add(self._GroupBox_General)
		self.Controls.Add(self._GroupBox_EM)		
		self.Controls.Add(self._GroupBox_Tran)		
		self.Controls.Add(self._GroupBox_Eye)
		self.Controls.Add(self._GroupBox_Comp)
		self.Controls.Add(self._Button_OK)
		self.Controls.Add(self._Button_Cancel)
		IconFile = path + "\\Resources\\LOGO.ico"
		self.Icon = Icon(IconFile)
		self.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen		
		self.Name = "Option_Form"
		self.Text = "Ansys DDR Wizard Options"		
		self.Load += self.Option_FormLoad
		self.ResizeEnd += self.Option_FormResizeEnd		
		self._GroupBox_General.ResumeLayout(False)
		self._GroupBox_General.PerformLayout()
		self._GroupBox_Eye.ResumeLayout(False)
		self._GroupBox_Eye.PerformLayout()
		self.ResumeLayout(False)

	def Option_FormLoad(self, sender, e):
		try:
			self._TextBox_Resource.Text = path + "\\Resources"
			self._TextBox_Def.Text = sub_DB.Cenv["File"]
			self._TextBox_Conf.Text = sub_DB.Uenv["File"]

			# EM
			if process_idx == 0:
				self._GroupBox_EM.Visible = True
				self._GroupBox_Tran.Visible = False
				self._GroupBox_Eye.Visible = False
			
			# TRAN
			elif process_idx == 1:
				self._GroupBox_EM.Visible = False
				self._GroupBox_Tran.Visible = True
				self._GroupBox_Eye.Visible = False
				
			# EYE
			elif process_idx == 2:
				self._GroupBox_EM.Visible = False
				self._GroupBox_Tran.Visible = False
				self._GroupBox_Eye.Visible = True				
				self._TreeView.SelectedNode = self._TreeView.Nodes[0]

			#####################################
			# Add [+ Setup/Hold] Analyze Method #
			#####################################
			temp = []
			for row in sub_DB.Net_Form._DataGridView.Rows:
				temp.append(row.Cells[2].Value)

			#if "DQS_P" in temp and "DQS_N" in temp:
			#	self._ComboBox_Analyze.SelectedIndex = 1

			######################
			# Load Configuration #
			######################
			for key in sub_DB.Uenv:
				if "[Eye]" in key:
					if "<Analyze Option>" in key:
						# Vref Method
						if "(Vref Method)" in key:							
							sub_DB.Option_Form._ComboBox_Vref.SelectedIndex = int(sub_DB.Uenv[key][0])

						# Analyze Method
						elif "(Analyze Method)" in key:
							sub_DB.Option_Form._ComboBox_Analyze.SelectedIndex = int(sub_DB.Uenv[key][0])				
							
						# Report Format
						elif "(Report Format)" in key:
							sub_DB.Option_Form._ComboBox_ReportFormat.SelectedIndex = int(sub_DB.Uenv[key][0])
							
			###################
			# Set Manual Vref #
			###################
			if not sub_DB.Eye_Form._TextBox_VcentDQ.Text == "Auto":
				sub_DB.Option_Form._ComboBox_Vref.SelectedIndex = 1
				sub_DB.Option_Form._TextBox_Vref.Text = sub_DB.Eye_Form._TextBox_VcentDQ.Text

			if sub_DB.Debug_Mode:
				self.Button_OKClick(self, sender)

		except Exception as e:			
			Log("[Option Form Load] = Failed")
			Log(traceback.format_exc())
			print traceback.format_exc()
			MessageBox.Show("Fail to load Option Form","Warning")			
			EXIT()

	def Option_FormResizeEnd(self, sender, e):
		try:
			# Get previous Start_Form width/height and resized Start_Form width/height
			# Calculate Gap betweent previous and resized width/height
			Gap_W = self.Size.Width - self.FormSize_W
			Gap_H = self.Size.Height - self.FormSize_H

			# Backup the resized Start_Form width/height as previous MainFomr width/height
			self.FormSize_W = self.Size.Width
			self.FormSize_H = self.Size.Height

			# Resize
			self._GroupBox_General.Size = System.Drawing.Size(self._GroupBox_General.Width + Gap_W, self._GroupBox_General.Height)
			self._GroupBox_EM.Size = System.Drawing.Size(self._GroupBox_EM.Width + Gap_W, self._GroupBox_EM.Height)
			self._GroupBox_Tran.Size = System.Drawing.Size(self._GroupBox_Tran.Width + Gap_W, self._GroupBox_Tran.Height)
			self._GroupBox_Eye.Size = System.Drawing.Size(self._GroupBox_Eye.Width + Gap_W, self._GroupBox_Eye.Height)
			self._GroupBox_Comp.Size = System.Drawing.Size(self._GroupBox_Comp.Width + Gap_W, self._GroupBox_Comp.Height)
			self._TextBox_Resource.Size = System.Drawing.Size(self._TextBox_Resource.Width + Gap_W, self._TextBox_Resource.Height)
			self._TextBox_Def.Size = System.Drawing.Size(self._TextBox_Def.Width + Gap_W, self._TextBox_Def.Height)
			self._TextBox_Conf.Size = System.Drawing.Size(self._TextBox_Conf.Width + Gap_W, self._TextBox_Conf.Height)
			self._TextBox_OutputExcelFile.Size = System.Drawing.Size(self._TextBox_OutputExcelFile.Width + Gap_W, self._TextBox_OutputExcelFile.Height)
			self._Label_V_Border1.Size = System.Drawing.Size(self._Label_V_Border1.Width + Gap_W, self._Label_V_Border1.Height)
			self._Label_V_Border2.Size = System.Drawing.Size(self._Label_V_Border2.Width + Gap_W, self._Label_V_Border2.Height)
			self._Label_V_Border3.Size = System.Drawing.Size(self._Label_V_Border3.Width + Gap_W, self._Label_V_Border3.Height)

			# Relocate
			self._Button_Import_Resource.Location = System.Drawing.Point(self._Button_Import_Resource.Location.X + Gap_W, self._Button_Import_Resource.Location.Y)
			self._Button_Import_Def.Location = System.Drawing.Point(self._Button_Import_Def.Location.X + Gap_W, self._Button_Import_Def.Location.Y)
			self._Button_Import_Conf.Location = System.Drawing.Point(self._Button_Import_Conf.Location.X + Gap_W, self._Button_Import_Conf.Location.Y)
			self._Button_OutputExcelFile.Location = System.Drawing.Point(self._Button_OutputExcelFile.Location.X + Gap_W, self._Button_OutputExcelFile.Location.Y)
			self._Button_OK.Location = System.Drawing.Point(self._Button_OK.Location.X + Gap_W, self._Button_OK.Location.Y)
			self._Button_Cancel.Location = System.Drawing.Point(self._Button_Cancel.Location.X + Gap_W, self._Button_Cancel.Location.Y)

		except Exception as e:			
			Log("[Option Form ResizeEnd] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to resize Option Form GUI","Warning")			
			EXIT()
				
	def TreeViewNodeMouseClick(self, sender, e):		
		#try:
		#	if e.Node.Level == 0:
		#		if e.Node.Index == 0: # for EM
		#			self._GroupBox_EM.Visible = True
		#			self._GroupBox_Tran.Visible = False
		#			self._GroupBox_Eye.Visible = False
		#			self._GroupBox_Comp.Visible = False
		#		elif e.Node.Index == 1: # for Tran
		#			self._GroupBox_EM.Visible = False
		#			self._GroupBox_Tran.Visible = True
		#			self._GroupBox_Eye.Visible = False
		#			self._GroupBox_Comp.Visible = False
		#		elif e.Node.Index == 2: # for Eye
		#			self._GroupBox_EM.Visible = False
		#			self._GroupBox_Tran.Visible = False
		#			self._GroupBox_Eye.Visible = True
		#			self._GroupBox_Comp.Visible = False
		#		elif e.Node.Index == 3: # for Comp
		#			self._GroupBox_EM.Visible = False
		#			self._GroupBox_Tran.Visible = False
		#			self._GroupBox_Eye.Visible = False
		#			self._GroupBox_Comp.Visible = True

		#except Exception as e:			
		#	Log("[Option Form Treeview Node Mouse Click] = Failed")
		#	Log(traceback.format_exc())
		#	MessageBox.Show("Fail to Select node in Option Form","Warning")			
		#	EXIT()
		pass

	def TextBox_EyeOffsetTextChanged(self, sender, e):		
		sub_DB.Eye_Form._TextBox_Offset.Text = self._TextBox_EyeOffset.Text		
		pass

	def TextBox_VrefTextChanged(self, sender, e):		
		# New Eye
		if sub_DB.Eyeflag:
			sub_DB.Eye_Form._TextBox_VcentDQ.Text = self._TextBox_Vref.Text
		# Old Eye
		else:
			sub_DB.Eye_Form._TextBox_Vref.Text = self._TextBox_Vref.Text

	def TextBox_ImageWidthTextChanged(self, sender, e):

		sub_DB.Net_Form._TextBox_ImageWidth.Text = sender.Text

	def Button_Import_ResourceClick(self, sender, e):
		try:
			dialog = self._folderBrowserDialog1			
			if dialog.ShowDialog(self) == DialogResult.OK:
				Path = dialog.SelectedPath
				self._TextBox_Resource.Text = Path
				Log("[Resource Directory] = %s" % Path)
			else:
				MessageBox.Show("Please Select a Folder for Ansys DDR Wizard Resources","Warning")

		except Exception as e:			
			Log("[Resource Directory] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to change resource directory","Warning")			
			EXIT()

	def Button_Import_DefClick(self, sender, e):
		try:
			sub_DB.Eye_Form.DDRConf_Load_ToolStripMenuItemClick(self, sender)
			self._TextBox_Def.Text = sub_DB.Cenv["File"]

		except Exception as e:			
			Log("[Load Definition File, Option] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to load DDR Wizard definition file, Option","Warning")			
			EXIT()

	def Button_Import_ConfClick(self, sender, e):
		try:
			sub_DB.Eye_Form.UserConf_Load_ToolStripMenuItemClick(self, sender)
			self._TextBox_Conf.Text = sub_DB.Uenv["File"]

		except Exception as e:			
			Log("[Load Configuration File, Option] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to load DDR Wizard configuration file, Option","Warning")			
			EXIT()

	def CheckBox_PlotEyeCheckedChanged(self, sender, e):
		try:
			if self._CheckBox_ExportExcelReport.Checked:
				self._Label_ImageWidth.Visible = sender.Checked
				self._Label_ImageWidth_Unit.Visible = sender.Checked
				self._TextBox_ImageWidth.Visible = sender.Checked

			sub_DB.Net_Form._CheckBox_PlotEye.Checked = sender.Checked
			sub_DB.Title[4] = str(sender.Checked)
			sub_DB.Eye_Form.Text = " : ".join(sub_DB.Title)

		except Exception as e:			
			Log("[Check Eye Plot] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to check eye plot","Warning")			
			EXIT()

	def CheckBox_CompianceCheckedChanged(self, sender, e):
		
		self._Button_Compliance.Visible = sender.Checked

	def ComboBox_VrefSelectedIndexChanged(self, sender, e):
		try:
			if sender.SelectedIndex == 0: # Auto Vref
				self._TextBox_Vref.Visible = False
				self._Label_mV.Visible = False
				# New Eye
				if sub_DB.Eyeflag:
					sub_DB.Eye_Form._TextBox_VcentDQ.Text = "Auto"
					sub_DB.Eye_Form._CheckBox_VcentDQ.Checked = True
				# Old Eye
				else:
					sub_DB.Eye_Form._TextBox_Vref.Text = "Auto"
					sub_DB.Eye_Form._CheckBox_Vref.Checked = True

			elif sender.SelectedIndex == 1: # Manual Vref				
				self._TextBox_Vref.Visible = True
				self._Label_mV.Visible = True			
				## New Eye
				#if sub_DB.Eyeflag:
				#	sub_DB.Eye_Form._TextBox_VcentDQ.Text = self._TextBox_Vref.Text
				## Old Eye
				#else:
				#	sub_DB.Eye_Form._TextBox_Vref.Text = self._TextBox_Vref.Text
			
			sub_DB.Title[2] = "%s" % self._ComboBox_Vref.Text
			sub_DB.Eye_Form.Text = " : ".join(sub_DB.Title)

		except Exception as e:			
			Log("[Vref Select] = Failed")
			Log(traceback.format_exc())
			print traceback.format_exc()
			MessageBox.Show("Fail to change Vref calculating method","Warning")			
			EXIT()

	def ComboBox_AnalyzeSelectedIndexChanged(self, sender, e):

		pass

	def CheckBox_ExportExcelReportCheckedChanged(self, sender, e):
		try:
			if self._CheckBox_PlotEye.Checked:
				self._TextBox_ImageWidth.Visible = sender.Checked			
				self._Label_ImageWidth.Visible = sender.Checked
				self._Label_ImageWidth_Unit.Visible = sender.Checked			
			self._Label_ReportFormat.Visible = sender.Checked
			self._ComboBox_ReportFormat.Visible = sender.Checked


			if sender.Checked:
				sub_DB.Title[5] = "True-%s" % self._ComboBox_ReportFormat.Text
			else:
				sub_DB.Title[5] = "False"
			sub_DB.Eye_Form.Text = " : ".join(sub_DB.Title)

		except Exception as e:			
			Log("[Check Excel Report] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to check excel report","Warning")			
			EXIT()
		
	def Button_OutputExcelFileClick(self, sender, e):
		try:
			dialog = self._saveFileDialog1
			dialog.Title = "Enter the Eye Anlyze Report Excel File"
			dialog.DefaultExt = "xlsx"
			dialog.Filter = "xlsx files(*.xlsx)|*.xlsx"
			if dialog.ShowDialog(self) == DialogResult.OK:			
				self._TextBox_OutputExcelFile.Text = dialog.FileName
			else:
				MessageBox.Show("Please Enter the Eye Anlyze Report Excel File Name","Warning")

		except Exception as e:			
			Log("[Setup Excel Report] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to set excel report","Warning")			
			EXIT()

	def Button_ComplianceClick(self, sender, e):

		sub_DB.Compliance_Form.ShowDialog()

	def Button_OKClick(self, sender, e):
		try:
			flag = True
			if self._TextBox_EyeOffset.Text == "":
				flag = False			
			elif self._TextBox_Vref.Visible:
				if self._TextBox_Vref.Text == "":
					flag = False
			elif self._CheckBox_ExportExcelReport.Checked:
				if self._TextBox_ImageWidth.Text == "":
					flag = False

			#if not self._CheckBox_PlotEye.Checked:
			#	if self._CheckBox_ExportExcelReport.Checked:
			#		if self._ComboBox_ReportFormat.Text.lower() == "default":					
			#			MessageBox.Show("To generate an Excel report in format \"Default\", Eye-diagram has to be plotted.", "Warning", MessageBoxButtons.OK, MessageBoxIcon.Warning)
			#			self._CheckBox_PlotEye.Checked = True
			#			flag = False

			if flag:
				Log("[Eye Analyzer Option]")
				Log("	<Eye Offset> = %s [ns]" % self._TextBox_EyeOffset.Text)
				Log("	<Vref Method> = %s" % self._ComboBox_Vref.Text)
				if self._TextBox_Vref.Visible:
					Log("	<Vref manual value> = %s [mV]" % self._TextBox_Vref.Text)
				Log("	<Eye Analyze Method> = %s" % self._ComboBox_Analyze.Text)
				Log("	<Plot Eye> = %s" % str(self._CheckBox_PlotEye.Checked))
				if self._CheckBox_ExportExcelReport.Checked:
					Log("	<Excel Report> = True")
					Log("		(Image Widht) = %s [pixel]" % self._TextBox_ImageWidth.Text)
					Log("		(Report Format) = %s" % self._ComboBox_ReportFormat.Text)
					Log("		(Output File) = %s" % self._TextBox_OutputExcelFile.Text)
				else:
					Log("	<Excel Report> = False")

				self.DialogResult = DialogResult.OK
				self.Close()
			else:
				MessageBox.Show("Please enter the value for DDR Wizard Eye Analyzer options","Warning")

		except Exception as e:			
			Log("[Setup Option] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to set eye analyzing options","Warning")			
			EXIT()

	def Button_CancelClick(self, sender, e):
		try:
			self.DialogResult = DialogResult.Cancel		
			self.Close()

		except Exception as e:			
			Log("[Cancel Option] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to cancel option","Warning")			
			EXIT()

class ComplianceForm(Form):
	def __init__(self):

		self.InitializeComponent()
	
	def InitializeComponent(self):		
		self._components = System.ComponentModel.Container()
		self._contextMenuStrip1 = System.Windows.Forms.ContextMenuStrip(self._components)
		self._showAllToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._showCheckItemOnlyToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._toolStripSeparator1 = System.Windows.Forms.ToolStripSeparator()
		self._checkAllToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._uncheckAllToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._autoCheckToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()

		self._DataGridView = System.Windows.Forms.DataGridView()
		dataGridViewCellStyle11 = System.Windows.Forms.DataGridViewCellStyle()
		self._Col_TestCheck = System.Windows.Forms.DataGridViewCheckBoxColumn()
		self._Col_TestItem = System.Windows.Forms.DataGridViewTextBoxColumn()
		self._Col_RequiredGroup = System.Windows.Forms.DataGridViewTextBoxColumn()
		self._Col_IdentifiedGroup = System.Windows.Forms.DataGridViewTextBoxColumn()
		self._Col_Note = System.Windows.Forms.DataGridViewTextBoxColumn()
		self._Col_Ref = System.Windows.Forms.DataGridViewComboBoxColumn()
		self._Col_Target = System.Windows.Forms.DataGridViewComboBoxColumn()
		self._Col_Description = System.Windows.Forms.DataGridViewTextBoxColumn()
		self._Col_Info = System.Windows.Forms.DataGridViewButtonColumn()
		
		self._Label_DQ_Timing = System.Windows.Forms.Label()
		self._Label_ADDR_Timing = System.Windows.Forms.Label()
		self._Label_DQS_Timing = System.Windows.Forms.Label()
		self._Label_CLK_Timing = System.Windows.Forms.Label()
		self._Label_Diff_Timing = System.Windows.Forms.Label()
		self._Label_Vref_Timing = System.Windows.Forms.Label()

		self._Button_ShowHide = System.Windows.Forms.Button()
		self._Button_Close = System.Windows.Forms.Button()

		self._DataGridView.BeginInit()
		self._contextMenuStrip1.SuspendLayout()
		self.SuspendLayout()
		# 
		# DataGridView
		# 
		self._DataGridView.AllowUserToAddRows = False
		self._DataGridView.AllowUserToDeleteRows = False
		self._DataGridView.AllowUserToResizeColumns = False
		self._DataGridView.AllowUserToResizeRows = False
		dataGridViewCellStyle11.BackColor = System.Drawing.SystemColors.Control
		dataGridViewCellStyle11.Font = System.Drawing.Font("Microsoft Sans Serif", 8.25, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 129)
		dataGridViewCellStyle11.ForeColor = System.Drawing.SystemColors.WindowText
		dataGridViewCellStyle11.SelectionBackColor = System.Drawing.SystemColors.Highlight
		dataGridViewCellStyle11.SelectionForeColor = System.Drawing.SystemColors.HighlightText
		dataGridViewCellStyle11.WrapMode = System.Windows.Forms.DataGridViewTriState.True
		self._DataGridView.ColumnHeadersDefaultCellStyle = dataGridViewCellStyle11
		self._DataGridView.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize
		self._DataGridView.Columns.AddRange(System.Array[System.Windows.Forms.DataGridViewColumn](
			[self._Col_TestCheck,
			self._Col_TestItem,
			self._Col_RequiredGroup,
			self._Col_IdentifiedGroup,
			self._Col_Note,
			self._Col_Ref,
			self._Col_Target,
			self._Col_Info]))
		self._DataGridView.ContextMenuStrip = self._contextMenuStrip1
		self._DataGridView.EditMode = System.Windows.Forms.DataGridViewEditMode.EditOnF2
		self._DataGridView.Location = System.Drawing.Point(12, 12)
		self._DataGridView.Name = "DataGridView"
		self._DataGridView.RowHeadersVisible = False
		self._DataGridView.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect
		self._DataGridView.Size = System.Drawing.Size(999, 805)
		self._DataGridView.TabIndex = 38
		self._DataGridView.KeyPress += self.DataGridViewKeyPress
		self._DataGridView.ColumnHeaderMouseClick += self.DataGridViewColumnHeaderMouseClick
		self._DataGridView.CellMouseClick += self.DataGridViewCellMouseClick
		# 
		# contextMenuStrip1
		# 
		self._contextMenuStrip1.Items.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._showAllToolStripMenuItem,
			self._showCheckItemOnlyToolStripMenuItem,
			self._toolStripSeparator1,
			self._checkAllToolStripMenuItem,
			self._uncheckAllToolStripMenuItem,
			self._autoCheckToolStripMenuItem]))
		self._contextMenuStrip1.Name = "contextMenuStrip1"
		self._contextMenuStrip1.Size = System.Drawing.Size(199, 120)
		# 
		# showAllToolStripMenuItem
		# 
		self._showAllToolStripMenuItem.Name = "showAllToolStripMenuItem"
		self._showAllToolStripMenuItem.Size = System.Drawing.Size(198, 22)
		self._showAllToolStripMenuItem.Text = "Show All"
		self._showAllToolStripMenuItem.Click += self.ShowAllToolStripMenuItemClick
		# 
		# showCheckItemOnlyToolStripMenuItem
		# 
		self._showCheckItemOnlyToolStripMenuItem.Name = "showCheckItemOnlyToolStripMenuItem"
		self._showCheckItemOnlyToolStripMenuItem.Size = System.Drawing.Size(198, 22)
		self._showCheckItemOnlyToolStripMenuItem.Text = "Show Check Item Only"
		self._showCheckItemOnlyToolStripMenuItem.Click += self.ShowCheckItemOnlyToolStripMenuItemClick
		# 
		# toolStripSeparator1
		# 
		self._toolStripSeparator1.Name = "toolStripSeparator1"
		self._toolStripSeparator1.Size = System.Drawing.Size(195, 6)
		# 
		# checkAllToolStripMenuItem
		# 
		self._checkAllToolStripMenuItem.Name = "checkAllToolStripMenuItem"
		self._checkAllToolStripMenuItem.Size = System.Drawing.Size(198, 22)
		self._checkAllToolStripMenuItem.Text = "Check All"
		self._checkAllToolStripMenuItem.Click += self.CheckAllToolStripMenuItemClick
		# 
		# uncheckAllToolStripMenuItem
		# 
		self._uncheckAllToolStripMenuItem.Name = "uncheckAllToolStripMenuItem"
		self._uncheckAllToolStripMenuItem.Size = System.Drawing.Size(198, 22)
		self._uncheckAllToolStripMenuItem.Text = "Uncheck All"
		self._uncheckAllToolStripMenuItem.Click += self.UncheckAllToolStripMenuItemClick
		# 
		# autoCheckToolStripMenuItem
		# 
		self._autoCheckToolStripMenuItem.Name = "autoCheckToolStripMenuItem"
		self._autoCheckToolStripMenuItem.Size = System.Drawing.Size(198, 22)
		self._autoCheckToolStripMenuItem.Text = "Auto Check"
		self._autoCheckToolStripMenuItem.Click += self.AutoCheckToolStripMenuItemClick
		# 
		# Col_TestCheck
		# 
		self._Col_TestCheck.HeaderText = ""
		self._Col_TestCheck.Name = "Col_TestCheck"
		self._Col_TestCheck.ReadOnly = False
		self._Col_TestCheck.Width = 26
		# 
		# Col_TestItem
		# 
		self._Col_TestItem.HeaderText = "Test Items"
		self._Col_TestItem.Name = "Col_TestItem"
		self._Col_TestItem.ReadOnly = True
		self._Col_TestItem.SortMode = System.Windows.Forms.DataGridViewColumnSortMode.NotSortable
		self._Col_TestItem.Width = 80
		self._Col_TestItem.DefaultCellStyle.Alignment = DataGridViewContentAlignment.MiddleCenter
		# 
		# Col_RequiredGroup
		# 
		self._Col_RequiredGroup.HeaderText = "Required Net Group"
		self._Col_RequiredGroup.Name = "Col_RequiredGroup"
		self._Col_RequiredGroup.ReadOnly = True
		self._Col_RequiredGroup.SortMode = System.Windows.Forms.DataGridViewColumnSortMode.NotSortable
		self._Col_RequiredGroup.Width = 80
		# 
		# Col_IdentifiedGroup
		# 
		self._Col_IdentifiedGroup.HeaderText = "Identified Net Group"
		self._Col_IdentifiedGroup.Name = "Col_IdentifiedGroup"
		self._Col_IdentifiedGroup.ReadOnly = True
		self._Col_IdentifiedGroup.SortMode = System.Windows.Forms.DataGridViewColumnSortMode.NotSortable
		self._Col_IdentifiedGroup.Width = 80
		# 
		# Col_Note
		# 
		self._Col_Note.HeaderText = "Note"
		self._Col_Note.Name = "Col_Note"
		self._Col_Note.ReadOnly = True
		self._Col_Note.SortMode = System.Windows.Forms.DataGridViewColumnSortMode.NotSortable
		self._Col_Note.Width = 200
		# 
		# Col_Ref
		# 
		self._Col_Ref.FlatStyle = System.Windows.Forms.FlatStyle.Flat
		self._Col_Ref.HeaderText = "Reference Net"
		self._Col_Ref.Name = "Col_Ref"
		self._Col_Ref.Width = 150
		# 
		# Col_Target
		# 
		self._Col_Target.FlatStyle = System.Windows.Forms.FlatStyle.Flat
		self._Col_Target.HeaderText = "Target Net"
		self._Col_Target.Name = "Col_Target"
		self._Col_Target.Width = 150
		# 
		# Col_Description
		# 
		self._Col_Description.HeaderText = "Detailed Description"
		self._Col_Description.Name = "Col_Description"
		self._Col_Description.ReadOnly = True
		self._Col_Description.SortMode = System.Windows.Forms.DataGridViewColumnSortMode.NotSortable
		self._Col_Description.Width = 400
		# 
		# Col_Info
		# 
		self._Col_Info.HeaderText = "Info"
		self._Col_Info.Name = "Col_Info"
		self._Col_Info.ReadOnly = True
		self._Col_Info.Text = "Info"
		self._Col_Info.UseColumnTextForButtonValue = True
		self._Col_Info.Width = 40
		self._Col_Info.DefaultCellStyle.Alignment = DataGridViewContentAlignment.MiddleCenter		
		# 
		# Label_DQ_Timing
		# 
		self._Label_DQ_Timing.BackColor = System.Drawing.Color.Black
		self._Label_DQ_Timing.Font = System.Drawing.Font("Arial", 9, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_DQ_Timing.ForeColor = System.Drawing.Color.White
		self._Label_DQ_Timing.Location = System.Drawing.Point(13, 46)
		self._Label_DQ_Timing.Name = "Label_DQ_Timing"
		self._Label_DQ_Timing.Size = System.Drawing.Size(781, 20)
		self._Label_DQ_Timing.TabIndex = 39
		self._Label_DQ_Timing.Text = "Data Timing"
		self._Label_DQ_Timing.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
		# 
		# Label_ADDR_Timing
		# 
		self._Label_ADDR_Timing.BackColor = System.Drawing.Color.Black
		self._Label_ADDR_Timing.Font = System.Drawing.Font("Arial", 9, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_ADDR_Timing.ForeColor = System.Drawing.Color.White
		self._Label_ADDR_Timing.Location = System.Drawing.Point(13, 174)
		self._Label_ADDR_Timing.Name = "Label_ADDR_Timing"
		self._Label_ADDR_Timing.Size = System.Drawing.Size(781, 20)
		self._Label_ADDR_Timing.TabIndex = 40
		self._Label_ADDR_Timing.Text = "Address Timing"
		self._Label_ADDR_Timing.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
		# 
		# Label_DQS_Timing
		# 
		self._Label_DQS_Timing.BackColor = System.Drawing.Color.Black
		self._Label_DQS_Timing.Font = System.Drawing.Font("Arial", 9, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_DQS_Timing.ForeColor = System.Drawing.Color.White
		self._Label_DQS_Timing.Location = System.Drawing.Point(13, 266)
		self._Label_DQS_Timing.Name = "Label_DQS_Timing"
		self._Label_DQS_Timing.Size = System.Drawing.Size(781, 20)
		self._Label_DQS_Timing.TabIndex = 41
		self._Label_DQS_Timing.Text = "Data Strobe Timing"
		self._Label_DQS_Timing.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
		# 
		# Label_CLK_Timing
		# 
		self._Label_CLK_Timing.BackColor = System.Drawing.Color.Black
		self._Label_CLK_Timing.Font = System.Drawing.Font("Arial", 9, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_CLK_Timing.ForeColor = System.Drawing.Color.White
		self._Label_CLK_Timing.Location = System.Drawing.Point(13, 322)
		self._Label_CLK_Timing.Name = "Label_CLK_Timing"
		self._Label_CLK_Timing.Size = System.Drawing.Size(781, 20)
		self._Label_CLK_Timing.TabIndex = 42
		self._Label_CLK_Timing.Text = "Clock Timing"
		self._Label_CLK_Timing.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
		# 
		# Label_Diff_Timing
		# 
		self._Label_Diff_Timing.BackColor = System.Drawing.Color.Black
		self._Label_Diff_Timing.Font = System.Drawing.Font("Arial", 9, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_Diff_Timing.ForeColor = System.Drawing.Color.White
		self._Label_Diff_Timing.Location = System.Drawing.Point(13, 486)
		self._Label_Diff_Timing.Name = "Label_Diff_Timing"
		self._Label_Diff_Timing.Size = System.Drawing.Size(781, 20)
		self._Label_Diff_Timing.TabIndex = 43
		self._Label_Diff_Timing.Text = "Differential & Single-ended Requirements for Strobe and Clock"
		self._Label_Diff_Timing.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
		# 
		# Label_Vref_Timing
		# 
		self._Label_Vref_Timing.BackColor = System.Drawing.Color.Black
		self._Label_Vref_Timing.Font = System.Drawing.Font("Arial", 9, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_Vref_Timing.ForeColor = System.Drawing.Color.White
		self._Label_Vref_Timing.Location = System.Drawing.Point(13, 650)
		self._Label_Vref_Timing.Name = "Label_Vref_Timing"
		self._Label_Vref_Timing.Size = System.Drawing.Size(781, 20)
		self._Label_Vref_Timing.TabIndex = 44
		self._Label_Vref_Timing.Text = "Reference Voltage Tolerance for Data and Address"
		self._Label_Vref_Timing.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
		# 
		# Button_ShowHide
		# 
		self._Button_ShowHide.Font = System.Drawing.Font("Arial", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_ShowHide.Location = System.Drawing.Point(332, 692)
		self._Button_ShowHide.Name = "Button_ShowHide"
		self._Button_ShowHide.Size = System.Drawing.Size(189, 25)
		self._Button_ShowHide.TabIndex = 45
		self._Button_ShowHide.Text = "Show Reference && Target Net"
		self._Button_ShowHide.UseVisualStyleBackColor = True
		self._Button_ShowHide.Click += self.Button_ShowHideClick
		# 
		# Button_Close
		# 
		self._Button_Close.Font = System.Drawing.Font("Arial", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_Close.Location = System.Drawing.Point(12, 692)
		self._Button_Close.Name = "Button_Close"
		self._Button_Close.Size = System.Drawing.Size(189, 25)
		self._Button_Close.TabIndex = 46
		self._Button_Close.Text = "Save && Close"
		self._Button_Close.UseVisualStyleBackColor = True
		self._Button_Close.Click += self.Button_CloseClick
		# 
		# ComplianceForm
		#		
		self.Shownetflag = False
		self.ClientSize = System.Drawing.Size(1032, 912)		
		self.Controls.Add(self._Button_Close)
		self.Controls.Add(self._Button_ShowHide)
		self.Controls.Add(self._Label_Vref_Timing)
		self.Controls.Add(self._Label_Diff_Timing)
		self.Controls.Add(self._Label_CLK_Timing)
		self.Controls.Add(self._Label_DQS_Timing)
		self.Controls.Add(self._Label_ADDR_Timing)
		self.Controls.Add(self._Label_DQ_Timing)
		self.Controls.Add(self._DataGridView)
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle
		self.Checked_Num = 0
		self.Init_flag = True
		IconFile = path + "\\Resources\\LOGO.ico"
		self.Icon = Icon(IconFile)
		self.StartPosition = System.Windows.Forms.FormStartPosition.Manual		
		self.Location = System.Drawing.Point(sub_DB.Option_Form.Location.X + sub_DB.Option_Form.Size.Width*2, sub_DB.Option_Form.Location.Y + sub_DB.Option_Form.Size.Height)
		self.Name = "ComplianceForm"
		self.Text = "Setting for DDR Compliacne Check"		
		self.Load += self.ComplianceFormLoad
		self._DataGridView.EndInit()
		self._contextMenuStrip1.ResumeLayout(False)
		self.ResumeLayout(False)

		#################################################################
		########## Add Rows for Compliacne Parameters ###################
		#################################################################
		#0
		self._DataGridView.Rows.Add(False, "tDS", "DQ, DQS", "N/A", "Data Setup Time")
		self._DataGridView.Rows.Add(False, "tDS", "DQ, DQS", "N/A", "Data Setup Time")
		self._DataGridView.Rows.Add(False, "tDH", "DQ, DQS", "N/A", "Data Hold Time")
		self._DataGridView.Rows.Add(False, "tDQSQ", "DQ, DQS", "N/A", "Strobe to Data Skew")
		self._DataGridView.Rows.Add(False, "tQH", "DQ, DQS", "N/A", "Data Output Hold Time")
		self._DataGridView.Rows.Add(False, "tDIPW", "DQ, (DM)", "N/A", "Input Pulse Width")
		self._DataGridView.Rows.Add(False, "tVAC(DQ)", "DQ", "N/A", "Valid Transition Time")		
		#7
		self._DataGridView.Rows.Add(False, "tIS", "ADDR, CLK", "N/A", "Address Setup Time")
		self._DataGridView.Rows.Add(False, "tIH", "ADDR, CLK", "N/A", "Address Hold Time")
		self._DataGridView.Rows.Add(False, "tIPW", "ADDR", "N/A", "Input Pulse Width")
		self._DataGridView.Rows.Add(False, "tVAC(ADDR)", "ADDR", "N/A", "Valid Transition Time")		
		#11
		self._DataGridView.Rows.Add(False, "tDQSL", "DQS", "N/A", "Diff. Input Low Pulse Width")
		self._DataGridView.Rows.Add(False, "tDQSH", "DQS", "N/A", "Diff. Input High Pulse Width")		
		#13
		self._DataGridView.Rows.Add(False, "tCK(avg)", "CLK", "N/A", "Average Clock Period")		
		self._DataGridView.Rows.Add(False, "tCL(avg)", "CLK", "N/A", "Average Clock Low Pulse Width")		
		self._DataGridView.Rows.Add(False, "tCH(avg)", "CLK", "N/A", "Average Clock High Pulse Width")
		self._DataGridView.Rows.Add(False, "tCK(abs)", "CLK", "N/A", "Absolute Clock Period")		
		self._DataGridView.Rows.Add(False, "tCL(abs)", "CLK", "N/A", "Absolute Clock Low Pulse Width")		
		self._DataGridView.Rows.Add(False, "tCH(abs)", "CLK", "N/A", "Absolute Clock High Pulse Width")
		self._DataGridView.Rows.Add(False, "tJIT(per)", "CLK", "N/A", "Clock Period Jitter")
		self._DataGridView.Rows.Add(False, "tJIT(cc)", "CLK", "N/A", "Clock Cycle to Cycle Period Jitter")		
		#21
		self._DataGridView.Rows.Add(False, "tDVAC(DQS)", "DQS", "N/A", "Allowed Time Before Ringback for DQS")		
		self._DataGridView.Rows.Add(False, "VSEL(DQS)", "DQS", "N/A", "Single-ended Low Level for Strobes")
		self._DataGridView.Rows.Add(False, "VSEH(DQS)", "DQS", "N/A", "Single-ended High Level for Strobes")
		self._DataGridView.Rows.Add(False, "VIX(DQS)", "DQS", "N/A", "Diff. Input Cross Point Voltage")
		self._DataGridView.Rows.Add(False, "tDVAC(CLK)", "CLK", "N/A", "Allowed Time Before Ringback for CLK")		
		self._DataGridView.Rows.Add(False, "VSEL(CLK)", "CLK", "N/A", "Single-ended Low Level for CLK")
		self._DataGridView.Rows.Add(False, "VSEH(CLK)", "CLK", "N/A", "Single-ended High Level for CLK")
		self._DataGridView.Rows.Add(False, "VIX(CLK)", "CLK", "N/A", "Diff. Input Cross Point Voltage")		
		#29
		self._DataGridView.Rows.Add(False, "VRefDQ(DC)", "Vref", "N/A", "Average of VRef(t)")
		# Set Row Height to 18
		for i in range(0, 30):		
			self._DataGridView.Rows[i].Height = 18

		#################################################################
		########## Add Tooltips for Detailed Description ################
		#################################################################
		# ToolTips
		# 1
		self._DataGridView.Rows[1].Cells[4].ToolTipText = "Data setup time to DQS, DQQS# referenced to Vih(ac)/Vil(ac) levels"
		self._DataGridView.Rows[2].Cells[4].ToolTipText = "Data hold time from DQS, DQS# referenced to Vih(dc)/Vil(dc) levels"
		self._DataGridView.Rows[3].Cells[4].ToolTipText = "DQS, DQS# to DQ skew, per group, per access"
		self._DataGridView.Rows[4].Cells[4].ToolTipText = "DQ output hold time from DQS, DQS#"
		self._DataGridView.Rows[5].Cells[4].ToolTipText = "DQ and DM input pulse width for each input"
		self._DataGridView.Rows[6].Cells[4].ToolTipText = "Required time for valid DQ transition"		
		# 7
		self._DataGridView.Rows[7].Cells[4].ToolTipText = "Address setupt time to CLK, CLK# referenced to Vih(ac)/Vil(ac) levels"
		self._DataGridView.Rows[8].Cells[4].ToolTipText = "Address hold time from CLK, CLK# referenced to Vih(dc)/Vil(dc) levels"
		self._DataGridView.Rows[9].Cells[4].ToolTipText = "Address input pulse width for each input"
		self._DataGridView.Rows[10].Cells[4].ToolTipText = "Required time for valid address transition"		
		# 11
		self._DataGridView.Rows[11].Cells[4].ToolTipText = "DQS, DQS# differential input low pulse width"
		self._DataGridView.Rows[12].Cells[4].ToolTipText = "DQS, DQS# differential input high pulse width"		
		self._DataGridView.Rows[24].Cells[4].ToolTipText = "Differential input cross point voltage relative to VDD/2 for DQS, DQS#"
		self._DataGridView.Rows[28].Cells[4].ToolTipText = "Differential input cross point voltage relative to VDD/2 for CLK, CLK#"
		
		#################################################################
		###### Add Diveder and Set Label Position and Width #############
		#################################################################
		# Add Divider
		self._DataGridView.Rows[0].DividerHeight = 20		
		self._DataGridView.Rows[0].Height = 20		
		self._DataGridView.Rows[6].DividerHeight = 20
		self._DataGridView.Rows[6].Height += 20		
		self._DataGridView.Rows[10].DividerHeight = 20
		self._DataGridView.Rows[10].Height += 20		
		self._DataGridView.Rows[12].DividerHeight = 20
		self._DataGridView.Rows[12].Height += 20		
		self._DataGridView.Rows[20].DividerHeight = 20
		self._DataGridView.Rows[20].Height += 20
		self._DataGridView.Rows[28].DividerHeight = 20
		self._DataGridView.Rows[28].Height += 20
		# Set Label Position
		self._Label_DQ_Timing.Location = System.Drawing.Point(13, 43)
		self._Label_ADDR_Timing.Location = System.Drawing.Point(13, 171)
		self._Label_DQS_Timing.Location = System.Drawing.Point(13, 263)
		self._Label_CLK_Timing.Location = System.Drawing.Point(13, 319)
		self._Label_Diff_Timing.Location = System.Drawing.Point(13, 483)
		self._Label_Vref_Timing.Location = System.Drawing.Point(13, 647)
		# Set Label Width
		self._Label_DQ_Timing.Width = 506
		self._Label_ADDR_Timing.Width = 506
		self._Label_DQS_Timing.Width = 506
		self._Label_CLK_Timing.Width = 506
		self._Label_Diff_Timing.Width = 506
		self._Label_Vref_Timing.Width = 506

	def ComplianceFormLoad(self, sender, e):
		if self.Shownetflag:
			self.Button_ShowHideClick(self, sender)

		if self.Init_flag:
			# Get Target Net Group
			group = []
			for row in sub_DB.Net_Form._DataGridView.Rows:
				if row.Cells[2].Value not in group:
					group.append(row.Cells[2].Value)

			# Get Target Net name for each Group
			Net_Name = {}
			Net_Name["DQ"]=[]
			Net_Name["DQS_P"]=[]
			Net_Name["DQS_N"]=[]
			Net_Name["DM"]=[]
			Net_Name["ADDR"]=[]
			Net_Name["CLK_P"]=[]
			Net_Name["CLK_N"]=[]
			Net_Name["Vref"]=[]
			for row in sub_DB.Net_Form._DataGridView.Rows:
				Net_Name[row.Cells[2].Value].append(row.Cells[1].Value)		

			######################################################################
			###### Check Compliance Test List based on the target net group ######
			######################################################################
			# Initialize : uncheck all
			for row in self._DataGridView.Rows:
				row.Cells[0].Value = False


			if "DQ" in group and "DQS_P" in group and "DQS_N" in group:
				self._DataGridView.Rows[1].Cells[0].Value = True
				self._DataGridView.Rows[2].Cells[0].Value = True
				self._DataGridView.Rows[3].Cells[0].Value = True
				self._DataGridView.Rows[4].Cells[0].Value = True

				self._DataGridView.Rows[1].Cells[5].Items.Add(["A","B"])
				self._DataGridView.Rows[1].Cells[6].Items.Add("B")
			
				#self._DataGridView.Rows[2].Cells[6].Value = True
				#self._DataGridView.Rows[3].Cells[6].Value = True
				#self._DataGridView.Rows[4].Cells[6].Value = True


			if "DQ" in group:
				self._DataGridView.Rows[5].Cells[0].Value = True
				self._DataGridView.Rows[6].Cells[0].Value = True

			if "DM" in group:
				self._DataGridView.Rows[5].Cells[0].Value = True

			if "ADDR" in group and "CLK_P" in group and "CLK_N" in group:
				self._DataGridView.Rows[7].Cells[0].Value= True
				self._DataGridView.Rows[8].Cells[0].Value= True

			if "ADDR" in group:
				self._DataGridView.Rows[9].Cells[0].Value = True
				self._DataGridView.Rows[10].Cells[0].Value = True

			if "DQS_P" in group and "DQS_N" in group:
				self._DataGridView.Rows[11].Cells[0].Value = True
				self._DataGridView.Rows[12].Cells[0].Value = True
				self._DataGridView.Rows[21].Cells[0].Value = True
				self._DataGridView.Rows[22].Cells[0].Value = True
				self._DataGridView.Rows[23].Cells[0].Value = True
				self._DataGridView.Rows[24].Cells[0].Value = True

			if "CLK_P" in group and "CLK_N" in group:
				self._DataGridView.Rows[13].Cells[0].Value = True
				self._DataGridView.Rows[14].Cells[0].Value = True
				self._DataGridView.Rows[15].Cells[0].Value= True
				self._DataGridView.Rows[16].Cells[0].Value= True
				self._DataGridView.Rows[17].Cells[0].Value= True
				self._DataGridView.Rows[18].Cells[0].Value= True
				self._DataGridView.Rows[19].Cells[0].Value= True
				self._DataGridView.Rows[20].Cells[0].Value= True
				self._DataGridView.Rows[25].Cells[0].Value= True
				self._DataGridView.Rows[26].Cells[0].Value= True
				self._DataGridView.Rows[27].Cells[0].Value= True
				self._DataGridView.Rows[28].Cells[0].Value= True		

			if "VREF" in group:
				self._DataGridView.Rows[29].Cells[0].Value= True

			#######################################################################
			############## Set Size of DataGridView and Client  ###################
			#######################################################################
			self._DataGridView.Size = System.Drawing.Size(509, 675)
			self.ClientSize = System.Drawing.Size(529, 722)

			##################################################################################################
			############## Set Column Display and Reference & Target Net Column Unvisible  ###################
			##################################################################################################
			self._DataGridView.Columns[7].DisplayIndex = 5
			self._DataGridView.Columns[5].Visible = False
			self._DataGridView.Columns[6].Visible = False

			#################################################################
			############## Set BackColor for Checked Rows ###################
			#################################################################
			for row in self._DataGridView.Rows:
				if row.Cells[0].Value:
					row.DefaultCellStyle.BackColor = System.Drawing.SystemColors.Info
					self.Checked_Num += 1
				else:
					row.DefaultCellStyle.BackColor = System.Drawing.SystemColors.Window

			self.Init_flag = False
		
	def DataGridViewKeyPress(self, sender, e):
		try:
			# Spacebar = Check/Uncheck all the selected rows
			if e.KeyChar == chr(32):
				for row in self._DataGridView.SelectedRows:
					row.Cells[0].Value = not row.Cells[0].Value
					if row.Cells[0].Value:
						row.DefaultCellStyle.BackColor = System.Drawing.SystemColors.Info
					else:
						row.DefaultCellStyle.BackColor = System.Drawing.SystemColors.Window

		except Exception as e:		
			Log("[Net Form Key Press] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to press key in Net Classificiton Form","Warning")			
			EXIT()

	def DataGridViewColumnHeaderMouseClick(self, sender, e):
		# TODO : Compliance Option Form DataGridView Column Header Mouse Click
		pass

	def DataGridViewCellMouseClick(self, sender, e):
		if e.ColumnIndex == 0:
			if self._DataGridView.Rows[e.RowIndex].Cells[0].Value:
				self._DataGridView.Rows[e.RowIndex].DefaultCellStyle.BackColor = System.Drawing.SystemColors.Window
			else:
				self._DataGridView.Rows[e.RowIndex].DefaultCellStyle.BackColor = System.Drawing.SystemColors.Info
	
	def Button_ShowHideClick(self, sender, e):		
		self.Shownetflag = not self.Shownetflag
		if self.Shownetflag:
			self._Button_ShowHide.Text = "Hide Reference && Target Net"
			self._DataGridView.Columns[5].Visible = True
			self._DataGridView.Columns[6].Visible = True
			
			self._Label_DQ_Timing.Width = 806
			self._Label_ADDR_Timing.Width = 806
			self._Label_DQS_Timing.Width = 806
			self._Label_CLK_Timing.Width = 806
			self._Label_Diff_Timing.Width = 806
			self._Label_Vref_Timing.Width = 806			
			
			self._Button_ShowHide.Location = System.Drawing.Point(632, 692)
			
			self._DataGridView.Size = System.Drawing.Size(809, 675)
			self.ClientSize = System.Drawing.Size(829, 722)
			
		else:
			self._Button_ShowHide.Text = "Show Reference && Target Net"
			self._DataGridView.Columns[5].Visible = False
			self._DataGridView.Columns[6].Visible = False
			
			self._Label_DQ_Timing.Width = 506
			self._Label_ADDR_Timing.Width = 506
			self._Label_DQS_Timing.Width = 506
			self._Label_CLK_Timing.Width = 506
			self._Label_Diff_Timing.Width = 506
			self._Label_Vref_Timing.Width = 506			
			
			self._Button_ShowHide.Location = System.Drawing.Point(332, 692)
			
			self._DataGridView.Size = System.Drawing.Size(509, 675)
			self.ClientSize = System.Drawing.Size(529, 722)

	def Button_CloseClick(self, sender, e):

		self.Close()

	def ShowAllToolStripMenuItemClick(self, sender, e):
		# TODO : Compliance Option Form 'Show All' ToolStripMenu
		pass

	def ShowCheckItemOnlyToolStripMenuItemClick(self, sender, e):
		# TODO : Compliance Option Form 'Show Checked Item Only' ToolStripMenu
		pass

	def CheckAllToolStripMenuItemClick(self, sender, e):
		# TODO : Compliance Option Form 'Check All' ToolStripMenu
		pass

	def UncheckAllToolStripMenuItemClick(self, sender, e):
		# TODO : Compliance Option Form 'Uncheck All' ToolStripMenu
		pass

	def AutoCheckToolStripMenuItemClick(self, sender, e):
		# TODO : Compliance Option Form 'Auto Check' ToolStripMenu
		pass

class IBIS_OptForm(Form):
	def __init__(self):

		self.InitializeComponent()
	
	def InitializeComponent(self):
		global path
		path = os.path.dirname(os.path.abspath(__file__))
		self._GroupBox_Rx = System.Windows.Forms.GroupBox()
		self._GroupBox_Tx = System.Windows.Forms.GroupBox()
		
		self._Label_IBIS_Tx = System.Windows.Forms.Label()
		self._Label_Comp_Tx = System.Windows.Forms.Label()
		self._Label_Model_Tx = System.Windows.Forms.Label()
		self._Label_IBIS_Rx = System.Windows.Forms.Label()
		self._Label_Comp_Rx = System.Windows.Forms.Label()
		self._Label_Model_Rx = System.Windows.Forms.Label()

		self._ComboBox_IBIS_Tx = System.Windows.Forms.ComboBox()
		self._ComboBox_Comp_Tx = System.Windows.Forms.ComboBox()
		self._ComboBox_Model_Tx = System.Windows.Forms.ComboBox()
		self._ComboBox_IBIS_Rx = System.Windows.Forms.ComboBox()
		self._ComboBox_Comp_Rx = System.Windows.Forms.ComboBox()
		self._ComboBox_Model_Rx = System.Windows.Forms.ComboBox()

		self._DataGridView_Tx = System.Windows.Forms.DataGridView()
		self._DataGridView_Tx_CheckBoxColumn = System.Windows.Forms.DataGridViewCheckBoxColumn()
		self._DataGridView_Tx_TextBoxColumn = System.Windows.Forms.DataGridViewTextBoxColumn()
		self._DataGridView_Tx_TextBoxColumn1 = System.Windows.Forms.DataGridViewTextBoxColumn()
		self._DataGridView_Rx = System.Windows.Forms.DataGridView()
		self._DataGridView_Rx_CheckBoxColumn = System.Windows.Forms.DataGridViewCheckBoxColumn()
		self._DataGridView_Rx_TextBoxColumn = System.Windows.Forms.DataGridViewTextBoxColumn()
		self._DataGridView_Rx_TextBoxColumn1 = System.Windows.Forms.DataGridViewTextBoxColumn()
		
		self._Button_View_Tx = System.Windows.Forms.Button()
		self._Button_View_Rx = System.Windows.Forms.Button()
		self._Button_CaseView = System.Windows.Forms.Button()
		self._Button_ResultView = System.Windows.Forms.Button()
		self._Button_AnalysisOption = System.Windows.Forms.Button()
		self._Button_Run = System.Windows.Forms.Button()
		
		self._ComboBox_IBIS_Tx_ToopTip = System.Windows.Forms.ToolTip()
		self._ComboBox_IBIS_Rx_ToopTip = System.Windows.Forms.ToolTip()

		self._GroupBox_Rx.SuspendLayout()
		self._DataGridView_Rx.BeginInit()
		self._GroupBox_Tx.SuspendLayout()
		self._DataGridView_Tx.BeginInit()
		self.SuspendLayout()
		# 
		# GroupBox_Tx
		# 		
		self._GroupBox_Tx.Controls.Add(self._ComboBox_Model_Tx)
		self._GroupBox_Tx.Controls.Add(self._ComboBox_Comp_Tx)		
		self._GroupBox_Tx.Controls.Add(self._DataGridView_Tx)
		self._GroupBox_Tx.Controls.Add(self._Button_View_Tx)
		self._GroupBox_Tx.Controls.Add(self._ComboBox_IBIS_Tx)
		self._GroupBox_Tx.Controls.Add(self._Label_Comp_Tx)
		self._GroupBox_Tx.Controls.Add(self._Label_Model_Tx)
		self._GroupBox_Tx.Controls.Add(self._Label_IBIS_Tx)
		self._GroupBox_Tx.Font = System.Drawing.Font("Arial", 10)
		self._GroupBox_Tx.Location = System.Drawing.Point(12, 12)
		self._GroupBox_Tx.Name = "GroupBox_Tx"
		self._GroupBox_Tx.Size = System.Drawing.Size(286, 275)
		self._GroupBox_Tx.TabIndex = 43
		self._GroupBox_Tx.TabStop = False
		self._GroupBox_Tx.Text = "Tx"
		# 
		# GroupBox_Rx
		# 		
		self._GroupBox_Rx.Controls.Add(self._ComboBox_Model_Rx)
		self._GroupBox_Rx.Controls.Add(self._ComboBox_Comp_Rx)		
		self._GroupBox_Rx.Controls.Add(self._DataGridView_Rx)
		self._GroupBox_Rx.Controls.Add(self._Button_View_Rx)
		self._GroupBox_Rx.Controls.Add(self._ComboBox_IBIS_Rx)
		self._GroupBox_Rx.Controls.Add(self._Label_Comp_Rx)
		self._GroupBox_Rx.Controls.Add(self._Label_Model_Rx)
		self._GroupBox_Rx.Controls.Add(self._Label_IBIS_Rx)
		self._GroupBox_Rx.Font = System.Drawing.Font("Arial", 10)
		self._GroupBox_Rx.Location = System.Drawing.Point(319, 12)
		self._GroupBox_Rx.Name = "GroupBox_Rx"
		self._GroupBox_Rx.Size = System.Drawing.Size(286, 275)
		self._GroupBox_Rx.TabIndex = 45
		self._GroupBox_Rx.TabStop = False
		self._GroupBox_Rx.Text = "Rx"
		# 
		# Label_IBIS_Tx
		# 
		self._Label_IBIS_Tx.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_IBIS_Tx.Location = System.Drawing.Point(6, 19)
		self._Label_IBIS_Tx.Name = "Label_IBIS_Tx"
		self._Label_IBIS_Tx.Size = System.Drawing.Size(42, 28)
		self._Label_IBIS_Tx.TabIndex = 30
		self._Label_IBIS_Tx.Text = "IBIS :"
		self._Label_IBIS_Tx.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_Comp_Tx
		# 
		self._Label_Comp_Tx.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_Comp_Tx.Location = System.Drawing.Point(6, 47)
		self._Label_Comp_Tx.Name = "Label_Comp_Tx"
		self._Label_Comp_Tx.Size = System.Drawing.Size(68, 28)
		self._Label_Comp_Tx.TabIndex = 38
		self._Label_Comp_Tx.Text = "Comp. :"
		self._Label_Comp_Tx.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_Model_Tx
		# 
		self._Label_Model_Tx.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_Model_Tx.Location = System.Drawing.Point(6, 77)
		self._Label_Model_Tx.Name = "Label_Model_Tx"
		self._Label_Model_Tx.Size = System.Drawing.Size(68, 28)
		self._Label_Model_Tx.TabIndex = 38
		self._Label_Model_Tx.Text = "Model :"
		self._Label_Model_Tx.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_IBIS_Rx
		# 
		self._Label_IBIS_Rx.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_IBIS_Rx.Location = System.Drawing.Point(6, 19)
		self._Label_IBIS_Rx.Name = "Label_IBIS_Rx"
		self._Label_IBIS_Rx.Size = System.Drawing.Size(42, 28)
		self._Label_IBIS_Rx.TabIndex = 30
		self._Label_IBIS_Rx.Text = "IBIS :"
		self._Label_IBIS_Rx.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_Comp_Rx
		# 
		self._Label_Comp_Rx.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_Comp_Rx.Location = System.Drawing.Point(6, 47)
		self._Label_Comp_Rx.Name = "Label_Comp_Rx"
		self._Label_Comp_Rx.Size = System.Drawing.Size(68, 28)
		self._Label_Comp_Rx.TabIndex = 38
		self._Label_Comp_Rx.Text = "Comp. :"
		self._Label_Comp_Rx.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_Model_Rx
		# 
		self._Label_Model_Rx.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Label_Model_Rx.Location = System.Drawing.Point(6, 77)
		self._Label_Model_Rx.Name = "Label_Model_Rx"
		self._Label_Model_Rx.Size = System.Drawing.Size(68, 28)
		self._Label_Model_Rx.TabIndex = 38
		self._Label_Model_Rx.Text = "Model :"
		self._Label_Model_Rx.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# ComboBox_IBIS_Tx
		# 
		self._ComboBox_IBIS_Tx.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._ComboBox_IBIS_Tx.FormattingEnabled = True
		self._ComboBox_IBIS_Tx.Location = System.Drawing.Point(59, 22)
		self._ComboBox_IBIS_Tx.Name = "ComboBox_IBIS_Tx"
		self._ComboBox_IBIS_Tx.Size = System.Drawing.Size(170, 24)
		self._ComboBox_IBIS_Tx.TabIndex = 31		
		self._ComboBox_IBIS_Tx.SelectedIndexChanged += self.ComboBox_IBIS_TxSelectedIndexChanged
		# 
		# ComboBox_Comp_Tx
		# 
		self._ComboBox_Comp_Tx.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._ComboBox_Comp_Tx.FormattingEnabled = True
		self._ComboBox_Comp_Tx.Location = System.Drawing.Point(59, 52)
		self._ComboBox_Comp_Tx.Name = "ComboBox_Comp_Tx"
		self._ComboBox_Comp_Tx.Size = System.Drawing.Size(170, 24)
		self._ComboBox_Comp_Tx.TabIndex = 39		
		self._ComboBox_Comp_Tx.SelectedIndexChanged += self.ComboBox_Comp_TxSelectedIndexChanged
		# 
		# ComboBox_Model_Tx
		# 
		self._ComboBox_Model_Tx.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._ComboBox_Model_Tx.FormattingEnabled = True
		self._ComboBox_Model_Tx.Location = System.Drawing.Point(59, 82)
		self._ComboBox_Model_Tx.Name = "ComboBox_Model_Tx"
		self._ComboBox_Model_Tx.Size = System.Drawing.Size(170, 24)
		self._ComboBox_Model_Tx.TabIndex = 39
		self._ComboBox_Model_Tx.SelectedIndexChanged += self.ComboBox_Model_TxSelectedIndexChanged
		# 
		# ComboBox_IBIS_Rx
		# 
		self._ComboBox_IBIS_Rx.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._ComboBox_IBIS_Rx.FormattingEnabled = True
		self._ComboBox_IBIS_Rx.Location = System.Drawing.Point(59, 22)
		self._ComboBox_IBIS_Rx.Name = "ComboBox_IBIS_Rx"
		self._ComboBox_IBIS_Rx.Size = System.Drawing.Size(170, 24)
		self._ComboBox_IBIS_Rx.TabIndex = 31
		self._ComboBox_IBIS_Rx.SelectedIndexChanged += self.ComboBox_IBIS_RxSelectedIndexChanged
		# 
		# ComboBox_Comp_Rx
		# 
		self._ComboBox_Comp_Rx.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._ComboBox_Comp_Rx.FormattingEnabled = True
		self._ComboBox_Comp_Rx.Location = System.Drawing.Point(59, 52)
		self._ComboBox_Comp_Rx.Name = "ComboBox_Comp_Rx"
		self._ComboBox_Comp_Rx.Size = System.Drawing.Size(170, 24)
		self._ComboBox_Comp_Rx.TabIndex = 39
		self._ComboBox_Comp_Rx.SelectedIndexChanged += self.ComboBox_Comp_RxSelectedIndexChanged
		# 
		# ComboBox_Model_Rx
		# 
		self._ComboBox_Model_Rx.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._ComboBox_Model_Rx.FormattingEnabled = True
		self._ComboBox_Model_Rx.Location = System.Drawing.Point(59, 82)
		self._ComboBox_Model_Rx.Name = "ComboBox_Model_Rx"
		self._ComboBox_Model_Rx.Size = System.Drawing.Size(170, 24)
		self._ComboBox_Model_Rx.TabIndex = 39
		self._ComboBox_Model_Rx.SelectedIndexChanged += self.ComboBox_Model_RxSelectedIndexChanged
		# 
		# DataGridView_Tx
		# 
		self._DataGridView_Tx.AllowUserToAddRows = False
		self._DataGridView_Tx.AllowUserToDeleteRows = False
		self._DataGridView_Tx.AllowUserToOrderColumns = True
		self._DataGridView_Tx.AllowUserToResizeRows = False
		self._DataGridView_Tx.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.AllCells
		self._DataGridView_Tx.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize
		self._DataGridView_Tx.Columns.AddRange(System.Array[System.Windows.Forms.DataGridViewColumn](
			[self._DataGridView_Tx_CheckBoxColumn,
			self._DataGridView_Tx_TextBoxColumn,
			self._DataGridView_Tx_TextBoxColumn1]))
		self._DataGridView_Tx.EditMode = System.Windows.Forms.DataGridViewEditMode.EditOnF2
		self._DataGridView_Tx.Location = System.Drawing.Point(6, 112)
		self._DataGridView_Tx.Name = "DataGridView_Tx"
		self._DataGridView_Tx.RowHeadersVisible = False
		self._DataGridView_Tx.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect
		self._DataGridView_Tx.Size = System.Drawing.Size(274, 156)
		self._DataGridView_Tx.TabIndex = 37
		self._DataGridView_Tx.Columns[1].ReadOnly = True
		self._DataGridView_Tx.Columns[2].ReadOnly = True
		self._DataGridView_Tx.KeyPress += self.DataGridView_TxKeyPress
		#self._DataGridView_Tx.ColumnHeaderMouseClick += self.DataGridView_TxColumnHeaderMouseClick
		self._DataGridView_Tx.CellMouseClick += self.DataGridView_TxCellMouseClick

		# 
		# DataGridView_Tx_CheckBoxColumn
		# 
		self._DataGridView_Tx_CheckBoxColumn.HeaderText = ""
		self._DataGridView_Tx_CheckBoxColumn.Name = "Col_TargetTxModel"
		self._DataGridView_Tx_CheckBoxColumn.Width = 35
		# 
		# DataGridView_Tx_TextBoxColumn
		# 
		self._DataGridView_Tx_TextBoxColumn.HeaderText = "Models"
		self._DataGridView_Tx_TextBoxColumn.Name = "Col_TxModelName"
		self._DataGridView_Tx_TextBoxColumn.Width = 100
		# 
		# DataGridView_Tx_TextBoxColumn1
		# 
		self._DataGridView_Tx_TextBoxColumn1.HeaderText = "Note"
		self._DataGridView_Tx_TextBoxColumn1.Name = "Col_TxNote"
		self._DataGridView_Tx_TextBoxColumn1.Width = 136
		# 
		# DataGridView_Rx
		# 
		self._DataGridView_Rx.AllowUserToAddRows = False
		self._DataGridView_Rx.AllowUserToDeleteRows = False
		self._DataGridView_Rx.AllowUserToOrderColumns = True
		self._DataGridView_Rx.AllowUserToResizeRows = False
		self._DataGridView_Rx.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.AllCells
		self._DataGridView_Rx.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize
		self._DataGridView_Rx.Columns.AddRange(System.Array[System.Windows.Forms.DataGridViewColumn](
			[self._DataGridView_Rx_CheckBoxColumn,
			self._DataGridView_Rx_TextBoxColumn,
			self._DataGridView_Rx_TextBoxColumn1]))
		self._DataGridView_Rx.EditMode = System.Windows.Forms.DataGridViewEditMode.EditOnF2
		self._DataGridView_Rx.Location = System.Drawing.Point(6, 112)
		self._DataGridView_Rx.Name = "DataGridView_Rx"
		self._DataGridView_Rx.RowHeadersVisible = False
		self._DataGridView_Rx.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect
		self._DataGridView_Rx.Size = System.Drawing.Size(274, 156)
		self._DataGridView_Rx.TabIndex = 37
		self._DataGridView_Rx.Columns[1].ReadOnly = True
		self._DataGridView_Rx.Columns[2].ReadOnly = True
		self._DataGridView_Rx.KeyPress += self.DataGridView_RxKeyPress
		#self._DataGridView_Rx.ColumnHeaderMouseClick += self.DataGridView_RxColumnHeaderMouseClick
		self._DataGridView_Rx.CellMouseClick += self.DataGridView_RxCellMouseClick
		# 
		# DataGridView_Rx_CheckBoxColumn
		# 
		self._DataGridView_Rx_CheckBoxColumn.HeaderText = ""
		self._DataGridView_Rx_CheckBoxColumn.Name = "Col_TargetTxModel"
		self._DataGridView_Rx_CheckBoxColumn.Width = 35
		# 
		# DataGridView_Rx_TextBoxColumn
		# 
		self._DataGridView_Rx_TextBoxColumn.HeaderText = "Models"
		self._DataGridView_Rx_TextBoxColumn.Name = "Col_RxModelName"
		self._DataGridView_Rx_TextBoxColumn.Width = 100
		# 
		# DataGridView_Rx_TextBoxColumn1
		# 
		self._DataGridView_Rx_TextBoxColumn1.HeaderText = "Note"
		self._DataGridView_Rx_TextBoxColumn1.Name = "Col_RxNote"
		self._DataGridView_Rx_TextBoxColumn1.Width = 136
		# 
		# Button_View_Tx
		# 
		self._Button_View_Tx.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_View_Tx.Location = System.Drawing.Point(235, 21)
		self._Button_View_Tx.Name = "Button_View_Tx"
		self._Button_View_Tx.Size = System.Drawing.Size(45, 25)
		self._Button_View_Tx.TabIndex = 33
		self._Button_View_Tx.Text = "View"
		self._Button_View_Tx.Enabled = False
		self._Button_View_Tx.UseVisualStyleBackColor = True
		self._Button_View_Tx.Click += self.Button_View_TxClick
		# 
		# Button_View_Rx
		# 
		self._Button_View_Rx.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_View_Rx.Location = System.Drawing.Point(235, 21)
		self._Button_View_Rx.Name = "Button_View_Rx"
		self._Button_View_Rx.Size = System.Drawing.Size(45, 25)
		self._Button_View_Rx.TabIndex = 33
		self._Button_View_Rx.Text = "View"
		self._Button_View_Rx.Enabled = False
		self._Button_View_Rx.UseVisualStyleBackColor = True
		self._Button_View_Rx.Click += self.Button_View_RxClick
		# 
		# Button_CaseView
		# 
		self._Button_CaseView.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_CaseView.Location = System.Drawing.Point(12, 293)
		self._Button_CaseView.Name = "Button_CaseView"
		self._Button_CaseView.Size = System.Drawing.Size(135, 35)
		self._Button_CaseView.TabIndex = 44
		self._Button_CaseView.Text = "Sim. Cases"
		self._Button_CaseView.UseVisualStyleBackColor = True
		self._Button_CaseView.Click += self.Button_CaseViewClick		
		# 
		# Button_AnalysisOption
		# 
		self._Button_AnalysisOption.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_AnalysisOption.Location = System.Drawing.Point(164, 293)
		self._Button_AnalysisOption.Name = "Button_AnalysisOption"
		self._Button_AnalysisOption.Size = System.Drawing.Size(135, 35)
		self._Button_AnalysisOption.TabIndex = 46
		self._Button_AnalysisOption.Text = "Analysis Option"
		self._Button_AnalysisOption.UseVisualStyleBackColor = True
		self._Button_AnalysisOption.Click += self.Button_AnalysisOptionClick
		# 
		# Button_Run
		# 
		self._Button_Run.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_Run.Location = System.Drawing.Point(316, 293)
		self._Button_Run.Name = "Button_Run"
		self._Button_Run.Size = System.Drawing.Size(135, 35)
		self._Button_Run.TabIndex = 42
		self._Button_Run.Text = "Run"
		self._Button_Run.UseVisualStyleBackColor = True
		self._Button_Run.Click += self.Button_RunClick
		# 
		# Button_ResultView
		# 
		self._Button_ResultView.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_ResultView.Location = System.Drawing.Point(470, 293)
		self._Button_ResultView.Name = "Button_ResultView"
		self._Button_ResultView.Size = System.Drawing.Size(135, 35)
		self._Button_ResultView.TabIndex = 44
		self._Button_ResultView.Enabled = False
		self._Button_ResultView.Text = "Results"
		self._Button_ResultView.UseVisualStyleBackColor = True
		self._Button_ResultView.Click += self.Button_ResultViewClick
		# 
		# IBIS_Form
		#
		self.def_Tx_model = ""
		self.def_Rx_model = ""
		self.ClientSize = System.Drawing.Size(618, 339)
		self.MinimumSize = System.Drawing.Size(self.Size.Width, self.Size.Height)
		self.FormSize_W = self.Size.Width
		self.FormSize_H = self.Size.Height
		self.Controls.Add(self._Button_ResultView)
		self.Controls.Add(self._Button_AnalysisOption)
		self.Controls.Add(self._GroupBox_Rx)
		self.Controls.Add(self._Button_CaseView)
		self.Controls.Add(self._GroupBox_Tx)
		self.Controls.Add(self._Button_Run)
		IconFile = path + "\\Resources\\LOGO.ico"
		self.Icon = Icon(IconFile)
		self.Name = "IBIS_Form"
		self.Text = "IBIS Optimizer"
		self.Load += self.IBIS_FormLoad
		self.ResizeEnd += self.IBIS_FormResizeEnd
		self.DoubleClick += self.IBIS_FormDoubleClick
		self._GroupBox_Rx.ResumeLayout(False)
		self._DataGridView_Rx.EndInit()
		self._GroupBox_Tx.ResumeLayout(False)
		self._DataGridView_Tx.EndInit()
		self.ResumeLayout(False)

	def IBIS_FormLoad(self, sender, e):
		try:			
			self.Cursor = Cursors.WaitCursor
			self.Text = "IBIS Optimizer - [Project]:%s, [Design]:%s" % (sub_DB.File.split('\\')[-1].split('.')[0].strip(), sub_DB.Eye_Form._ComboBox_Design.Text)
			##########
			# for Tx #
			##########
			File = ""
			if not self._ComboBox_IBIS_Tx.Text == "":
				###############################
				# 1.Get full path for Tx IBIS #
				###############################
				for item in sub_DB.Parsing_data['IBIS_File']:
					if self._ComboBox_IBIS_Tx.Text in item:
						File = item
						break
				
				if not File == "":
					#########################
					# 2.Parsing for Tx IBIS #
					#########################					
					sub_DB.IBIS_Tx = IBIS_Parsing(File)
					#sub_DB.IBISInfo_Tx_Form = IBIS_Viwer(File, True)
					
					###################
					# 3.Add Component #
					###################
					count = 0
					for item in sub_DB.IBIS_Tx['Component']:
						if not item in self._ComboBox_Comp_Tx.Items:
							self._ComboBox_Comp_Tx.Items.Add(item)
							count += 1

					###########################
					# 4.Set Default Component #
					###########################
					if count == 1:
						self._ComboBox_Comp_Tx.SelectedIndex = 0
					else:
						for i in range(0, self._ComboBox_Comp_Tx.Items.Count):
							if self._ComboBox_Comp_Tx.Items[i] in sub_DB.Parsing_data['IBIS_Component']:
								self._ComboBox_Comp_Tx.SelectedIndex = i
					
			##########
			# for Rx #
			##########
			File = ""
			if not self._ComboBox_IBIS_Rx.Text == "":
				###############################
				# 1.Get full path for Tx IBIS #
				###############################
				for item in sub_DB.Parsing_data['IBIS_File']:
					if self._ComboBox_IBIS_Rx.Text in item:
						File = item
						break

				if not File == "":
					#########################
					# 2.Parsing for Tx IBIS #
					#########################					
					sub_DB.IBIS_Rx = IBIS_Parsing(File)
					#sub_DB.IBISInfo_Rx_Form = IBIS_Viwer(File, False)

					###################
					# 3.Add Component #
					###################				
					count = 0	
					for item in sub_DB.IBIS_Rx['Component']:
						if not item in self._ComboBox_Comp_Rx.Items:
							self._ComboBox_Comp_Rx.Items.Add(item)
							count += 1

					###########################
					# 4.Set Default Component #
					###########################
					if count == 1:
						self._ComboBox_Comp_Rx.SelectedIndex = 0
					else:
						for i in range(0, self._ComboBox_Comp_Rx.Items.Count):
							if self._ComboBox_Comp_Rx.Items[i] in sub_DB.Parsing_data['IBIS_Component']:
								self._ComboBox_Comp_Rx.SelectedIndex = i

			self.Cursor = Cursors.Default

			# Set ToopTip			
			self._ComboBox_IBIS_Tx_ToopTip.SetToolTip(self._ComboBox_IBIS_Tx, self._ComboBox_IBIS_Tx.Text)
			self._ComboBox_IBIS_Rx_ToopTip.SetToolTip(self._ComboBox_IBIS_Rx, self._ComboBox_IBIS_Rx.Text)

		except Exception as e:			
			Log("[IBIS Form Load] = Failed")
			Log(traceback.format_exc())
			print traceback.format_exc()
			MessageBox.Show("Fail to load IBIS Opt Form","Warning")
			EXIT()

	def IBIS_FormResizeEnd(self, sender, e):
		try:
			# Get previous Eye_Form width/height and resized Eye_Form width/height
			# Calculate Gap betweent previous and resized width/height		
			Gap_W = self.Size.Width - self.FormSize_W
			Gap_H = self.Size.Height - self.FormSize_H
			
			# Backup the resized Eye_Form width/height as previous MainFomr width/height
			self.FormSize_W = self.Size.Width
			self.FormSize_H = self.Size.Height

			# Resize
			self._GroupBox_Tx.Size = System.Drawing.Size(self._GroupBox_Tx.Width + Gap_W/2, self._GroupBox_Tx.Height + Gap_H)
			self._GroupBox_Rx.Size = System.Drawing.Size(self._GroupBox_Rx.Width + Gap_W/2, self._GroupBox_Rx.Height + Gap_H)
			self._DataGridView_Tx.Size = System.Drawing.Size(self._DataGridView_Tx.Width + Gap_W/2, self._DataGridView_Tx.Height + Gap_H)
			self._DataGridView_Tx_TextBoxColumn.Width = self._DataGridView_Tx_TextBoxColumn.Width + Gap_W/2
			self._DataGridView_Rx.Size = System.Drawing.Size(self._DataGridView_Rx.Width + Gap_W/2, self._DataGridView_Rx.Height + Gap_H)			
			self._DataGridView_Rx_TextBoxColumn.Width = self._DataGridView_Rx_TextBoxColumn.Width + Gap_W/2
			self._ComboBox_IBIS_Tx.Size = System.Drawing.Size(self._ComboBox_IBIS_Tx.Width + Gap_W/2, self._ComboBox_IBIS_Tx.Height)
			self._ComboBox_Comp_Tx.Size = System.Drawing.Size(self._ComboBox_Comp_Tx.Width + Gap_W/2, self._ComboBox_Comp_Tx.Height)
			self._ComboBox_Model_Tx.Size = System.Drawing.Size(self._ComboBox_Model_Tx.Width + Gap_W/2, self._ComboBox_Model_Tx.Height)
			self._ComboBox_IBIS_Rx.Size = System.Drawing.Size(self._ComboBox_IBIS_Rx.Width + Gap_W/2, self._ComboBox_IBIS_Rx.Height)
			self._ComboBox_Comp_Rx.Size = System.Drawing.Size(self._ComboBox_Comp_Rx.Width + Gap_W/2, self._ComboBox_Comp_Rx.Height)
			self._ComboBox_Model_Rx.Size = System.Drawing.Size(self._ComboBox_Model_Rx.Width + Gap_W/2, self._ComboBox_Model_Rx.Height)
			
			# Relocate
			self._GroupBox_Rx.Location = System.Drawing.Point(self._GroupBox_Rx.Location.X + Gap_W/2, self._GroupBox_Rx.Location.Y)
			self._Button_View_Tx.Location = System.Drawing.Point(self._Button_View_Tx.Location.X + Gap_W/2, self._Button_View_Tx.Location.Y)
			self._Button_View_Rx.Location = System.Drawing.Point(self._Button_View_Rx.Location.X + Gap_W/2, self._Button_View_Rx.Location.Y)
			self._Button_CaseView.Location = System.Drawing.Point(self._Button_CaseView.Location.X, self._Button_CaseView.Location.Y + Gap_H)
			self._Button_AnalysisOption.Location = System.Drawing.Point(self._Button_AnalysisOption.Location.X, self._Button_AnalysisOption.Location.Y + Gap_H)
			self._Button_Run.Location = System.Drawing.Point(self._Button_Run.Location.X, self._Button_Run.Location.Y + Gap_H)
			self._Button_ResultView.Location = System.Drawing.Point(self._Button_ResultView.Location.X, self._Button_ResultView.Location.Y + Gap_H)

		except Exception as e:			
			Log("[IBIS_FormResizeEnd] = Failed")
			Log(traceback.format_exc())
			print traceback.format_exc()
			MessageBox.Show("Fail to resize Eye Analyzer IBIS Optimizer GUI","Warning")			
			EXIT()

	def IBIS_FormDoubleClick(self, sender, e):				
		self._GroupBox_Tx.Location = System.Drawing.Point(12, 12)		
		self._GroupBox_Tx.Size = System.Drawing.Size(286, 275)
		self._GroupBox_Rx.Location = System.Drawing.Point(319, 12)		
		self._GroupBox_Rx.Size = System.Drawing.Size(286, 275)
		self._DataGridView_Tx.Location = System.Drawing.Point(6, 112)
		self._DataGridView_Tx.Size = System.Drawing.Size(274, 156)
		self._DataGridView_Tx_CheckBoxColumn.Width = 35		
		self._DataGridView_Tx_TextBoxColumn.Width = 236		
		self._DataGridView_Rx.Location = System.Drawing.Point(6, 112)		
		self._DataGridView_Rx.Size = System.Drawing.Size(274, 156)		
		self._DataGridView_Rx_CheckBoxColumn.Width = 35		
		self._DataGridView_Rx_TextBoxColumn.Width = 236
		self._ComboBox_IBIS_Tx.Location = System.Drawing.Point(59, 22)		
		self._ComboBox_IBIS_Tx.Size = System.Drawing.Size(170, 24)		
		self._ComboBox_Comp_Tx.Location = System.Drawing.Point(59, 52)
		self._ComboBox_Comp_Tx.Size = System.Drawing.Size(170, 24)
		self._ComboBox_Model_Tx.Location = System.Drawing.Point(59, 82)		
		self._ComboBox_Model_Tx.Size = System.Drawing.Size(170, 24)
		self._ComboBox_IBIS_Rx.Location = System.Drawing.Point(59, 22)
		self._ComboBox_IBIS_Rx.Size = System.Drawing.Size(170, 24)		
		self._ComboBox_Comp_Rx.Location = System.Drawing.Point(59, 52)		
		self._ComboBox_Comp_Rx.Size = System.Drawing.Size(170, 24)		
		self._ComboBox_Model_Rx.Location = System.Drawing.Point(59, 82)		
		self._ComboBox_Model_Rx.Size = System.Drawing.Size(170, 24)
		self._Button_View_Tx.Location = System.Drawing.Point(235, 21)		
		self._Button_View_Rx.Location = System.Drawing.Point(235, 21)
		self._Button_CaseView.Location = System.Drawing.Point(12, 293)		
		self._Button_AnalysisOption.Location = System.Drawing.Point(164, 293)		
		self._Button_Run.Location = System.Drawing.Point(316, 293)		
		self._Button_ResultView.Location = System.Drawing.Point(470, 293)		
		self.ClientSize = System.Drawing.Size(618, 339)
		self.FormSize_W = self.Size.Width
		self.FormSize_H = self.Size.Height

	def ComboBox_IBIS_TxSelectedIndexChanged(self, sender, e):		
		try:
			self.Cursor = Cursors.WaitCursor
			####################
			# 0.Initialization #
			####################
			self._DataGridView_Tx.Rows.Clear()
			self._ComboBox_Comp_Tx.Items.Clear()
			self._ComboBox_Model_Tx.Items.Clear()

			###############################
			# 1.Get full path for Tx IBIS #
			###############################
			for item in sub_DB.Parsing_data['IBIS_File']:
				if self._ComboBox_IBIS_Tx.Text in item:
					File = item
					break

			#########################
			# 2.Parsing for Tx IBIS #
			#########################			
			sub_DB.IBIS_Tx = IBIS_Parsing(File)
			#sub_DB.IBISInfo_Tx_Form = IBIS_Viwer(File, True)

			###################
			# 3.Add Component #
			###################
			count = 0
			for item in sub_DB.IBIS_Tx['Component']:
				if not item in self._ComboBox_Comp_Tx.Items:
					self._ComboBox_Comp_Tx.Items.Add(item)
					count += 1
			
			###########################
			# 4.Set Default Component #
			###########################
			if count == 1:
				self._ComboBox_Comp_Tx.SelectedIndex = 0
			else:
				for i in range(0, self._ComboBox_Comp_Tx.Items.Count):
					if self._ComboBox_Comp_Tx.Items[i] in sub_DB.Parsing_data['IBIS_Component']:
						self._ComboBox_Comp_Tx.SelectedIndex = i
			
			################
			# 5.Add Models #
			################
			# If [Model Selector] exists
			if not len(sub_DB.IBIS_Tx["Model Selector"]) == 0:
				for models in sub_DB.IBIS_Tx["Model Selector"].keys():
					self._ComboBox_Model_Tx.Items.Add(models)
			
				# Set Default Model
				for models in sub_DB.IBIS_Tx["Model Selector"].keys():				
					for model in sub_DB.IBIS_Tx["Model Selector"][models]:					
						if model[0] in sub_DB.Parsing_data['IBIS_Model']:
							self.def_Tx_model = model[0]
							self._ComboBox_Model_Tx.Text = models
							break

			# If [Model Selector] is not exists
			else:				
				self._ComboBox_Model_Tx.Text = "N/A"
				for model in sub_DB.IBIS_Tx["Model"]:
					if model in sub_DB.Parsing_data['IBIS_Model']:
						self.def_Tx_model = model
						break
				iter = 0
				for model in sub_DB.IBIS_Tx["Model"]:
					if model == self.def_Tx_model:
						self._DataGridView_Tx.Rows.Add(True, model, "N/A")
						self._DataGridView_Tx.Rows[iter].DefaultCellStyle.BackColor = System.Drawing.SystemColors.Info
						iter += 1
					else:
						self._DataGridView_Tx.Rows.Add(False, model, "N/A")
						iter += 1
			
			#################
			# 6.Set ToopTip #
			#################
			self._ComboBox_IBIS_Tx_ToopTip.SetToolTip(self._ComboBox_IBIS_Tx, self._ComboBox_IBIS_Tx.Text)
			self.Cursor = Cursors.Default

		except Exception as e:			
			Log("[IBIS Form Tx File ComboBox] = Index Change Failed")
			Log(traceback.format_exc())
			print traceback.format_exc()
			MessageBox.Show("Fail to change index for Tx IBIS File","Warning")
			EXIT()

	def ComboBox_IBIS_RxSelectedIndexChanged(self, sender, e):		
		try:
			self.Cursor = Cursors.WaitCursor	
			####################
			# 0.Initialization #
			####################
			self._DataGridView_Rx.Rows.Clear()
			self._ComboBox_Comp_Rx.Items.Clear()
			self._ComboBox_Model_Rx.Items.Clear()

			###############################
			# 1.Get full path for Tx IBIS #
			###############################
			for item in sub_DB.Parsing_data['IBIS_File']:
				if self._ComboBox_IBIS_Rx.Text in item:
					File = item
					break

			#########################
			# 2.Parsing for Tx IBIS #
			#########################			
			sub_DB.IBIS_Rx = IBIS_Parsing(File)
			#sub_DB.IBISInfo_Rx_Form = IBIS_Viwer(File, False)

			###################
			# 3.Add Component #
			###################
			count = 0
			for item in sub_DB.IBIS_Rx['Component']:
				if not item in self._ComboBox_Comp_Rx.Items:
					self._ComboBox_Comp_Rx.Items.Add(item)
					count += 1

			###########################
			# 4.Set Default Component #
			###########################
			if count == 1:
				self._ComboBox_Comp_Rx.SelectedIndex = 0
			else:
				for i in range(0, self._ComboBox_Comp_Rx.Items.Count):
					if self._ComboBox_Comp_Rx.Items[i] in sub_DB.Parsing_data['IBIS_Component']:
						self._ComboBox_Comp_Rx.SelectedIndex = i

			################
			# 5.Add Models #
			################
			# If [Model Selector] exists
			if not len(sub_DB.IBIS_Rx["Model Selector"]) == 0:
				for models in sub_DB.IBIS_Rx["Model Selector"].keys():
					self._ComboBox_Model_Rx.Items.Add(models)
			
				# Set Default Model
				for models in sub_DB.IBIS_Rx["Model Selector"].keys():				
					for model in sub_DB.IBIS_Rx["Model Selector"][models]:					
						if model[0] in sub_DB.Parsing_data['IBIS_Model']:
							self.def_Rx_model = model[0]
							self._ComboBox_Model_Rx.Text = models
							break

			# If [Model Selector] is not exists
			else:				
				self._ComboBox_Model_Rx.Text = "N/A"
				for model in sub_DB.IBIS_Rx["Model"]:
					if model in sub_DB.Parsing_data['IBIS_Model']:
						self.def_Rx_model = model
						break
				iter = 0
				for model in sub_DB.IBIS_Rx["Model"]:
					if model == self.def_Rx_model:
						self._DataGridView_Rx.Rows.Add(True, model, "N/A")
						self._DataGridView_Rx.Rows[iter].DefaultCellStyle.BackColor = System.Drawing.SystemColors.Info
						iter += 1
					else:
						self._DataGridView_Rx.Rows.Add(False, model, "N/A")
						iter += 1

			#################
			# 6.Set ToopTip #
			#################
			self._ComboBox_IBIS_Rx_ToopTip.SetToolTip(self._ComboBox_IBIS_Rx, self._ComboBox_IBIS_Rx.Text)
			self.Cursor = Cursors.Default

		except Exception as e:			
			Log("[IBIS Form Rx File ComboBox] = Index Change Failed")
			Log(traceback.format_exc())
			print traceback.format_exc()
			MessageBox.Show("Fail to change index for Rx IBIS File","Warning")
			EXIT()

	def ComboBox_Comp_TxSelectedIndexChanged(self, sender, e):
		try:
			#print sub_DB.IBIS_Tx['Model Selector'].keys()
			#self.IBIS["Model Selector"] = {self.DB["Text"][init_idx].split(']')[-1].strip():temp}
			pass

		except Exception as e:			
			Log("[IBIS Form Tx Comp ComboBox] = Index Change Failed")
			Log(traceback.format_exc())
			print traceback.format_exc()
			MessageBox.Show("Fail to change index for Tx Component","Warning")
			EXIT()

	def ComboBox_Comp_RxSelectedIndexChanged(self, sender, e):

		pass

	def ComboBox_Model_TxSelectedIndexChanged(self, sender, e):
		#self.IBIS_FormDoubleClick(self, sender)
		self._ComboBox_Model_Tx.BackColor = System.Drawing.SystemColors.Window
		self._DataGridView_Tx.Rows.Clear()
		iter = 0
		for item in sub_DB.IBIS_Tx["Model Selector"][self._ComboBox_Model_Tx.Text]:
			if item[0] == self.def_Tx_model:
				self._DataGridView_Tx.Rows.Add(True, item[0], item[1])
				self._DataGridView_Tx.Rows[iter].DefaultCellStyle.BackColor = System.Drawing.SystemColors.Info
				iter += 1
			else:
				self._DataGridView_Tx.Rows.Add(False, item[0], item[1])
				iter += 1		

		#Gap = self._DataGridView_Tx_TextBoxColumn.Width + self._DataGridView_Tx_TextBoxColumn1.Width - 275
		#self._GroupBox_Tx.Size = System.Drawing.Size(self._GroupBox_Tx.Width + Gap, self._GroupBox_Tx.Height)
		#self._DataGridView_Tx.Size = System.Drawing.Size(self._DataGridView_Tx.Width + Gap, self._DataGridView_Tx.Height)
		#self._ComboBox_IBIS_Tx.Size = System.Drawing.Size(self._ComboBox_IBIS_Tx.Width + Gap, self._ComboBox_IBIS_Tx.Height)
		#self._ComboBox_Comp_Tx.Size = System.Drawing.Size(self._ComboBox_Comp_Tx.Width + Gap, self._ComboBox_Comp_Tx.Height)
		#self._ComboBox_Model_Tx.Size = System.Drawing.Size(self._ComboBox_Model_Tx.Width + Gap, self._ComboBox_Model_Tx.Height)
		#self.ClientSize = System.Drawing.Size(self.Size.Width + Gap, self.Size.Height)
		#self._Button_View_Tx.Location = System.Drawing.Point(self._Button_View_Tx.Location.X + Gap, self._Button_View_Tx.Location.Y)
		#self._GroupBox_Rx.Location = System.Drawing.Point(self._GroupBox_Rx.Location.X + Gap, self._GroupBox_Rx.Location.Y)
		pass

	def ComboBox_Model_RxSelectedIndexChanged(self, sender, e):
		#self.IBIS_FormDoubleClick(self, sender)
		self._ComboBox_Model_Rx.BackColor = System.Drawing.SystemColors.Window
		self._DataGridView_Rx.Rows.Clear()
		iter = 0
		for item in sub_DB.IBIS_Rx["Model Selector"][self._ComboBox_Model_Rx.Text]:
			if item[0] == self.def_Rx_model:
				self._DataGridView_Rx.Rows.Add(True, item[0], item[1])
				self._DataGridView_Rx.Rows[iter].DefaultCellStyle.BackColor = System.Drawing.SystemColors.Info
				iter += 1
			else:
				self._DataGridView_Rx.Rows.Add(False, item[0], item[1])
				iter += 1

		#Gap = self._DataGridView_Rx_TextBoxColumn.Width + self._DataGridView_Rx_TextBoxColumn1.Width - 275
		#self._GroupBox_Rx.Size = System.Drawing.Size(self._GroupBox_Rx.Width + Gap, self._GroupBox_Rx.Height)
		#self._DataGridView_Rx.Size = System.Drawing.Size(self._DataGridView_Rx.Width + Gap, self._DataGridView_Rx.Height)
		#self._ComboBox_IBIS_Rx.Size = System.Drawing.Size(self._ComboBox_IBIS_Rx.Width + Gap, self._ComboBox_IBIS_Rx.Height)
		#self._ComboBox_Comp_Rx.Size = System.Drawing.Size(self._ComboBox_Comp_Rx.Width + Gap, self._ComboBox_Comp_Rx.Height)
		#self._ComboBox_Model_Rx.Size = System.Drawing.Size(self._ComboBox_Model_Rx.Width + Gap, self._ComboBox_Model_Rx.Height)
		#self.ClientSize = System.Drawing.Size(self.Size.Width + Gap, self.Size.Height)
		#self._Button_View_Rx.Location = System.Drawing.Point(self._Button_View_Rx.Location.X + Gap, self._Button_View_Rx.Location.Y)
		pass

	def DataGridView_TxKeyPress(self, sender, e):
		try:
			# Spacebar = Check/Uncheck all the selected rows
			if e.KeyChar == chr(32):
				for row in self._DataGridView_Tx.SelectedRows:
					row.Cells[0].Value = not row.Cells[0].Value
					if row.Cells[0].Value:
						row.DefaultCellStyle.BackColor = System.Drawing.SystemColors.Info
					else:
						row.DefaultCellStyle.BackColor = System.Drawing.SystemColors.Window

				# Calculate Total Simulation Cases
				tx_count = 0
				for row in self._DataGridView_Tx.Rows:			
					if row.Cells[0].Value:
						tx_count += 1

				rx_count = 0
				for row in self._DataGridView_Rx.Rows:
					if row.Cells[0].Value:
						rx_count += 1

				case = tx_count*rx_count
				self._Button_CaseView.Text = ""
				self._Button_CaseView.Text = "Sim. Cases:[%d]" % case

		except Exception as e:		
			Log("[Net Form Key Press] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to press key in Net Classificiton Form","Warning")			
			EXIT()

	def DataGridView_TxCellMouseClick(self, sender, e):
		# Set Checked and Un-checked Row Back Color
		if e.ColumnIndex == 0:
			if self._DataGridView_Tx.Rows[e.RowIndex].Cells[0].Value:
				self._DataGridView_Tx.Rows[e.RowIndex].DefaultCellStyle.BackColor = System.Drawing.SystemColors.Window
			else:
				self._DataGridView_Tx.Rows[e.RowIndex].DefaultCellStyle.BackColor = System.Drawing.SystemColors.Info

		# Calculate Total Simulation Cases
		tx_count = 0
		for row in self._DataGridView_Tx.Rows:			
			if row.Cells[0].Value:
				tx_count += 1

		rx_count = 0
		for row in self._DataGridView_Rx.Rows:
			if row.Cells[0].Value:
				rx_count += 1

		case = tx_count*rx_count
		self._Button_CaseView.Text = ""
		self._Button_CaseView.Text = "Sim. Cases:[%d]" % case

	def DataGridView_RxKeyPress(self, sender, e):
		try:
			# Spacebar = Check/Uncheck all the selected rows
			if e.KeyChar == chr(32):
				for row in self._DataGridView_Rx.SelectedRows:
					row.Cells[0].Value = not row.Cells[0].Value
					if row.Cells[0].Value:
						row.DefaultCellStyle.BackColor = System.Drawing.SystemColors.Info
					else:
						row.DefaultCellStyle.BackColor = System.Drawing.SystemColors.Window

				# Calculate Total Simulation Cases
				tx_count = 0
				for row in self._DataGridView_Tx.Rows:			
					if row.Cells[0].Value:
						tx_count += 1

				rx_count = 0
				for row in self._DataGridView_Rx.Rows:
					if row.Cells[0].Value:
						rx_count += 1

				case = tx_count*rx_count
				self._Button_CaseView.Text = ""
				self._Button_CaseView.Text = "Sim. Cases:[%d]" % case

		except Exception as e:		
			Log("[Net Form Key Press] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to press key in Net Classificiton Form","Warning")			
			EXIT()

	def DataGridView_RxCellMouseClick(self, sender, e):
		if e.ColumnIndex == 0:
			if self._DataGridView_Rx.Rows[e.RowIndex].Cells[0].Value:
				self._DataGridView_Rx.Rows[e.RowIndex].DefaultCellStyle.BackColor = System.Drawing.SystemColors.Window
			else:
				self._DataGridView_Rx.Rows[e.RowIndex].DefaultCellStyle.BackColor = System.Drawing.SystemColors.Info

		# Calculate Total Simulation Cases
		tx_count = 0
		for row in self._DataGridView_Tx.Rows:			
			if row.Cells[0].Value:
				tx_count += 1

		rx_count = 0
		for row in self._DataGridView_Rx.Rows:
			if row.Cells[0].Value:
				rx_count += 1

		case = tx_count*rx_count
		self._Button_CaseView.Text = ""
		self._Button_CaseView.Text = "Sim. Cases:[%d]" % case

	def Button_View_TxClick(self, sender, e):
		try:
			if not sub_DB.IBISInfo_Tx_Form == "":
				sub_DB.IBISInfo_Tx_Form.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
				sub_DB.IBISInfo_Tx_Form.ShowDialog()

		except Exception as e:			
			Log("[Tx IBIS Viwer Launch] = Failed")
			Log(traceback.format_exc())
			print traceback.format_exc()
			MessageBox.Show("Fail to Open Tx IBIS Viwer","Warning")
			EXIT()

	def Button_View_RxClick(self, sender, e):
		try:
			if not sub_DB.IBISInfo_Rx_Form == "":
				sub_DB.IBISInfo_Rx_Form.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
				sub_DB.IBISInfo_Rx_Form.ShowDialog()

		except Exception as e:			
			Log("[Rx IBIS Viwer Launch] = Failed")
			Log(traceback.format_exc())
			print traceback.format_exc()
			MessageBox.Show("Fail to Open Rx IBIS Viwer","Warning")
			EXIT()

	def Button_CaseViewClick(self, sender, e):
		sub_DB.IBIS_Form = self
		sub_DB.IBIS_Result_Init_Flag = True
		sub_DB.IBIS_CaseForm = IBIS_Case()
		sub_DB.IBIS_CaseForm.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
		sub_DB.IBIS_CaseForm.ShowDialog()

	def Button_AnalysisOptionClick(self, sender, e):
		sub_DB.Option_Form.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
		sub_DB.Option_Form.ShowDialog()

	def Button_RunClick(self, sender, e):	
		IBIS_Init()
		self.Cursor = Cursors.WaitCursor
		sub_DB.IBIS_Result_Init_Flag = True
		sub_DB.IBIS_ResultForm = IBIS_Case()		
		sub_DB.IBIS_ResultForm.IBIS_CaseFormLoad(self, sender)		
		sub_DB.IBIS_ResultForm._DataGridView.Columns.Add(sub_DB.IBIS_ResultForm._Col_Results)
		sub_DB.IBIS_ResultForm._DataGridView.Columns.Add(sub_DB.IBIS_ResultForm._Col_Avg_Width)
		sub_DB.IBIS_ResultForm._DataGridView.Columns.Add(sub_DB.IBIS_ResultForm._Col_Avg_Margin)
		sub_DB.IBIS_ResultForm._DataGridView.Columns.Add(sub_DB.IBIS_ResultForm._Col_Worst_Width)
		sub_DB.IBIS_ResultForm._DataGridView.Columns.Add(sub_DB.IBIS_ResultForm._Col_Worst_Margin)
		sub_DB.IBIS_ResultForm._DataGridView.Columns.Add(sub_DB.IBIS_ResultForm._Col_Vref)
		sub_DB.IBIS_ResultForm._DataGridView.Size = System.Drawing.Size(659, 300)
		sub_DB.IBIS_ResultForm.Size = System.Drawing.Size(700, 390)
		sub_DB.IBIS_ResultForm.Text = "IBIS Optimization Results"
		IBIS_Opt_Run(self)
		self.Cursor = Cursors.Default
		self._Button_ResultView.Enabled = True
		sub_DB.IBIS_ResultForm.ShowDialog()

	def Button_ResultViewClick(self, sender, e):
		sub_DB.IBIS_ResultForm.ShowDialog()
		pass

class IBIS_Viwer(Form):
	def __init__(self, File, Flag):

		self.InitializeComponent(File, Flag)
	
	def InitializeComponent(self, File, Flag):
		global path
		path = os.path.dirname(os.path.abspath(__file__))
		self._components = System.ComponentModel.Container()
		self._treeView1 = System.Windows.Forms.TreeView()
		self._richTextBox1 = System.Windows.Forms.RichTextBox()
		self._openFileDialog1 = System.Windows.Forms.OpenFileDialog()		
		self._contextMenuStrip1 = System.Windows.Forms.ContextMenuStrip(self._components)
		self._expandAllToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._collapseAllToolStripMenuItem = System.Windows.Forms.ToolStripMenuItem()
		self._label1 = System.Windows.Forms.Label()
		self._label2 = System.Windows.Forms.Label()
		self._progressBar1 = System.Windows.Forms.ProgressBar()
		self._button1 = System.Windows.Forms.Button()
		self._contextMenuStrip1.SuspendLayout()
		self.SuspendLayout()
		# 
		# treeView1
		# 
		self._treeView1.BackColor = System.Drawing.Color.White
		self._treeView1.ContextMenuStrip = self._contextMenuStrip1
		self._treeView1.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._treeView1.Location = System.Drawing.Point(12, 30)
		self._treeView1.Name = "treeView1"
		self._treeView1.Size = System.Drawing.Size(375, 537)
		self._treeView1.TabIndex = 0
		self._treeView1.NodeMouseClick += self.TreeView1NodeMouseClick
		# 
		# richTextBox1
		# 
		self._richTextBox1.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._richTextBox1.Location = System.Drawing.Point(406, 30)
		self._richTextBox1.Name = "richTextBox1"
		self._richTextBox1.Size = System.Drawing.Size(637, 537)
		self._richTextBox1.TabIndex = 1
		self._richTextBox1.Text = ""
		# 
		# openFileDialog1
		# 
		self._openFileDialog1.FileName = "openFileDialog1"
		# 
		# contextMenuStrip1
		# 
		self._contextMenuStrip1.Items.AddRange(System.Array[System.Windows.Forms.ToolStripItem](
			[self._expandAllToolStripMenuItem,
			self._collapseAllToolStripMenuItem]))
		self._contextMenuStrip1.Name = "contextMenuStrip1"
		self._contextMenuStrip1.Size = System.Drawing.Size(138, 48)
		# 
		# expandAllToolStripMenuItem
		# 
		self._expandAllToolStripMenuItem.Name = "expandAllToolStripMenuItem"
		self._expandAllToolStripMenuItem.Size = System.Drawing.Size(137, 22)
		self._expandAllToolStripMenuItem.Text = "Expand All"
		self._expandAllToolStripMenuItem.Click += self.ExpandAllToolStripMenuItemClick
		# 
		# collapseAllToolStripMenuItem
		# 
		self._collapseAllToolStripMenuItem.Name = "collapseAllToolStripMenuItem"
		self._collapseAllToolStripMenuItem.Size = System.Drawing.Size(137, 22)
		self._collapseAllToolStripMenuItem.Text = "Collapse All"
		self._collapseAllToolStripMenuItem.Click += self.CollapseAllToolStripMenuItemClick
		# 
		# label1
		# 
		self._label1.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._label1.Location = System.Drawing.Point(12, 12)
		self._label1.Name = "label1"
		self._label1.Size = System.Drawing.Size(350, 15)
		self._label1.TabIndex = 2
		self._label1.Text = "label1"
		# 
		# label2
		# 
		self._label2.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._label2.Location = System.Drawing.Point(406, 12)
		self._label2.Name = "label2"
		self._label2.Size = System.Drawing.Size(400, 15)
		self._label2.TabIndex = 3
		self._label2.Text = "label2"
		# 
		# progressBar1
		# 
		self._progressBar1.Location = System.Drawing.Point(12, 573)
		self._progressBar1.Name = "progressBar1"
		self._progressBar1.Size = System.Drawing.Size(940, 22)
		self._progressBar1.Style = System.Windows.Forms.ProgressBarStyle.Continuous
		self._progressBar1.Visible = False
		self._progressBar1.TabIndex = 4
		# 
		# button1
		# 
		self._button1.Font = System.Drawing.Font("Microsoft Sans Serif", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._button1.Location = System.Drawing.Point(964, 571)
		self._button1.Name = "button1"
		self._button1.Size = System.Drawing.Size(78, 25)
		self._button1.TabIndex = 5
		self._button1.Text = "Close"
		self._button1.UseVisualStyleBackColor = True
		self._button1.Click += self.Button1Click
		# 
		# MainForm
		# 
		self.ClientSize = System.Drawing.Size(1055, 604)
		self.MinimumSize = System.Drawing.Size(self.Size.Width, self.Size.Height)
		self.FormSize_W = self.Size.Width
		self.FormSize_H = self.Size.Height
		self.ResizeEnd += self.MainFormResizeEnd
		self.Controls.Add(self._button1)
		self.Controls.Add(self._progressBar1)
		self.Controls.Add(self._label2)
		self.Controls.Add(self._label1)
		self.Controls.Add(self._richTextBox1)
		self.Controls.Add(self._treeView1)
		IconFile = path + "\\Resources\\LOGO.ico"
		self.Icon = Icon(IconFile)
		self.Name = "MainForm"
		if Flag:
			self.Text = "Tx IBIS Model"
		else:
			self.Text = "Rx IBIS Model"
		self._label1.Text = "Hierarchy view for " + File.split('\\')[-1]
		self._label2.Text = File.split('\\')[-1]
		self._contextMenuStrip1.ResumeLayout(False)
		self.ResumeLayout(False)
		self.PerformLayout()		

		self.IBIS = {}

		self.IBIS["Model Selector"] = {}

		self.IBIS["Model"] = {}
		self.IBIS["Model"]["Name"] = []
		self.IBIS["Model"]["Type"] = []

		self.IBIS["Pin"] = {}
		self.IBIS["Pin"]["Name"] = []
		self.IBIS["Pin"]["Signal_name"] = []
		self.IBIS["Pin"]["Model_name"] = []

		self.IBIS["Diff_pin"] = {}
		self.IBIS["Diff_pin"]["Name"] = []
		self.IBIS["Diff_pin"]["Signal_name"] = []
		self.IBIS["Diff_pin"]["Model_name"] = []

		self.IBIS["AMI"] = {}
		self.IBIS["AMI"]["Ex"] = []
		self.IBIS["AMI"]["OS"] = []
		self.IBIS["AMI"]["Compiler"] = []
		self.IBIS["AMI"]["Platform"] = []
		self.IBIS["AMI"]["Ex_file"] = []	# *.dll
		self.IBIS["AMI"]["Para_file"] = []	# *.ami		

		self.AMI_flag = False
		self.Algorithmic_model_flag = False
		self.DB = {}
		self.Line = {}
		self.Length = {}
		self.Key = {}
		self.Model_Type = []
		self.TopNode_keyword = []
		self.SecondNode_keyword = {}
		self.ThirdNode_keyword = {}
		self.FourthNode_keyword = {}
		self.File = File
		

		self.Model_Type = [
			"Input",
			"I/O",
			"I/O_open_drain",
			"I/O_open_sink",
			"I/O_open_source",
			"Input_ECL",
			"I/O_ECL",
			"Terminator",
			"Output",
			"3-state",
			"Open_sink",
			"Open_drain",
			"Open_source",
			"Input_ECL",
			"Output_ECL",
			"I/O_ECL",
			"3-state_ECL",
			"Series",
			"Series_switch",
			"Input_diff",
			"Output_diff",
			"I/O_diff",
			"3-state_diff"
			]

		self.TopNode_keyword = [
			# [Header]
			"[Component]",
			"[Model Selector]",
			"[Model]",
			"[Submodel]",
			"[External Circuit]",
			"[Test Data]",
			"[Test Load]",
			"[Define Package Model]",
			"[Interconnect Model Set]",
			"[End]"
			]

		self.SecondNode_keyword["[Header]"] = [
			"[IBIS Ver]",
			"[Comment Char]",
			"[File Name]",
			"[File Rev]",
			"[Date]",
			"[Source]",
			"[Notes]",
			"[Disclaimer]",
			"[Copyright]"
			]

		self.SecondNode_keyword["[Component]"] = [
			"[Manufacturer]",
			"[Package]",
			"[Pin]",
			"[Package Model]",				
			"[Interconnect Model Group]",
			"[Pin Mapping]",
			"[Bus Label]",
			"[Die Supply Pads]",
			"[Diff Pin]",
			"[Repeater Pin]",
			"[Series Pin Mapping]",
			"[Series Switch Groups]",
			"[Node Declarations]",
			"[Circuit Call]",
			"[Begin EMI Component]"
			]

		self.SecondNode_keyword["[Model]"] = [
			"[Model Spec]",
			"[Receiver Thresholds]",
			"[Add Submodel]",
			"[Driver Schedule]",
			"[Temperature Range]",
			"[Voltage Range]",
			"[Pullup Reference]",
			"[Pulldown Reference]",
			"[POWER Clamp Reference]",
			"[GND Clamp Reference]",
			"[External Reference]",
			"[C Comp Corner]",
			"[TTgnd]",
			"[TTpower]",
			"[Pulldown]",
			"[Pullup]",
			"[GND Clamp]",
			"[POWER Clamp]",
			"[ISSO PU]",
			"[ISSO PD]",
			"[Rgnd]",
			"[Rpower]",
			"[Rac]",
			"[Cac]",
			"[On]",
			"[Off]",
			"[R Series]",
			"[L Series]",
			"[Rl Series]",
			"[C Series]",
			"[Lc Seeries]",
			"[Rc Series]",
			"[Series Current]",
			"[Series MOSFET]",
			"[Ramp]",
			"[Rising Waveform]",
			"[Falling Waveform]",				
			"[Initial Delay]",
			"[External Model]",
			"[Algorithmic Model]",
			"[Begin EMI Model]"
			]

		self.SecondNode_keyword["[Submodel]"] = [
			"[Submodel Spec]",
			"[POWER Pulse Table]",
			"[GND Pulse Table]",
			"[Pulldown]",
			"[Pullup]",
			"[GND Clamp]",
			"[POWER Clamp]",
			"[Ramp]",
			"[Rising Waveform]",
			"[Falling Waveform]",
			"[Initial Delay]"
			]

		self.SecondNode_keyword["[External Circuit]"] = [
			"[End External Circuit]"
			]

		self.SecondNode_keyword["[Test Data]"] = [
			"[Rising Waveform Near]",
			"[Falling Waveform Near]",
			"[Rising Waveform Far]",
			"[Falling Waveform Far]",
			"[Diff Rising Waveform Near]",
			"[Diff Falling Waveform Near]",
			"[Diff Rising Waveform Far]",
			"[Diff Falling Waveform Far]"
			]

		self.SecondNode_keyword["[Define Package Model]"] = [
			"[Manufacturer]",
			"[OEM]",
			"[Description]",
			"[Number Of Sections]",
			"[Number of Pins]",
			"[Pin Numbers]",
			"[Merged Pins]",
			"[Model Data]",
			"[End Package Model]"
			]

		self.SecondNode_keyword["[Interconnect Model Set]"] = [
			"[Manufacturer]",
			"[Description]",
			"[Interconnect Model]",
			"[End Interconnect Model Set]"
			]

		self.ThirdNode_keyword["[Package Model]"] = [
			"[Alternate Package Models]"			
			]

		self.ThirdNode_keyword["[Interconnect Model Group]"] = [
			"[End Interconnect Model Group]"
			]
		
		self.ThirdNode_keyword["[Node Declarations]"] = [
			"[End Node Declarations]"
			]

		self.ThirdNode_keyword["[Circuit Call]"] = [
			"[End Circuit Call]"
			]

		self.ThirdNode_keyword["[Begin EMI Component]"] = [			
			"[Pin EMI]",
			"[Pin Domain EMI]",
			"[End EMI Component]"
			]

		self.ThirdNode_keyword["[Rising Waveform]"] = [
			"[Composite Current]"	
			]

		self.ThirdNode_keyword["[Falling Waveform]"] = [
			"[Composite Current]"	
			]

		self.ThirdNode_keyword["[External Model]"] = [
			"[End External Model]"
			]

		self.ThirdNode_keyword["[Algorithmic Model]"] = [
			"[End Algorithmic Model]"
			]
		
		self.ThirdNode_keyword["[Begin EMI Model]"] = [
			"[End EMI Model]"
			]

		self.ThirdNode_keyword["[Model Data]"] = [
			"[Resistance Matrix]",
			"[Inductance Matrix]",
			"[Capacitance Matrix]",
			"[End Model Data]"
			]

		self.ThirdNode_keyword["[Interconnect Model]"] = [
			"[End Interconnect Model]"
			]

		self.FourthNode_keyword["[Alternate Package Models]"] = [
			"[End Alternate Package Models]"
			]

		self.FourthNode_keyword["[Resistance Matrix]"] = [
			"[Bandwidth]",
			"[Row]"
			]

		self.FourthNode_keyword["[Inductance Matrix]"] = [
			"[Bandwidth]",
			"[Row]"
			]

		self.FourthNode_keyword["[Capacitance Matrix]"] = [
			"[Bandwidth]",
			"[Row]"
			]
	
		try:
			self._treeView1.Nodes.Clear()
			self._richTextBox1.Clear()
			self.DB = {}
			self.Line = {}
			self.Length = {}
			self.Key = {}

			self._treeView1.Nodes.Add(File.split('\\')[-1])

			iter = 0			
			self.DB["Text"] = []							
			with open(File) as fp:
				total_lines = sum(1 for line in fp)
			self._progressBar1.Maximum = total_lines
			fp.close()

			with open(File) as fp:
				for line in fp:
					if not line[0] == "|":
						if line.find('[') > 0:
							line = line.replace('[','(').replace(']',')')						
					self.DB["Text"].append(line)
					if line[0]=="|":
						self._richTextBox1.SelectionColor = Color.Green						
					else:
						self._richTextBox1.SelectionColor = Color.Black							
					self._richTextBox1.AppendText(line)
					iter += 1
					self._progressBar1.Value = iter					
			fp.close()
			
			self._treeView1.Nodes[0].Nodes.Add("[Header]")			
			Line_iter = 0
			index = 0
			self.Line["0"] = 0
			self.Length["0"] = 1
			self.Key["0"] = "Start"

			self.Line["0_0"] = 0
			self.Length["0_0"] = 1
			self.Key["0_0"] = "[Header]"
			while(1):
				line = self.DB["Text"][Line_iter]
				for key in self.SecondNode_keyword["[Header]"]:
					if line.lower().find(key.lower()) != -1:						
						self._treeView1.Nodes[0].Nodes[0].Nodes.Add(line)
						dic_key = "0_0" + "_" + str(index)
						self.Line[dic_key] = Line_iter
						self.Length[dic_key] = self.DB["Text"][Line_iter].Length
						self.Key[dic_key] = key
						index += 1
					
				if line.lower().find(self.TopNode_keyword[0].lower()) != -1:					
					break
				Line_iter += 1			

			Line_iter -= 1
			TopNode_index = 1
			SecondNode_index = 0
			ThirdNode_index = 0
			FourthNode_index = 0
			keyword = "junghyun"
			pre_keyword2 = "junghyun"
			pre_keyword3 = "junghyun"   
			flag = True				
			while(1):				
				# End of Line : Escape While				
				if keyword.lower() == "[end]":
					key1 = [s for s in self.TopNode_keyword if keyword.lower() in s.lower()]
					if not len(key1) == 0:
						self._treeView1.Nodes[0].Nodes.Add(self.DB["Text"][Line_iter])
						dic_key = "0_"+str(TopNode_index)
						self.Line[dic_key] = Line_iter
						self.Length[dic_key] = self.DB["Text"][Line_iter].Length
						self.Key[dic_key] = key1[0]
					break

				# Get Line Text until the text include "["
				if flag:
					keyword, Line_iter = Get_Keyword(Line_iter, self)						
					
				# Find First Node
				key1 = [s for s in self.TopNode_keyword if keyword.lower() in s.lower()]					
				if not len(key1) == 0:
					# ==================== Get Component Info. ====================
					if key1[0].lower() == "[component]":						
						self.IBIS["Component"] = self.DB["Text"][Line_iter].split(']')[-1].strip()						

					# ==================== Get Model Selector Info. ====================
					if key1[0].lower() == "[model selector]":
						temp = []
						init_idx = Line_iter
						while(1):
							Line_iter += 1
							if self.DB["Text"][Line_iter][0] != "|" and self.DB["Text"][Line_iter].strip() != "":
								if self.DB["Text"][Line_iter][0] == "[":									
									break
								else:									
									model = ' '.join(self.DB["Text"][Line_iter].split()).split(" ", 1)[0]
									note = ' '.join(self.DB["Text"][Line_iter].split()).split(" ", 1)[1]
									temp.append([model, note])						
						self.IBIS["Model Selector"][self.DB["Text"][init_idx].split(']')[-1].strip()] = temp
						Line_iter = init_idx
						
					# ==================== Get Model Info. ====================
					elif key1[0].lower() == "[model]":						
						self.IBIS["Model"]["Name"].append(self.DB["Text"][Line_iter].split(']')[-1].lstrip().rstrip())
						self.IBIS["Model"]["Type"].append(self.DB["Text"][Line_iter+1].split(' ')[-1].lstrip().rstrip())						

					self._treeView1.Nodes[0].Nodes.Add(self.DB["Text"][Line_iter])						
					dic_key = "0_" + str(TopNode_index)
					self.Line[dic_key] = Line_iter
					self.Length[dic_key] = self.DB["Text"][Line_iter].Length
					self.Key[dic_key] = key1[0]
					TopNode_index += 1
					SecondNode_index = 0

					temp_key = [s for s in self.SecondNode_keyword.keys() if key1[0].lower() in s.lower()]						
					if not len(temp_key) == 0:
						while(1):
							keyword, Line_iter = Get_Keyword(Line_iter, self)
							key2 = [s for s in self.SecondNode_keyword[temp_key[0]] if keyword.lower() in s.lower()]								
							if not len(key2) == 0:
								# ==================== Get Pin Info. ====================
								if key2[0].lower() == "[pin]":
									iter = 0
									while(1):
										iter += 1
										if self.DB["Text"][Line_iter+iter][0] == "[":
											break
										elif self.DB["Text"][Line_iter+iter].lstrip() == "" or self.DB["Text"][Line_iter+iter][0] == "|":
											pass
										else:
											self.IBIS["Pin"]["Name"].append(self.DB["Text"][Line_iter+iter].split()[0])
											self.IBIS["Pin"]["Signal_name"].append(self.DB["Text"][Line_iter+iter].split()[1])
											self.IBIS["Pin"]["Model_name"].append(self.DB["Text"][Line_iter+iter].split()[2])											
											
								# ==================== Get Diff Pin Info. ====================
								elif key2[0].lower() == "[diff pin]":
									iter = 0
									while(1):
										iter += 1
										if self.DB["Text"][Line_iter+iter][0] == "[":
											break
										elif self.DB["Text"][Line_iter+iter].lstrip() == "" or self.DB["Text"][Line_iter+iter][0] == "|":
											pass
										else:											
											self.IBIS["Diff_pin"]["Name"].append(self.DB["Text"][Line_iter+iter].split()[0] + " - " + self.DB["Text"][Line_iter+iter].split()[1])
											pos_index = self.IBIS["Pin"]["Name"].index(self.DB["Text"][Line_iter+iter].split()[0])
											neg_index = self.IBIS["Pin"]["Name"].index(self.DB["Text"][Line_iter+iter].split()[1])
											self.IBIS["Diff_pin"]["Signal_name"].append(self.IBIS["Pin"]["Signal_name"][pos_index] + " - " + self.IBIS["Pin"]["Signal_name"][neg_index])
											self.IBIS["Diff_pin"]["Model_name"].append(self.IBIS["Pin"]["Model_name"][pos_index] + " - " + self.IBIS["Pin"]["Model_name"][neg_index])											

								# ==================== Get AMI Info. ====================
								elif key2[0].lower() == "[algorithmic model]":									
									self.Algorithmic_model_flag = True
									iter = 0
									while(1):
										iter += 1
										if self.DB["Text"][Line_iter+iter][0] == "[":
											break
										elif self.DB["Text"][Line_iter+iter].lstrip() == "" or self.DB["Text"][Line_iter+iter][0] == "|":
											pass
										else:											
											self.IBIS["AMI"]["Ex"].append(self.DB["Text"][Line_iter+iter].split()[0])
											self.IBIS["AMI"]["OS"].append(self.DB["Text"][Line_iter+iter].split()[1].split("_")[0])
											self.IBIS["AMI"]["Compiler"].append(self.DB["Text"][Line_iter+iter].split()[1].split("_")[1])
											self.IBIS["AMI"]["Platform"].append(self.DB["Text"][Line_iter+iter].split()[1].split("_")[2])
											self.IBIS["AMI"]["Ex_file"].append(self.DB["Text"][Line_iter+iter].split()[2])
											self.IBIS["AMI"]["Para_file"].append(self.DB["Text"][Line_iter+iter].split()[3])
											
											ex_file_path = os.path.dirname(File) + "\\" + self.DB["Text"][Line_iter+iter].split()[2]
											para_file_path = os.path.dirname(File) + "\\" + self.DB["Text"][Line_iter+iter].split()[3]

											if not os.path.isfile(ex_file_path):
												MessageBox.Show("Please check the AMI executable model file \"" + self.DB["Text"][Line_iter+iter].split()[2] + "\"",
													"Executable model file(*.dll/*.so) is missed",MessageBoxButtons.OK, MessageBoxIcon.Error)
												self.AMI_flag = False
											if not os.path.isfile(para_file_path):
												MessageBox.Show("Please check the AMI parameter definition file \"" + self.DB["Text"][Line_iter+iter].split()[3] + "\"",
													"Control file(*.ami) is missed",MessageBoxButtons.OK, MessageBoxIcon.Error)
												self.AMI_flag = False

								pre_keyword2 = key2[0]
								self._treeView1.Nodes[0].Nodes[TopNode_index- 1].Nodes.Add(key2[0])
								dic_key = "0_" + str(TopNode_index-1) + "_" + str(SecondNode_index)									
								self.Line[dic_key] = Line_iter
								self.Length[dic_key] = self.DB["Text"][Line_iter].Length
								self.Key[dic_key] = key2[0]
								SecondNode_index += 1
								ThirdNode_index = 0
							else:
								temp_key2 = [s for s in self.ThirdNode_keyword.keys() if pre_keyword2 in s]
								if not len(temp_key2) == 0:
									key3 = [s for s in self.ThirdNode_keyword[pre_keyword2] if keyword.lower() in s.lower()]										
									if not len(key3) == 0:
										pre_keyword3 = key3[0]
										self._treeView1.Nodes[0].Nodes[TopNode_index- 1].Nodes[SecondNode_index-1].Nodes.Add(key3[0])
										dic_key = "0_" + str(TopNode_index-1) + "_" + str(SecondNode_index-1) + "_" + str(ThirdNode_index)
										self.Line[dic_key] = Line_iter
										self.Length[dic_key] = self.DB["Text"][Line_iter].Length
										self.Key[dic_key] = key3[0]
										ThirdNode_index += 1
										FourthNode_index = 0
									else:
										temp_key3 = [s for s in self.FourthNode_keyword.keys() if pre_keyword3 in s]
										if not len(temp_key3) == 0:
											key4 = [s for s in self.FourthNode_keyword[pre_keyword3] if keyword.lower() in s.lower()]
											if not len(key4) == 0:
												self._treeView1.Nodes[0].Nodes[TopNode_index-1].Nodes[SecondNode_index-1].Nodes[ThirdNode_index-1].Nodes.Add(key4[0])
												dic_key = "0_" + str(TopNode_index-1) + "_" + str(SecondNode_index-1) + "_" + str(ThirdNode_index-1) + "_" + str(FourthNode_index)
												self.Line[dic_key] = Line_iter
												self.Length[dic_key] = self.DB["Text"][Line_iter].Length
												self.Key[dic_key] = key4[0]
												FourthNode_index += 1
											else:
												flag = False
												break
										else:
											flag = False
											break
								else:
									flag = False
									break
					else:
						flag = True

			self._treeView1.Nodes[0].Expand()
			if Flag:
				sub_DB.IBIS_Tx = self.IBIS
			else:
				sub_DB.IBIS_Rx = self.IBIS			

		except Exception as e:	
			print traceback.format_exc()
			self._treeView1.Nodes[0].Expand()
			MessageBox.Show("Fail to completely generate IBIS Keyword Tree.\nPlease check the keword " + keyword, "IBIS Information",
			    MessageBoxButtons.OK, MessageBoxIcon.Error)

		#if self.AMI_flag and self.Algorithmic_model_flag:
		#	self.AMI_flag = True
		#else:
		#	self.AMI_flag = False

		#if not self.Algorithmic_model_flag:
		#	if Flag:
		#		TxRx = "Tx"
		#	else:
		#		TxRx = "Rx"
		#	MessageBox.Show("Imported " + TxRx + " IBIS Model does not have \"[Algorithmic Model]\"\nPlease Check the AMI Model", "IBIS AMI Information",
		#	    MessageBoxButtons.OK, MessageBoxIcon.Error)
		pass

	def MainFormResizeEnd(self, sender, e):				
		# Get previous Eye_Form width/height and resized Eye_Form width/height
		# Calculate Gap betweent previous and resized width/height		
		Gap_W = self.Size.Width - self.FormSize_W
		Gap_H = self.Size.Height - self.FormSize_H

		# Backup the resized Eye_Form width/height as previous MainFomr width/height
		self.FormSize_W = self.Size.Width
		self.FormSize_H = self.Size.Height

		# Resize
		self._treeView1.Size = System.Drawing.Size(self._treeView1.Width + Gap_W/2, self._treeView1.Height + Gap_H)
		self._richTextBox1.Size = System.Drawing.Size(self._richTextBox1.Width + Gap_W/2, self._richTextBox1.Height + Gap_H)
		self._progressBar1.Size = System.Drawing.Size(self._progressBar1.Width + Gap_W, self._progressBar1.Height)

		# Relocate
		self._richTextBox1.Location = System.Drawing.Point(self._richTextBox1.Location.X + Gap_W/2, self._richTextBox1.Location.Y)
		self._progressBar1.Location = System.Drawing.Point(self._progressBar1.Location.X, self._progressBar1.Location.Y + Gap_H)
		self._button1.Location = System.Drawing.Point(self._button1.Location.X + Gap_W, self._button1.Location.Y + Gap_H)
		
	def TreeView1NodeMouseClick(self, sender, e):
		key = str(e.Node.Index)
		temp_Node = e.Node
		while(temp_Node.Parent != None):			
			key = str(temp_Node.Parent.Index) + "_" + key
			temp_Node = temp_Node.Parent
		
		if key != "0_0":
			HighLight_IBIS(self, key)

	def ExpandAllToolStripMenuItemClick(self, sender, e):

		self._treeView1.ExpandAll()

	def CollapseAllToolStripMenuItemClick(self, sender, e):
		self._treeView1.CollapseAll()
		self._treeView1.Nodes[0].Expand()

	def Button1Click(self, sender, e):		

		self.Close()

	def AMI_ListView_ModelSpecSelectedIndexChanged(self, sender, e):

		pass

class IBIS_Case(Form):
	def __init__(self):

		self.InitializeComponent()

	def InitializeComponent(self):
		path = os.path.dirname(os.path.abspath(__file__))

		self._DataGridView = System.Windows.Forms.DataGridView()
		self._Col_CaseNum = System.Windows.Forms.DataGridViewTextBoxColumn()
		self._Col_Tx_IBIS_Model = System.Windows.Forms.DataGridViewComboBoxColumn()
		self._Col_Rx_IBIS_Model = System.Windows.Forms.DataGridViewComboBoxColumn()
		
		self._Col_Results = System.Windows.Forms.DataGridViewButtonColumn()
		self._Col_Avg_Width = System.Windows.Forms.DataGridViewTextBoxColumn()
		self._Col_Avg_Margin = System.Windows.Forms.DataGridViewTextBoxColumn()
		self._Col_Worst_Width = System.Windows.Forms.DataGridViewTextBoxColumn()
		self._Col_Worst_Margin = System.Windows.Forms.DataGridViewTextBoxColumn()
		self._Col_Vref = System.Windows.Forms.DataGridViewTextBoxColumn()

		self._Button_Add = System.Windows.Forms.Button()
		self._Button_Delete = System.Windows.Forms.Button()
		self._Button_Close = System.Windows.Forms.Button()

		self.SuspendLayout()
		# 
		# DataGridView
		# 
		self._DataGridView.AllowUserToAddRows = False
		self._DataGridView.AllowUserToDeleteRows = False
		self._DataGridView.AllowUserToOrderColumns = True
		self._DataGridView.AllowUserToResizeRows = False
		self._DataGridView.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.AllCells
		self._DataGridView.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize
		self._DataGridView.Columns.AddRange(System.Array[System.Windows.Forms.DataGridViewColumn](
			[self._Col_CaseNum,
			self._Col_Tx_IBIS_Model,
			self._Col_Rx_IBIS_Model]))
		self._DataGridView.EditMode = System.Windows.Forms.DataGridViewEditMode.EditOnF2
		self._DataGridView.Location = System.Drawing.Point(12, 12)
		self._DataGridView.Name = "DataGridView"
		self._DataGridView.RowHeadersVisible = False
		self._DataGridView.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect
		self._DataGridView.Size = System.Drawing.Size(259, 300)
		self._DataGridView.TabIndex = 36
		self._DataGridView.CellMouseClick += self.DataGridViewCellMouseClick
		# 
		# Col_CaseNum
		# 
		self._Col_CaseNum.HeaderText = "#"
		self._Col_CaseNum.Name = "Col_CaseNum"
		self._Col_CaseNum.Width = 26
		# 
		# Col_Tx_IBIS_Model
		# 
		self._Col_Tx_IBIS_Model.HeaderText = "Tx IBIS Model"
		self._Col_Tx_IBIS_Model.Name = "Col_Tx_IBIS_Model"
		self._Col_Tx_IBIS_Model.Width = 130		
		for row in sub_DB.IBIS_Form._DataGridView_Tx.Rows:			
			#if row.Cells[0].Value:				
			#	self._Col_Tx_IBIS_Model.Items.Add(row.Cells[1].Value)
			self._Col_Tx_IBIS_Model.Items.Add(row.Cells[1].Value)
		# 
		# Col_Rx_IBIS_Model
		#
		self._Col_Rx_IBIS_Model.HeaderText = "Rx IBIS Model"
		self._Col_Rx_IBIS_Model.Name = "Col_Rx_IBIS_Model"
		self._Col_Rx_IBIS_Model.Width = 130
		for row in sub_DB.IBIS_Form._DataGridView_Rx.Rows:
			#if row.Cells[0].Value:
			#	self._Col_Rx_IBIS_Model.Items.Add(row.Cells[1].Value)
			self._Col_Rx_IBIS_Model.Items.Add(row.Cells[1].Value)
		# 
		# Col_Results
		# 
		self._Col_Results.HeaderText = "Result"
		self._Col_Results.Name = "Col_Results"
		self._Col_Results.ReadOnly = True
		self._Col_Results.Text = "Result"
		self._Col_Results.UseColumnTextForButtonValue = True
		self._Col_Results.Width = 100
		self._Col_Results.DefaultCellStyle.Alignment = DataGridViewContentAlignment.MiddleCenter
		# 
		# Col_Avg_Width
		# 
		self._Col_Avg_Width.HeaderText = "Width(Avg.)"
		self._Col_Avg_Width.Name = "Col_Avg_Width"
		self._Col_Avg_Width.Width = 100
		# 
		# Col_Avg_Margin
		# 
		self._Col_Avg_Margin.HeaderText = "Margin(Avg.)"
		self._Col_Avg_Margin.Name = "Col_Avg_Margin"
		self._Col_Avg_Margin.Width = 100
		# 
		# Col_Worst_Width
		# 
		self._Col_Worst_Width.HeaderText = "Width(Worst)"
		self._Col_Worst_Width.Name = "Col_Worst_Width"
		self._Col_Worst_Width.Width = 100
		# 
		# Col_Worst_Margin
		# 
		self._Col_Worst_Margin.HeaderText = "Margin(Worst)"
		self._Col_Worst_Margin.Name = "Col_Worst_Margin"
		self._Col_Worst_Margin.Width = 100
		# 
		# Col_Vref
		# 
		self._Col_Vref.HeaderText = "Vref"
		self._Col_Vref.Name = "Col_Vref"
		self._Col_Vref.Width = 80
		# 
		# Button_Add
		# 
		self._Button_Add.Font = System.Drawing.Font("Arial", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_Add.Location = System.Drawing.Point(12, 320)
		self._Button_Add.Name = "Button_Add"
		self._Button_Add.Size = System.Drawing.Size(80, 25)
		self._Button_Add.TabIndex = 33
		self._Button_Add.Text = "Add"		
		self._Button_Add.UseVisualStyleBackColor = True
		self._Button_Add.Enabled = False
		self._Button_Add.Click += self.Button_AddClick
		# 
		# Button_Delete
		# 
		self._Button_Delete.Font = System.Drawing.Font("Arial", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_Delete.Location = System.Drawing.Point(102, 320)
		self._Button_Delete.Name = "Button_Delete"
		self._Button_Delete.Size = System.Drawing.Size(80, 25)
		self._Button_Delete.TabIndex = 33
		self._Button_Delete.Text = "Delete"		
		self._Button_Delete.UseVisualStyleBackColor = True
		self._Button_Delete.Enabled = False
		self._Button_Delete.Click += self.Button_DeleteClick
		# 
		# Button_Close
		# 
		self._Button_Close.Font = System.Drawing.Font("Arial", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_Close.Location = System.Drawing.Point(192, 320)
		self._Button_Close.Name = "Button_Close"
		self._Button_Close.Size = System.Drawing.Size(80, 25)
		self._Button_Close.TabIndex = 33
		self._Button_Close.Text = "Close"		
		self._Button_Close.UseVisualStyleBackColor = True
		self._Button_Close.Click += self.Button_CloseClick

		# 
		# IBIS_CaseForm
		#
		self.Size = System.Drawing.Size(300, 390)
		self.MinimumSize = System.Drawing.Size(300, 390)
		self.FormSize_W = self.Size.Width
		self.FormSize_H = self.Size.Height
		self.Controls.Add(self._Button_Close)
		self.Controls.Add(self._Button_Delete)
		self.Controls.Add(self._Button_Add)
		self.Controls.Add(self._DataGridView)
		IconFile = path + "\\Resources\\LOGO.ico"
		self.Icon = Icon(IconFile)
		self.StartPosition = System.Windows.Forms.FormStartPosition.Manual		
		self.Location = System.Drawing.Point(sub_DB.Eye_Form.Location.X + sub_DB.Eye_Form.Size.Width, sub_DB.Eye_Form.Location.Y)
		self.Name = "IBIS_CaseForm"
		self.Text = "IBIS Simulation Cases"
		self.Load += self.IBIS_CaseFormLoad
		self.ResizeEnd += self.IBIS_CaseFormResizeEnd
		self.DoubleClick += self.IBIS_CaseFormDoubleClick
		self.ResumeLayout(False)
		self.PerformLayout()

		self.case = 1		

	def IBIS_CaseFormLoad(self, sender, e):
		try:
			if sub_DB.IBIS_Result_Init_Flag:
				sub_DB.IBIS_Result_Init_Flag = False
				for tx_row in sub_DB.IBIS_Form._DataGridView_Tx.Rows:
					if tx_row.Cells[0].Value:
						for rx_row in sub_DB.IBIS_Form._DataGridView_Rx.Rows:
							if rx_row.Cells[0].Value:
								for tx_item in self._Col_Tx_IBIS_Model.Items:								
									if tx_item == tx_row.Cells[1].Value:									
										break

								for rx_item in self._Col_Rx_IBIS_Model.Items:
									if rx_item == rx_row.Cells[1].Value:									
										break

								self._DataGridView.Rows.Add(self.case, tx_item, rx_item)
								self.case += 1

		except Exception as e:			
			Log("[IBIS Result Form Load] = Failed")
			Log(traceback.format_exc())
			print traceback.format_exc()
			MessageBox.Show("Fail to load IBIS Result Form","Warning")
			EXIT()

	def IBIS_CaseFormResizeEnd(self, sender, e):
		try:
			# Get previous Eye_Form width/height and resized Eye_Form width/height
			# Calculate Gap betweent previous and resized width/height		
			Gap_W = self.Size.Width - self.FormSize_W
			Gap_H = self.Size.Height - self.FormSize_H
			
			# Backup the resized Eye_Form width/height as previous MainFomr width/height
			self.FormSize_W = self.Size.Width
			self.FormSize_H = self.Size.Height

			# Resize
			self._DataGridView.Size = System.Drawing.Size(self._DataGridView.Width + Gap_W, self._DataGridView.Height + Gap_H)
			
			# Relocate			
			self._Button_Add.Location = System.Drawing.Point(self._Button_Add.Location.X, self._Button_Add.Location.Y + Gap_H)
			self._Button_Delete.Location = System.Drawing.Point(self._Button_Delete.Location.X, self._Button_Delete.Location.Y + Gap_H)
			self._Button_Close.Location = System.Drawing.Point(self._Button_Close.Location.X, self._Button_Close.Location.Y + Gap_H)

		except Exception as e:			
			Log("[IBIS_CaseFormResizeEnd] = Failed")
			Log(traceback.format_exc())
			print traceback.format_exc()
			MessageBox.Show("Fail to resize Eye Analyzer IBIS Result GUI","Warning")			
			EXIT()

	def IBIS_CaseFormDoubleClick(self, sender, e):		
		self._DataGridView.Size = System.Drawing.Size(259, 300)		
		self._Col_CaseNum.Width = 26		
		self._Col_Tx_IBIS_Model.Width = 130				
		self._Col_Rx_IBIS_Model.Width = 130		
		self._Button_Add.Location = System.Drawing.Point(12, 320)
		self._Button_Add.Size = System.Drawing.Size(80, 25)
		self._Button_Delete.Location = System.Drawing.Point(102, 320)
		self._Button_Delete.Size = System.Drawing.Size(80, 25)
		self._Button_Close.Location = System.Drawing.Point(192, 320)
		self._Button_Close.Size = System.Drawing.Size(80, 25)
		self.Size = System.Drawing.Size(300, 390)
		self.MinimumSize = System.Drawing.Size(300, 390)
		self.FormSize_W = self.Size.Width
		self.FormSize_H = self.Size.Height

	def DataGridViewCellMouseClick(self, sender, e):
		for row in self._DataGridView.Rows:
			if row.Selected:
				self._Button_Delete.Enabled = False
				break
			else:
				self._Button_Delete.Enabled = False

	def Button_AddClick(self, sender, e):
		self._DataGridView.Rows.Add(self.case, "", "")
		self.case += 1
		self.Refresh()

	def Button_DeleteClick(self, sender, e):
		try:
			#for row in self._DataGridView.Rows:			
			#	if row.Selected:
			#		self._DataGridView.Rows.Remove(row)
			for i in range(0, self._DataGridView.Rows.Count-1):
				if self._DataGridView.Rows[i].Selected:
					self._DataGridView.Rows.Remove(self._DataGridView.Rows[i])
					#i -= 1

			self.Refresh()

		except Exception as e:						
			print traceback.format_exc()			

	def Button_CloseClick(self, sender, e):

		self.Close()


def HighLight_IBIS(self, key):
	for temp_key in self.Line:
		self._richTextBox1.Select(self._richTextBox1.GetFirstCharIndexFromLine(self.Line[temp_key]), self.Length[temp_key])
		self._richTextBox1.SelectionColor = Color.Black
		self._richTextBox1.SelectionFont = Font("Arial", 9)
	
	self._richTextBox1.Select(self._richTextBox1.GetFirstCharIndexFromLine(self.Line[key]), self.Length[key])
	self._richTextBox1.Focus()
	self._richTextBox1.SelectionColor = Color.Blue
	self._richTextBox1.SelectionFont = Font("Arial", 12, FontStyle.Bold)
		
def Get_Keyword(Line_iter, self):
	while(1):
		Line_iter += 1					
		line = self.DB["Text"][Line_iter]		
		if line.find("[") == 0:
			keyword = "[" + line.replace("_"," ").split("[")[1].split("]")[0] + "]"
			break

	return keyword, Line_iter