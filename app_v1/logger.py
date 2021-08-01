import logging

LOG_FOLDER = 'C:/Users/marugger/Documents/Programas\Python/Peluqueria/Logs/'
LOG_FILE = 'logs.xls'
LOG = LOG_FOLDER + LOG_FILE

LOG_LEVEL = logging.DEBUG
LOG_FORMAT_DATE = '%d/%m/%Y %H:%M:%S'
LOG_FORMAT = '%(asctime)s ; %(name)s ; %(levelname)s ; %(message)s'

logging.basicConfig(
                      filename = LOG,
                      format= LOG_FORMAT,
                      datefmt = LOG_FORMAT_DATE,
                      level = LOG_LEVEL,
                    )