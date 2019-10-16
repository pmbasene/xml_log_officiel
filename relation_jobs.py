#coding: utf8

from class_job import *

""" cette classe me servira de module pour tous les parsing que j'aurais à faire"""



#---- Mes notes
# Note1: !!! n'oublie pas le message ID de la section concernée
# !!! les messages Id generee par les jobs sont du type:
#                IIS-DSTAGE-RUN-I-0070           debut du job :  ou sont definis tous les paramtres
#                IIS-DSTAGE-RUN-I-0126           lister l' environnement utilisé par Datastage
#                IIS-DSTAGE-RUN-E-0268
#                IIS-DSTAGE-RUN-I-0019
#                IIS-DSTAGE-RUN-I-0034
#                IIS-DSTAGE-RUN-I-0019
#                IIS-DSTAGE-RUN-I-0019
#                IIS-DSTAGE-RUN-I-00..
#                IIS-DSTAGE-RUN-I-0034
#                IIS-DSTAGE-RUN-I-0034
#                IIS-DSTAGE-RUN-I-0077           fin du job

# !!! La methode blocEventId ne capte (ignore) le id suivant de chaque job puisque ce dernier car ne contient aucnune information utile 

#---- My insights
# insight 1 : !!! essayeer dintegrer elasticsearch danas le code




############### main ###################
#########################################
# if __name__ == "__main__":
        
workdir = '/Users/ganasene/Desktop/insyco/doc/temp'                   # path ou se trouve les excecutables(jobs)

os.chdir(workdir)                                              # os.chdir permet de changer de repertoire  prend comme argument le path "wordir". Elle ne retourne rien
# Les lignes suivantes  permettent de supprimer le fichier .DS_Store de mac present dans les dossier et qui me nargue a chaque execution ;). Ce fichier est propre au mac.
for jobname in os.listdir(workdir): 
    if jobname == '.DS_Store':
        subprocess.call(['rm', '.DS_Store'])
        print('... Suppression du fichier cachee .DS_Store dans le  rep {}'.format(os.getcwd()))
    else:
        pass
 ######

thread = CreeRelation(workdir)                          # instanciation du premier objet                      
files = thread.listFileInDir()                          # files stocke tous les fichiers(jobs)
paths = thread.absoluePathFile()                        # permet d'obtenir les chemins absolus des fichiers a traiter


##### Lecture  des jobs et filtrage des fichiers FF.
matches_parameter = {}                                   # on initialise un dictionnnaire qui va stocker comme clé les fichiers FF consommes par les jobs et comme valeur la liste de  tous les jobs dans lesquelles ils sont lus
for file in paths:
    reader = thread.readFiles(file)
    match_parameter = thread.findExpression(r'Par.+\s?=\s?FF.*', reader)     #  Tu 
    matches_parameter[file] = match_parameter           # append FF file and jobname to dictionnary 
#####
# ------------------------------------------------------
# pprint(matches_parameter)                             # dictionnaire {job : list_parametre}
list_ficPartages = []
for job, list_paramtre in matches_parameter.items():
    if len(list_paramtre) != 0:
        # print(job+':\n\t'+str(list_paramtre)+'\n')
        for elt in list_paramtre:
            # print(elt)
            list_ficPartages.append(elt)
# print(list_ficPartages)
# print(len(list_ficPartages))
# -----------------------------
# ------------------------------------------------------
nvx_list_ficPartages = list(set(list_ficPartages))       # suppression des doublons (lignes similaires ) puis conversion en liste ordonnee
# print(len(nvx_list_ficPartages))

 # -------------------------
list_FichierFF = thread.getValueInList(nvx_list_ficPartages, sep="=")
# print(list_FichierFF)
# print(len(list_FichierFF))   
#  ##  __________--------___--

nvx_list_FichierFF = list(set(list_FichierFF))          # suppression des doublons (lignes similaires ) puis conversion en liste ordonnee
print(len(nvx_list_FichierFF))                             #  afficher les fichier partageees
# print("Le nombre de fichier csv partage est {} ".format(len(nvx_list_FichierFF)))


#  a deommenter
#    ###### 
# coll = {}                                              # creer un dicto vide pour collecter l'ensemble des fichiers csv avec les jobs correspondant  
# for num , fichierFF in enumerate (nvx_list_FichierFF):
#     list_job = []                                      # liste vide pour recuperer les jobs 
#     for job in os.listdir(workdir):   
#         # print(job)                      
#         reader_f = thread.readFiles(job)
#         if fichierFF in reader_f:
#             # print(num, fichierFF, job)
#             list_job.append(job)
#             coll[fichierFF] = list_job   
# # pprint(coll)
# # print(coll.values())       

#  #####################################################################
# # collecter les fichiers qui sont concernes dans les echanges de fichiers csv
#     # par exemple s'appuyer sur la variables coll.values(), supprimer les doublons 
#     # avec la commande list(selt(maListe)) en faisant une loop for puis append 

#  # print("fichierCSV|job|EventID|messageID|action|1|2|3|4|5|6|7|8|9|10|11")
# print("fichierCSV||job||EventID||messageID||action")
# for jobname in os.listdir(workdir):
#     for fic_csv in nvx_list_FichierFF:
#         job_name = Job_class(workdir,jobname, fic_csv)
#         # print('\n')
#         # print(job_name)
        
#         with open(jobname, 'r') as jb:
#             # for i in range(100):
#             jb = jb.read()
#             # decouper  le document en bloc (Event ID --- Message)
#             bloc_jb = job_name.blockEventID(jb)
#             if bloc_jb ==[]:
#                 pass
#             else: 
#                 # print(bloc_jb[1])
#                 del bloc_jb[1]
#                 # print(bloc_jb)
#                 # print('\n')

#                 for num, line in enumerate(bloc_jb):
#                     rep = line.find(fic_csv)
#                     # print(rep)
#                     if rep != -1:
#                         # print(job_name)
                    
#                         linespliter = line.split('\n')
#                         # print(linespliter)
#                         del linespliter[1:4]
#                         del linespliter[2:4]
#                         linespliter.pop()
#                         # print(linespliter)

#                         EventID = linespliter[0]
#                         messageID = linespliter[1]

#                         action = linespliter[2:]
#                         # print(action)

#  ####    output en fichier csv separe par des pipes ou , ou ; double pipe           
#                         # print(fic_csv+"||"+jobname+"||"+EventID+"||"+messageID+"||"+str(action))
#                     else:
#                         print("No matches for {}".format(fic_csv))
#                         pass
                    

# #-----Utilister cette commande et excuter la en console bash
# # python /Users/ganasene/Desktop/NoteInsyco/relation_jobs.py > /Users/ganasene/Desktop/NoteInsyco/resultat_relation.csv

     


