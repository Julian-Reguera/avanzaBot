import time
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import pantallaReserva

def mesToNumero(mes):
    switcher = {
        "enero": 1,
        "febrero": 2,
        "marzo": 3,
        "abril": 4,
        "mayo": 5,
        "junio": 6,
        "julio": 7,
        "agosto": 8,
        "septiembre": 9,
        "octubre": 10,
        "noviembre": 11,
        "diciembre": 12
    }

    return switcher.get(mes.lower(), None)

class pantallaInicio:
    def __init__(self,oculto):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--log-level=3")
            if oculto:
                options.add_argument('--headless=new')
                options.add_argument('--disable-gpu')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
            self.driver = webdriver.Chrome(options=options)
            self.driver.get("https://www.avanzabus.com/")
            
        except Exception as e:
            print(e)
            raise RuntimeError("No se pudo iniciar el driver de Chrome")
    
    def __getPagCal(self):
        mes = mesToNumero(self.driver.find_element(By.CSS_SELECTOR, "span[class='ui-datepicker-month']").text)
        anio = self.driver.find_element(By.CSS_SELECTOR, "span[class='ui-datepicker-year']").text
        return mes,int(anio)

    def getFechaSleccionada(self):
        fecha = self.driver.find_element(By.ID, "date_going")
        fecha_obj = datetime.strptime(fecha.get_attribute("value"), "%d-%m-%Y")
        return fecha_obj.day,fecha_obj.month,fecha_obj.year

    def selectFecha(self,dia,mes,anio):
        if datetime.now().date() > datetime(anio, mes, dia).date():
                raise ValueError("La fecha seleccionada es anterior a la fecha actual")
            
        if((dia,mes,anio) != self.getFechaSleccionada()):
            self.driver.find_element(By.ID, "date_going").click()
            
            mesPAg,anioPag = self.__getPagCal()
            diferencia = (anio - anioPag) * 12 + mes - mesPAg
            for i in range(diferencia):
                self.driver.find_element(By.CSS_SELECTOR, "a[title='Sig&#x3e;']").click()
                
            dias = self.driver.find_elements(By.CSS_SELECTOR, "a[class='ui-state-default']")
            for i in dias:
                if i.text == str(dia):
                    i.click()
                    break
 
    def selectFecha(self,fecha):
        if datetime.now().date() > fecha.date():
                raise ValueError("La fecha seleccionada es anterior a la fecha actual")
        
        dia = fecha.day
        mes = fecha.month
        anio = fecha.year

        if((dia,mes,anio) != self.getFechaSleccionada()):
            self.driver.find_element(By.ID, "date_going").click()
            
            mesPAg,anioPag = self.__getPagCal()
            diferencia = (anio - anioPag) * 12 + mes - mesPAg
            for i in range(diferencia):
                self.driver.find_element(By.CSS_SELECTOR, "a[title='Sig&#x3e;']").click()
                
            dias = self.driver.find_elements(By.CSS_SELECTOR, "a[class='ui-state-default']")
            for i in dias:
                if i.text == str(dia):
                    i.click()
                    break

    def selectDestino(self,ubDestino):
        destino = None
        selecciones = self.driver.find_elements(By.CSS_SELECTOR, "span[class='select2-selection__rendered']")
        
        for i in selecciones:
            if i.text == "Destino":
                destino = i
           
        idContendor = destino.get_attribute("id")     
        destino.click()
        input_destino = self.driver.find_element(By.CSS_SELECTOR, "input[class='select2-search__field']")
        input_destino.send_keys(ubDestino)
        input_destino.send_keys(Keys.RETURN)
        destino = self.driver.find_element(By.ID, idContendor)
        
        if destino.text != ubDestino:
            raise ValueError("No se ha encontrado la ubicación de destino (revisa la ortografia)")

    def selectOrigen(self, ubOrigen):
        origen = None
        selecciones = self.driver.find_elements(By.CSS_SELECTOR, "span[class='select2-selection__rendered']")
        
        for i in selecciones:
            if i.text == "Origen":
                origen = i

        idContenedor = origen.get_attribute("id")
        origen.click()
        input_origen = self.driver.find_element(By.CSS_SELECTOR, "input[class='select2-search__field']")
        input_origen.send_keys(ubOrigen)
        input_origen.send_keys(Keys.RETURN)
        origen = self.driver.find_element(By.ID, idContenedor)
        if origen.text != ubOrigen:
            raise ValueError("No se ha encontrado el origen (revisa la ortografia)")
        
    def selectIda(self):
        label = self.driver.find_element(By.CSS_SELECTOR, "label[for='radio_iv_I']")
        label.click()

    def acceptarCookies(self):
        try:
            cookies = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "cookiescript_accept"))
            )
            cookies.click()
        except Exception as e:
            return
        
    def buscarViajes(self):
        boton = self.driver.find_element(By.ID, "buscarViajes")
        boton.click()
        WebDriverWait(self.driver,30)
        pantReserva = pantallaReserva.pantallaReserva(self.driver)
        pantReserva.esperarViajesCargados()
        error = None
        try:
            error= self.driver.find_element(By.CSS_SELECTOR, "div[class='alert alert-warning alert-dismissible']")
        except Exception as e:
            return pantReserva
        raise Exception(error.text)
        
    
    def cerrar(self):
        self.driver.quit()