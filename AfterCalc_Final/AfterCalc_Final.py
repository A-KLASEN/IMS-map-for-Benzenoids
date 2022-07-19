import shutil
import os
import math

###############################################################################



#Initialisation des Path
source = os.getcwd()
PathLecture = source + "/input/"
PathResultat = source + "/output/"
# if os.path.isdir(PathLecture) == False :
#     os.mkdir(PathLecture)
# if os.path.isdir(PathResultat) == False :
#     os.mkdir(PathResultat)

#destruction ancien "Dossier resultat" et ses fichiers pour reset
shutil.rmtree("output")
os.mkdir("output")

#fichier ignoré lors du traitement
open("Non_conforme.txt",'w').close
reset = False

#Lecture des fichiers 1 par 1
for file_name in os.listdir(PathLecture):
    a = PathLecture + os.path.join(file_name)
    
    reset = False
    if os.path.isfile(a):
        
        #verifie si l'extension du fichier est un .log 
        if file_name[len(file_name)-4:len(file_name)] == ".log" :
            print(a)    
            Index = 0
            #Attribuer tout le texte du log lu à une liste 
            log = open(a, "r")
            loglu = log.readlines()
            loglist = []
            for log_ligne in loglu :
                log_mots = log_ligne.split()
                loglist.append(log_mots)
            log.close()
            
            #Scan fichier pour trouver  "Input orientation" et recup Isotropie des Bq
            new_fileISO = []
            for i in range(0,len(loglist)) :
                if len(loglist[i]) >= 2 :
                    if loglist[i][0] == "Input" :
                        if loglist[i][1] == "orientation:" :
                            repere = i
                    if loglist[i][0] == "Error" and loglist[i][1] == "termination"  :
                        NonConf = open("Non_conforme.txt",'a')
                        NonConf.write(file_name + "   Error termination\n")
                        NonConf.close()
                        reset = True
                if len(loglist[i]) >= 5 :
                    if loglist[i][1] == "Bq" :
                        if loglist[i][2] == "Isotropic" :
                            if loglist[i][5] == "Anisotropy" :
                                new_fileISO.append(loglist[i][4])    
            if reset == True :
                continue
                
           
            #Initialisation variable
            NbrAtoms, NbrBQ = 0, 0
            atoms_Num_XYZ = []
            size_X_coord, size_Y_coord = [0,0], [0,0]
            
            #Stockage des atomes et de leur coordonnée, C et H
            for i in range(repere+5,len(loglist)) :
                stopcountAtoms= loglist[i][0]   
                #arrete la boucle quand fin des données sur position atome
                if stopcountAtoms[0] == "-" :
                    break  
                
                atoms_Num_XYZ.append([loglist[i][1] ,loglist[i][3], loglist[i][4], loglist[i][5]])
                
                if loglist[i][1] == "6" or loglist[i][1] == "1" :   
                    NbrAtoms = NbrAtoms + 1
                if loglist[i][1] == "0" :   
                    NbrBQ = NbrBQ + 1
                    
                    ########################
                    #pour trouver size X et Y 
                    # for n in range(0,2):
                    if size_X_coord[0] > float(loglist[i][3]) :
                        size_X_coord[0] = float(loglist[i][3])
                    if size_X_coord[1] < float(loglist[i][3]) :
                        size_X_coord[1] = float(loglist[i][3])
                    
                    if size_Y_coord[0] > float(loglist[i][4]) :
                        size_Y_coord[0] = float(loglist[i][4])
                    if size_Y_coord[1] < float(loglist[i][4]) :
                        size_Y_coord[1] = float(loglist[i][4])
                    
                    ########################
            size_X = abs(size_X_coord[0]) + abs(size_X_coord[1])
            size_Y = abs(size_Y_coord[0]) + abs(size_Y_coord[1])
            
            
            FlatCount = 0
            for i in range(0,len(atoms_Num_XYZ)) :
                if float(atoms_Num_XYZ[i][3]) == 0.0 :
                    FlatCount = FlatCount + 1
                if float(atoms_Num_XYZ[i][3]) == 1.0 :
                    FlatCount = FlatCount + 1  
                    
            print(FlatCount)
            print(NbrAtoms + NbrBQ)
            if FlatCount == NbrAtoms + NbrBQ :
                Flat = True
                
            if FlatCount != NbrAtoms + NbrBQ :
                
                Flat = False
