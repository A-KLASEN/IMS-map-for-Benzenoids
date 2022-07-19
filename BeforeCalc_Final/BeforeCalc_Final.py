###############################################################################
import shutil
import os
from openbabel import openbabel
import rdkit.Chem
import numpy as np
from skspatial.objects import Plane
from skspatial.objects import Points


#destruction ancien "output" et ses fichiers pour reset
source = os.getcwd()
shutil.rmtree("output")
os.mkdir("output")

#Initialisation des Path
PathLecture = source + "/input/"
PathResultat = source + "/output/"
PathBonds = source + "/bonds/"
#Creation du fichier où son stocker le nom des fichiers non traiter et la raison
open("Non_conforme.txt",'w').close
###############################################################################
#copier du code de yannick sur ims3D

class MolecularGraph():

    def __init__(self, geomfile, out):
        mol_filename = generate_mol(geomfile, None, out)
        self.molecule = rdkit.Chem.MolFromMolFile(mol_filename, removeHs=False)
        
    def getCycles(self):
        return self.molecule.GetRingInfo().AtomRings()

    def getEdges(self):
        return self.molecule.GetBonds()
    
    def getnum(self):
        return self.molecule.GetNumAtoms()
      
    def getbonds(self):
        return self.molecule.GetNumBonds()
    
def generate_mol(geomfile, logger, out):
    #mol_filename = "tmpfile_{:05d}.mol".format(int(random.uniform(0, 99999)))
    mol_filename = PathResultat + file_name[0:len(file_name)-4] + ".mol"
    print(mol_filename)
    obConversion = openbabel.OBConversion()
    obConversion.SetInAndOutFormats("xyz", "mol")

    mol = openbabel.OBMol()
    obConversion.ReadFile(mol, geomfile)
    obConversion.WriteFile(mol, mol_filename)

    return mol_filename

###############################################################################
#copier sur internet

def rotation_matrix_from_vectors(vec1, vec2):
    """ Find the rotation matrix that aligns vec1 to vec2
    :param vec1: A 3d "source" vector
    :param vec2: A 3d "destination" vector
    :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
    """
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
    return rotation_matrix

###############################################################################

def lectureFile() :
    # Attribuer tout le texte du xyz lu à une liste 
    log = open(a, "r")
    loglu = log.readlines()
    log.close()
    loglist = []
    for log_ligne in loglu :
        log_mots = log_ligne.split()
        loglist.append(log_mots)
    return loglist
###############################################################################

def ATOMSlist_xyz(loglist) :
    #recup atoms range depart a 2 pour eviter nbr atom et energy
    init_xyz,init_atom = [], []
    NbrAtoms,nbr_H = 0, 0
    for i in range(2,len(loglist)) : 
        init_atom.append(loglist[i][0])
        if loglist[i][0] == "H" :
            nbr_H = nbr_H + 1
        init_xyz.append([float(loglist[i][1]),float(loglist[i][2]),float(loglist[i][3])])
        NbrAtoms = NbrAtoms + 1
    energy = loglist[1][1]
    return init_xyz, init_atom, NbrAtoms, nbr_H , energy
###############################################################################

