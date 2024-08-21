# SAMBA_ilum Copyright (C) 2024 - Closed source

from pymatgen.io.vasp import Poscar
from pymatgen.core import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
#--------------------------------------------------------
import numpy as np
import shutil
import json
import uuid
import sys
import os


# replace_type_pseudo
# replace_type_XC
# replace_type_vdW


# =========================================
# Verificando arquivos da sereme lidos: ===
# =========================================
l_file = 'null';  l_file_SO = 'null'
if os.path.isfile('output/info_scf.txt'):       l_file = 'info_scf.txt'
if os.path.isfile('output/info_bands.txt'):     l_file = 'info_bands.txt'
if os.path.isfile('output/info_scf_SO.txt'):    l_file_SO = 'info_scf_SO.txt'
if os.path.isfile('output/info_bands_SO.txt'):  l_file_SO = 'info_bands_SO.txt'
if (l_file == 'null' and l_file_SO == 'null'):  sys.exit(0)


# ============================================================
# Extraindo informações de configuração da Heteroestrutura ===
# ============================================================
if os.path.isfile('output/POSCAR'):
   #----------------------------------
   poscar = open('output/POSCAR', "r")
   VTemp = poscar.readline().split()
   poscar.close()
   #------------------------
   if (VTemp[0] == 'SAMBA'):
      #----------------------------------------------------------------
      l_materials = VTemp[1].replace('+', ' ').replace('_', '').split()
      n_materials = len(l_materials)
      #------------------------------------------
      r_ions_materials = []; nions_materials = []
      nion = 0;  passo = 0
      #-----------------------------
      for m in range(n_materials):
          r_ions_materials.append( str(1 + nion) + ':')
          nion += int(VTemp[m+2])
          r_ions_materials[m] += str(nion)
          nions_materials.append(int(VTemp[m+2]))
      #------------------------------------------
      if (n_materials > 1):
         rotate_materials = [];  mismatch_materials = [];  id_materials = []
         passo = n_materials +1
         for i in range(n_materials -1):
             passo += 4
             mismatch_materials.append(str(VTemp[passo]))
         #-----------------------------------------------
         for i in range(n_materials -1):
             passo += 4
             rotate_materials.append(str(VTemp[passo]))
         #---------------------------------------------
         passo += 1
         for i in range(n_materials):
             passo += 1 
             id_materials.append(str(VTemp[passo]))
      #--------------------------------------------
      temp_id = VTemp[-1].replace('_', ' ').split()
      formula_quimica = temp_id[0]
      id_code = temp_id[-1]
   #-----------------------------------------------
   if (VTemp[0] != 'SAMBA'): exit()
   #-------------------------------


# ============================================================
# Extraindo informações de configuração da Heteroestrutura ===
# ============================================================
poscar = open('output/POSCAR', "r")
VTemp = poscar.readline().split()
materials = VTemp[1].replace('+', ' ').split()
#---------------------------------------------
t_ions_materials = []
for i in range(len(materials)):
    ions_vector = []
    mat_temp = materials[i].replace('_', ' ').split()
    for j in range(len(mat_temp)): 
        ions_vector.append(str(mat_temp[j]))
    t_ions_materials.append(ions_vector)
#-------------------------------------------
for i in range(6): VTemp = poscar.readline().split()
t_nions_materials = [];  number = -1
for i in range(len(materials)):
    nions_vector = []
    mat_temp = materials[i].replace('_', ' ').split()
    for j in range(len(mat_temp)):
        number += 1
        nions_vector.append(int(VTemp[number]))
    t_nions_materials.append(nions_vector)
#-------------
poscar.close()
#-------------


# ==========================================
# Extraindo as posições dos ions da Rede ===
# ==========================================
poscar = open('output/POSCAR', "r")
for i in range(5): VTemp = poscar.readline()
type_ions = poscar.readline().split()
type_ions_n = poscar.readline().split()
poscar.readline()
coord_ions = []
for i in range(len(type_ions)):
    for j in range(int(type_ions_n[i])):
        VTemp = poscar.readline().split()
        coord_ions.append([ str(type_ions[i]), float(VTemp[0]), float(VTemp[1]), float(VTemp[2]) ])
poscar.close()


