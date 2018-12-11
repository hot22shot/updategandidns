#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import time, re, sys
import requests
import json
import logging
import unicodedata

# Nom du fichier de log
logfile = 'updateDNSGandi.log'

# Répertoire du fichier de log
logpath = '/usr/local/scripts/updatedns/'

# Fichier de log
logging.basicConfig(filename=logpath+logfile,level=logging.INFO)

# URL de la page retournant l'ip publique au format ipv4
urlpage = 'https://v4.ifconfig.co/json'

# Clef API Gandi
apikey = 'A MODIFIER'

# Domaine concerné (à modifier)
mydomain = 'A MODIFIER'

# Horodatage
asctime = time.asctime( time.localtime() )

# headers gandi
ghg = {
    'X-Api-Key': '{0}'.format(apikey)
    }
ghp = {
    'Content-Type': 'application/json',
    'X-Api-Key': '{0}'.format(apikey),
    }

# user-agent
ua = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'
    }

##################################

try:
    # récupération de l'id de zone associée au domaine
    zoneuuid=requests.get("https://dns.api.gandi.net/api/v5/domains/{0}".format(mydomain),headers=ghg).json()['zone_uuid']
    # récupération de l'ip configurée chez gandi
    oldip = requests.get("https://dns.api.gandi.net/api/v5/zones/{0}/records/%40/A".format(zoneuuid),headers=ghg).json()['rrset_values'][0]
    # récupération de l'adresse ip actuelle
    currip = requests.get("{0}".format(urlpage),headers=ua).json()['ip']
    pattern = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    result = re.search(pattern,currip,0)
    if result == None:
        logging.info("{0} : pas d'adresse ip actuelle trouvée !!".format(asctime))
        sys.exit()     
    # Comparaison et mise à jour si besoin
    if oldip != currip:
        logging.info("{0} : l'adresse ip enregistrée chez gandi est {1}.".format(asctime,oldip))
        logging.info("{0} : l'adresse ip actuelle est {1}.".format(asctime,currip))
        # On cree un snapshot de la zone pour restauration en cas de pépin
        snap = requests.post("https://dns.api.gandi.net/api/v5/zones/{0}/snapshots".format(zoneuuid),headers=ghp).json()['message']
        # Mise a jour de la zone
        data = '{"rrset_values": ["%s"]}' % currip
        maj = requests.put('https://dns.api.gandi.net/api/v5/zones/{0}/records/%40/A'.format(zoneuuid), headers=ghp, data=data).json()['message']
        logging.info("{0} : remplacement de {1} par {2} effectuée.".format(asctime,oldip,currip))
finally:
        sys.exit()
