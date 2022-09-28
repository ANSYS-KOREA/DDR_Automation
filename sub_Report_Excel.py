#coding: utf8
import clr

clr.AddReference('Microsoft.Office.Interop.Excel')

from Microsoft.Office.Interop import Excel
from sub_functions import *

def Create_Excel_Report():
	try:
		xlApp = Excel.ApplicationClass()
		Report_Name = ""
		for item in sub_DB.Eye_Form._CheckedListBox_ReportName.CheckedItems:			
			Report_Name += item + ""

		xlApp.Caption = sub_DB.Eye_Form._ComboBox_Design.Text + " : " + Report_Name
		xlApp.Visible = True
		xlApp.DisplayAlerts = False	

		xlbook = xlApp.Workbooks.Add()
	
		# Create Eye Diagram Image Report Worksheet
		xlsheet = xlbook.Worksheets['Sheet1']
		xlsheet.Name = "EYE Diagrams"
		Log("		(Launch Excel) = Done")

		#Save_File = sub_DB.Option_Form._TextBox_OutputExcelFile.Text

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
		xlsheet_table.Cells[1,4] = "Timing Margin [ps]"
		xlsheet_table.Cells[1,5] = "Width [%]"
		xlsheet_table.Cells[1,6] = "Timing Margin [%]"
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
				xlsheet_table.Cells[row_idx,3] = sub_DB.Eye_Measure_Results[net_name][0]							# Width [ps]				
				xlsheet_table.Cells[row_idx,4] = sub_DB.Eye_Measure_Results[net_name][2]							# Margin [ps]
				xlsheet_table.Cells[row_idx,5] = round((sub_DB.Eye_Measure_Results[net_name][0]/sub_DB.UI)*100, 1)	# Width [%]
				xlsheet_table.Cells[row_idx,6] = round((sub_DB.Eye_Measure_Results[net_name][2]/sub_DB.UI)*100, 1)	# Margin [%]
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
		#xlbook.SaveAs(Save_File)
		#xlbook.Close()
		#xlApp.Quit()
		xlApp.DisplayAlerts = True
		ReleaseObject(Col_Header)
		ReleaseObject(Row_Header)
		ReleaseObject(Data_Cell)
		ReleaseObject(Merge_Cell)
		ReleaseObject(xlsheet)
		ReleaseObject(xlsheet_table)
		ReleaseObject(xlbook)
		ReleaseObject(xlApp)

		#Log("		(File Save) = Done, %s" % Save_File)

	except Exception as e:		
		Log("	<Create Excel Report> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to create excel report","Warning")						
		EXIT()

def Create_Excel_Report_wo_fig():
	try:
		xlApp = Excel.ApplicationClass()
		Report_Name = ""
		for item in sub_DB.Eye_Form._CheckedListBox_ReportName.CheckedItems:			
			Report_Name += item + ""

		xlApp.Caption = sub_DB.Eye_Form._ComboBox_Design.Text + " : " + Report_Name
		xlApp.Visible = True
		xlApp.DisplayAlerts = False	

		xlbook = xlApp.Workbooks.Add()
	
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
		xlsheet_table.Cells[1,4] = "Timing Margin [ps]"
		xlsheet_table.Cells[1,5] = "Width [%]"		
		xlsheet_table.Cells[1,6] = "Timing Margin [%]"
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
				xlsheet_table.Cells[row_idx,3] = sub_DB.Eye_Measure_Results[net_name][0]							# Width [ps]				
				xlsheet_table.Cells[row_idx,4] = sub_DB.Eye_Measure_Results[net_name][2]							# Margin [ps]
				xlsheet_table.Cells[row_idx,5] = round((sub_DB.Eye_Measure_Results[net_name][0]/sub_DB.UI)*100, 1)	# Width [%]
				xlsheet_table.Cells[row_idx,6] = round((sub_DB.Eye_Measure_Results[net_name][2]/sub_DB.UI)*100, 1)	# Margin [%]
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
		#xlbook.SaveAs(Save_File)
		#xlbook.Close()
		#xlApp.Quit()
		xlApp.DisplayAlerts = True
		ReleaseObject(Col_Header)
		ReleaseObject(Row_Header)
		ReleaseObject(Data_Cell)
		ReleaseObject(Merge_Cell)
		ReleaseObject(xlsheet_table)
		ReleaseObject(xlbook)
		ReleaseObject(xlApp)

		#Log("		(File Save) = Done, %s" % Save_File)

	except Exception as e:		
		Log("	<Create Excel Report> = Failed")
		Log(traceback.format_exc())
		print traceback.format_exc()
		MessageBox.Show("Fail to create excel report","Warning")						
		EXIT()

