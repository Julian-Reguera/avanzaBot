from selenium import webdriver
from datetime import datetime
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

class Bus:
    def __init__(self, horaIda = None, horaVuelta = None, origen = None,destino = None,tipoRuta = None):
        self.horaIda = horaIda
        self.horaVuelta = horaVuelta
        self.origen = origen
        self.destino = destino
        self.tipoRuta = tipoRuta

def tramaBusDisponible(bus):
    if(bus.horaIda == None):
        raise Exception("No se ha especificado la hora de salida")
    
    strBusqueda = "div[data-departure='"+bus.horaIda +"']"
    
    if bus.horaVuelta != None:
        strBusqueda += "[data-arrival='"+bus.horaVuelta+"']"
    if bus.origen != None:
        strBusqueda += "[data-origen='"+bus.origen+"']"
    if bus.destino != None:
        strBusqueda += "[data-destino='"+bus.destino+"']"
        
    return strBusqueda     

class pantallaReserva:
    def __init__(self, webDriver):
        self.driver = webDriver
        
    def aceptarCookies(self):
        try:
            time.sleep(1)
            self.driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        except Exception as e:
            print(e)
            print("No se han podido aceptar las cookies")
            return
    
    def esperarViajesCargados(self):
        WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "div[class='loading-block']"))
            )
    
    def viajeDisponible(self,datos):
        try:
            trama =  tramaBusDisponible(datos)
            bus = None
            if datos.tipoRuta != None:
                buses = self.driver.find_elements(By.CSS_SELECTOR, trama)
                datos.tipoRuta = datos.tipoRuta.strip(" ()")
                for i in buses:
                    tRuta = i.find_element(By.CSS_SELECTOR, "span[class='route-type']").text
                    tRuta = tRuta.strip(" ()")
                    if tRuta == datos.tipoRuta:
                        bus = i
                        break
            else:
                bus = self.driver.find_element(By.CSS_SELECTOR, trama)
            
            if bus==None:
                raise Exception("No se ha encontrado ningún bus con esas características")
            
            if "disponible" == bus.get_attribute("data-tripavailabilitycode"):
                return True
            else:
                return False
        except:
            raise Exception("No existe ningún bus a esa hora")
    
    def refrescar(self):
        self.driver.refresh()