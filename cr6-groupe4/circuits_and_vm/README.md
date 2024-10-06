# Circuit booléen et machine virtuelle

## Circuit booléen

Vous pouvez appeler directement `python3 circuits.py -b 8` pour exécuter le programme et afficher le graphe du circuit.


`circuits.py` contient les classes `Graph` et `Node` qui permettent de créer un circuit booléen et de l'évaluer.

La fonction `create_min_n` permet de créer un circuit qui prend en entrée deux nombres en base 2 et renvoie le plus petit.

La fonction `plot_graph` permet de visualiser le graphe du circuit.

`circuits_test.py` contient les tests unitaires pour les fonctions de `circuits.py`.

## Machine virtuelle

`virtual_machine.py` contient la classe `VirtualMachine` qui permet de simuler une machine virtuelle et notamment de compiler un circuit booléen en une suite d'instructions pour la machine virtuelle.

La compilation du circuit booléen se trouve dans la fonction `compile`.

Il est possible d'exécuter le code compilé avec la fonction `run`.

`virtual_machine_test.py` contient les tests unitaires pour les fonctions de `virtual_machine.py`.
Puisque les tests sont relativement long une prévision du temps d'exécution est donnée.