def Create_Excel_Report_Imported():
	try:
		xlApp = Excel.ApplicationClass()
		xlApp.Caption = sub_DB.Eye_Form._ComboBox_Design.Text + " : " + Report_Name
		xlApp.Visible = True
		xlApp.DisplayAlerts = False	
		xlbook = xlApp.Workbooks.Add()
		
		# Create Eye Diagram Image Report Worksheet
		xlsheet = xlbook.Worksheets['Sheet1']
		xlsheet.Name = "EYE Diagrams"
		Log("		(Launch Excel) = Done")
	
		#Save_File = sub_DB.Option_Form._TextBox_OutputExcelFile.Text

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
		xlsheet_table.Cells[1,4] = "Timing Margin [ps]"
		xlsheet_table.Cells[1,5] = "Width [%]"
		xlsheet_table.Cells[1,6] = "Timing Margin [%]"
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
				xlsheet_table.Cells[row_idx,3] = sub_DB.Eye_Measure_Results[net_name][0]							# Width [ps]				
				xlsheet_table.Cells[row_idx,4] = sub_DB.Eye_Measure_Results[net_name][2]							# Margin [ps]
				xlsheet_table.Cells[row_idx,5] = round((sub_DB.Eye_Measure_Results[net_name][0]/sub_DB.UI)*100, 1)	# Width [%]
				xlsheet_table.Cells[row_idx,6] = round((sub_DB.Eye_Measure_Results[net_name][2]/sub_DB.UI)*100, 1)	# Margin [%]
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
		#xlbook.SaveAs(Save_File)
		#xlbook.Close()
		#xlApp.Quit()
		xlApp.DisplayAlerts = True
		ReleaseObject(Col_Header)
		ReleaseObject(Row_Header)
		ReleaseObject(Data_Cell)
		ReleaseObject(Merge_Cell)
		ReleaseObject(xlsheet)
		ReleaseObject(xlsheet_table)
		ReleaseObject(xlbook)
		ReleaseObject(xlApp)

		#Log("		(File Save) = Done, %s" % Save_File)

	except Exception as e:		
		Log("	<Create Excel Report> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to create excel report","Warning")						
		EXIT()

def Create_Excel_Report_Imported_wo_fig():
	try:
		xlApp = Excel.ApplicationClass()		
		xlApp.Caption = sub_DB.Eye_Form._ComboBox_Design.Text + " : " + Report_Name
		xlApp.Visible = True
		xlApp.DisplayAlerts = False	
		xlbook = xlApp.Workbooks.Add()
		
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
		xlsheet_table.Cells[1,4] = "Timing Margin [ps]"
		xlsheet_table.Cells[1,5] = "Width [%]"		
		xlsheet_table.Cells[1,6] = "Timing Margin [%]"
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
				xlsheet_table.Cells[row_idx,3] = sub_DB.Eye_Measure_Results[net_name][0]							# Width [ps]				
				xlsheet_table.Cells[row_idx,4] = sub_DB.Eye_Measure_Results[net_name][2]							# Margin [ps]
				xlsheet_table.Cells[row_idx,5] = round((sub_DB.Eye_Measure_Results[net_name][0]/sub_DB.UI)*100, 1)	# Width [%]
				xlsheet_table.Cells[row_idx,6] = round((sub_DB.Eye_Measure_Results[net_name][2]/sub_DB.UI)*100, 1)	# Margin [%]
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
		#xlbook.SaveAs(Save_File)
		#xlbook.Close()
		#xlApp.Quit()
		xlApp.DisplayAlerts = True
		ReleaseObject(Col_Header)
		ReleaseObject(Row_Header)
		ReleaseObject(Data_Cell)
		ReleaseObject(Merge_Cell)		
		ReleaseObject(xlsheet_table)
		ReleaseObject(xlbook)
		ReleaseObject(xlApp)

		#Log("		(File Save) = Done, %s" % Save_File)

	except Exception as e:		
		Log("	<Create Excel Report> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to create excel report","Warning")						
		EXIT()

