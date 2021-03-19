import openpyxl

wb=openpyxl.load_workbook('Panel_data.xlsx')

for sheet_name in wb.sheetnames:
    for col in wb[sheet_name].columns:
        max_length=0
        column=col[0].column
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2) * 1.5
        # col[0].column_letter為第幾行A、B、C...
        wb[sheet_name].column_dimensions[col[0].column_letter].width = adjusted_width

wb.save('Panel_data.xlsx')
