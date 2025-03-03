import time
from datetime import datetime
import pantallaInicio
import pantallaReserva
import winsound
import bot as botAvanza

bot = botAvanza.bot(False)
bot.anadirBillete("SEGOVIA (todas las paradas)","Madrid Moncloa",datetime(2025, 3, 5), "07:15", False)

bot.buscarBilletes("SEGOVIA (todas las paradas)","Madrid Moncloa",datetime(2025, 3, 5),30) #origen,destino,fecha,espera

winsound.Beep(1000, 10000)  #Frecuencia de 1000 Hz, duración de 10000 ms (10 segundo)