import hashlib
import time

######################################################
#      Attaque de mot de passe par dictionnaire      #
######################################################

#On lit le fichier shadow en lecture seule 'r'
with open("shadow", "r") as shad:
    #Objet user => password
    objPwd = {}
    for ligne in shad:
        # On s'évite les erreurs
        if len(ligne.split(":")) >= 2:
            user = ligne.split(":")[0]
            password = ligne.split(":")[1]
            #On exclu les cas *,  !
            if password not in ('*', '!'):
                #Enfin on rempli notre objet
                # en retirant l'indice d'algo
                objPwd[password[3:]] = user.split()
                start = time.time() + 60 * 60;

#On lit le fichier dico en lecture seule 'r'
with open('dico_mini_fr', 'r') as dico:
    lignes = dico.readlines()
    #Pour tous les mots
    for ligne in lignes:
        mot = ligne.strip()
        #On hash le mot, MD5 pour notre atelier
        mothashé = hashlib.md5(mot.encode('utf')).hexdigest()
        for l in objPwd.items():
            #Si un des mots hashé match avec un du shadow
            if mothashé == l[0]:
                end = time.time() + 60 * 60;
                #On l'affiche dans la console
                if end - start < 1 :
                    tps="en moins d'une seconde"
                else:
                    tps = str(time.strftime("%H:%M:%S", time.gmtime(end - start))) + 'H'
                msg="Trouvé en {}, le mot de passe pour {} est {} ".format(tps, l[1][0], mot)
                print(msg)
                with open('resultatDico.txt', 'a') as file:
                    file.write(msg + '\n')

