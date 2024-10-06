# Transfert inconscient basé sur RSA

## Test

Dans `test_ot_rsa.py` se trouvent les tests unitaires de `ot_rsa.py`.

Commande pour lancer les lancer (en considérant que vous vous trouvez dans le dossier `ot_rsa/`):

```cmd
python -m unittest test_ot_rsa.py
```

## Implémentation

Dans `ot_rsa.py` 2 classes et 4 fonctions sont mises à disposition pour procéder au transfert inconscient:

1. `Alice`
   1. `to_bob1`
   2. `to_bob2`
2. `Bob`
   1. `to_alice1`
   2. `to_alice2`

Pour plus de détails veuillez consulter la documentation présente dans `ot_rsa.py`.

## Démo

Une démo de trouve à la fin du fichier `ot_rsa.py`.