##############################################################################
            print(Flat)
            if Flat == True :
                
                #Creation fichier dat
                new_file_dat = PathResultat + file_name[0:len(file_name)-4] +".dat"
                open(new_file_dat,'w').close
                
                #Ecriture fichier dat
                Modifier = open(new_file_dat, "a")
                oldX = atoms_Num_XYZ[NbrAtoms][1]
                #NbrAtoms dans la boucle permet de passer directemet au BQ en nbr et indexage
                for i in range(NbrAtoms,len(atoms_Num_XYZ)) :
                    newX = atoms_Num_XYZ[i][1]
                    if newX != oldX :
                        Modifier.write("\n")
                    edit = atoms_Num_XYZ[i][1] + " " + atoms_Num_XYZ[i][2] + " " + new_fileISO[i-NbrAtoms] + "\n"
                    Modifier.write(edit)
                    oldX = atoms_Num_XYZ[i][1]
                Modifier.write("\n\n")

          ################################################   
                  
                BondFile = PathLecture + file_name[2:len(file_name)-4] + "_Bonds.dat"
                Bonds = open(BondFile, "r")
                Bondslu = Bonds.readlines()
                
                for Bonds_ligne in Bondslu :
                    Bonds_mots = Bonds_ligne.split()
                    Index = Index + 1
                    for mot in Bonds_mots :
                        Modifier.write(mot + " ")
                    Modifier.write("\n")
                    
                    
                Bonds.close()
                Modifier.close()
                
 ##############################################################################           
                
    #Création des fichiers.gnu lier au .dat 
                gnu = open("ims_template_squelette.gnu", "r")
                gnulu = gnu.readlines()
                gnulist = []
                for gnu_ligne in gnulu :
                    gnu_mots = gnu_ligne.split()
                    gnulist.append(gnu_mots)
                gnu.close()
                #pour size du canvas
                
                print(size_X,size_Y)
                
                if size_X > size_Y :
                    size_factor = size_X / size_Y
                    size_change = 1
                if size_X < size_Y :
                    size_factor = size_Y / size_X
                    size_change = 2
                if size_X == size_Y :
                    size_change = 3
                for i in range(0,len(gnulist)) :
                    # size du canvas
                    if gnulist[i][0] =="set" and gnulist[i][1] =="term" and gnulist[i][5] =="size" :
                        if size_change == 1 :
                            gnulist[i][6] = str(600*size_factor) + ","
                            gnulist[i][7] = str(600)
                        if size_change == 2 :
                            gnulist[i][6] = str(600) + ","
                            gnulist[i][7] = str(600*size_factor)
                        if size_change == 3 :
                            gnulist[i][6] = str(600) + ","
                            gnulist[i][7] = str(600)
                    
                    # pour x range
                    if gnulist[i][0] =="set" and gnulist[i][1] =="xrange" :
                        gnulist[i][2] = "[" + str(size_X_coord[0]) + ":" + str(size_X_coord[1]) + "]"

                    # pour y range
                    if gnulist[i][0] =="set" and gnulist[i][1] =="yrange" :
                        gnulist[i][2] = "[" + str(size_Y_coord[0]) + ":" + str(size_Y_coord[1]) + "]"
                    
                    #pour xtics
                    if gnulist[i][0] =="set" and gnulist[i][1] =="xtics" :
                        gnulist[i][2] = str(math.floor(size_X_coord[0])) + "," + "2" +  "," + str(math.ceil(size_X_coord[1]))
                    #pour ytics
                    if gnulist[i][0] =="set" and gnulist[i][1] =="ytics" :
                        gnulist[i][2] = str(math.floor(size_Y_coord[0])) + "," + "2" +  "," + str(math.ceil(size_Y_coord[1]))
                        
                    # le nom du fichier pdf
                    if gnulist[i][0] =="set" and gnulist[i][1] =="output" :
                        gnulist[i][2] = "\"" + file_name[0:len(file_name)-4] + ".png" + "\""
                    
                    # Les parametre du premier splot
                    if gnulist[i][0] =="splot" and gnulist[i][4] =="u" and gnulist[i][5] =="1:2:3" :
                        gnulist[i][1] = "\"" + file_name[0:len(file_name)-4] + ".dat" + "\""
                        gnulist[i][3] = "0"
                    # Les parametre du deuxième splot
                    if gnulist[i][0] =="splot" and gnulist[i][4] =="using" and gnulist[i][5] =="1:2:3" :
                        gnulist[i][1] = "\"" + file_name[0:len(file_name)-4] + ".dat" + "\""
                        gnulist[i][3] = "1:" + str(int(Index/4))
                        
                #creation du fichier.gnu
                new_file_gnu = PathResultat + file_name[0:len(file_name)-4] +".gnu"
                open(new_file_gnu,'w').close
                file_gnu_edit = open(new_file_gnu, 'a')
                for i in range(0,len(gnulist)) :
                    for n in range(0,len(gnulist[i])) :
                        file_gnu_edit.write(gnulist[i][n])
                        file_gnu_edit.write(" ")
                    file_gnu_edit.write("\n")
                file_gnu_edit.close()
                
                ###########################
                
                #creation du fichier.txt
                new_file_txt = PathResultat + file_name[0:len(file_name)-4] +".txt"
                open(new_file_txt,'w').close
                file_txt_edit = open(new_file_txt, 'a')
                
                for i in range(0,NbrAtoms) :
                    if atoms_Num_XYZ[i][0] == "6" :
                        file_txt_edit.write("C " + atoms_Num_XYZ[i][1] + " " + atoms_Num_XYZ[i][2] + " " + atoms_Num_XYZ[i][3] + "\n")
                    if atoms_Num_XYZ[i][0] == "1" :
                        file_txt_edit.write("H " + atoms_Num_XYZ[i][1] + " " + atoms_Num_XYZ[i][2] + " " + atoms_Num_XYZ[i][3] + "\n")

                file_txt_edit.write("\n")
                
                #liaisons
                file_txt_edit.write("Liaisons\n\n")
                for Bonds_ligne in Bondslu :
                    Bonds_mots = Bonds_ligne.split()
                    for mot in Bonds_mots :
                        file_txt_edit.write(mot + " ")
                    
                    file_txt_edit.write("\n") 
                
                
                
                Xcount = 1
                Ycount = 0

                file_txt_edit.write("origine " + atoms_Num_XYZ[NbrAtoms][1] + " " + atoms_Num_XYZ[NbrAtoms][2] + " " + atoms_Num_XYZ[NbrAtoms][3] + "\n\n"  )
                Xtest = atoms_Num_XYZ[NbrAtoms][1] 
                Ytest = 0
                for i in range(NbrAtoms,len(atoms_Num_XYZ)) :  
                    if Xtest != atoms_Num_XYZ[i][1] :
                        Xcount = Xcount + 1 
                        Xtest = atoms_Num_XYZ[i][1]

                for i in range(NbrAtoms,len(atoms_Num_XYZ)) :  
                    if Ytest == atoms_Num_XYZ[i][2] :
                        break
                    if Ytest == 0 :
                        Ytest = atoms_Num_XYZ[i][2]
                    Ycount = Ycount + 1

                file_txt_edit.write("V1 0 0.1 0 " + str(Xcount) + "\n")
                file_txt_edit.write("V2 0.1 0 0 " + str(Ycount) + "\n\n")
                Xtest = atoms_Num_XYZ[0][1] 
                for i in range (NbrAtoms,len(new_fileISO)+NbrAtoms) :
                    if Xtest != atoms_Num_XYZ[i][1] :
                        Xtest = atoms_Num_XYZ[i][1]
                        file_txt_edit.write("\n")
                    file_txt_edit.write(new_fileISO[i-NbrAtoms] + "\n")
                    print(i-NbrAtoms)
                file_txt_edit.close()
            
