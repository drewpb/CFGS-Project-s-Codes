    #Librería para la base de datos
from sys import displayhook
import pandas as pd
import matplotlib.pyplot as plt
import pdfkit as pdf


ruta_proyecto = "/home/pi/_myDrew_/Proyecto_DS18B20/generateFiles/"

headers = ["Id","Temperatura", "Fecha_YYYYMMDD", "Fecha_EPOCH", "Hora", "Dispositivo"]

options = {
    'page-size': 'A5',
    'margin-top': '0.6in',
    'margin-right': '1.1in',
    'margin-bottom': '0.18in',
    'margin-left': '0.9in',
    'orientation': 'Landscape',
    'header-right': 'SJM2',
    'header-center': 'TÍTULO',
}

ds18b20 = pd.read_csv(f'{ruta_proyecto}table_xtra.csv', index_col=0, names=headers)
df1 = ds18b20.style.set_table_styles([dict(selector='th', props=[('text-align','center')])])

ds18b20.to_html(f'{ruta_proyecto}temp_html_tabla_xtra.html')
pdf.from_file(f'{ruta_proyecto}temp_html_tabla_xtra.html', f'{ruta_proyecto}TABLA_DS18B20_xtra.pdf', options=options)
ds18b20.plot("Hora","Temperatura", marker='o', c='c',  ls='-.', lw=2, ms=6)
plt.savefig(f"{ruta_proyecto}GRAFICA_DS18B20_Temp-F_xtra.jpg", bbox_inches='tight')
print(True)
