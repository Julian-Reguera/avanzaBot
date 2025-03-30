import time
from datetime import datetime
import pantallaInicio
import pantallaReserva
import winsound
import bot as botAvanza

bot = botAvanza.bot(True)

bot.anadirBillete("SEGOVIA (todas las paradas)","Madrid Moncloa",datetime(2025, 3, 31), "07:00", True)
bot.anadirBillete("SEGOVIA (todas las paradas)","Madrid Moncloa",datetime(2025, 3, 31), "07:00", False)
bot.anadirBillete("SEGOVIA (todas las paradas)","Madrid Moncloa",datetime(2025, 3, 31), "07:15", True)
bot.anadirBillete("SEGOVIA (todas las paradas)","Madrid Moncloa",datetime(2025, 3, 31), "07:15", False)

bot.buscarBilletes("SEGOVIA (todas las paradas)","Madrid Moncloa",datetime(2025, 3, 31),30) #origen,destino,fecha,espera

winsound.Beep(1000, 10000)  #Frecuencia de 1000 Hz, duración de 10000 ms (10 segundo)