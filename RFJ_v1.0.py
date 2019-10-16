
import os
import csv
from pprint import pprint

"""  # General purpose
    ===============
    Ce script contient trois programmes ou classe python:
    - Le premier(Purpose 1 ou P1) a ete implemente afin de supprimer les doublons (replication de lignes) de la table
    job-file-stage (JFS) deja cr\'ee que Christpher m'a signal\'e.

    NB: P1 sera integr\'e dans le 'script_job_file_stage_Plus.py' afin d'optimiser le workflow.
    En effet, ce processus \'a deux etapes, n'est pas une solution perenne donc will probably be 
    move into JFS_plus.py.

    - Le deuxieme(Purpose 2 ou  P2), permet d'etablir la relation entre File et Job (RFJ) d'o\'u le nom du script
    L'idee est, pour chaque file donn\'e, qu'on puisse lister les jobs qui l'utlisent soit en Cible, soit en Source.
    NB: Ces deux scripts s'appuient sur le fichier 'jobName_fileName_truefileName_stageName_idenfiantIO_TypeIO.csv' comme input file et
        qui est le fichier de sortie(output file) de 'script_job_file_stage_Plus.py'.  

    - Le troisieme(Purpose 3), permet d'etablir une relation entre stageCible , StageSource et Fichier. 

    # Mode d'excution des scripts
    --------------------------
    Pour executer un de ces scripts, il faut aller \'a la section 'MAIN <PROGRAMM' qui se trouve en bas du code et 
    ensuite d\'ecommenter la partie qui voous interesse. Par exemple  si vous voulez executer 'MAIN P1', il faut le decommenter
    et ensuite commenter les sections main P2 et P3
    !!! Attention: P1 est completement independant de P2 et P3. Donc vous pouvez l'executer en commentant les deux autres.
                   Cependant, P2 et P3 sont completementaires donc li\'es. En effet, P2 herite de P3 . 
                   P2 prend en parametres deux arguments qui sont les returns des methodes createRFJ et colValueUniq de la classe Rfj
    
"""
########################################
"""Purpose 1:
    --------
    Suppressions des doublons de table 'cf variable path'. 

    Note pour moi (pas important):
    --- 
    voir pourquoi ce fichier ci dessous, a 'CORPSPAR_NOM_FIC_CATEL' apres l'extension:
    /export/home/exp/applications/doc/onide/datastage/source/TMP_FF_PENEF_EXTRANA_ONIDE_20190702150043.csvCORPSPAR_NOM_FIC_CATEL
"""
class SupprimerDoublonsLignesCSV():
    """Cette classe comporte deux principales fonctions et une fonction utilitaire. 
    Les fonctions principales sont <removeCsvLines()> , <writeNewCSV()>.
        - <removeCsvLines()> permet de lire le input file et de supprimer les doublons. 
        - <writeNewCSV()> permet d'enregistrer la nouvelle version (lignes sans doublons)  dans 
        un fichier qui est stock\'e dans vers le chemin precis\'e au niveau des proprietes(fonction init)
    
    La fonction utilitaire <supprimerDoublons()> permet juste supprimer des eventuels doublons au cours du coding.

    La fonction <removeCsvLines()> est execut\'ee en premier. Elle prend inmplitement en parametre le fichier INPUT qui a
    d'eventuels doublons, il s'agit du fichier (job-file-stage (JFS) et retourne une liste de lignes sans doubons.
    Elle genere en retour une liste de lignes sans doublons. Cette liste sera utlis\'e par la fonction writeNewCSV().
    """
    def __init__(self):

        self.rep = r'C:\Users\papas\Desktop\insyco\projet_xml_insyco\xml_log_officiel\resulats_projet_executable'                       # self.rep est le dirname 
        self.pathInput =os.path.join(self.rep,'jobName_fileName_truefileName_stageName_idenfiantIO_TypeIO.csv')        # self.pathinput est le path absolu du fichier input cad le fichier lu en imput
        self.pathOuput =os.path.join(self.rep,'jobName_fileName_truefileName_stageName_idenfiantIO_TypeIO_clean.csv')  # self.pathOuput est path absolu pour renommer le nouveau fichier

    def supprimerDoublons(self, doublonsList):
        ### supprimer doublons(list comprehension methods) 
            # list2=[]
            # list2= [line2 for line2 in list1 if line2 not in list2]
        cleanList = []
        for i in doublonsList:
            if i not in cleanList:
                cleanList.append(i)
        return cleanList
    
    def removeCsvLines(self):

        with open(self.pathInput, 'r') as file1:
            reader = csv.reader(file1)
            # next(reader)
            list1=[line for line in reader]        
            list1_clean = self.supprimerDoublons(list1)

            # list2 = []
            # for i in list1:
            #     if i not in list2:
            #         list2.append(i)
        # return list2
        nb_supprime = len(list1)- len(list1_clean)
        print('Le nombre de lignes de depart est de {}'.format(len(list1)))
        print('Le nombre de lignes apres suppression  est de {}\n Soit {} lignes supprimees '.format( len(list1_clean) , nb_supprime ))
        
        return list1_clean

    ## Ecriture

    def writeNewCSV(self, list1_clean):

        with open(self.pathOuput, 'w') as file2:
            csv_writer = csv.writer(file2)
            for line2 in list1_clean:
                csv_writer.writerow(line2)
        print('Enregistre')