# ==========================================
# Splitando o arquivo POSCAR ===============
# ==========================================

if (n_materials > 1):

   #----------------------------------
   poscar = open('output/POSCAR', 'r')
   #----------------------------------
   VTemp = poscar.readline().split()
   label_materials = VTemp[1].replace('+', ' ').split()
   n_Lattice = len(label_materials);  nion = 0
   range_ion_Lattice = []; ntype_ions = ['']*n_Lattice           
   #--------------------------------------------------
   for m in range(n_Lattice):
       range_ion_Lattice.append( str(1 + nion) + ' ')
       nion += int(VTemp[m+2])
       range_ion_Lattice[m] += str(nion)
   #----------------------------------------------------
   for m in range(6):  VTemp = poscar.readline().split()
   #----------------------------------------------------
   poscar.close()
   #-------------
   for m in range(n_Lattice):
       contador = 0
       for n in range(len(VTemp)):
           contador += int(VTemp[n])
           range_ion = range_ion_Lattice[m].split()
           ion_i = int(range_ion[0]);  ion_f = int(range_ion[1])
           if (contador >= ion_i and contador <= ion_f):
              ntype_ions[m] += str(VTemp[n]) + ' '

   for m in range(n_Lattice):
       #----------------------------------
       poscar = open('output/POSCAR', 'r')
       poscar_new = open('output/POSCAR.material_' + str(m+1), 'w')
       #-----------------------------------------------------------
       VTemp = poscar.readline()
       poscar_new.write(f'POSCAR \n')
       #-----------------------------
       for n in range(4):
           VTemp = poscar.readline()
           poscar_new.write(f'{VTemp}')
       #-------------------------------
       print(label_materials)
       VTemp = poscar.readline()
       temp = label_materials[m].replace('_', ' ')
       poscar_new.write(f'{temp} \n')
       #-----------------------------
       VTemp = poscar.readline()
       poscar_new.write(f'{ntype_ions[m]} \n')
       #--------------------------------------
       VTemp = poscar.readline()
       poscar_new.write(f'direct \n')
       #---------------------------------------
       range_ion = range_ion_Lattice[m].split()
       ion_i = int(range_ion[0]);  ion_f = int(range_ion[1])
       #----------------------------------------------------
       for n in range(1,(nion+1)):
           VTemp = poscar.readline()
           if (n >= ion_i and n <= ion_f):  poscar_new.write(f'{VTemp}')
       #----------------------------------------------------------------
       poscar.close()
       poscar_new.close()
       #-----------------

# ===============================================
# Construindo o arquivo .json ===================
# ===============================================

#------------------------------------------------------
# Inicializando o arquivo JSON com um dicionário vazio:
#------------------------------------------------------
with open('output/info.json', 'w') as file:
    json.dump({}, file)

# ===============================================
# Atualizando as informações do arquivo .json ===
# ===============================================

