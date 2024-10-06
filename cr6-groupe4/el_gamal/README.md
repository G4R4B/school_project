# El Gamal et BSGS
## Lancement du programme
### Prérequis
- Python 3
- GMP
- GCC
- Make

### Compilation
```bash
make
```

### Lancement

`python3 el_gamal.py --mode demo` Pour un exemple de chiffrement , déchiffrement et attaque

`python3 el_gamal.py --mode encrypt --plain Hello` Pour chiffrer un message avec El Gamal 

`python3 el_gamal.py --mode decrypt -p p -a a -B B --cypher CYPHER` Pour déchiffrer un message avec El Gamal

`python3 el_gamal.py --mode break -p p -g g -A A [-B B] [--cypher CYPHER]` Pour l'attaque baby-step giant-step


`./bsgs <A> <p> <g>` Pour l'attaque baby-step giant-step directement en C

## Exemple
```
python3 el_gamal.py --mode encrypt --plain Hello
Plaintext:  b'Hi, this a long messageeeeee'
p: 212764390827058404212754067030563750517931869034507477640101685883140144584147
g: 60942915679218244853771285047621537677313720526796122190911050520180622519997
a: 56802601294024252257719806976371514170321228662821073760442707754484713339548
A: 127716074087008373645545327344364342291271069512605111454904921583876542250747
B: 10284920656103693912021821531321946569155266397656873792263219655880322290704
cyphertext: 172020239743388647863862868277388721530776020106554604973848434736629764534887
Plaintext recovered from decryption:  b'Hi, this a long messageeeeee'
```

```
python3 el_gamal.py --mode decrypt -p 212764390827058404212754067030563750517931869034507477640101685883140144584147 -a 56802601294024252257719806976371514170321228662821073760442707754484713339548 -B 10284920656103693912021821531321946569155266397656873792263219655880322290704 --cypher 172020239743388647863862868277388721530776020106554604973848434736629764534887
Plaintext:  b'Hi, this a long messageeeeee'
```

```
python3 el_gamal.py --mode encrypt --plain AHAH
Plaintext:  b'AHAH'
p: 10142763723683
g: 3709737877499
a: 5255564060362
A: 5636664036269
B: 6472040058373
cyphertext: 7269429172918
Plaintext recovered from decryption:  b'AHAH'
```

```
python3 el_gamal.py --mode break -p 10142763723683 -g 3709737877499 -A 5636664036269 --cypher 7269429172918 -B 6472040058373
Private key breaked:  5255564060362
Plaintext recovered:  b'AHAH'
```

## Hashmap

La hashmap utilisée pour l'attaque baby-step giant-step est une hashmap en C en licence libre trouvé sur [Github](https://github.com/tidwall/hashmap.c). Ainsi les fichiers `hashmap.h` et `hashmap.c` ne représentent pas notre travail mais celui de l'auteur de la librairie.

