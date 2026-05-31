import pandas as pd
import re

def normalitzar_text(text):
    if pd.isna(text):
        return text

    text = text.strip()

    # eliminar articles
    patterns = [" (El)", " (La)", " (Els)", " (Les)", ", el", ", la", ", els", ", les", " (L')", " (L’)", ", l'", ", L'"]
    for p in patterns:
        text = text.replace(p, "")

    # espais dobles
    text = re.sub(r"\s+", " ", text)

    return text

# 1. Carregar dades
cert  = pd.read_csv("../data/raw/Certificats_d’eficiència_energètica_d’edificis_20260531.csv", low_memory=False)
renda = pd.read_csv("../data/raw/renda_municipis.csv", sep=";")


# 2. Neteja bàsica
# Eliminar files sense informació de municipi o amb municipis no identificables
cert = cert.rename(columns={"POBLACIO": "municipi", "COMARCA": "comarca"})
cert = cert.dropna(subset=["municipi"])
cert = cert[~cert["municipi"].str.contains("\\?", na=False)]
cert = cert[~cert["municipi"].str.contains("�", na=False)]
cert = cert[~cert["comarca"].str.contains("\\?", na=False)]
cert = cert[~cert["comarca"].str.contains("�", na=False)]
cert = cert.dropna(subset=["ANY_CONSTRUCCIO"])

# Normalitzar noms de municipis
cert["municipi"]  = cert["municipi"].apply(normalitzar_text)
cert["comarca"]   = cert["comarca"].apply(normalitzar_text)
renda["municipi"] = renda["municipi"].apply(normalitzar_text)

# Convertir a numèric les columnes d'interès
cols_numeriques = [
    "Energia primària no renovable",
    "Emissions de CO2",
    "ANY_CONSTRUCCIO"
]

for col in cols_numeriques:
    cert[col] = (
        cert[col]
        .astype(str)
        .str.replace(",", ".", regex=False)
    )
    cert[col] = pd.to_numeric(cert[col], errors="coerce")

#Filtrar per indicador i any
renda = renda[(renda["indicador"] == "per habitant (€)") & (renda["any"] == 2023)]

#Seleccionar només les columnes necessàries
renda_recent = renda[["municipi", "valor"]].rename(columns={"valor": "renda"})

# 3. Crear mètriques per municipi
agr = cert.groupby(["municipi", "comarca"]).agg(
    certs=("municipi", "count"),
    energia=("Energia primària no renovable", "mean"),
    emissions=("Emissions de CO2", "mean"),
    any_mitja=("ANY_CONSTRUCCIO", "mean"),
    pct_ab=("Qualificació de consum d'energia primaria no renovable", 
             lambda x: (x.isin(["A","B"]).mean()) * 100),
    pct_fg=("Qualificació de consum d'energia primaria no renovable", 
             lambda x: (x.isin(["F","G"]).mean()) * 100)
).reset_index()

# Filtrar la comarca més representada per cada municipi
agr = agr.sort_values("certs", ascending=False).drop_duplicates("municipi")

# 5. Afegir renda
final = agr.merge(renda_recent, on="municipi", how="inner")

# 6. Arrodonir valors
final["energia"] = final["energia"].round(2)
final["emissions"] = final["emissions"].round(2)
final["any_mitja"] = final["any_mitja"].round(0)
final["pct_ab"] = final["pct_ab"].round(1)
final["pct_fg"] = final["pct_fg"].round(1)
final["renda"] = final["renda"].round(0)

# 7. Guardar resultat
final.to_csv("../data/processed/municipis_energetics.csv", index=False)
final.to_json("../data/processed/observable_municipis.json", orient="records", force_ascii=False)

print("Dataset creat correctament")