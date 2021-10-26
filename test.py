from tkinter.constants import N


a = 'IMG%LINE%^0^ (Personnalisé)%4-2,5,3-2,6,4-c2'

(name, line) = a.split('%')[2:]

print(name, line)