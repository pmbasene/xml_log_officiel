#coding: utf8
import os
import re
import subprocess

""" Ce module comporte toutes les methodes(fonctions) usuelles. 
Elles sont appelées dans les modules comme relation_jobs 
ou parserCSV_relation """
class CreeRelation():

    """ CreeRelation est le nom du projet  """

    def __init__(self, path_to_folder='/Users/ganasene/Desktop/insyco/doc/temp'):
        self.path_to_folder = path_to_folder                    #
        self.absolue_paths = []
        self.value_fic = []
        self.files = []

    # def __str__(self):
    #     return "Le chemin de dossier des jobs : {}".format(self.path_to_folder)

    def listFileInDir(self):
        """ return a list of all files in a working dir """
        # files = []    # transformé en attribut d'instance
        for file in os.listdir(self.path_to_folder):
            self.files.append(file)
        return self.files

    def absoluePathFile(self):
        '''cette fonction retourne une liste des chemins absolus de tous les fichiers contenus dans un dossier '''
        # paths = []                          # transformé en attribut d'instance
        for f in self.files:
            path = os.path.join(self.path_to_folder, f)
            self.absolue_paths.append(path)
        return self.absolue_paths

    def readFiles(self, file):
        # print("####################************* lecture du fichier ' {} '*********************#########################################################".format(file))
        '''Cette fonction permet de lire fichier <file>(absolue path) en entree et retourne un str '''
        with open(file, 'r') as rf:
            reader = rf.read()    
        return reader

    def findExpression(self, pattern, text):
        '''Cette fonction retourne une liste de toutes les lignes d'un <text> correspondant au <pattern> '''
        # matches_parameter = []                       # transformé en attribut d'instance
        pattern = re.compile(pattern)
        matches_parameter = re.findall(pattern, text)
        return matches_parameter

    def recupererCleOuValeurInString(self, string, sep=" "):
        '''cette fonction prend en entree une chaine de caractere <str>  
        et un separateur(= ou , ou ; ou : etc) et retourne la cle et la valeur de la chaine splitee'''
        key, val = string.split(sep)
        Key = key.strip()
        Val = val.strip()
        return Key, Val

    def getValueInList(self, list_File, sep=" "):
        '''Ceci retourne une liste de toutes les  valeur à droite d'un string comportant un sep par exemple = , :,  ect.'''
        for string in list_File:
            k, v = self.recupererCleOuValeurInString(string, sep)
            self.value_fic.append(v)
        return self.value_fic


class Job_class(CreeRelation):

    """cette classe JOB est propre à un seul et unique job. Elle a comme attribut
        - Le nom du job
        - Le fichier csv recherché """

    def __init__(self, path_to_folder, jobname, fic_csv):
        CreeRelation.__init__(self, path_to_folder)
        self.jobname = jobname
        self.fic_csv = fic_csv
        # self.Message         = []   , # self.EventID         = [] ,  # self.Time            = []   etc.
        self.nvx_list_ficPartages = []

        self.pattern_things = r'Id\s?: \s?[0-9]*\nTime\s?:\s?.*\n.*\s?:\s?.*\n.*\s?:\s?.*\n.*\s?:\s?.*\n.*\s?:\s?.*\nMessage\t\s?:\s?.*\n?.*\n?.*'

    def __repr__(self):
        # return " Le fichier csv {} est lu en input dans le job {}".format(self.fic_csv, self.jobname)
        return "Instance, {} = Job_class({}, {})".format(self.jobname, self.jobname, self.fic_csv)

    def yop(self, instance, list_absolue_paths):  # pas encore aboutie
        matches_parameter = {}
        for file in list_absolue_paths:
            # print(p)
            reader = instance.self.readFiles(file)
            # print(reader)
            match_parameter = instance.self.findExpression(
                r'Par.+\s?=\s?FF.*\.csv', reader)
            matches_parameter[file] = match_parameter
        return matches_parameter

    def readline_File(self, file):  # not use
        '''Cette fonction permet de lire fichier <file> en entree et retourne une liste ou chaque item correspond a une ligne'''
        with open(file, 'r') as rf:
            # i= 1
            while True:
                list_reader = rf.readline()
                if list_reader == " ":
                    break
                # i+=1
        return list_reader

    def get_value(self):
        pass

    def get_all_messageID(self, string):
        pass
    #     # pattern_msgID = r'Message Id\s?:\s?.*'
    #     pattern_mess = re.compile(self.pattern_msgID)
    #     matches_msgID = re.findall(pattern_mess, string)
    #     return matches_msgID

    def blockEventID(self, string):
        '''ici on va prendre le separator_word Event iD
        sep_word=Event 
        !!! Dans les listes qui seront generees il en y aura certaines qui sont vide. 
        Donc il faut en prendre compte lors de suppression des occurences de la liste bloc_jb'''
        bloc_jb = string.split(
            'Event ')          # Note : prendre juste Event plus espace pour que ca marche

        # del bloc_jb[2]                          # permet d'enlever la deuxieme occurence qui comporte que les parametre de conf du datastage
        # enleve la permiere occ qui est vide
        del bloc_jb[0]

        bloc_jb = bloc_jb[:]
        return bloc_jb

    def removeDuplicates(self, listDoublons):  # not use
        '''cette methode permet de supprimer les doublons dans une liste. 
        Prendre en entree une liste et retourne une liste dans laquelle elements dupliques sont supprimes'''
        for i in listDoublons:
            if i not in self.nvx_list_ficPartages:
                self.nvx_list_ficPartages.append(i)
        return self.nvx_list_ficPartages



if __name__ == "__main__":
    p = CreeRelation()


    