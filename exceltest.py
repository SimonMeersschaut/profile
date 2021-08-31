import xlsxwriter
 
workbook = xlsxwriter.Workbook('Example2.xlsx')
worksheet = workbook.add_worksheet()
 
# Start from the first cell.
# Rows and columns are zero indexed.
row = 0
column = 0
 
content = ["ankit", "rahul", "priya", "harshita",
                    "sumit", "neeraj", "shivam"]
 
# iterating through content list
cell_format = workbook.add_format()

cell_format.set_pattern(1)  # This is optional when using a solid fill.
cell_format.set_bg_color('green')
for item in content :
 
    # write operation perform
    worksheet.write(row, column, item, cell_format)
 
    # incrementing the value of row by one
    # with each iterations.
    row += 1
     
workbook.close()