def ATOMSlist_log(loglist) :
    #Scan fichier pour trouver dernier "Standard orientation" ou pou annuler le traitement du fichier
    Standard = False
    repere = 0
    for i in range(-1,-len(loglist),-1) :
        if len(loglist[i]) >= 2 :
            if loglist[i][0] == "Standard" and loglist[i][1] == "orientation:" :
                repere = len(loglist) + i
                Standard = True       
                break
    print(repere)
    if Standard == False :
        for i in range(-1,-len(loglist),-1) :
            if len(loglist[i]) >= 2 :
                if loglist[i][0] == "Input" and loglist[i][1] == "orientation:" :
                    repere = len(loglist) + i
                    Standard = True
                    print("on trouve finalement " + str(repere) + " comme repere")
                    break

    # if Standard == False :
    #     NonConf = open("Non_conforme.txt",'a')
    #     NonConf.write(file_name + "   Standard orientation non présent\n")
    #     NonConf.close()
    #     continue
    # Opt = False
    # if Opt == True :
    #     NonConf = open("Non_conforme.txt",'a')
    #     NonConf.write(file_name + "   Fichier opt présent\n")
    #     NonConf.close()
    #     # continue

    #Stockage des atomes et de leur coordonnée, C et H
    init_xyz,init_atom = [], []
    NbrAtoms,nbr_H = 0, 0
    for i in range(repere+5,len(loglist)) :
        #arrete la boucle quand fin des données sur position atome
        stopcountAtoms= loglist[i][0]   
        if stopcountAtoms[0] == "-" :
            break
        
        if loglist[i][1] == "6" or loglist[i][1] == "1" :
            if len(loglist[i]) < 6 :
                NonConf = open("Non_conforme.txt",'a')
                NonConf.write(file_name + "   Manque une coordonée sur le log\n")
                NonConf.close()
                continue
            if loglist[i][1] == "6" :
                init_atom.append("C")
            if loglist[i][1] == "1" :
                init_atom.append("H")
                nbr_H = nbr_H + 1
            # for n in range(0,len(new_fileXYZ)) :
                # init_xyz.append (loglist[i][n+3])
            init_xyz.append([float(loglist[i][3]),float(loglist[i][4]),float(loglist[i][5])])
        NbrAtoms = NbrAtoms + 1
    return init_xyz, init_atom, NbrAtoms, nbr_H
###############################################################################

def flatCheck(init_xyz) :
    #on check si molécule est plate avant traitement
   
    xyz_max, xyz_min, xyz = [0,0,0], [0,0,0], ["x","y","z"]
    for i in range(0,len(init_xyz)) :
        for n in range(0,len(init_xyz[i])) :
            if xyz_max[n] < init_xyz[i][n] :
                xyz_max[n] = init_xyz[i][n]
            if xyz_min[n] > init_xyz[i][n] :
                xyz_min[n] = init_xyz[i][n]
    dimension = [0,0,0] 
    dimensionCheck = 0
    for i in range(0,len(dimension)) : 
        dimension[i] = xyz_max[i] - xyz_min[i]
        if dimension[i] == 0 :
            aligner = xyz[i]
            dimensionCheck = dimensionCheck + 1
    if dimensionCheck == 0 :
        print("Molécule non plate")
        return False, "plate", False, xyz_max, xyz_min
    
    if dimensionCheck == 1 :
        print("Molécule plate avec axe perpendiculaire sur " + aligner)
        if aligner == "x" or aligner == "y" :
            alignement_ou_pas = True
        if aligner == "z" :
            alignement_ou_pas = False
        return alignement_ou_pas, aligner, True, xyz_max, xyz_min
        
        
    if dimensionCheck > 1 :
        print("C'est un baton t'as molécule de merde")
        return 

###############################################################################

def alignement(init_xyz) : 

    rota_xyz = np.array([init_xyz[0]])
    for i in range(1,len(init_xyz)):
        rota_xyz = np.append(rota_xyz, [init_xyz[i]], axis = 0)
    
    points = Points([init_xyz[0]])
    for i in range(1,len(init_xyz)):
        points = np.append(points, [init_xyz[i]], axis = 0)
    
    plane = Plane.best_fit(points)
    Normal_init = plane.normal
    
    #Matrice de rotation et rotation
    mat = rotation_matrix_from_vectors(Normal_init,[0,0,1])
    rota_finish = np.dot(points, mat.T)
    
    for i in range(0,len(init_xyz)) :
        for n in range(0,len(init_xyz[i])) :
            init_xyz[i][n] = float(rota_finish[i,n])
    
    return init_xyz
    # #creation nv fichier xyz
    # rota = b[0:len(b)-4] + "_rota.xyz"
    # open(rota,'w').close
    # new_rota = open(rota,'a')
    
    # new_rota.write(loglist[0][0] + "\n")
    # new_rota.write(loglist[1][0] + " " + loglist[1][1] + "\n")
    # for i in range(0,len(init_atom)) :
    #     new_rota.write(init_atom[i] + " ")
    #     edit = str(rota_finish[i,0]) + " " + str(rota_finish[i,1]) + " " + str(rota_finish[i,2]) + "\n"
    #     new_rota.write(edit)
    # new_rota.close()
###############################################################################