############################################################################################################            
            if Flat == False :
                
                #Creation fichier dat
                new_file_dat = PathResultat + file_name[0:len(file_name)-4] +".dat"
                open(new_file_dat,'w').close
                
                #Ecriture fichier dat
                Modifier = open(new_file_dat, "a")
                # oldX = atoms_Num_XYZ[0][1]
                compteur,compteur2,index1 = 0, 0, 0
                # index = False
                compteurEnd = 40
                
                
                for i in range(-1,-(len(atoms_Num_XYZ)-NbrAtoms)-1,-1) :
                    # newX = new_fileXYZ[0][]
                    if compteur >= compteurEnd :
                        Modifier.write("\n")
                        compteur = 0
                        compteur2 = compteur2 + 1
                    if compteur2 >= compteurEnd :
                        Modifier.write("\n")

                        index1 = index1 +1

                        compteur2 = 0

                    
                    # if atoms_Num_XYZ[i][0] != "0" :
                    #     print("MAUVAIS")
                    #     exit
                    edit = atoms_Num_XYZ[i][1] + " " + atoms_Num_XYZ[i][2] + " " + new_fileISO[i] + "\n"
                    Modifier.write(edit)
                    compteur = compteur +1
                    
                    
                    
                    
                Modifier.write("\n\n")
                # Modifier.close()
            ################################################      
                BondFile = PathLecture + file_name[2:len(file_name)-4] + "_Bonds.dat"
                Bonds = open(BondFile, "r")
                Bondslu = Bonds.readlines()
                Bonds.close()
                
                for Bonds_ligne in Bondslu :
                    Bonds_mots = Bonds_ligne.split()
                    Index = Index + 1
                    for mot in Bonds_mots :
                        Modifier.write(mot + " ")
                    Modifier.write("\n")
                    
                    
                
                Modifier.close()

            ######################################################
                #gnu lier au dat 
                gnu = open("ims_template_squelette.gnu", "r")
                gnulu = gnu.readlines()
                gnulist = []
                for gnu_ligne in gnulu :
                    gnu_mots = gnu_ligne.split()
                    gnulist.append(gnu_mots)
                gnu.close()
                #pour size du canvas
                
                
                # print(size_X,size_Y)
                
                if size_X > size_Y :
                    size_factor = size_X / size_Y
                    size_change = 1
                if size_X < size_Y :
                    size_factor = size_Y / size_X
                    size_change = 2
                if size_X == size_Y :
                    size_change = 3
                for i in range(0,len(gnulist)) :
                    # size du canvas
                    if gnulist[i][0] =="set" and gnulist[i][1] =="term" and gnulist[i][5] =="size" :
                        if size_change == 1 :
                            gnulist[i][6] = str(600*size_factor) + ","
                            gnulist[i][7] = str(600)
                        if size_change == 2 :
                            gnulist[i][6] = str(600) + ","
                            gnulist[i][7] = str(600*size_factor)
                        if size_change == 3 :
                            gnulist[i][6] = str(600) + ","
                            gnulist[i][7] = str(600)
                    
                    # pour x range
                    if gnulist[i][0] =="set" and gnulist[i][1] =="xrange" :
                        gnulist[i][2] = "[" + str(size_X_coord[0]) + ":" + str(size_X_coord[1]) + "]"

                    # pour y range
                    if gnulist[i][0] =="set" and gnulist[i][1] =="yrange" :
                        gnulist[i][2] = "[" + str(size_Y_coord[0]) + ":" + str(size_Y_coord[1]) + "]"
                    
                    #pour xtics
                    if gnulist[i][0] =="set" and gnulist[i][1] =="xtics" :
                        gnulist[i][2] = str(math.floor(size_X_coord[0])) + "," + "2" +  "," + str(math.ceil(size_X_coord[1]))
                    #pour ytics
                    if gnulist[i][0] =="set" and gnulist[i][1] =="ytics" :
                        gnulist[i][2] = str(math.floor(size_Y_coord[0])) + "," + "2" +  "," + str(math.ceil(size_Y_coord[1]))
                        
                    # le nom du fichier pdf
                    if gnulist[i][0] =="set" and gnulist[i][1] =="output" :
                        gnulist[i][2] = "\"" + file_name[0:len(file_name)-4] + ".png" + "\""
                    
                    # Les parametre du premier splot
                    if gnulist[i][0] =="splot" and gnulist[i][4] =="u" and gnulist[i][5] =="1:2:3" :
                        gnulist[i][1] = "\"" + file_name[0:len(file_name)-4] + ".dat" + "\""
                        gnulist[i][3] = "0:" + str(index1)
                    
                    
                    
                    # Les parametre du deuxième splot
                    if gnulist[i][0] =="splot" and gnulist[i][4] =="using" and gnulist[i][5] =="1:2:3" :
                        gnulist[i][1] = "\"" + file_name[0:len(file_name)-4] + ".dat" + "\""
                        gnulist[i][3] = str(index1 + 1) + ":" + str(index1 + 1 + int(Index/4))
                   
                    #Enlever les iso contours
                    if gnulist[i][0] =="set" and gnulist[i][1] =="cont" :
                        gnulist[i][0] = "#set"
                    if gnulist[i][0] =="set" and gnulist[i][1] =="cntrparam" :
                        gnulist[i][0] = "#set"
                        
                #creation du fichier.gnu
                new_file_gnu = PathResultat + file_name[0:len(file_name)-4] +".gnu"
                open(new_file_gnu,'w').close
                file_gnu_edit = open(new_file_gnu, 'a')
                for i in range(0,len(gnulist)) :
                    for n in range(0,len(gnulist[i])) :
                        file_gnu_edit.write(gnulist[i][n])
                        file_gnu_edit.write(" ")
                    file_gnu_edit.write("\n")
                file_gnu_edit.close()
                
                
                
                #############################################################################
                #creation du fichier.txt
                new_file_txt = PathResultat + file_name[0:len(file_name)-4] +".txt"
                open(new_file_txt,'w').close
                file_txt_edit = open(new_file_txt, 'a')
                
                for i in range(0,NbrAtoms) :
                    if atoms_Num_XYZ[i][0] == "6" :
                        file_txt_edit.write("C " + atoms_Num_XYZ[i][1] + " " + atoms_Num_XYZ[i][2] + " " + atoms_Num_XYZ[i][3] + "\n")
                    if atoms_Num_XYZ[i][0] == "1" :
                        file_txt_edit.write("H " + atoms_Num_XYZ[i][1] + " " + atoms_Num_XYZ[i][2] + " " + atoms_Num_XYZ[i][3] + "\n")

                file_txt_edit.write("\n")
                
                #Ecriture des liaisons
                file_txt_edit.write("Liaisons\n\n")
                for Bonds_ligne in Bondslu :
                    Bonds_mots = Bonds_ligne.split()
                    for mot in Bonds_mots :
                        file_txt_edit.write(mot + " ")
                    
                    file_txt_edit.write("\n") 
                
                #ecriture des différentes plaques de BQ
                Xcount = 1
                Ycount = 0
                V1, V2 = [0,0,0], [0,0,0]
                compteurBQ = compteurEnd**2
                compteur3 = 0
                for i in range (NbrAtoms,len(atoms_Num_XYZ)) :
                    
                    if compteur3 == 0 : 
                        file_txt_edit.write("origine " + atoms_Num_XYZ[i][1] + " " + atoms_Num_XYZ[i][2] + " " + atoms_Num_XYZ[i][3] + "\n\n"  )
                
                        for n in range(0,len(V1)):
                            # V1[n] = float(new_fileXYZ[n][i+1]) - float(new_fileXYZ[n][i]) 
                            # V2[n] = float(new_fileXYZ[n][i+compteurEnd]) - float(new_fileXYZ[n][i])
                            
                            V1[n] = float(atoms_Num_XYZ[i+1][n+1]) - float(atoms_Num_XYZ[i][n+1])
                            V2[n] = float(atoms_Num_XYZ[i+compteurEnd][n+1]) - float(atoms_Num_XYZ[i][n+1])

                        file_txt_edit.write("V1" + " " + str(V1[0]) + " "  + str(V1[1]) + " "  + str(V1[2]) + " "  + str(compteurEnd) + "\n")
                        file_txt_edit.write("V2" + " " + str(V2[0]) + " " + str(V2[1]) + " " + str(V2[2]) + " " + str(compteurEnd) + "\n\n")
                    
                    file_txt_edit.write(new_fileISO[i-NbrAtoms])
                    
                    if i != len(atoms_Num_XYZ)-1 :
                        file_txt_edit.write("\n")
                    compteur3 = compteur3 + 1
                    
                    if compteur3 % 40 == 0 and i != len(atoms_Num_XYZ)-1 :
                        file_txt_edit.write("\n")
                    
                    if compteur3 == compteurBQ and i != len(atoms_Num_XYZ)-1 :
                        file_txt_edit.write("\n")
                        compteur3 =0
                if i != len(atoms_Num_XYZ)-1 :
                    file_txt_edit.write("\n")
                
                file_txt_edit.close()
























