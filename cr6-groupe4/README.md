# CR6-Groupe4

## Installation

Pour installer les dépendances, exécutez la commande suivante:
```bash
pip install -r requirements.txt
```
Dans le cas où vous n'avez pas `pip`, vous pouvez l'installer avec la commande suivante:
```bash
sudo apt install python3-pip
```
Pour les fichiers en C, vous pouvez les compiler avec la commande suivante:
```bash
make -C el_gamal
make -C rsa
```

## Plan

1-2-3. Paul Vie  
4. Tony Ly Soan  
5-6. Yanis Lacenne / Paul Vie  
7. Paul Vie  
8-9. Louka Chenal / Avon FitzGerald

## Q1
Fichiers:
```
aes_ctr.py
```

Utilisation de la librairie `Crypto.Cipher` de python

Vous pouvez exécuter le fichier avec la commande suivante:
```bash
python3 aes_ctr.py --mode demo -p "Hello, World"
```
Vous pouvez aussi éxécuter les tests avec la commande suivante:
```bash 
python3 aes_ctr_test.py --mode test
```

## Q2 - Q3
Fichiers:
```
el_gamal/
    |- hashmap.h
    |- bsgs.c
    |- hashmap.c
    |- Makefile
    |- README.md
    \ el_gamal.py
rsa/
    |- rho_pollard_rsa.c
    \ rsa.py
```

Pour plus d'informations concernant l'implémentation d'El Gamal (resp. RSA), voir le fichier `el_gamal/README.md` (resp. `rsa/README.md`).

Utilisation de l'algorithme de Miller Rabin pour RSA et El Gamal.

## Q4

Fichiers nécessaires pour la mise en place du transfert inconscient utilisant RSA:
```
ot_rsa/
├── ot_rsa.py
└── test_ot_rsa.py
```

Voir le fichier `ot_rsa/README.md` pour plus d'informations.

## Q5-Q6-Q7

Fichiers:
```
circuits_and_vm/
    |- circuits.py
    |- circuits_test.py
    |- virtual_machine.py
    \ virtual_machine_test.py
```

La fonction `min_n` prends deux listes de même longueur représentant deux nombres en base 2, et renvoie la liste caractérisant le nombre le plus petit.

Voir le fichier `circuits_and_vm/README.md` pour plus d'informations.

#### Exemple
```py
a = [0, 1, 0, 1]  # 5
b = [1, 1, 0, 0]  # 12
print(min_n(a, b))
```
```
[0, 1, 0, 1]
```
La fonction renvoie bien le résultat attendu.

#### Tests

Pour effectuer les tests:
```
cd circuits_and_vm
python3 -m unittest circuits_test.py
python3 -m unittest virtual_machine_test.py
```
Cela risque de prendre quelques minutes.

## Q8-Q9

Fichiers:
```
garbled_circuits/
    |- garbled_circuits.py
    |- garbled_circuits_test.py
```
`garbled_circuits.py` contient 2 fonctions prévues pour être utilisées de l'extérieur : `new_garbled_circuit` et `evaluation`.

`new_garbled_circuit` prend notamment en paramètre un circuit construit à partir de `create_min_n` provenant de `circuits.py`.
`evaluation` doit ensuite être appelée après la création du circuit brouillé à partir des tableaux, des clés de A et des instances de Bob où un oblivious transfer a été effectué.
Les instances de Bob sont évidemment créées à l'extérieur de `new_garbled_circuit`.

Pour effectuer les tests:
```
cd garbled_circuits && python3 -m unittest garbled_circuits_test.py

```
## Members

- Paul Vie
- Louka Chenal
- Avon Fitzgerald
- Tony Ly Soan
- Yanis Lacenne
