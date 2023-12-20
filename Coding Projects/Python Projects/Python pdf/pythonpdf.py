from fpdf import FPDF  # fpdf class


class PDF(FPDF):
    pass  # nothing happens when it is executed.

  
  pdf = PDF()#pdf object  
  pdf=PDF(orientation='L') # landscape
  pdf=PDF(unit='mm') #unit of measurement
  pdf=PDF(format='A4') #page format. A4 is the default value of the format, you don't have to specify it.
# full syntax
PDF(orientation={'P'(def.) or 'L'}, measure{'mm'(def.),'cm','pt','in'}, format{'A4'(def.),'A3','A5','Letter','Legal')

#default
pdf = PDF(orientation='P', unit='mm', format='A4')
                                                                               
pdf.add_page()
pdf.output('test.pdf','F')
                                                                               
pdf_w=210
pdf_h=297
                                                                               
  class PDF(FPDF):                                                                        
    def lines(self):
        self.set_line_width(0.0)
        self.line(0,pdf_h/2,210,pdf_h/2)
line(x1,y1,x2,y2)
                                                                               
  class PDF(FPDF):                                                                         
    def lines(self):
        self.set_line_width(0.0)
        self.line(5.0,5.0,205.0,5.0) # top one
        self.line(5.0,292.0,205.0,292.0) # bottom one
        self.line(5.0,5.0,5.0,292.0) # left one
        self.line(205.0,5.0,205.0,292.0) # right one

class PDF(FPDF):
    def lines(self):
        self.rect(5.0, 5.0, 200.0,287.0)
                                                                               
class PDF(FPDF):
    def lines(self):
        self.rect(5.0, 5.0, 200.0,287.0)
        self.rect(8.0, 8.0, 194.0,282.0)    
                                                                               
class PDF(FPDF):
    def lines(self):
        self.set_fill_color(32.0, 47.0, 250.0) # color for outer rectangle
        self.rect(5.0, 5.0, 200.0,287.0,'DF')
        self.set_fill_color(255, 255, 255) # color for inner rectangle
        self.rect(8.0, 8.0, 194.0,282.0,'FD')
                                                                               

def imagex(self):
        self.set_xy(6.0,6.0)
        self.image(sctplt,  link='', type='', w=1586/80, h=1920/80)
        self.set_xy(183.0,6.0)
        self.image(sctplt2,  link='', type='', w=1586/80, h=1920/80)                                                                     
                                                                               
import plotly.express as px
import plotly
import os
df = px.data.iris()
pltx= px.scatter(df, x="sepal_width", y="sepal_length", color="species",
                 size='petal_length', hover_data=['petal_width'])
plotly.io.write_image(pltx,file='pltx.png',format='png',width=700, height=450)
pltx=(os.getcwd()+'/'+"pltx.png")
### define a method
def charts(self):
        self.set_xy(40.0,25.0)
        self.image(plt,  link='', type='', w=700/5, h=450/5)
                                                                               
def titles(self):
        self.set_xy(0.0,0.0)
        self.set_font('Arial', 'B', 16)
        self.set_text_color(220, 50, 50)
        self.cell(w=210.0, h=40.0, align='C', txt="LORD OF THE PDFS", border=0)
                                                                               
def texts(self,name):
        with open(name,'rb') as xy:
            txt=xy.read().decode('latin-1')
        self.set_xy(10.0,80.0)    
        self.set_text_color(76.0, 32.0, 250.0)
        self.set_font('Arial', '', 12)
        self.multi_cell(0,10,txt)   
pdf.set_author('Eser SAYGIN')   

pdf.add_page()
pdf.output("test.pdf", "F")


