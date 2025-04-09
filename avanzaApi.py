import time
from datetime import datetime
import pantallaInicio
import pantallaReserva
import winsound
import bot as botAvanza
from plyer import notification

bot = botAvanza.bot(True)

bot.anadirBillete("Madrid Moncloa","SEGOVIA (todas las paradas)",datetime(2025, 4, 9), "21:00", True)

bot.buscarBilletes("Madrid Moncloa","SEGOVIA (todas las paradas)",datetime(2025, 4, 9),30) #origen,destino,fecha,espera

notification.notify(
    title="Avanza Bot",
    message="¡Se ha encontrado un billete disponible!",
    app_name="Avanza Bot",
    timeout=10  # Duración de la notificación en segundos
)

winsound.Beep(1000, 10000)  #Frecuencia de 1000 Hz, duración de 10000 ms (10 segundo)
