import os

print(os.path.abspath(''))   # print: /home/martin/Programas/Peluqueria/pruebas

def path_rep(path , repeticion = 0):
  index = [idx for idx, x in enumerate(path) if x=='/'][repeticion]
  return path[0:index]

def path_find(path, key):
  len_key = len(key)
  index = path.find(key)
  return path[0:(index + len_key)]


print(path_rep(os.path.abspath(''),-2))
print(path_find(os.path.abspath(''),'pruebas'))