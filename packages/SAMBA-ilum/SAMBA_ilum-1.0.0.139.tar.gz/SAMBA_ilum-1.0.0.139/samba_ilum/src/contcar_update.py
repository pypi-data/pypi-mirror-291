# SAMBA_ilum Copyright (C) 2024 - Closed source


#===========================
poscar = open('POSCAR', 'r')
VTemp = poscar.readline();  VTemp = str(VTemp)
poscar.close()
#=============


#========================================================
with open('CONTCAR', 'r') as file: line = file.readlines()
line[0] = VTemp
with open('CONTCAR', 'w') as file: file.writelines(line)
#========================================================


#===========================================================
# Fixando o arquivo POSCAR com coordenadas cartesianas =====
#===========================================================
poscar = open('POSCAR', "r")
for i in range(8): VTemp = poscar.readline()
poscar.close()
#------------------
string = str(VTemp)
if (string[0] == 'D' or string[0] == 'd'):
   contcar = open('CONTCAR', "r")
   poscar = open('POSCAR', "w")
   VTemp = contcar.readline();  poscar.write(f'{VTemp}')
   VTemp = contcar.readline();  poscar.write(f'{VTemp}');  param = float(VTemp)
   VTemp = contcar.readline();  poscar.write(f'{VTemp}');  VTemp = VTemp.split();  A = [float(VTemp[0])*param, float(VTemp[1])*param, float(VTemp[2])*param]  
   VTemp = contcar.readline();  poscar.write(f'{VTemp}');  VTemp = VTemp.split();  B = [float(VTemp[0])*param, float(VTemp[1])*param, float(VTemp[2])*param]
   VTemp = contcar.readline();  poscar.write(f'{VTemp}');  VTemp = VTemp.split();  C = [float(VTemp[0])*param, float(VTemp[1])*param, float(VTemp[2])*param]
   VTemp = contcar.readline();  poscar.write(f'{VTemp}')
   VTemp = contcar.readline();  poscar.write(f'{VTemp}')
   #----------------------------------------------------
   nions = 0;  VTemp = VTemp.split()
   for k in range(len(VTemp)): nions += int(VTemp[k])
   #---------------------------------------------------------
   VTemp = contcar.readline();  poscar.write(f'Cartesian \n')
   #-----------------------------------------------------------
   # Escrita das coordenadas cartesianas ----------------------
   #-----------------------------------------------------------
   for k in range(nions):
       VTemp = contcar.readline().split()
       k1 = float(VTemp[0]); k2 = float(VTemp[1]); k3 = float(VTemp[2])
       coord_x = ((k1*A[0]) + (k2*B[0]) + (k3*C[0]))*param
       coord_y = ((k1*A[1]) + (k2*B[1]) + (k3*C[1]))*param
       coord_z = ((k1*A[2]) + (k2*B[2]) + (k3*C[2]))*param
       poscar.write(f'{coord_x:>28,.21f} {coord_y:>28,.21f} {coord_z:>28,.21f} \n')
   #--------------
   contcar.close()   
   poscar.close()
   #-------------
