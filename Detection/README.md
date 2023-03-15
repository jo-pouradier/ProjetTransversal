# Optimisation opencv

quand on install opencv avec pip, les library C ne sont pas optimisées pour la machine. Il faut donc les recompiler.

## Installation

```bash
pip install --no-binary opencv-python opencv-contrib-python
```
