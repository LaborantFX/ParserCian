import gspread

gc = gspread.service_account(filename = 'parcercian-988532820585.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1H7bzGN66zt4NVV9RugCakmyiynjO4fXvVjse2MPU3fI')


#print(sh.sheet1.get('A2'))
worksheet = sh.get_worksheet(0)
worksheet.format ("A1", {
    "backgroundColor": {
      "red": 0.3,
      "green": 0.3,
      "blue": 0.7
    }
})
#print(worksheet.acell('A2').value)
#print(sh.worksheets())
#print(worksheet.col_values(1))