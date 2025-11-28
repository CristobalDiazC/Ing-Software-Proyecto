# Configuración del proyecto

## Backend

### Creación de entorno virtual he instalación de dependencias

```bash
cd Libreria-Back-End
python3 -m venv .venv
source venv/bin/activate
pip install -r requeriments.txt
```

## Frontend

### Ejecución de la app

**Requerimientos**:

> Debes tener instalado Node.js y NPM

```bash
pnpm install -g browser-sync # o npm i -g browser-sync
```

**Ejecución**:

```bash
cd Libreria-Front-End
browser-sync start --server --port 5500 --files "**/*"
```
