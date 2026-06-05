# catalunya-eficiencia-energetica
Anàlisi i visualització de l'eficiència energètica dels edificis a Catalunya a partir dels certificats energètics de l'ICAEN i dades socioeconòmiques de l'Idescat.

## Estructura del projecte
```text
catalunya-eficiencia-energetica/
├── data/
│   ├── processed/
│   │   ├── municipis_energetics.csv
│   │   └── observable_municipis.json
│   └── raw/ 
│       ├── Certificats_d_eficiencia_energetica_edificis_20260531.csv (no inclòs al repositori per la mida de les dades)
│       └── renda_municipis.csv
├── notebooks/
│   └── processament_dades.py
├── LICENSE
└── README.md
```

# Informació
El projecte consta de dues carpetes, "data", on hi ha el CSV amb les rendes dels municipis, i els fitxer de sortida que son el json que s'utilitza per a Observable i el json amb format CSV per poder veure les dades, i "notebooks", on hi ha el fitxer per fer la neteja de les dades.
Té llicència MIT i es public.

# Observacions:
- Degut al tamany del dataset principal, supera el tamany maxim permes al github. Però estan disponibles al Drive (https://drive.google.com/drive/folders/1GHclBchV6INBO25YeVQw6TekUtv4u4xx?usp=drive_link). 
- Per poder executar el python, s'ha d'afegir el CSV Certificats_d’eficiència_energètica_d’edificis_20260531.csv a la carpeta "data/raw"

# Les dades utilitzades son:
Dataset principal: Certificats d’eficiència energètica d’edificis | Dades obertes de Catalunya (https://analisi.transparenciacatalunya.cat/Energia/Certificats-d-efici-ncia-energ-tica-d-edificis/j6ii-t3w2/about_data)
Dataset enriquiment: Idescat. Renda familiar disponible bruta territorial. Catalunya (https://www.idescat.cat/pub/?id=rfdbc)

# Enllaç al Observable:
https://observablehq.com/d/7ec24c06d7a7d079