def alignementSoft(init_xyz, aligner, xyz_max, xyz_min) : 
    init_xyz_soft, xyz_max_soft, xyz_min_soft = [], [], []

    if aligner == "x" :
        for i in range(0,len(init_xyz)) :
            # for n in range(0,len(init_xyz[i])) :
            init_xyz_soft.append([init_xyz[i][1], init_xyz[i][2], init_xyz[i][0]])

        xyz_max_soft = [xyz_max[1], xyz_max[2], xyz_max[0]]
        xyz_min_soft = [xyz_min[1], xyz_min[2], xyz_min[0]]
        

    if aligner == "y" :
        for i in range(0,len(init_xyz)) :
            init_xyz_soft.append([init_xyz[i][2], init_xyz[i][0], init_xyz[i][1]])

        xyz_max_soft = [xyz_max[2], xyz_max[0], xyz_max[1]]
        xyz_min_soft = [xyz_min[2], xyz_min[0], xyz_min[1]]

    return init_xyz_soft, xyz_max_soft, xyz_min_soft

###############################################################################

def rotafile(init_xyz, NbrAtoms, init_atom) :
    #creation nv fichier xyz
    rota_file = b[0:len(b)-4] + "_rota.xyz"
    open(rota_file,'w').close
    new_rota = open(rota_file,'a')
    
    new_rota.write(str(NbrAtoms) + "\n")
    new_rota.write("Energy: " + "-200" + "\n")
    for i in range(0,len(init_atom)) :
        new_rota.write(init_atom[i] + " ")
        edit = str(init_xyz[i][0]) + " " + str(init_xyz[i][1]) + " " + str(init_xyz[i][2]) + "\n"
        new_rota.write(edit)
    new_rota.close()

    return rota_file

###############################################################################

def BQflat(xyz_max, xyz_min) :
    
    #on étend les bordures
    for i in range(0,len(xyz_max)) :
        xyz_max[i] = xyz_max[i] + 0.5
        xyz_min[i] = xyz_min[i] - 0.5
    
    #on génére le quadrillage de la grille (ligne/colonne)
    bq_xy_bordure = [[],[]]
    Step = 0.1
    for i in range(0,len(bq_xy_bordure)) :
        bq_xy_bordure[i] = np.arange(start=xyz_min[i],stop=xyz_max[i],step=Step)
    
    # print(bq_xy_bordure)
    #Creation des BQ
    bq_xyz = []
    for x in bq_xy_bordure[0] :
        for y in bq_xy_bordure[1] :
            bq_xyz.append([x, y, float(1)])
    
    return bq_xyz

###############################################################################    

def rdkit_init(rota_file) :
    
    mdl_file = MolecularGraph(rota_file,b)

    return mdl_file

###############################################################################

def rdkit_bonds(mdl_file, init_xyz, ) :
    
    Bonds = mdl_file.getEdges()
    
    init_bonds = []
    init_bonds_idx = []
    
    for i in Bonds :
        
        init_bonds_idx.append([])
        init_bonds.append([])
        
        y = len(init_bonds)-1 
        
        x = i.GetBeginAtomIdx()
        init_bonds_idx[y].append(x)
        z = i.GetBeginAtom()
        init_bonds_idx[y].append(z.GetAtomicNum())
        
        for n in range(0,len(init_xyz[x])) :
            init_bonds[y].append(init_xyz[x][n])
        
        
        x = i.GetEndAtomIdx()
        init_bonds_idx[y].append(x)
        z = i.GetEndAtom()
        init_bonds_idx[y].append(z.GetAtomicNum())
         
        for n in range(0,len(init_xyz[x])) :
            init_bonds[y].append(init_xyz[x][n])
            
    return init_bonds, init_bonds_idx

    
###############################################################################
    
def rdkit_bonds_file(init_bonds) :

    BondFile = PathResultat + file_name[0:len(file_name)-4] + "_Bonds.dat"
    open(BondFile,'w').close
    file = open(BondFile,'a')
    count = 0
    for i in range(0,len(init_bonds)) :
        for x in range(0,len(init_bonds[i])) :
            file.write(str(init_bonds[i][x]))
            count = count + 1
            
            if count != 3 :
                file.write(" ")
            
            if count == 3 :
                file.write("\n")
                count = 0
        file.write("\n\n")
    file.close()   
    

###############################################################################
    