##########################################

"""Purpose 2
    --------
    YANN REQUIREMENT(S) :
    ---------------
    << j'aimerai que en priorite tu puisses nous determiner 
    les relations entre les jobs en se basant sur le nom du fichier.>>

    En tete tableur ['Projet','job','file','truefile','stage','idIO','typeIO']
"""
class Rfj:

    def __init__(self):
        #bien precise le path absolu qui depend bien du type de OS

        self.rep = r'C:\Users\papas\Desktop\insyco\projet_xml_insyco\xml_log_officiel\resulats_projet_executable'
        self.pathOffileOuput = os.path.join(self.rep,'RFJ_basedOnTrueFile.csv')
        self.pathOffileInput = os.path.join(self.rep, 'jobName_fileName_truefileName_stageName_idenfiantIO_TypeIO2.csv')

    def __str__(self):
        return self.pathOffileOuput

    def buildFilePath(self, filepath):
        """cette fonction permet separer un filename du path absolu pour le cas des 'file'"""
        extensions = ['.ds', '.txt', '.csv',' ']
        extensions2 = ['.csv\\(2)0', '.csv\(2)0', '.txt\\(2)0', '.txt\(2)0']
        fileSplitted = filepath.split('#')
        # print(fileSplitted)
        ext = fileSplitted[-1]
        if len(fileSplitted) > 3:
            lastPar = fileSplitted[-2]
            if ext in extensions:
                fic = lastPar+ext
                # print(fic)
            elif ext in extensions2:
                extf = ext.rstrip('.txt\\(2)0')
                fic = lastPar+extf
                # print(fic)
            else:
                fic = lastPar
        else:

            fic = ext.split('/')[-1]
            if r'\('in fic:
                fic = fic.rstrip('\(2)0')
                # print(fic)
            else:
                fic= ext

        return fic

    def splitPath(self, path):
        return os.path.split(path)
    
    def supprimerDoublons(self, doublonsList):
            ### supprimer doublons    (list comprehension methode)
            # list2=[]
            # list2= [line2 for line2 in list1 if line2 not in list2]
        cleanList = []
        for i in doublonsList:
            if i not in cleanList:
                cleanList.append(i)
        return cleanList
            
    def colValueUniq(self, colCible='file'):
        """
            Cette fonction permet d'extraire, nettoyer et collecter l'ensemble des lignes d'une colonne <colCible> (par exemple file ou truefile).
            Elle prend en parametre le nom de la colonne <cible> de la table (JFS) et retourne une liste d'items uniques de cette colonne <colCible> 
            NB1: <colCible> est la colonne Centrale.
            Note : Ameliorer cette fonction pour qu'elle prenne en charge les autres colonnes en tant que colonnes-cilbles. Parce qua ce stade on prend en compte que les 
            les file et les truefiles, stage.

        """
        with open(self.pathOffileInput, 'r') as file1:
            reader = csv.DictReader(file1, delimiter=',')

            # print(reader)
            # Note :next(reader)   # IS FOR reader methods
            # Note :  on peut pas utiliser le curseur deux fois dans un meme context manager

            if colCible == 'truefile':
                colItems = [f[colCible] for f in reader] 
                # ### trie et supprimer des valeurs NaN
                colItems.sort()
                colItems = [l for l in colItems if l != ' ']

                # ### suppression des doublons PATH ABSOLU(path + filename) afin de ne pas avoir une replication des resultats
                colItemsFilter = list(set(colItems))
                colItemsFilter_list = [os.path.split(tf)[1] for tf in colItemsFilter]
                colItemsFilter_list = self.supprimerDoublons(colItemsFilter_list) # Supprimer les doublons filename
                # print(colItemsFilter_list)
                # colItemsIO = [f['typeIO'] for f in reader]
                # print(colItemsIO)

            elif colCible == 'file':
                colItems = [f[colCible] for f in reader]
                colItems.sort()
                # print(len(colItems))
                # colItems = [self.buildFilePath(l) for l in colItems]

                # split du path pour file 
                colItems2 = [] 
                for f in colItems:
                    colCible = self.buildFilePath(f)     # extraire juste le filename
                    colItems2.append(colCible)
                # print(len(colItems2))
                colItemsFilter_list = self.supprimerDoublons(colItems2)
                # print(len(colItemsFilter_list))

            elif colCible == 'stage':
                colItemsFilter = []

                # colItems = [f[colCible]  for f in reader]
                for f in reader:
                    stageAndType = (f['stage'], f['typeIO'], f['truefile'])
                    colItemsFilter.append(stageAndType)

                colItemsFilter_list = colItemsFilter

        return colItemsFilter_list

    def createRFJ(self, colCible='file', colAttachedToCible='job'):
        with open(self.pathOffileInput, 'r') as file1:
            reader = csv.DictReader(file1, delimiter= ',')
            lines = [line for line in reader]
    
            if colCible == 'truefile':
                colItemsFilter_list = self.colValueUniq(colCible)   # appel de la fonction  <metadataVlue()
                rows = []
                for fileS in colItemsFilter_list:
                    for line in lines:
                        fileCibleB = self.splitPath(line[colCible])[1]
                        if fileS == fileCibleB:
                            row = [fileS, line[colAttachedToCible], line['typeIO']]
                            rows.append(row)
                # print(len(rows))
            elif colCible == 'file':
                colItemsFilter_list = self.colValueUniq(colCible)    # appel de la fonction  <metadataVlue()
                rows= []
                for fileS in colItemsFilter_list:
                    for line in lines:
                        # fileCibleB = self.splitPath(line[colCible])[1]
                        fileCibleB = line[colCible]
                        fileCibleB = self.buildFilePath(fileCibleB) # extraire just le filname
                        # print(fileCibleB)
                        if fileS == fileCibleB:
                            row = [fileS, line[colAttachedToCible], line['typeIO']]
                            rows.append(row)

        rows_clean = self.supprimerDoublons(rows)   # suppression des doublons lignes

        return rows_clean

    def writeRFJ_ToCSV(self, rows):
        """
        cette fonction permet d'ecrire en format (enregistrer) les resulats obtenus grace a la fonction <createRFJ()> . 
        Elle prend en entree collection de liste(liste de liste ) Job-file et None"""
        path, name = os.path.split(self.pathOffileOuput)

        with open(self.pathOffileOuput, 'w') as csvfile:
            fieldnames = ['FILE','JOB' ]
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(fieldnames)
            writer.writerows(rows)
            print('Fichier enregistre dans {}\n--> sous le nom: {}!'.format(path, name))

    def displayResultat(self):
        #### En cours d'implimentation
        # # read
        # with open(pathOffileOuput, 'r') as csvfile:
        #     reader = csv.reader(csvfile)
        #     # print(reader)
        #     # print(dict(reader))
        #     for line in reader:
        #         print(line)
        #         # csvfile.write("%s,%s\n" % (key, value))
        pass

