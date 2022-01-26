# txt = """National offres :
#
# 1 --> Télévendeurs ayant une expérience en Energie TÉLÉTRAVAIL
# 2 --> Chargés de Clientèle débutant
# 3 --> Experience en Centre d'appel (junior & senior)
# 4 --> Autres
#
# # --> page d'accueil"""

txt = """International offres :1 --> Cuisiniers
2 --> Superviseurs de restauration
3 --> Pâtissier boulanger
4 --> Profil IT
5 --> Autres

# --> page d'accueil"""

ll = []
for i in txt.split("-->"):
    ii = i.replace("\n", "").replace("National offres :1", "").replace("#", "").replace("page d'accueil", "").replace("International offres :1", "")
    print(ii)
    if ii.strip() :
        ll.append(ii.strip())

print(ll)