def rdkit_bonds_file3D(init_bonds, CoordProject) :

    BondFile = PathResultat + file_name[0:len(file_name)-4] + "_Bonds.dat"
    open(BondFile,'w').close
    file = open(BondFile,'a')
    count = 0
    for i in range(0,len(init_bonds)) :
        for x in range(0,len(init_bonds[i])) :
            file.write(str(init_bonds[i][x]))
            count = count + 1
            
            if count != 3 :
                file.write(" ")
            
            if count == 3 :
                file.write("\n")
                count = 0
        file.write("\n\n")
    file.write("Stop\n")
    
    
    for i in range(0,len(CoordProject)) :
        X = str((CoordProject[i][0]/CoordProject[i][3]))
        Y = str((CoordProject[i][1]/CoordProject[i][3]))
        Z = str((CoordProject[i][2]/CoordProject[i][3]))
        file.write(X + " " + Y + " " + Z + "\n")
    
    file.close()   
    
    
    

###############################################################################

def BQ3D_3Dbonds(mdl_file, init_xyz, init_bonds, init_bonds_idx  ) :

            
    AllCycles = mdl_file.getCycles()
    bq_xyz = []
    

    CoordProject = []
    for i in range(0,len(init_xyz)) :
        CoordProject.append([0,0,0,0])
    
    for Cycle in AllCycles :

        centre = [0,0,0]

        ATOM = []
        
        #additionne coordonnée des atome du cycle
        for atoms in Cycle : 
            
            centre[0] = centre[0] + float(init_xyz[atoms][0])
            centre[1] = centre[1] + float(init_xyz[atoms][1])
            centre[2] = centre[2] + float(init_xyz[atoms][2])

            
            ATOM.append([float(init_xyz[atoms][0]),float(init_xyz[atoms][1]),float(init_xyz[atoms][2])])
            
        #calcul le centre du cycle       
        for c in range(0,len(centre)) :
            centre[c] = centre[c]/6
        
        ATOM.append([float(centre[0]),float(centre[1]),float(centre[2])])
       
        points = Points([[ATOM[0][0],ATOM[0][1],ATOM[0][2]],[ATOM[1][0],ATOM[1][1],ATOM[1][2]],[ATOM[2][0],ATOM[2][1],ATOM[2][2]],[ATOM[3][0],ATOM[3][1],ATOM[3][2]],[ATOM[4][0],ATOM[4][1],ATOM[4][2]],[ATOM[5][0],ATOM[5][1],ATOM[5][2]],[ATOM[6][0],ATOM[6][1],ATOM[6][2]]])
        
        plane = Plane.best_fit(points)
        Normal = plane.normal
        
        nvcentre = [float(centre[0]+(Normal[0])),float(centre[1]+(Normal[1])),float(centre[2]+(Normal[2]))]
        
        #on génére le quadrillage de la grille (ligne/colonne)
        bq_xy_bordure = [[],[]]
        Step = 0.1
        Start = 0
        Stop = 4
        
        for i in range(0,len(bq_xy_bordure)) :
            bq_xy_bordure[i] = np.arange(start=Start,stop=Stop,step=Step)
        
        # print(bq_xy_bordure)
        #Creation des BQ
        bq_xyz_temp = []
        for x in bq_xy_bordure[0] :
            for y in bq_xy_bordure[1] :
                bq_xyz_temp.append([x, y, float(0)])
        
        #return bq_xyz
        
        Norme = np.array([Normal[0],Normal[1],Normal[2]])
        # Norme2 = np.array([[Normal[0],Normal[1],Normal[2]]])
        BQVector = np.array([0,0,1])
        # BQVector2 = np.array([[0,0,1]])

        
        BQCoord = np.array([[bq_xyz_temp[0][0],bq_xyz_temp[0][1],bq_xyz_temp[0][2]]])
        for i in range(1,len(bq_xyz_temp)):
            BQCoord = np.append(BQCoord, [bq_xyz_temp [i]], axis = 0)
        
          
        mat = rotation_matrix_from_vectors(BQVector,Norme)

        BQCoord2 = np.dot(BQCoord, mat.T)
        
        moyenne = (BQCoord2[0] + BQCoord2[len(BQCoord2)-1])/2
        correction = np.array(nvcentre) - moyenne
        
        for i in range(0,len(BQCoord2)) :
            BQCoord2[i,0] = BQCoord2[i,0] + correction[0]
            BQCoord2[i,1] = BQCoord2[i,1] + correction[1]
            BQCoord2[i,2] = BQCoord2[i,2] + correction[2]
        
        if Norme[2] < 0 : 
            for i in range(0,len(BQCoord2)) :
                BQCoord2[i,0] = BQCoord2[i,0] + ((Norme[0]*2)*-1)
                BQCoord2[i,1] = BQCoord2[i,1] + ((Norme[1]*2)*-1)
                BQCoord2[i,2] = BQCoord2[i,2] + ((Norme[2]*2)*-1)
        
        for i in range(0,len(bq_xyz_temp)) :
            bq_xyz.append([BQCoord2[i,0], BQCoord2[i,1], BQCoord2[i,2]])

        

        for atoms in Cycle :

            for i in range(0,3) :
                if Normal[2] < 0 : 
                    CoordProject[atoms][i] = CoordProject[atoms][i] + (Normal[i]*-1)
                if Normal[2] > 0 :   
                    CoordProject[atoms][i] = CoordProject[atoms][i] + Normal[i]
            CoordProject[atoms][3] = CoordProject[atoms][3] + 1
            

            for i in range(0,len(init_bonds_idx)) : 
                H_idx = -1
                if atoms == init_bonds_idx[i][0] and init_bonds_idx[i][3] == 1 :
                    H_idx =  init_bonds_idx[i][2]
                if atoms == init_bonds_idx[i][2] and init_bonds_idx[i][1] == 1 :
                    H_idx =  init_bonds_idx[i][0]
                if H_idx == -1:
                    continue
                
                for i in range(0,3) :
                    if Normal[2] < 0 : 
                        CoordProject[H_idx][i] = CoordProject[H_idx][i] + (Normal[i]*-1)
                    if Normal[2] > 0 :   
                        CoordProject[H_idx][i] = CoordProject[H_idx][i] + Normal[i]
                CoordProject[H_idx][3] = CoordProject[H_idx][3] + 1
    

    for i in range(0,len(init_bonds_idx)) :
        # if init_bonds[i][0]_idx == 
        for n in range(0,3) :
            init_bonds[i][n] = init_bonds[i][n] + (CoordProject[init_bonds_idx[i][0]][n]/CoordProject[init_bonds_idx[i][0]][3])
        for n in range(3,6) :
            
            init_bonds[i][n] = init_bonds[i][n] + (CoordProject[init_bonds_idx[i][2]][n-3]/CoordProject[init_bonds_idx[i][2]][3])
    

    return bq_xyz, init_bonds, CoordProject