"""Purpose 3
    --------
    CHRIS REQUIREMENTS :
    ---------------

"""

class Rsfs(Rfj):
    """ DOCSTRING
        Rsfs : relation Stage Source - file - stage Cible
        Elle herite toutes les methodes definies dans la classe Rfj
     """

    def __init__(self):
        Rfj.__init__(self)
        self.LC = []   # list des items cibles(stage cible,file). 
        self.LS = []   # list des items sources(stage source , file)
        self.pathWrite = os.path.join(self.rep, 'resultatRsfs.csv')

    def removeExt(self, string):
        """Permet d'enlever l'extension du nom 
            Arguments:
                string {[type]} -- [le fichier avec l'extension]
            Returns:
                [tuple] -- [couple nom - ext. cependant on tient compte que du nom]
        """
        if '.' in string:
            l, r = string.split('.')
        else:
            l = string
        return l

    def getListSourceAndListCible(self, colItemsFilter_list, rows):

        for fic in colItemsFilter_list:
            fic = self.removeExt(fic)
            for line in rows:     # lignes du fichier csv
                linef = self.removeExt(line[0])
                lineIO = line[2]
                if fic == linef:     # Cad  les deux fichiers des deux listes sont idem
                    if lineIO == 'Cible':
                        lCible = linef, line[1]
                        self.LC.append(lCible)
                        # print(lCible, 'cible')
                    elif lineIO == 'Source':
                        lSource = line[1], linef
                        self.LS.append(lSource)
                        # print('Source', lSource)
        LS_clean = a.supprimerDoublons(self.LS)
        LC_clean = a.supprimerDoublons(self.LC)
        return LS_clean, LC_clean

    def Write_StgSource_File_StgCible(self,colItemsFilter_list, rows):

        Arows = []
        with open(self.pathWrite,'w') as wf:
            # reader_csv = csv.writer(wf)
            filedNames= "StageSource,File,StageCible\n"
            wf.write(filedNames)   
            LS, LC = self.getListSourceAndListCible(colItemsFilter_list, rows)
            for source in LS:
                for cible in LC:
                    if source[1] == cible[0]:
                        row = source[0]+','+source[1]+','+cible[1]+'\n'
                        # print(row)
                        # row = tuple(row)
                        Arows.append(row)
                        wf.write(row)
                        # reader_csv.writerows(row)
        print("Write ! Its done!")
        pprint(Arows)
        return Arows


