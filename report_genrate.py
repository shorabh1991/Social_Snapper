from fpdf import FPDF
import csv
from fpdf import Template


class PDF(FPDF):
    def header(self):
        # Logo
        self.image('icons/army2.jpeg', 80, 10, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


class GenrateReport(PDF):
    """Method to Genrate Report"""


    def genrate_report(folder):
        pdf = PDF()
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font("Arial", size=14)
        list_header = ["Facebook-id",
                       "Active/Deactive", "Date/Time", "Remarks"]
        pdf.set_font("Arial", 'B', size=10)
        with open("screenshots/Facebook/{}/report.csv".format(folder), newline='') as myfile:
            reader = csv.reader(myfile)
            for i in range(0, 4):
                pdf.cell(20+50, 20, txt="{}".format(list_header[i]), align="L")
            pdf.set_font("Arial", 'I', size=9)
            for row in reader:
                for i in range(0, 3):
                    pdf.cell(20+50, 30, txt="{}".format(row[i]), align="L")
                pdf.ln(10)
            pdf.output("screenshots/Facebook/{}/report.pdf".format(folder))
