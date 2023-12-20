from fpdf import FPDF  # fpdf class


class PDF(FPDF):
    pass  # nothing happens when it is executed.


pdf = PDF(
    format="A4"
)  # page format. A4 is the default value of the format, you don't have to specify it.

pdf.add_page()
pdf.output("test.pdf", "F")