###---------------- Programme Main---------------------------------------------------------------------------------------- ###


## Pour memo les schema de la table JFS ['Projet','job','file','truefile','stage','idIO','typeIO']


# ################  MAIN CLASS  SupprimerDoublonsLignesCSV     ###################
                    #-------------------------------------------#
# sD = SupprimerDoublonsLignesCSV.
# # print(len(list1))
# # print(len(list1_clean))

##################  MAIN CLASS  Rfj  #############################################
            #-------------------------------------------#
a = Rfj()
####
colItemsFilter_list = a.colValueUniq('truefile')


# print(colItemsFilter_list)
# print(len(colItemsFilter_list))
# colItemsFilter_list= a.supprimerDoublons(colItemsFilter_list)
# print(len(colItemsFilter_list))

################## Lecture ###################
rows = a.createRFJ('truefile', 'stage')
# pprint(rows)
# print(len(rows))


################# ecriture #############
# a.writeRFJ_ToCSV(rows)


###################  MAIN CLASS  Rfj   ##############################################
                #-------------------------------------------#
#### lecture classe Rsfs() ######
b = Rsfs()
ls, lc = b.getListSourceAndListCible(colItemsFilter_list, rows)
# print(ls)

Arows = b.Write_StgSource_File_StgCible(colItemsFilter_list, rows)
# pprint(Arows)
