# updategandidns
Script Python permettant de mettre à jour l'adresse IP d'un domaine chez gandi avec l'API Live DNS (https://doc.livedns.gandi.net/)

Mode d'emploie :

Editer le fichier et renseigner :
- l'API Key obtenue sur le site de Gandi.
- le domaine concerné.
- le chemin de log qui vous convient.

Faire une tache planifié.

Le script avant toute modification fait un snapshot de la zone. En cas de soucis vous pouvez restaurer la configuration de la zone dans l'interface de Gandi.

Testé sur un NAS Synology DS916+.
