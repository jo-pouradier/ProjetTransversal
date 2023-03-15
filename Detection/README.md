# Optimisation opencv

quand on install opencv avec pip, les library C ne sont pas optimisées pour la machine. Il faut donc les recompiler.
/!\ cela peut prendre plusieur dizaines de minutes voir plusieur heures /!\

## Dépendences

Pour verifier l'installation des dépendences, on install opencv normalement puis on le supprime pour ne garder que les dépendences.

```bash
pip install opencv-python
pip uninstall opencv-python
pip list | grep opencv ## rien ne doit s'afficher
```

## Installation

```bash
pip install --no-binary opencv-python opencv-contrib-python
```
