# Club Atlético Yaguarí — Historial

App de historial del Club Atlético Yaguarí en la Liga Universitaria de Deportes.

## Estructura

```
yaguari-app/
├── index.html              # App principal
├── netlify.toml            # Config de Netlify
└── netlify/
    └── functions/
        ├── liga.mjs        # Proxy para API de partidos
        └── posiciones.mjs  # Proxy para API de tablas
```

## Deploy

1. Conectar este repo a Netlify
2. Build settings: publish directory = `.`
3. Netlify detecta automáticamente las functions

## Actualización de datos

Los datos históricos están embebidos en `index.html`.  
Los datos de la temporada en curso se cargan en tiempo real desde la API de la Liga.

Para agregar datos de una temporada nueva:
- Correr el script de recolección en la consola de ligauniversitaria.org.uy
- Subir el JSON generado
- Fusionar con el existente en index.html
