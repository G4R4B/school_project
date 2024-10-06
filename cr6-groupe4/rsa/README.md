# RSA et Rhô de Pollard
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

`python3 rsa --mode demo` Pour un exemple de chiffrement , déchiffrement et attaque

`python3 el_gamal.py --mode encrypt [-p P] --plain Hello` Pour chiffrer un message avec RSA

`python3 el_gamal.py --mode decrypt --private (n,d) --cypher CYPHER` Pour déchiffrer un message avec RSA

`python3 el_gamal.py --mode break --public (n,e) [--cypher CYPHER]` Pour l'attaque basé sur rho de Pollard

`./rho_pollard_rsa <N>` Pour l'attaque basé sur rho de Pollard en C

## Exemple
```
python3 rsa.py --mode demo
Plaintext: b'Hello bob!'
Public key: (11362329784152838510332386659, 65537)
Private key: (11362329784152838510332386659, 2450450419903439466768947473)
Cyphertext: 680319829071643953480327505
Plaintext recovered : b'Hello bob!'
d = 278019818647751
n/d = 40868776331909

Private key breaked: 11362329784152838510332386659 2450450419903439466768947473
Plaintext breaked: b'Hello bob!'
```

```
python3 rsa.py --mode encrypt --plain test
Public key: (20310326687801233040968329132025182331, 65537)
Private key: (20310326687801233040968329132025182331, 2783578044613434778163395254836556305)
Cyphertext: 975055739114768571641943070035854034
```

```
python3 rsa.py --mode decrypt --private "(20310326687801233040968329132025182331, 2783578044613434778163395254836556305)" -c 975055739114768571641943070035854034
Plaintext: b'test'
```

```
python3 rsa.py --mode break --public "(11362329784152838510332386659, 65537)" -c 680319829071643953480327505
d = 278019818647751
n/d = 40868776331909

Private key: 11362329784152838510332386659 2450450419903439466768947473
Plaintext: b'Hello bob!'
```