###############################################################################

def ecriture(nbr_H, init_atom, init_xyz, bq_xyz, file_name, PathResultat) :
    
    #Calcul multiplicite molecule
    if nbr_H%2 == 0 :
        multiplicite = "1"
    if nbr_H%2 == 1 :
        multiplicite = "2"  
    
    # create_file = PathResultat + file_name[0:len(file_name)-3] + "com"
    
    
    #texte début fichier 
    Parametre = "%nproc=8\n%mem=32GB\n"
    Intro = "#P Ub3lyp/6-311++G(d,p) SCF(Tight) CPHF(Separate) Int(Grid=SuperFine) NMR geom=connectivity guess=mix\n\n"
    Intro2 = "#P Rb3lyp/6-311++G(d,p) SCF(Tight) CPHF(Separate) Int(Grid=SuperFine) NMR geom=connectivity\n\n"
    StateMulti = "0 " + multiplicite + "\n"
    
    Title = "U_" + file_name[0:len(file_name)-4] + "\n\n"
    create_file = PathResultat + "U_" + file_name[0:len(file_name)-4] + ".com"
    
    open(create_file,'w').close
    file_com = open(create_file,'a')
    
    file_com.write(Parametre + Intro + Title + StateMulti)

    nbr = 0
    #ecriture des atomes C et H
    for i in range(0,len(init_atom)) :
        edit = init_atom[i] + " " + str(init_xyz[i][0]) + " " + str(init_xyz[i][1]) + " " + str(init_xyz[i][2]) + "\n"
        nbr = nbr + 1
        file_com.write(edit)
    
    #ecriture des bq
    for i in range(0,len(bq_xyz)) :
        edit = "Bq " + str(bq_xyz[i][0]) + " " + str(bq_xyz[i][1]) + " " + str(bq_xyz[i][2]) + "\n"
        nbr = nbr + 1
        file_com.write(edit)  
    file_com.write("\n")  
    
    for i in range(1,nbr+1) :
        edit = str(i) + "\n"
        file_com.write(edit)  
    
    #cree le R_ si multiplicité 1
    if multiplicite == "1" :
        
        Title = "R_" + file_name[0:len(file_name)-4] + "\n\n"
        create_file = PathResultat + "R_" + file_name[0:len(file_name)-4] + ".com"
        
        open(create_file,'w').close
        file_com = open(create_file,'a')
        
        file_com.write(Parametre + Intro2 + Title + StateMulti)

        nbr = 0
        #ecriture des atomes C et H
        for i in range(0,len(init_atom)) :
            edit = init_atom[i] + " " + str(init_xyz[i][0]) + " " + str(init_xyz[i][1]) + " " + str(init_xyz[i][2]) + "\n"
            nbr = nbr + 1
            file_com.write(edit)
        
        #ecriture des bq
        for i in range(0,len(bq_xyz)) :
            edit = "Bq " + str(bq_xyz[i][0]) + " " + str(bq_xyz[i][1]) + " " + str(bq_xyz[i][2]) + "\n"
            nbr = nbr + 1
            file_com.write(edit)  
        file_com.write("\n")  
        
        for i in range(1,nbr+1) :
            edit = str(i) + "\n"
            file_com.write(edit)  
    
    
    
    
    
    
    
    
    file_com.close()
    
