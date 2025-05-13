from fpdf import FPDF  # fpdf class
import plotly.express as px
import plotly
import os

class PDF(FPDF):
    def lines(self):
        self.set_line_width(0.0)
        self.line(5.0, 5.0, 205.0, 5.0)  # top one
        self.line(5.0, 292.0, 205.0, 292.0)  # bottom one
        self.line(5.0, 5.0, 5.0, 292.0)  # left one
        self.line(205.0, 5.0, 205.0, 292.0)  # right one
        self.rect(5.0, 5.0, 200.0, 287.0)
        self.rect(8.0, 8.0, 194.0, 282.0)
        self.set_fill_color(32.0, 47.0, 250.0)  # color for outer rectangle
        self.rect(5.0, 5.0, 200.0, 287.0, 'DF')
        self.set_fill_color(255, 255, 255)  # color for inner rectangle
        self.rect(8.0, 8.0, 194.0, 282.0, 'FD')

    def imagex(self, sctplt, sctplt2):
        self.set_xy(6.0, 6.0)
        self.image(sctplt, link='', type='', w=1586/80, h=1920/80)
        self.set_xy(183.0, 6.0)
        self.image(sctplt2, link='', type='', w=1586/80, h=1920/80)

    def charts(self, plt):
        self.set_xy(40.0, 25.0)
        self.image(plt, link='', type='', w=700/5, h=450/5)

    def titles(self):
        self.set_xy(0.0, 0.0)
        self.set_font('Arial', 'B', 16)
        self.set_text_color(220, 50, 50)
        self.cell(w=210.0, h=40.0, align='C', txt="LORD OF THE PDFS", border=0)

    def texts(self, name):
        with open(name, 'rb') as xy:
            txt = xy.read().decode('latin-1')
        self.set_xy(10.0, 80.0)
        self.set_text_color(76.0, 32.0, 250.0)
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, txt)

# Initialize PDF with default settings
pdf = PDF(orientation='P', unit='mm', format='A4')
pdf.set_author('Eser SAYGIN')

# Example usage for generating a PDF
pdf.add_page()

# Generate a sample plot for demonstration (if needed)
df = px.data.iris()
pltx = px.scatter(df, x="sepal_width", y="sepal_length", color="species",
                  size='petal_length', hover_data=['petal_width'])
plotly.io.write_image(pltx, file='pltx.png', format='png', width=700, height=450)
plt_path = os.path.join(os.getcwd(), "pltx.png")

# Apply methods (commented out as they require specific inputs)
# pdf.lines()
# pdf.imagex(sctplt, sctplt2)  # Requires sctplt and sctplt2 to be defined
# pdf.charts(plt_path)
# pdf.titles()
# pdf.texts('sample.txt')  # Requires a sample.txt file

pdf.output("test.pdf", "F")
