import time
import pantallaInicio
import pantallaReserva

class bot:
    def __init__(self, visible):
        self.visible = visible
        self.horarios = {}

    def anadirBillete(self, origen, destino, fecha, hora, directo):
        if (origen,destino,fecha) not in self.horarios:
            self.horarios[(origen,destino,fecha)] = []
        if directo:
            self.horarios[(origen,destino,fecha)].append(pantallaReserva.Bus(horaIda=hora,tipoRuta="Directo"))
            self.horarios[(origen,destino,fecha)].append(pantallaReserva.Bus(horaIda=hora,tipoRuta="directo"))
        else:
            self.horarios[(origen,destino,fecha)].append(pantallaReserva.Bus(horaIda=hora,tipoRuta="SemiDirecto"))
            self.horarios[(origen,destino,fecha)].append(pantallaReserva.Bus(horaIda=hora,tipoRuta="Semidirecto"))
            self.horarios[(origen,destino,fecha)].append(pantallaReserva.Bus(horaIda=hora,tipoRuta="semidirecto"))
            self.horarios[(origen,destino,fecha)].append(pantallaReserva.Bus(horaIda=hora,tipoRuta="semiDirecto"))
    
    def buscarBilletes(self, origen,destino,fecha,espera):
        ini , pantReservas = self.__iniciarWeb(origen,destino,fecha)

        disponible = False
        cont = 0
                                                              
        while not self.__disponibles(pantReservas,origen,destino,fecha):
            time.sleep(espera)
            if cont == 10:
                cont = 0
                ini.cerrar()
                ini , pantReservas = self.__iniciarWeb(origen,destino,fecha)
            else:
                pantReservas.refrescar()
                pantReservas.esperarViajesCargados()
            cont += 1
        
        ini.cerrar()

    def __disponibles(self,pantReservas,origen,destino,fecha):
        disponible = False
        cont = 0
        for i in self.horarios[(origen,destino,fecha)]:
                
                try:
                    print("prueba: "+i.horaIda+" "+i.tipoRuta)
                    disponible = disponible or pantReservas.viajeDisponible(i)
                    print("prueba: "+i.horaIda+" "+i.tipoRuta)
                except:
                    cont += 1
        return disponible

    def __iniciarWeb(self,origen,destino,fecha):
        ini = pantallaInicio.pantallaInicio(self.visible)
        ini.acceptarCookies()
        ini.selectIda()
        ini.selectOrigen(origen)
        time.sleep(1)
        ini.selectDestino(destino)
        ini.selectFecha(fecha)
        pantReservas = ini.buscarViajes()
        pantReservas.esperarViajesCargados()
        return ini, pantReservas

