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
from System.Drawing import *
from System.Windows.Forms import *

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
		self.MinimumSize = System.Drawing.Size(self.Size.Width, self.Size.Height)
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
		self._Label_GroupName = System.Windows.Forms.Label()
		self._Label_H_Border1 = System.Windows.Forms.Label()
		self._ComboBox_AnalyzeGroup = System.Windows.Forms.ComboBox()
		self._Button_Update = System.Windows.Forms.Button()
		self._Button_Auto = System.Windows.Forms.Button()
		self._Button_EditRule = System.Windows.Forms.Button()		
		self._Button_Identify = System.Windows.Forms.Button()
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
		self._DataGridView.Size = System.Drawing.Size(456, 777)
		self._DataGridView.TabIndex = 36
		self._DataGridView.Columns[1].ReadOnly = True
		self._DataGridView.Columns[3].ReadOnly = True
		self._DataGridView.KeyPress += self.DataGridViewKeyPress
		self._DataGridView.ColumnHeaderMouseClick += self.DataGridViewColumnHeaderMouseClick
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
		self._Col_Group.Items.AddRange(System.Array[System.Object](["DM","DQ","DQS","CLK","ADDR","OTHER"]))
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
		self._Col_Width.HeaderText = "Eye Width [ps]"
		self._Col_Width.Name = "Eye_Width"
		self._Col_Width.Width = 101
		# 
		# Col_Margin
		# 
		self._Col_Margin.HeaderText = "Timing Margin [ps]"
		self._Col_Margin.Name = "Eye_Margin"
		self._Col_Margin.Width = 118
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
		self._Label_H_Border1.Size = System.Drawing.Size(456, 2)
		self._Label_H_Border1.TabIndex = 39
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
		self._Button_Auto.Location = System.Drawing.Point(327, 799)
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
		# Button_Close
		# 
		self._Button_Close.Font = System.Drawing.Font("Arial", 12, System.Drawing.FontStyle.Bold)
		self._Button_Close.Location = System.Drawing.Point(368, 837)
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
		self.MinimumSize = System.Drawing.Size(self.Size.Width, self.Size.Height)
		self.FormSize_W = self.Size.Width
		self.FormSize_H = self.Size.Height
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
			self._Label_H_Border1.Location = System.Drawing.Point(self._Label_H_Border1.Location.X, self._Label_H_Border1.Location.Y + Gap_H)
			self._ComboBox_AnalyzeGroup.Location = System.Drawing.Point(self._ComboBox_AnalyzeGroup.Location.X, self._ComboBox_AnalyzeGroup.Location.Y + Gap_H)
			self._Button_Update.Location = System.Drawing.Point(self._Button_Update.Location.X + Gap_W, self._Button_Update.Location.Y + Gap_H)
			self._Button_Auto.Location = System.Drawing.Point(self._Button_Auto.Location.X + Gap_W, self._Button_Auto.Location.Y + Gap_H)
			self._Button_EditRule.Location = System.Drawing.Point(self._Button_EditRule.Location.X + Gap_W, self._Button_EditRule.Location.Y + Gap_H)
			self._Button_Identify.Location = System.Drawing.Point(self._Button_Identify.Location.X + Gap_W, self._Button_Identify.Location.Y + Gap_H)
			self._Button_Close.Location = System.Drawing.Point(self._Button_Close.Location.X + Gap_W, self._Button_Close.Location.Y + Gap_H)

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
					oDesign = sub_DB.AEDT["Design"]
					oModule = oDesign.GetModule("ReportSetup")

					Report_Name = []
					Report_Name = sub_DB.Eye_Form._CheckedListBox_ReportName.CheckedItems
					Netlist = []
					for report in Report_Name:
						for net in oModule.GetReportTraceNames(report):							
							Netlist.append(net.replace("-","_"))

					sub_DB.Netlist = Netlist

				elif sub_DB.InputFile_Flag == 2: # for *.csv input
					# Netlist and Waveforms are loaded at file import process
					Netlist = sub_DB.Netlist
		
				# Net Identify			
				file = sub_DB.Uenv["File"]
				Uenv = Load_env(sub_DB.Uenv["File"])
				Uenv["File"] = file
				sub_DB.Uenv = Uenv

				# for New Eye
				if sub_DB.Eyeflag:
					self._DataGridView.Rows.Clear()
					LVitem_List = []
					iter = 0
					for net in Netlist:			
						Group_idx, Match = Net_Identify(net.strip(), sub_DB.Uenv) # Match = "Group prefix / Net Number prefix"
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
						for text in temp_list:
							val += ord(text)
						Name_idx.append(val)
					Name_idx = sorted(range(len(Name_idx)),key=lambda k: Name_idx[k], reverse=sub_DB.NetSort_Flag)

					# Clear row and add row as sorted sequentially
					self._DataGridView.Rows.Clear()
					for i in range(0, len(Name_idx)):
						self._DataGridView.Rows.Add(Backup_row[Name_idx[i]])
			
				# for Old Eye
				else:
					self._DataGridView.Rows.Clear()

			else:
				pass

			for row in self._DataGridView.Rows:
				if row.Cells[0].Value:
					row.DefaultCellStyle.BackColor = System.Drawing.SystemColors.Info
				else:
					row.DefaultCellStyle.BackColor = System.Drawing.SystemColors.Window

		except Exception as e:		
			Log("[Net Form Load] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to load Net Classification Form","Warning")			
			EXIT()

	def DataGridViewKeyPress(self, sender, e):
		try:
			# Spacebar = Check/Uncheck all the selected rows
			if e.KeyChar == chr(32):
				for row in self._DataGridView.SelectedRows:
					row.Cells[0].Value = not row.Cells[0].Value

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
					for text in temp_list:
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
		sub_DB.Env_Form = EnvEditor(sub_DB.Uenv["File"])
		sub_DB.Env_Form.ShowDialog()		

	def Button_IdentifyClick(self, sender, e):
		try:
			Uenv = {}
			File = sub_DB.Uenv["File"]
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
							Uenv[key+"[Net Identification]"] =  temp_data

						elif line.find("<DQ>") != -1:
							key="<DQ>"
							temp_data = []
							temp = line.strip().split("=")[-1].split(",")
							for cell in temp:
								if not cell == "":
									temp_data.append(cell.strip())
							Uenv[key+"[Net Identification]"] =  temp_data

						elif line.find("<DQS>") != -1:
							key="<DQS>"
							temp_data = []
							temp = line.strip().split("=")[-1].split(",")
							for cell in temp:
								if not cell == "":
									temp_data.append(cell.strip())
							Uenv[key+"[Net Identification]"] =  temp_data

						elif line.find("<CLK>") != -1:
							key="<CLK>"
							temp_data = []
							temp = line.strip().split("=")[-1].split(",")
							for cell in temp:
								if not cell == "":
									temp_data.append(cell.strip())
							Uenv[key+"[Net Identification]"] =  temp_data

						elif line.find("<ADDR>") != -1:
							key="<ADDR>"
							temp_data = []
							temp = line.strip().split("=")[-1].split(",")
							for cell in temp:
								if not cell == "":
									temp_data.append(cell.strip())
							Uenv[key+"[Net Identification]"] =  temp_data

						elif line.find("<Ignore>") != -1:
							key="<Ignore>"
							temp_data = []
							temp = line.strip().split("=")[-1].split(",")
							for cell in temp:
								if not cell == "":
									temp_data.append(cell.strip())
							Uenv[key+"[Net Identification]"] =  temp_data

			fp.close()
			self._DataGridView.Rows.Clear()
			sub_DB.Uenv = Uenv
			sub_DB.Uenv["File"] = File
			self.Text = "Target Net Setup - " + sub_DB.Uenv["File"].split("\\")[-1]

			if sub_DB.Eyeflag:
				LVitem_List = []
				iter = 0
				for net in sub_DB.Netlist:			
					Group_idx, Match = Net_Identify(net.strip(), sub_DB.Uenv)
					if Group_idx == 1: # for DQ Group -> Check
						self._DataGridView.Rows.Add(True, net, self._Col_Group.Items[Group_idx], Match, self._Col_AnalyzeGroup.Items[0])
					else: # Un-check
						self._DataGridView.Rows.Add(False, net, self._Col_Group.Items[Group_idx], Match, self._Col_AnalyzeGroup.Items[0])

				for row in self._DataGridView.Rows:
					if row.Cells[0].Value:
						row.DefaultCellStyle.BackColor = System.Drawing.SystemColors.Info

			else:
				pass

		except Exception as e:		
			Log("[Net Identify] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to identify target nets","Warning")			
			EXIT()

	def Button_CloseClick(self, sender, e):
		if sub_DB.Result_Flag:
			try:
				Log("	<Eye Analyze Results>")
				Log("		= Net Name, Eye Width[ps], Timing Margin[ps], Analyze Group, Signal Group, Matched String")
				for row in self._DataGridView.Rows:
					if row.Cells[0].Value:
						Log("		= %s, %s, %s, %s, %s, %s" % (row.Cells[1].Value, row.Cells[5].Value, row.Cells[6].Value, row.Cells[4].Value, row.Cells[2].Value, row.Cells[3].Value))

				sub_DB.Net_Form = self
				self.Close()

			except Exception as e:
				Log("	<Close Eye Analyze Results Form> = Failed")
				Log(traceback.format_exc())
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
		self._TreeView.Nodes.AddRange(System.Array[System.Windows.Forms.TreeNode](
			[TreeNode_EM,
			TreeNode_Tran,
			TreeNode_Eye]))
		self._TreeView.Size = System.Drawing.Size(232, 404)
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
		self._GroupBox_General.Text = "General Directories"
		# 
		# GroupBox_EM
		# 
		self._GroupBox_EM.Font = System.Drawing.Font("Arial", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._GroupBox_EM.Location = System.Drawing.Point(255, 141)
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
		self._GroupBox_Tran.Location = System.Drawing.Point(255, 141)
		self._GroupBox_Tran.Name = "GroupBox_Tran"
		self._GroupBox_Tran.Size = System.Drawing.Size(543, 275)
		self._GroupBox_Tran.TabIndex = 36
		self._GroupBox_Tran.TabStop = False
		self._GroupBox_Tran.Visible = False
		self._GroupBox_Tran.Text = "Circuit Simulator"
		# 
		# GroupBox_Eye
		#
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
		self._GroupBox_Eye.Controls.Add(self._Label_OutputExcelFile)
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
		self._GroupBox_Eye.Location = System.Drawing.Point(255, 141)
		self._GroupBox_Eye.Name = "GroupBox_Eye"
		self._GroupBox_Eye.Size = System.Drawing.Size(543, 275)
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
		self._Button_OutputExcelFile.Click += self.Button_OutputExcelFileClick
		# 
		# Button_Compliance
		# 
		self._Button_Compliance.Font = System.Drawing.Font("Arial", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._Button_Compliance.Location = System.Drawing.Point(404, 235)
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
		self._Button_OK.Location = System.Drawing.Point(652, 422)
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
		self._Button_Cancel.Location = System.Drawing.Point(728, 422)
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
		self._Label_TotalWaveform.Size = System.Drawing.Size(289, 28)
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
		self._Label_mV.Location = System.Drawing.Point(274, 72)
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
		self._Label_Analyze.Location = System.Drawing.Point(316, 72)
		self._Label_Analyze.Name = "Label_Analyze"
		self._Label_Analyze.Size = System.Drawing.Size(101, 28)
		self._Label_Analyze.TabIndex = 62
		self._Label_Analyze.Text = "Analyze Method :"
		self._Label_Analyze.TextAlign = System.Drawing.ContentAlignment.MiddleRight		
		# 
		# Label_ImageWidth
		# 
		self._Label_ImageWidth.Font = System.Drawing.Font("Arial", 9)
		self._Label_ImageWidth.Location = System.Drawing.Point(73, 152)
		self._Label_ImageWidth.Name = "Label_ImageWidth"
		self._Label_ImageWidth.Size = System.Drawing.Size(103, 28)
		self._Label_ImageWidth.TabIndex = 47
		self._Label_ImageWidth.Text = "Image Width :"
		self._Label_ImageWidth.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_ImageWidth_Unit
		# 
		self._Label_ImageWidth_Unit.Font = System.Drawing.Font("Arial", 9)
		self._Label_ImageWidth_Unit.Location = System.Drawing.Point(269, 152)
		self._Label_ImageWidth_Unit.Name = "Label_ImageWidth_Unit"
		self._Label_ImageWidth_Unit.Size = System.Drawing.Size(51, 28)
		self._Label_ImageWidth_Unit.TabIndex = 49
		self._Label_ImageWidth_Unit.Text = "[pixel]"
		self._Label_ImageWidth_Unit.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_ReportFormat
		# 		
		self._Label_ReportFormat.Font = System.Drawing.Font("Arial", 9)
		self._Label_ReportFormat.Location = System.Drawing.Point(326, 152)
		self._Label_ReportFormat.Name = "Label_ReportFormat"
		self._Label_ReportFormat.Size = System.Drawing.Size(95, 28)
		self._Label_ReportFormat.TabIndex = 66
		self._Label_ReportFormat.Text = "Report Format :"
		self._Label_ReportFormat.TextAlign = System.Drawing.ContentAlignment.MiddleLeft		
		# 
		# Label_OutputExcelFile
		# 
		self._Label_OutputExcelFile.Font = System.Drawing.Font("Arial", 9)
		self._Label_OutputExcelFile.Location = System.Drawing.Point(73, 186)
		self._Label_OutputExcelFile.Name = "Label_OutputExcelFile"
		self._Label_OutputExcelFile.Size = System.Drawing.Size(113, 28)
		self._Label_OutputExcelFile.TabIndex = 53
		self._Label_OutputExcelFile.Text = "Output Excel File :"
		self._Label_OutputExcelFile.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
		# 
		# Label_V_Border1
		# 
		self._Label_V_Border1.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
		self._Label_V_Border1.Location = System.Drawing.Point(22, 62)
		self._Label_V_Border1.Name = "Label_V_Border1"
		self._Label_V_Border1.Size = System.Drawing.Size(512, 2)
		self._Label_V_Border1.TabIndex = 56		
		# 
		# Label_V_Border2
		# 
		self._Label_V_Border2.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
		self._Label_V_Border2.Location = System.Drawing.Point(22, 112)
		self._Label_V_Border2.Name = "Label_V_Border2"
		self._Label_V_Border2.Size = System.Drawing.Size(512, 2)
		self._Label_V_Border2.TabIndex = 58
		# 
		# Label_V_Border3
		# 
		self._Label_V_Border3.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D
		self._Label_V_Border3.Location = System.Drawing.Point(22, 225)
		self._Label_V_Border3.Name = "Label_V_Border3"
		self._Label_V_Border3.Size = System.Drawing.Size(512, 2)
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
		self._ComboBox_Vref.Text = "Auto"
		self._ComboBox_Vref.SelectedIndexChanged += self.ComboBox_VrefSelectedIndexChanged
		# 
		# ComboBox_Analyze
		# 
		self._ComboBox_Analyze.FormattingEnabled = True
		self._ComboBox_Analyze.Items.AddRange(System.Array[System.Object](
			["Default"]))
		self._ComboBox_Analyze.Location = System.Drawing.Point(418, 76)
		self._ComboBox_Analyze.Name = "ComboBox_Analyze"
		self._ComboBox_Analyze.Size = System.Drawing.Size(74, 23)
		self._ComboBox_Analyze.TabIndex = 63
		self._ComboBox_Analyze.Text = "Default"
		# 
		# ComboBox_ReportFormat
		# 
		self._ComboBox_ReportFormat.FormattingEnabled = True
		self._ComboBox_ReportFormat.Items.AddRange(System.Array[System.Object](
			["Default"]))
		self._ComboBox_ReportFormat.Location = System.Drawing.Point(418, 156)
		self._ComboBox_ReportFormat.Name = "ComboBox_ReportFormat"
		self._ComboBox_ReportFormat.Size = System.Drawing.Size(74, 23)
		self._ComboBox_ReportFormat.TabIndex = 67
		self._ComboBox_ReportFormat.Text = "Default"
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
		self._TextBox_EyeOffset.Text = "5"
		self._TextBox_EyeOffset.TabIndex = 42
		# 
		# TextBox_Vref
		# 
		self._TextBox_Vref.BackColor = System.Drawing.SystemColors.Window
		self._TextBox_Vref.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_Vref.Location = System.Drawing.Point(203, 76)
		self._TextBox_Vref.Name = "TextBox_Vref"
		self._TextBox_Vref.Size = System.Drawing.Size(70, 23)
		self._TextBox_Vref.Visible = False
		self._TextBox_Vref.TabIndex = 64
		# 
		# TextBox_ImageWidth
		# 
		self._TextBox_ImageWidth.BackColor = System.Drawing.SystemColors.Window
		self._TextBox_ImageWidth.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_ImageWidth.Location = System.Drawing.Point(180, 155)
		self._TextBox_ImageWidth.Name = "TextBox_ImageWidth"
		self._TextBox_ImageWidth.Size = System.Drawing.Size(83, 23)
		self._TextBox_ImageWidth.Text = "200"
		self._TextBox_ImageWidth.TabIndex = 48
		# 
		# TextBox_OutputExcelFile
		# 
		self._TextBox_OutputExcelFile.BackColor = System.Drawing.SystemColors.Window
		self._TextBox_OutputExcelFile.Font = System.Drawing.Font("Arial", 10, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._TextBox_OutputExcelFile.Location = System.Drawing.Point(180, 189)
		self._TextBox_OutputExcelFile.Name = "TextBox_OutputExcelFile"
		self._TextBox_OutputExcelFile.Size = System.Drawing.Size(312, 23)
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
		self._CheckBox_PlotEye.Checked = True
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
		self._CheckBox_ExportExcelReport.Checked = True
		self._CheckBox_ExportExcelReport.UseVisualStyleBackColor = True
		self._CheckBox_ExportExcelReport.CheckedChanged += self.CheckBox_ExportExcelReportCheckedChanged
		# 
		# CheckBox_Compiance
		# 
		self._CheckBox_Compiance.Font = System.Drawing.Font("Arial", 9)
		self._CheckBox_Compiance.Location = System.Drawing.Point(240, 232)
		self._CheckBox_Compiance.Name = "CheckBox_Compiance"
		self._CheckBox_Compiance.Size = System.Drawing.Size(162, 29)
		self._CheckBox_Compiance.TabIndex = 68
		self._CheckBox_Compiance.Text = "Check DDR Compliance"
		self._CheckBox_Compiance.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		self._CheckBox_Compiance.UseVisualStyleBackColor = True
		self._CheckBox_Compiance.CheckedChanged += self.CheckBox_CompianceCheckedChanged
		# 
		# openFileDialog1
		# 
		self._openFileDialog1.FileName = "openFileDialog1"		
		# 
		# Option_Form
		# 
		self.ClientSize = System.Drawing.Size(805, 457)
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
			if process_idx == 0:
				self._GroupBox_EM.Visible = True
				self._GroupBox_Tran.Visible = False
				self._GroupBox_Eye.Visible = False
				#self._GroupBox_Comp.Visible = False
			elif process_idx == 1:
				self._GroupBox_EM.Visible = False
				self._GroupBox_Tran.Visible = True
				self._GroupBox_Eye.Visible = False
				#self._GroupBox_Comp.Visible = False
			elif process_idx == 2:
				self._GroupBox_EM.Visible = False
				self._GroupBox_Tran.Visible = False
				self._GroupBox_Eye.Visible = True
				#self._GroupBox_Comp.Visible = False
				self._TreeView.SelectedNode = self._TreeView.Nodes[2]
			#elif process_idx == 3:
			#	self._GroupBox_EM.Visible = False
			#	self._GroupBox_Tran.Visible = False
			#	self._GroupBox_Eye.Visible = False
			#	self._GroupBox_Comp.Visible = True

			if sub_DB.Debug_Mode:
				self._TextBox_EyeOffset.Text = "5"			
				self._CheckBox_PlotEye.Checked = True
				self._CheckBox_ExportExcelReport.Checked = True
				self._TextBox_ImageWidth.Text = "200"
				self._TextBox_OutputExcelFile.Text = "D:\\1_Work\\20220106_DDR_Compliance\\2_Results\\Test.xlsx"

		except Exception as e:			
			Log("[Option Form Load] = Failed")
			Log(traceback.format_exc())
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
		try:
			if e.Node.Level == 0:
				if e.Node.Index == 0: # for EM
					self._GroupBox_EM.Visible = True
					self._GroupBox_Tran.Visible = False
					self._GroupBox_Eye.Visible = False
					self._GroupBox_Comp.Visible = False
				elif e.Node.Index == 1: # for Tran
					self._GroupBox_EM.Visible = False
					self._GroupBox_Tran.Visible = True
					self._GroupBox_Eye.Visible = False
					self._GroupBox_Comp.Visible = False
				elif e.Node.Index == 2: # for Eye
					self._GroupBox_EM.Visible = False
					self._GroupBox_Tran.Visible = False
					self._GroupBox_Eye.Visible = True
					self._GroupBox_Comp.Visible = False
				elif e.Node.Index == 3: # for Comp
					self._GroupBox_EM.Visible = False
					self._GroupBox_Tran.Visible = False
					self._GroupBox_Eye.Visible = False
					self._GroupBox_Comp.Visible = True

		except Exception as e:			
			Log("[Option Form Treeview Node Mouse Click] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to Select node in Option Form","Warning")			
			EXIT()

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
			if not sender.Checked:
				if self._CheckBox_ExportExcelReport.Checked:
					if self._ComboBox_ReportFormat.Text.lower() == "default":
						MessageBox.Show("To generate an Excel report in format \"Default\", Eye-diagram has to be plotted.", "Warning", MessageBoxButtons.OK, MessageBoxIcon.Warning)
						sender.Checked = True

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
			elif sender.SelectedIndex == 1: # Manual Vref
				self._TextBox_Vref.Visible = True
				self._Label_mV.Visible = True			

		except Exception as e:			
			Log("[Vref Select] = Failed")
			Log(traceback.format_exc())
			MessageBox.Show("Fail to change Vref calculating method","Warning")			
			EXIT()

	def CheckBox_ExportExcelReportCheckedChanged(self, sender, e):
		try:
			self._TextBox_ImageWidth.Visible = sender.Checked
			self._TextBox_OutputExcelFile.Visible = sender.Checked
			self._Button_OutputExcelFile.Visible = sender.Checked
			self._Label_ImageWidth.Visible = sender.Checked
			self._Label_ImageWidth_Unit.Visible = sender.Checked
			self._Label_OutputExcelFile.Visible = sender.Checked
			self._Label_ReportFormat.Visible = sender.Checked
			self._ComboBox_ReportFormat.Visible = sender.Checked

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
		# TODO : Link Compliance Check Option and Previous Process
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
				elif self._TextBox_OutputExcelFile.Text == "":
					flag = False

			if not self._CheckBox_PlotEye.Checked:
				if self._CheckBox_ExportExcelReport.Checked:
					if self._ComboBox_ReportFormat.Text.lower() == "default":					
						MessageBox.Show("To generate an Excel report in format \"Default\", Eye-diagram has to be plotted.", "Warning", MessageBoxButtons.OK, MessageBoxIcon.Warning)
						self._CheckBox_PlotEye.Checked = True
						flag = False

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
		self._DataGridView.ColumnHeaderMouseClick += self.DataGridViewColumnHeaderMouseClick		
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
		self._Col_TestCheck.ReadOnly = True
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
		# ComplianceForm
		# 
		#self.Shownetflag = False
		self.Shownetflag = False
		self.ClientSize = System.Drawing.Size(1032, 912)		
		self.Controls.Add(self._Button_ShowHide)
		self.Controls.Add(self._Label_Vref_Timing)
		self.Controls.Add(self._Label_Diff_Timing)
		self.Controls.Add(self._Label_CLK_Timing)
		self.Controls.Add(self._Label_DQS_Timing)
		self.Controls.Add(self._Label_ADDR_Timing)
		self.Controls.Add(self._Label_DQ_Timing)
		self.Controls.Add(self._DataGridView)
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle
		IconFile = path + "\\Resources\\LOGO.ico"
		self.Icon = Icon(IconFile)
		self.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
		self.Name = "ComplianceForm"
		self.Text = "Setting for DDR Compliacne Check"		
		self.Load += self.ComplianceFormLoad
		self._DataGridView.EndInit()
		self._contextMenuStrip1.ResumeLayout(False)
		self.ResumeLayout(False)

	def ComplianceFormLoad(self, sender, e):
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
		self._DataGridView.Rows.Add(False, "tCH(avg)", "CLK", "N/A", "Average Clock High Pulse Width")
		self._DataGridView.Rows.Add(False, "tCL(avg)", "CLK", "N/A", "Average Clock Low Pulse Width")		
		self._DataGridView.Rows.Add(False, "tCK(abs)", "CLK", "N/A", "Absolute Clock Period")
		self._DataGridView.Rows.Add(False, "tCH(abs)", "CLK", "N/A", "Absolute Clock High Pulse Width")
		self._DataGridView.Rows.Add(False, "tCL(abs)", "CLK", "N/A", "Absolute Clock Low Pulse Width")		
		self._DataGridView.Rows.Add(False, "tJIT(per)", "CLK", "N/A", "Clock Period Jitter")
		self._DataGridView.Rows.Add(False, "tJIT(cc)", "CLK", "N/A", "Clock Cycle to Cycle Period Jitter")		
		#21
		self._DataGridView.Rows.Add(False, "tDVAC(DQS)", "DQS", "N/A", "Allowed Time Before Ringback for DQS")
		self._DataGridView.Rows.Add(False, "VSEH(DQS)", "DQS", "N/A", "Single-ended High Level for Strobes")
		self._DataGridView.Rows.Add(False, "VSEL(DQS)", "DQS", "N/A", "Single-ended Low Level for Strobes")
		self._DataGridView.Rows.Add(False, "VIX(DQS)", "DQS", "N/A", "Diff. Input Cross Point Voltage")
		self._DataGridView.Rows.Add(False, "tDVAC(CLK)", "CLK", "N/A", "Allowed Time Before Ringback for CLK")
		self._DataGridView.Rows.Add(False, "VSEH(CLK)", "CLK", "N/A", "Single-ended High Level for CLK")
		self._DataGridView.Rows.Add(False, "VSEL(CLK)", "CLK", "N/A", "Single-ended Low Level for CLK")
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

		#################################################################
		############## Set BackColor for Checked Rows ###################
		#################################################################
		for row in self._DataGridView.Rows:
			if row.Cells[0].Value:
				row.DefaultCellStyle.BackColor = System.Drawing.SystemColors.Info
			else:
				row.DefaultCellStyle.BackColor = System.Drawing.SystemColors.Window

		##################################################################################################
		############## Set Column Display and Reference & Target Net Column Unvisible  ###################
		##################################################################################################
		self._DataGridView.Columns[7].DisplayIndex = 5
		self._DataGridView.Columns[5].Visible = False
		self._DataGridView.Columns[6].Visible = False

		#######################################################################
		############## Set Size of DataGridView and Client  ###################
		#######################################################################
		#self._DataGridView.Rows[1].Cells[5].Items.Add("Test")
		#self._DataGridView.Rows[1].Cells[5].Value = self._DataGridView.Rows[1].Cells[5].Items[0]		

		self._DataGridView.Size = System.Drawing.Size(509, 675)
		self.ClientSize = System.Drawing.Size(529, 722)
		
	def DataGridViewColumnHeaderMouseClick(self, sender, e):
		# TODO : Compliance Option Form DataGridView Column Header Mouse Click
		pass
	
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