###############################################################################



#Lecture des fichiers 1 par 1
for file_name in os.listdir(PathLecture):
    # Standard, Opt = False, False
    # Optcheck, Ocheck, repere = 0, 0, 0
    a = PathLecture + os.path.join(file_name)
    b = PathResultat + os.path.join(file_name)
    if os.path.isfile(a):
        file = 0
        #verifie l'extension du fichier pour choix du traitement
        if file_name[len(file_name)-4:len(file_name)] == ".xyz" :
            file = "xyz"
        if file_name[len(file_name)-4:len(file_name)] == ".log" :
            file = "log"
        if file == 0 : 
            continue
        print(a)
        
        loglist = lectureFile()
        
        if file == "xyz" :
            print("xyz")
            init_xyz, init_atom, NbrAtoms, nbr_H , energy = ATOMSlist_xyz(loglist)
        
        if file == "log" :
            print("log")
            init_xyz, init_atom, NbrAtoms, nbr_H = ATOMSlist_log(loglist)
        
        alignement_ou_pas, aligner, flat, xyz_max, xyz_min = flatCheck(init_xyz)
        
        
        #on l'aligne et on tente de voir si elle plate au final
        if flat == False :
            init_xyz = alignement(init_xyz)
            alignement_ou_pas, aligner, flat, xyz_max, xyz_min = flatCheck(init_xyz)
            
        
        #On généreles BQ 
        if flat == True :
            if aligner == "y" or aligner == "x"  :    
                init_xyz, xyz_max, xyz_min = alignementSoft(init_xyz, aligner, xyz_max, xyz_min)
                
            bq_xyz = BQflat(xyz_max, xyz_min)
                
            ecriture(nbr_H, init_atom, init_xyz, bq_xyz, file_name, PathResultat)
            
            rota_file = rotafile(init_xyz, NbrAtoms, init_atom)
            mdl_file = rdkit_init(rota_file)
            init_bonds, init_bonds_idx = rdkit_bonds(mdl_file, init_xyz, )
            rdkit_bonds_file(init_bonds)
            
            continue
            
        
        
        if flat == False :
            
            rota_file = rotafile(init_xyz, NbrAtoms, init_atom)
            mdl_file = rdkit_init(rota_file)
            init_bonds, init_bonds_idx = rdkit_bonds(mdl_file, init_xyz, )
            
            bq_xyz, init_bonds, CoordProject = BQ3D_3Dbonds(mdl_file, init_xyz, init_bonds, init_bonds_idx  )
            
            rdkit_bonds_file3D(init_bonds, CoordProject)
            
            ecriture(nbr_H, init_atom, init_xyz, bq_xyz, file_name, PathResultat)
            
            
            
            
            
            
            