#!/usr/bin/python3 -I
# Prepara la lista Casa de la tele a partir de canales.txt y de la lista de TDTChannels.
import os
import re
import sys
import urllib.request

ORIGEN = "https://www.tdtchannels.com/lists/tv.m3u8"
GUIA = "https://www.tdtchannels.com/epg/TV.xml.gz"
CARPETA = os.environ.get("LISTA_CASA_DIR", "/opt/servicios/lista-casa")
CANALES = os.path.join(CARPETA, "canales.txt")
DESTINO = os.path.join(CARPETA, "web", "casa.m3u")
AVISO = os.path.join(CARPETA, "aviso-kuma.url")

# Estos enlaces meten anuncios en el canal.
CON_ANUNCIOS = re.compile(r"ottera\.tv|[?&]avod=1")
# Algunos servidores solo responden a navegadores, así que se prueban como la tele.
COMO_LA_TELE = "TiviMate/5.1.6 (Android 12)"


def funciona(url):
    try:
        peticion = urllib.request.Request(url, headers={"User-Agent": COMO_LA_TELE})
        with urllib.request.urlopen(peticion, timeout=10) as r:
            return r.read(7) == b"#EXTM3U"
    except Exception:
        return False


def leer_canales():
    canales = []
    with open(CANALES, encoding="utf-8") as f:
        for n, linea in enumerate(f, 1):
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue
            partes = [p.strip() for p in linea.split("|")]
            if len(partes) != 4 or not partes[0].isdigit() or not partes[1]:
                raise ValueError(f"canales.txt, línea {n}: no tiene el formato número | nombre | de dónde sale | guía")
            numero, nombre, origen, guia = partes
            if origen.startswith("TDTChannels:"):
                origen = origen.split(":", 1)[1]
            opciones = [o.strip() for o in origen.split(";") if o.strip()]
            if not opciones:
                raise ValueError(f"canales.txt, línea {n}: no dice de dónde sale el canal")
            canales.append((numero, nombre, opciones, guia))
    return canales


def leer_lista(texto):
    entradas = []
    lineas = texto.splitlines()
    for i, linea in enumerate(lineas):
        if linea.startswith("#EXTINF") and i + 1 < len(lineas):
            url = lineas[i + 1].strip()
            if not url.startswith("http"):
                continue
            nombre = linea.rsplit(",", 1)[-1].strip()
            logo = re.search(r'tvg-logo="([^"]*)"', linea)
            entradas.append((nombre, url, logo.group(1) if logo else ""))
    return entradas


def lista_anterior():
    try:
        with open(DESTINO, encoding="utf-8") as f:
            return {n: (u, l) for n, u, l in leer_lista(f.read())}
    except FileNotFoundError:
        return {}


def main():
    try:
        canales = leer_canales()
    except (OSError, ValueError) as e:
        print(f"Error en canales.txt: {e}. Se queda la lista de ayer.")
        return 1

    nueva = []
    if any(not o.startswith("http") for _, _, opciones, _ in canales for o in opciones):
        try:
            # Con el identificador de Python, TDTChannels responde 403.
            peticion = urllib.request.Request(ORIGEN, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(peticion, timeout=60) as r:
                nueva = leer_lista(r.read().decode("utf-8", "replace"))
        except Exception as e:
            print(f"No se pudo descargar la lista de TDTChannels: {e}. Se queda la de ayer.")
            return 1
        if len(nueva) < 100:
            print(f"La lista de TDTChannels solo tiene {len(nueva)} canales. Se queda la de ayer.")
            return 1

    anterior = lista_anterior()
    # url-tvg hace que TiviMate y otros programas carguen la guía solos.
    salida = [f'#EXTM3U url-tvg="{GUIA}"']
    faltan = []
    for numero, nombre, opciones, guia in canales:
        # Cada opción es un nombre de TDTChannels (puede tener varias entradas) o un enlace directo.
        candidatos = []
        for o in opciones:
            if o.startswith("http"):
                candidatos.append((o, ""))
            else:
                candidatos += [(u, l) for n, u, l in nueva if n == o and not CON_ANUNCIOS.search(u)]
        elegido = next(((u, l) for u, l in candidatos if funciona(u)), None)
        if elegido and not elegido[1]:
            elegido = (elegido[0], next((l for u, l in candidatos if l), ""))
        if not elegido:
            faltan.append(nombre)
            elegido = anterior.get(nombre)
            if not elegido:
                continue
        url, logo = elegido
        guia_attr = f' tvg-id="{guia}"' if guia else ""
        logo_attr = f' tvg-logo="{logo}"' if logo else ""
        salida.append(
            f'#EXTINF:-1{guia_attr} tvg-chno="{numero}" tvg-name="{nombre}"{logo_attr} group-title="Casa",{nombre}'
        )
        salida.append(url)

    temporal = DESTINO + ".nuevo"
    with open(temporal, "w", encoding="utf-8") as f:
        f.write("\n".join(salida) + "\n")
    os.chmod(temporal, 0o644)
    os.replace(temporal, DESTINO)

    if faltan:
        print("No encontrados hoy (se queda el enlace de ayer si lo había): " + ", ".join(faltan))
        return 0
    print(f"Lista Casa preparada con {len(canales)} canales.")
    try:
        with open(AVISO, encoding="utf-8") as f:
            aviso = f.read().strip()
        if aviso:
            urllib.request.urlopen(aviso, timeout=10).read()
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"No se pudo avisar a Kuma: {e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