def Create_Setup_Hold_Excel_Report():
	try:
		xlApp = Excel.ApplicationClass()
		Report_Name = ""
		for item in sub_DB.Eye_Form._CheckedListBox_ReportName.CheckedItems:			
			Report_Name += item + ""

		xlApp.Caption = sub_DB.File.split("\\")[-1].split(".")[0] + " : " + RReport_Name
		xlApp.Visible = True
		xlApp.DisplayAlerts = False	

		xlbook = xlApp.Workbooks.Add()
	
		# Create Eye Diagram Image Report Worksheet
		xlsheet = xlbook.Worksheets['Sheet1']
		xlsheet.Name = "EYE Diagrams"
		Log("		(Launch Excel) = Done")

		#Save_File = sub_DB.Option_Form._TextBox_OutputExcelFile.Text

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
		xlsheet_table.Cells[1,6] = "Timing Margin [ps]"
		xlsheet_table.Cells[1,7] = "Setup Time [ps]"
		xlsheet_table.Cells[1,8] = "Hold Time [ps]"
		xlsheet_table.Cells[1,9] = "Vcent_DQ [mV]"
		Log("		(Create Column) = Done")

		# Create Column Range
		Col_Header = xlsheet_table.Range[xlsheet_table.Cells[1, 1], xlsheet_table.Cells[1, 9]]

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
				#xlsheet_table.Cells[row_idx,4] = round(sub_DB.Jitter_RMS[net_name], 1) # Jitter_RMS
				xlsheet_table.Cells[row_idx,4] = "N/A"
				xlsheet_table.Cells[row_idx,5] = sub_DB.Eye_Measure_Results[net_name][1] # Jitter
				xlsheet_table.Cells[row_idx,6] = sub_DB.Eye_Measure_Results[net_name][2] # Margin
				xlsheet_table.Cells[row_idx,7] = sub_DB.Setup[net_name] # Setup
				xlsheet_table.Cells[row_idx,8] = sub_DB.Hold[net_name] # Hold
				xlsheet_table.Cells[row_idx,9] = round(sub_DB.Vref, 1) # Vref
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
		Merge_Cell = xlsheet_table.Range[xlsheet_table.Cells[2, 9], xlsheet_table.Cells[row_idx, 9]]
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
		Data_Cell = xlsheet_table.Range[xlsheet_table.Cells[2, 2], xlsheet_table.Cells[row_idx, 9]]
		Data_Cell.Borders.LineStyle = Excel.XlLineStyle.xlContinuous
		Data_Cell.Borders.Weight = Excel.XlBorderWeight.xlThin

		# Auto Fit
		xlsheet_table.Range[xlsheet_table.Cells[1, 1], xlsheet_table.Cells[2, 9]].Columns.AutoFit()
		Log("		(Column Width AutoFit) = Done")
	
		# Save and Release
		#xlbook.SaveAs(Save_File)
		#xlbook.Close()
		#xlApp.Quit()
		xlApp.DisplayAlerts = True
		ReleaseObject(Col_Header)
		ReleaseObject(Row_Header)
		ReleaseObject(Data_Cell)
		ReleaseObject(Merge_Cell)
		ReleaseObject(xlsheet)
		ReleaseObject(xlsheet_table)
		ReleaseObject(xlbook)
		ReleaseObject(xlApp)

		#Log("		(File Save) = Done, %s" % Save_File)

	except Exception as e:		
		Log("	<Create Excel Report> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to create excel report","Warning")						
		EXIT()

def Create_Setup_Hold_Excel_Report_wo_fig():
	try:
		xlApp = Excel.ApplicationClass()
		Report_Name = ""
		for item in sub_DB.Eye_Form._CheckedListBox_ReportName.CheckedItems:			
			Report_Name += item + ""

		xlApp.Caption = sub_DB.File.split("\\")[-1].split(".")[0] + " : " + Report_Name
		xlApp.Visible = True
		xlApp.DisplayAlerts = False	

		xlbook = xlApp.Workbooks.Add()
	
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
		xlsheet_table.Cells[1,6] = "Timing Margin [ps]"
		xlsheet_table.Cells[1,7] = "Setup Time [ps]"
		xlsheet_table.Cells[1,8] = "Hold Time [ps]"
		xlsheet_table.Cells[1,9] = "Vcent_DQ [mV]"
		Log("		(Create Column) = Done")

		# Create Column Range
		Col_Header = xlsheet_table.Range[xlsheet_table.Cells[1, 1], xlsheet_table.Cells[1, 9]]

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
				#xlsheet_table.Cells[row_idx,4] = round(sub_DB.Jitter_RMS[net_name], 1) # Jitter_RMS
				xlsheet_table.Cells[row_idx,4] = "N/A"
				xlsheet_table.Cells[row_idx,5] = sub_DB.Eye_Measure_Results[net_name][1] # Jitter
				xlsheet_table.Cells[row_idx,6] = sub_DB.Eye_Measure_Results[net_name][2] # Margin
				xlsheet_table.Cells[row_idx,7] = sub_DB.Setup[net_name] # Setup
				xlsheet_table.Cells[row_idx,8] = sub_DB.Hold[net_name] # Hold
				xlsheet_table.Cells[row_idx,9] = round(sub_DB.Vref, 1) # Vref
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
		Merge_Cell = xlsheet_table.Range[xlsheet_table.Cells[2, 9], xlsheet_table.Cells[row_idx, 9]]
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
		Data_Cell = xlsheet_table.Range[xlsheet_table.Cells[2, 2], xlsheet_table.Cells[row_idx, 9]]
		Data_Cell.Borders.LineStyle = Excel.XlLineStyle.xlContinuous
		Data_Cell.Borders.Weight = Excel.XlBorderWeight.xlThin

		# Auto Fit
		xlsheet_table.Range[xlsheet_table.Cells[1, 1], xlsheet_table.Cells[2, 9]].Columns.AutoFit()
		Log("		(Column Width AutoFit) = Done")
	
		# Save and Release
		#xlbook.SaveAs(Save_File)
		#xlbook.Close()
		#xlApp.Quit()
		xlApp.DisplayAlerts = True
		ReleaseObject(Col_Header)
		ReleaseObject(Row_Header)
		ReleaseObject(Data_Cell)
		ReleaseObject(Merge_Cell)
		ReleaseObject(xlsheet_table)
		ReleaseObject(xlbook)
		ReleaseObject(xlApp)

		#Log("		(File Save) = Done, %s" % Save_File)

	except Exception as e:		
		Log("	<Create Excel Report> = Failed")
		Log(traceback.format_exc())
		MessageBox.Show("Fail to create excel report","Warning")						
		EXIT()
