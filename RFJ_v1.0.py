
import os
import csv
from pprint import pprint

"""
General purpose
===============
Ce script contient trois programmes:
- Le premier(Purpose 1) a ete implemente afin de supprimer les doublons (replication de lignes) de la table
job-file-stage (JFS) deja cree que Christpher m'a signale.( Probably Will be move into JFS_plus.py )

NB: Integrer ce scrpit dans  script_job_file_stage_Plus.py afin de d'optimiser le workflow. ( Probably Will be 
move into JFS_plus.py ). Ce processus a\' deux etapes n'est pas une solution perenne.

- Le deuxieme(Purpose 2), permet d'etablir la relation entre File et Job (RFJ) d'ou le nom du script. L'idee c'est que, 
pour chaque file donn\'e, lister les jobs qui l'utlisent soit en Cible ou en Source.
NB: ces deux scripts executent en entree le fichier-output nomm\'e 'script_job_file_stage_Plus.py'.  
Pour executer le script  du purpose 1, il faut dabord le decommente et en commenter parallelelement celui 
du Purpose2, et vise-versa.

- Le troisieme(Purpose 3), permet d'etablir une relation entre stageCible , StageSource et Fichier. 

Next Purpose 
-----------
Creer une fonction pour chaque script ou si besoin une classe.

"""
########################################
"""
Purpose 1:
--------
Suppressions des doublons de table 'cf variable path'. 

Note pour moi :
--- 
voir pourquoi ce fichier ci dessous, a 'CORPSPAR_NOM_FIC_CATEL' apres l'extension:
/export/home/exp/applications/doc/onide/datastage/source/TMP_FF_PENEF_EXTRANA_ONIDE_20190702150043.csvCORPSPAR_NOM_FIC_CATEL
"""
class SupprimerDoublonsLignesCSV():
    """Cette classe comporte deux principales fonctions et une fonction utilitaire. 
    Les fonctions principales sont  <removeCsvLines()> ,  <writeNewCSV()> . <removeCsvLines()> permet de lire
    en supprimant les doublons et la fonction <removeCsvLines()> est la phase d'ecriture <writeNewCSV()> .
    La fonction utilitaire <supprimerDoublons()> 

    La fonction <removeCsvLines()> est execut\'e en premier. Elle prend en entree un fichier INPUT avec eventuellement
    des doublons (job-file-stage (JFS), en l'occurence) et retourne une liste de lignes sans doubons.
    Elle genere en retour une liste de lignes sans doublons. Cette liste sera utlis\'e par la fonction writeNewCSV().

    La fonction writeNewCSV()  un fichier qui est stock\'e dans vers le chemin precis\'e au niveau des proprietes
    (fonction init)
    """
    def __init__(self):
        self.rep = '/Users/ganasene/Downloads/projet_xml_insyco/code/resulats_projet_executable'
        self.pathInput =os.path.join(self.rep,'jobName_fileName_truefileName_stageName_idenfiantIO_TypeIO.csv')
        self.pathOuput =os.path.join(self.rep,'jobName_fileName_truefileName_stageName_idenfiantIO_TypeIO_clean.csv')

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

 

###########################################################################

"""
Purpose 2
--------
YANN REQUIREMENT(S) :
---------------
 << j'aimerai que en priorite tu puisses nous determiner 
les relations entre les jobs en se basant sur le nom du fichier.>>

En tete tableur ['Projet','job','file','truefile','stage','idIO','typeIO']
"""
class Rfj:

    def __init__(self):

        self.rep ='/Users/ganasene/Desktop/insyco/projet_xml_insyco/code/resulats_projet_executable'
        self.pathOffileOuput = os.path.join(rep,'RFJ_basedOnTrueFile.csv')
        self.pathOffileInput = os.path.join(rep, 'jobName_fileName_truefileName_stageName_idenfiantIO_TypeIO2.csv')

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
        """cette fonction permet d'extraire, nettoyer et collecter les lignes de la  colonne <colCible>(par exemple file ou truefile)
        Elle prend en entree le nom de la colonne cible de la table (JFS) et retourne une liste d'items uniques de cette colonne <colCible> 
        NB1: <colCible> est la colonne Centrale
        Note : Ameliorer cette fonction pour qu'elle prend en charge les autres colonnes en tant que colonnes-cilbles. Parce qua ce stade on prend en compte que les 
        les file et les truefiles """
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

            # elif colCible == 'file':
            #     colItemsFilter_list = self.colValueUniq(colCible)    # appel de la fonction  <metadataVlue()
            #     rows= []
            #     for fileS in colItemsFilter_list:
            #         for line in lines:
            #             # fileCibleB = self.splitPath(line[colCible])[1]
            #             fileCibleB = line[colCible]
            #             fileCibleB = self.buildFilePath(fileCibleB) # extraire just le filname
            #             # print(fileCibleB)
            #             if fileS == fileCibleB:
            #                 row = [fileS, line[colAttachedToCible]]
            #                 rows.append(row)
        # print(len(rows))
        rows_clean = self.supprimerDoublons(rows)   # suppression des doublons lignes

        return rows_clean

    def writeRFJ_ToCSV(self, rows):
        '''cette fonction permet d'ecrire (enregistrer) les resulats obtenus grace a la fonction <createRFJ()> , en format csv. 
        Elle prend en entree collection de liste(liste de liste ) Job-file et None'''
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


"""
Purpose 3
--------
CHRIS REQUIREMENTS :
---------------

"""

class Rsfs(Rfj):
    """ Rsfs : relation Stage Source - file - stage Cible
    Elle herite toutes les methodes definies dans la classe Rfj """

    def removeExt(self, string):
        """
        Permet d'enlever l'extension du nom 
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
        LC = []
        LS = []
        for fic in colItemsFilter_list:
            fic = self.removeExt(fic)
            for line in rows:     # lignes du fichier csv
                linef = self.removeExt(line[0])
                lineIO = line[2]
                if fic == linef:     # cad  les deux fichiers des deux listes sont idem
                    if lineIO == 'Cible':
                        lCible = linef, line[1]
                        LC.append(lCible)
                        print(lCible, 'cible')
                    elif lineIO == 'Source':

                        lSource = line[1], linef
                        LS.append(lSource)
                        print('Source', lSource)
        LS = a.supprimerDoublons(LS)
        LC = a.supprimerDoublons(LC)
        return LS, LC

    def Write_StgSource_File_StgCible(self, LS, LC):
        rows = []
        for source in LS:
            for cible in LC:
                if source[1] == cible[0]:
                    row = source[0]+','+source[1]+','+cible[1]+'\n'
                    # row = tuple(row)
                    rows.append(row)
        pprint(rows)
        return rows




###---------------- Programme Main---------------------------------------------------------------------------------------- ###

## Pour memo les schema de la table JFS ['Projet','job','file','truefile','stage','idIO','typeIO']
rep = "/Users/ganasene/Desktop/insyco/projet_xml_insyco/code/resulats_projet_executable"
# pathOffileInput = os.path.join(rep, 'jobName_fileName_truefileName_stageName_idenfiantIO_TypeIO2.csv')
pathOffileOuput = os.path.join(rep, 'RFJ_fileCentertris.csv')


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
lrow = b.Write_StgSource_File_StgCible(ls, lc)
