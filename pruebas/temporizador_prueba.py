from datetime import datetime, timedelta
from threading import Thread
from time import sleep

import logger

log = logger.logging.getLogger('Temporizador')

class Temporizador(Thread):
  def __init__(self, name, hora, delay, funcion):
    # El constructor recibe como parámetros:
    ## hora = en un string con formato hh:mm:ss y es la hora a la que queremos que se ejecute la función.
    ## delay = tiempo de espera entre comprobaciones en segundos.
    ## funcion = función a ejecutar.

    super(Temporizador, self).__init__()
    self.name = name
    self._estado = True
    self.hora = hora
    self.delay = delay
    self.funcion = funcion

  def stop(self):
    log.debug(f'function stop(): Temporizador "{self.name}"')
    self._estado = False

  def run(self):
    log.info(f'Inicio temporizador "{self.name}"')
    # Pasamos el string a dato tipo datetime
    aux = datetime.strptime(self.hora, '%H:%M:%S')
    # Obtenemos la fecha y hora actuales.
    hora = datetime.now()
    # Sustituimos la hora por la hora a ejecutar la función.
    hora = hora.replace(hour = aux.hour, minute=aux.minute, second=aux.second, microsecond = 0)
    # Comprobamos si la hora ya a pasado o no, si ha pasado sumamos un dia.
    if hora <= datetime.now():
      hora += timedelta(days=1)

    # Iniciamos el ciclo:
    while self._estado:
      # Comparamos la hora actual con la de ejecución y ejecutamos o no la función.
      ## Si se ejecuta sumamos un dia a la fecha objetivo.
      if hora <= datetime.now():
        self.funcion()
        log.info(f'Temporizador "{self.name}": Ejecucion programada ejecutada el {hora.date()} a las {hora.time()}')
        hora += timedelta(days=1)
      
      # Esperamos x segundos para volver a ejecutar la comprobación.
      sleep(self.delay)
      log.debug(f'ejecucion temporizador')
      
    else:
      log.info(f'Fin temporizador "{self.name}"')


#=========================================================================================
#Ejemplo de uso:

def ejecutar():
  log.debug(f'run fuction ejecutar')

# main:
name = 'Probando temporizador'
time = '05:52:00'
delay_seconds = 5
funcion = ejecutar
t = Temporizador(name,time,delay_seconds,funcion) # Instanciamos nuestra clase Temporizador
t.start() #Iniciamos el hilo

## code programa principal
i = 0
while  i < 10:
  i = i + 1
  log.debug(f'Imprimiendo desde hilo principal {i}')
  sleep(2)

log.setLevel('INFO')


while  i < 20:
  i = i + 1
  log.debug(f'Imprimiendo desde hilo principal {i}')
  log.error(f'Imprimiendo desde hilo principal {i}')
  sleep(2)

t.stop()