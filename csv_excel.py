import csv
import xlwt
import itertools
from xlwt import Workbook

class CsvToExcel:
    """Method to convert csv file to excel"""

    def csv2excel(folder_name, folder_name_2):
        wb = Workbook()
        sheet1 = wb.add_sheet('Sheet 1')
        col_width = 256 * 40
        try:
            for i in itertools.count():
                j = i + 1
                sheet1.col(j). width = col_width
        except ValueError:
            pass

        with open("screenshots/{}/{}/report.csv".format(folder_name_2, folder_name), newline='') as myfile:
            reader = csv.reader(myfile)
            j = 0
            for row in reader:
                try:
                    for i in range(6):
                        sheet1.write(j, i, row[i])
                    j += 1
                except:
                    pass


        wb.save("screenshots/{}/{}/report.xls".format(folder_name_2, folder_name))
