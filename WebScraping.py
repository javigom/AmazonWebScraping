# pip install selenium
# pip install requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd

# Lanzamos el navegador
driver = webdriver.Chrome()
driver.get("https://www.amazon.es/")

# Aceptamos cookies
driver.find_element(By.ID, "sp-cc-accept").click()

# Introducimos en la barra de búsqueda "tarjeta gráfica"
text_area = driver.find_element(By.ID, "twotabsearchtextbox")
text_area.clear()
text_area.send_keys("tarjeta gráfica")

# Pulsamos el botón de buscar
button_search = driver.find_element(By.ID, "nav-search-submit-button")
button_search.click()

# Establecemos que nos muestre resultados de entre 50-100 euros
price_list = driver.find_element(By.ID, "priceRefinements")
items = price_list.find_elements(By.TAG_NAME, "li")

for item in items:
    if(item.text == "50 - 100 EUR"):
        item_50_100 = item

check_box = item_50_100.find_element(By.TAG_NAME, "span").find_element(By.TAG_NAME, "a").find_element(By.TAG_NAME, "div").find_element(By.TAG_NAME, "i")

check_box.click()

# Establecemos un orden según la valoración de los clientes
order_button = driver.find_element(By.ID, "s-result-sort-select")
order_button.send_keys("Valoración media de los clientes")

# Resultados de la búsqueda
result_list = driver.find_elements(By.CLASS_NAME, "s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16".replace(" ", "."))

# Listas donde almacenamos los resultados
titulo = []
valoracion = []
precio = []
tam_ram = []
tipo_ram = []
tarjeta = []
velocidad = []

# Seleccionamos los primeros 10 resultados
for i in range(0, 10):
        
    # TÍTULO
    titulo.append(result_list[i].find_element(By.CLASS_NAME, "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal".replace(" ", ".")).text)
    
    # VALORACIÓN
    val = result_list[i].find_element(By.CLASS_NAME, "a-row.a-size-small").find_element(By.TAG_NAME, "span")
    valoracion.append(val.get_attribute("aria-label").replace("de 5 estrellas", ""))
    
    # PRECIO (algunos productos no lo tienen)
    try:
        precio.append(result_list[i].find_element(By.CLASS_NAME, "a-price").text)
    except:
        precio.append("-")
    
    # SPECS (algunos productos no contienen ninguna especificación)               
    try:
        # Obtenemos los datos y los guardamos en las listas creadas anteriormente
        data = result_list[i].find_elements(By.CLASS_NAME, "s-product-specs-view")[0].find_elements(By.CLASS_NAME, "a-text-bold")
        tam_ram.append(data[0].text)
        tipo_ram.append(data[1].text)
        tarjeta.append(data[2].text)
        velocidad.append(data[3].text)
        
    except:
        tam_ram.append("-")
        tipo_ram.append("-")
        tarjeta.append("-")
        velocidad.append("-")

# Guardamos los resultados en un DataFrame de Pandas
df = pd.DataFrame()
df['Titulo'] = titulo
df['Valoracion'] = valoracion
df['Precio'] = precio
df['Tamaño RAM'] = tam_ram
df['Tipo RAM'] = tipo_ram
df['Tarjeta Gráfica'] = tarjeta
df['Velocidad Memoria'] = velocidad

# print(df)

# Lo guardamos en un csv
df.to_csv('search_results.csv', header = True)