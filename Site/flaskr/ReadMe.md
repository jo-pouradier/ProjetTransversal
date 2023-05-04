# Utilisation du site Flask

## Installation
installer le module Flask et tout les autres imports
```bash
pip install -r ../../requirements.txt
```

## Lancement du site
```bash
python -m flask --app ./Site/flaskr/main run --host=0.0.0.0 
```

##Installation des modules pour lancer le site
'''bash 
pip install -r .\requirements.txt
'''

## compilation

d'abord il faut mettre en place un environnement virtuel:
```bash
python -m venv env
source env/bin/activate
```

puis installer les modules:
```bash
pip install -r ../../requirements.txt
```

enfin on peut compiler avec la commande
```bash
pyinstaller -F --hidden-import=flask --paths ./env/lib/python3.11/site-packages --add-data "./templates:./templates" --add-data "./static:./static" main.py
```