for n in range(2):

    #-------
    crit = 1
    #-----------
    if (n == 0):
       file = l_file
       if (file == 'null'):  crit = 0
    #-----------
    if (n == 1):
       file = l_file_SO
       if (file == 'null'):  crit = 0
    #---------

    if (crit == 1):
       # ===================================================
       # Iniciando tags com valores vazios "--" ============
       # ===================================================
       loop = 0
       id = '--';  id_monolayers = '--'
       label = '--';  label_materials = '--';  formula = '--';  stoichiometry = '--'
       nlayers = '--';  nions = '--';  nions_monolayers = '--';  range_ions_materials = '--'
       type_ions_materials = '--';  type_nions_materials = '--' 
       mismatch = '--';  rotate_angle = '--';
       lattice_type = '--';  point_group = [];  point_group_schoenflies = [];  space_group = [];  space_group_number = [];  inversion_symmetry = []
       param_a = '--';  a1 = '--';  a2 = '--';  a3 = '--';  param_b = '--';  b1 = '--';  b2 = '--';  b3 = '--'
       module_a1_a2_a3 = '--'; module_b1_b2_b3 = '--';  angle_a1a2_a1a3_a2a3 = '--'; angle_b1b2_b1b3_b2b3 = '--'
       cell_area = '--';  cell_vol = '--';  thickness = '--';  z_separation = '--';  zb_area = '--';  zb_volume = '--'
       direct_coord_ions = '--';  k_path = '--'
       #-----------------------------------------------------------------------------------------------------------------------
       e_fermi = '--';  total_energy = '--';  e_binding = '--';  e_slide = '--';  charge_transfer = '--';  work_function = '--'
       nk = '--';  nb = '--';  ne = '--';  ne_valence = '--';  vbm = '--';  cbm = '--'
       gap = '--';  type_gap = '--';  ki_gap = '--';  kf_gap = '--';  lorbit = '--';  ispin = '--'
       #------------------------------------------------------------------------------------------
       non_collinear = '--';  spin_orbit = '--';  lorbit = '--';  ispin = '--'
       e_fermi_SO = '--';  total_energy_SO = '--';  e_binding_SO = '--';  e_slide_SO = '--';  charge_transfer_SO = '--';  work_function_SO = '--'
       nk_SO = '--';  nb_SO = '--';  ne_SO = '--';  ne_valence_SO = '--';  vbm_SO = '--';  cbm_SO = '--'
       gap_SO = '--';  type_gap_SO = '--';  ki_gap_SO = '--';  kf_gap_SO = '--';  lorbit_SO = '--';  ispin_SO = '--'
       #------------------------------------------------------------------------------------------------------------


       # ===========================================
       # Extraindo dados da saída do VASProcar =====
       # ===========================================
       with open('output/' + file, "r") as info: lines = info.readlines()
       #-----------------------------------------------------------------
       for i in range(len(lines)):
           VTemp = lines[i].replace('(', ' ( ').replace(')', ' ) ').replace(';', '').replace(',', '').split()
           if (len(VTemp) > 0):
              #----------------------------------------
              if (VTemp[0] == 'LNONCOLLINEAR'):  non_collinear = str(VTemp[2])
              #----------------------------------------
              elif (VTemp[0] == 'LSORBIT'):  spin_orbit = str(VTemp[2])
              #----------------------------------------
              elif (VTemp[0] == 'nº' or VTemp[0] == 'nÂº'):
                 if (VTemp[1] == 'k-points'):  nk = int(VTemp[3])
                 if (VTemp[5] == 'bands'):  nb = int(VTemp[7])
                 if (VTemp[1] == 'ions'):  ni = int(VTemp[3])
                 if (VTemp[5] == 'electrons'):  ne = float(VTemp[7])
              #----------------------------------------
              elif (VTemp[0] == 'LORBIT'):
                 lorbit = int(VTemp[2])
                 if (VTemp[3] == 'ISPIN'):  ispin = int(VTemp[5])
              #----------------------------------------
              elif (VTemp[0] == 'Last'):  vbm = int(VTemp[4])
              #----------------------------------------
              # elif (VTemp[0] == 'First'):  cbm = int(VTemp[4])
              elif (VTemp[0] == 'First'):  cbm = vbm +1
              #----------------------------------------
              elif (VTemp[0] == 'GAP'):
                type_gap = str(VTemp[2])
                gap = float(VTemp[5])
                if (VTemp[8] == 'k-point'):
                   ki_gap = int(VTemp[9])
                   kf_gap = ki_gap
                if (VTemp[8] == 'k-points'):
                   ki_gap = int(VTemp[9])
                   kf_gap = int(VTemp[11])
              #----------------------------------------
              elif (VTemp[0] == 'Fermi'):  e_fermi = float(VTemp[3])           
              #----------------------------------------
              elif (VTemp[0] == 'free'):  total_energy = float(VTemp[4])   
              #----------------------------------------
              elif (VTemp[0] == 'Volume_cell'):  Volume_cell = float(VTemp[2])   
              #----------------------------------------
              elif (VTemp[0] == 'Param.'):  param = float(VTemp[2])   
              #----------------------------------------
              elif (VTemp[0] == 'A1'):
                   a1 = [float(VTemp[4]), float(VTemp[5]), float(VTemp[6])]                  
                   A1 = np.array([float(VTemp[4]), float(VTemp[5]), float(VTemp[6])])*param;  module_a1_a2_a3 = []; module_a1_a2_a3.append(np.linalg.norm(A1))
              elif (VTemp[0] == 'A2'):
                   a2 = [float(VTemp[4]), float(VTemp[5]), float(VTemp[6])]
                   A2 = np.array([float(VTemp[4]), float(VTemp[5]), float(VTemp[6])])*param;  module_a1_a2_a3.append(np.linalg.norm(A2))
              elif (VTemp[0] == 'A3'):
                   a3 = [float(VTemp[4]), float(VTemp[5]), float(VTemp[6])]
                   A3 = np.array([float(VTemp[4]), float(VTemp[5]), float(VTemp[6])])*param;  module_a1_a2_a3.append(np.linalg.norm(A3))
                   #-------------------------------------------------------
                   angle_a1a2_a1a3_a2a3 = []
                   angle_a1a2_a1a3_a2a3.append(round(np.degrees(np.arccos(np.dot(A1,A2) / (np.linalg.norm(A1) * np.linalg.norm(A2)))), 3))
                   angle_a1a2_a1a3_a2a3.append(round(np.degrees(np.arccos(np.dot(A1,A3) / (np.linalg.norm(A1) * np.linalg.norm(A3)))), 3))
                   angle_a1a2_a1a3_a2a3.append(round(np.degrees(np.arccos(np.dot(A2,A3) / (np.linalg.norm(A2) * np.linalg.norm(A3)))), 3))
              #----------------------------------------
              elif (VTemp[0] == '2pi/Param.'):  fator_rec = float(VTemp[2])   
              #----------------------------------------
              elif (VTemp[0] == 'B1'):
                   b1 = [float(VTemp[4]), float(VTemp[5]), float(VTemp[6])]
                   B1 = np.array([float(VTemp[4]), float(VTemp[5]), float(VTemp[6])])*fator_rec;  module_b1_b2_b3 = []; module_b1_b2_b3.append(np.linalg.norm(B1))
              elif (VTemp[0] == 'B2'):
                   b2 = [float(VTemp[4]), float(VTemp[5]), float(VTemp[6])]
                   B2 = np.array([float(VTemp[4]), float(VTemp[5]), float(VTemp[6])])*fator_rec;  module_b1_b2_b3.append(np.linalg.norm(B2))
              elif (VTemp[0] == 'B3'):
                   b3 = [float(VTemp[4]), float(VTemp[5]), float(VTemp[6])]
                   B3 = np.array([float(VTemp[4]), float(VTemp[5]), float(VTemp[6])])*fator_rec;  module_b1_b2_b3.append(np.linalg.norm(B3))
                   #-------------------------------------------------------
                   angle_b1b2_b1b3_b2b3 = []
                   angle_b1b2_b1b3_b2b3.append(round(np.degrees(np.arccos(np.dot(B1,B2) / (np.linalg.norm(B1) * np.linalg.norm(B2)))), 3))
                   angle_b1b2_b1b3_b2b3.append(round(np.degrees(np.arccos(np.dot(B1,B3) / (np.linalg.norm(B1) * np.linalg.norm(B3)))), 3))
                   angle_b1b2_b1b3_b2b3.append(round(np.degrees(np.arccos(np.dot(B2,B3) / (np.linalg.norm(B2) * np.linalg.norm(B3)))), 3))
              #----------------------------------------
              elif (VTemp[0] == 'Volume_ZB'):  vol_zb = float(VTemp[2])   
              #----------------------------------------
              elif (VTemp[0] == 'k-points'):  loop = i+3


       if (file == 'info_bands.txt' or file == 'info_bands_SO.txt'):
          # =======================================================
          # Obtando e organizando as informações dos pontos-k =====
          # =======================================================
          info = open('output/' + file, "r")
          #---------------------------------
          if (loop != 0):
             #-----------------------------------------------------
             k_points_direct = []; k_points_cart = [];  k_path = []
             #---------------------------------------------
             for i in range(loop):  VTemp = info.readline()
             for i in range(nk):
                 VTemp = info.readline().split()
                 k_points_direct.append([float(VTemp[1]), float(VTemp[2]), float(VTemp[3])])
                 k_points_cart.append([float(VTemp[4]), float(VTemp[5]), float(VTemp[6])])
                 k_path.append(float(VTemp[7]))
          #-----------
          info.close()


       # =========================================================
       # Obtendo as simetrias da rede ============================
       # =========================================================

       #--------------------------------------------------------------------
       # Dicionário de mapeamento de Hermann-Mauguin para Schoenflies ------
       #--------------------------------------------------------------------
       schoenflies = {"1": "C1",  "-1": "Ci",  "2": "C2",  "m": "Cs",  "2/m": "C2h",  "222": "D2",  "mm2": "C2v",  "mmm": "D2h",  "4": "C4",  "-4": "S4",  "4/m": "C4h",
                      "422": "D4",  "4mm": "C4v",  "-42m": "D2d",  "4/mmm": "D4h",  "3": "C3",  "-3": "C3i",  "32": "D3",  "3m": "C3v",  "-3m": "D3d",  "6": "C6",  "-6": "C3h",  
                      "6/m": "C6h",  "622": "D6",  "6mm": "C6v",  "-6m2": "D3h",  "6/mmm": "D6h",  "23": "T",  "m-3": "Th",  "432": "O",  "-43m": "Td",  "m-3m": "Oh"}
       #--------------------------------------------------------------------
       stoichiometry = ''
       #-----------------
       if (n_materials == 1): passo = 1
       if (n_materials >  1): passo = n_materials +1
       #--------------------------------------------
       for i in range(passo):
           #-----------------
           if (i == 0): structure = Poscar.from_file('output/POSCAR').structure
           if (i >  0): structure = Poscar.from_file('output/POSCAR.material_' + str(i)).structure
           analyzer = SpacegroupAnalyzer(structure)
           #----------------------------------------------------
           point_group.append(analyzer.get_point_group_symbol())
           space_group.append(analyzer.get_space_group_symbol())
           space_group_number.append(analyzer.get_space_group_number())
           inversion_symmetry.append(analyzer.is_laue())
           if (i > 0):
              stoichiometry += structure.composition.reduced_formula
              if (i < n_materials): stoichiometry += '+'
           # formula = structure.formula;  formula = formula.replace(' ', '')
           if (i == 0): lattice_type = analyzer.get_lattice_type()
           point_group_schoenflies.append(schoenflies.get(point_group[0], "Desconhecido"))
           #------------------------------------------------------------------------------
           # if (i > 0): os.remove('output/POSCAR.material_' + str(i)) # ERROR !!!!!!!!!!!


       if os.path.isfile('output/z-scan/info_z-scan.dat'):
          #-------------------------------------------------
          zscan = open('output/z-scan/info_z-scan.dat', "r")
          #-------------------------------------------------
          for i in range(3): VTemp = zscan.readline().split()
          z_separation = float(VTemp[2])    
          for i in range(2): VTemp = zscan.readline().split()
          e_binding = float(VTemp[2])
          #------------
          zscan.close()


       if os.path.isfile('output/xy-scan/info_xy-scan.dat'):
          #----------------------------------------------------
          xyscan = open('output/xy-scan/info_xy-scan.dat', "r")
          #----------------------------------------------------
          for i in range(6): VTemp = xyscan.readline().split()
          e_slide = float(VTemp[2])
          #-------------
          xyscan.close()


       #=======================================
       # Obtendo a área no plano XY da rede ===
       #=======================================
       V1 = np.array([A1[0], A1[1]])
       V2 = np.array([A2[0], A2[1]])
       #----------------------------
       # Área da célula no plano XY
       Area_cell = np.linalg.norm(np.cross(V1, V2))
       #-------------------------------------------


       #=======================================
       # Obtendo a área no plano KxKy da ZB ===
       #=======================================
       V1 = np.array([B1[0], B1[1]])
       V2 = np.array([B2[0], B2[1]])
       #----------------------------
       # Área da zb no plano KxKy
       Area_ZB = np.linalg.norm(np.cross(V1, V2))
       #-----------------------------------------


       # ===========================================
       # Criando o Dicionário ======================
       # ===========================================

       dados0 = {
                "id": id_code,
                "id_monolayers": id_materials  if n_materials > 1 else None,
                "formula": formula_quimica,
                "stoichiometry": stoichiometry,
                "number_monolayers": len(label_materials),
                "type_ions_monolayers": t_ions_materials,
                "number_ions_monolayers": nions_materials  if n_materials > 1 else None,
                "number_type_ions_monolayers": t_nions_materials,
                "range_ions_monolayers": r_ions_materials  if n_materials > 1 else None,
                "number_ions": ni,
                "mismatch": mismatch_materials  if n_materials > 1 else None,
                "rotate_angle": rotate_materials  if n_materials > 1 else None,
                "z_separation": z_separation  if n_materials > 1 else None,
                "lattice_type": lattice_type,
                "point_group": point_group,
                # "point_group_schoenflies": point_group_schoenflies,
                "space_group": space_group,
                "space_group_number": space_group_number,
                "inversion_symmetry": inversion_symmetry,
                "pseudo_type": pseudo_type,
                "exchange_correlation_functional": exchange_correlation_functional,
                "vdW": vdW,
                "non_collinear": non_collinear,
                "spin_orbit": spin_orbit,
                "param_a": param,
                "a1": a1,
                "a2": a2,
                "a3": a3,
                "module_a1_a2_a3": module_a1_a2_a3,
                "angle_a1a2_a1a3_a2a3": angle_a1a2_a1a3_a2a3,
                "cell_area": Area_cell,
                "cell_vol": Volume_cell,
                "param_b": fator_rec,
                "b1": b1,
                "b2": b2,
                "b3": b3,
                "module_b1_b2_b3": module_b1_b2_b3,
                "angle_b1b2_b1b3_b2b3": angle_b1b2_b1b3_b2b3,
                "zb_area": Area_ZB,
                "zb_volume": vol_zb,
                "direct_coord_ions": coord_ions,
                }


       if (n == 0):
          #---------
          dados1 = {
                   "lorbit": lorbit,
                   "ispin": ispin,
                   "nk": nk,
                   "nb": nb,
                   "ne": ne,
                   "vbm": vbm,
                   "cbm": cbm,
                   "gap": gap,
                   "type_gap": type_gap,
                   "ki_gap": ki_gap,
                   "kf_gap": kf_gap,
                   "e_fermi": e_fermi,
                   "e_binding": e_binding  if n_materials > 1 else None,
                   "e_slide": e_slide  if n_materials > 1 else None,
                   "total_energy": total_energy,
                   }


       if (n == 1):
          #---------
          dados1 = {
                   "lorbit_SO": lorbit,
                   "ispin_SO": ispin,
                   "nk_SO": nk,
                   "nb_SO": nb,
                   "ne_SO": ne,
                   "vbm_SO": vbm,
                   "cbm_SO": cbm,
                   "gap_SO": gap,
                   "type_gap_SO": type_gap,
                   "ki_gap_SO": ki_gap,
                   "kf_gap_SO": kf_gap,
                   "e_fermi_SO": e_fermi,
                   "e_binding_SO": e_binding  if n_materials > 1 else None,
                   "e_slide_SO": e_slide  if n_materials > 1 else None,
                   "total_energy_SO": total_energy,
                   }


       """
       charge_transfer = '--';  work_function = '--'
       thickness_Z = '--';
       k_path = '--'
       """


       # ==================================================
       # Inserindo as informações no arquivo .json ========
       # ==================================================
       with open('output/info.json', 'r') as file:  data = json.load(file)            # Carregando o conteúdo atual do arquivo info.json
       data.update(dados0)                                                            # Atualizando o dicionário com as novas informações
       with open('output/info.json', 'w') as file: json.dump(data, file, indent=4)    # Salvar o conteúdo atualizado no arquivo info.json
       #----------------------
       with open('output/info.json', 'r') as file:  data = json.load(file)            # Carregando o conteúdo atual do arquivo info.json
       data.update(dados1)                                                            # Atualizando o dicionário com as novas informações
       with open('output/info.json', 'w') as file: json.dump(data, file, indent=4)    # Salvar o conteúdo atualizado no arquivo info.json


# ===============================================
# Abrindo e lendo o data-base .json =============
# ===============================================
with open('output/info.json', "r") as file_json: date = json.load(file_json)
#------------------------------------------------
print(" ")
print("===========================")
print("Dados do arquivo info.json:")
print("===========================")
print(" ")
for chave, valor in date.items(): print(f"{chave}: {valor}")
