#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import logger
log = logger.logging.getLogger(__name__)

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_v1.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
    
    ## INICIAR EJECUCION AUTOMATIZADA DE CREACION DE DETAIL
    try:
        from calendar_api.services.created_detail_calendar import created_detail_calendar
        from temporizador import Temporizador
        ## Se inicia la ejecucion del temporizador
        name = 'Temporizador created_detail_calendar'
        time = '20:10:00'
        delay_seconds = 5
        funcion = created_detail_calendar
        t = Temporizador(name,time,delay_seconds,funcion) # Instanciamos nuestra clase Temporizador
        t.start() #Iniciamos el hilo
    except Exception as ex:
        log.critical(f'Error al iniciar el temporizador: {name}, no se ejecutara automaticamente el creador de detail calendar; {ex.message}')


if __name__ == '__main__':
    main()
