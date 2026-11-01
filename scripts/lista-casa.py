#!/usr/bin/python3 -I
# Prepara la lista Casa de la tele a partir de canales.txt y de la lista de TDTChannels.
import fcntl
import os
import re
import sys
import tempfile
import urllib.request

# Las dos variables de entorno solo sirven para probar el script sin internet.
ORIGEN = os.environ.get("LISTA_CASA_ORIGEN", "https://www.tdtchannels.com/lists/tv.m3u8")
GUIA_ORIGEN = os.environ.get("LISTA_CASA_GUIA_ORIGEN", "https://www.tdtchannels.com/epg/TV.xml.gz")
CARPETA = os.environ.get("LISTA_CASA_DIR", "/opt/servicios/lista-casa")
CANALES = os.path.join(CARPETA, "canales.txt")
WEB = os.path.join(CARPETA, "web")
DESTINO = os.path.join(WEB, "casa.m3u")
GUIA = os.path.join(WEB, "guia.xml.gz")
AVISO = os.path.join(CARPETA, "aviso-kuma.url")
# Dirección con la que la tele pide la guía al servidor. Va en el servicio de systemd, no aquí.
GUIA_LOCAL = os.environ.get("LISTA_CASA_GUIA_URL", "")

# Estos enlaces meten anuncios en el canal.
CON_ANUNCIOS = re.compile(r"ottera\.tv|[?&]avod=1")
# Algunos servidores solo responden a navegadores, así que se prueban como la tele.
COMO_LA_TELE = "TiviMate/5.1.6 (Android 12)"
# El nombre del canal va después de la última comilla de los atributos, aunque lleve comas.
NOMBRE_EXTINF = re.compile(r'^#EXTINF:\s*-?\d+(?:\s+[^\s=]+="[^"]*")*\s*,(.*)$')


def descargar(url, timeout, agente="Mozilla/5.0"):
    peticion = urllib.request.Request(url, headers={"User-Agent": agente})
    with urllib.request.urlopen(peticion, timeout=timeout) as r:
        return r.read()


def funciona(url):
    try:
        texto = descargar(url, 10, COMO_LA_TELE)[:65536].decode("utf-8", "replace").lstrip("﻿ \r\n\t")
    except Exception:
        return False
    # Una lista en directo de verdad trae calidades o trozos de vídeo, y no está terminada.
    return (texto.startswith("#EXTM3U")
            and ("#EXT-X-STREAM-INF" in texto or "#EXTINF" in texto)
            and "#EXT-X-ENDLIST" not in texto)


def leer_canales():
    canales, numeros, nombres = [], set(), set()
    with open(CANALES, encoding="utf-8-sig") as f:
        for n, linea in enumerate(f, 1):
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue
            partes = [p.strip() for p in linea.split("|")]
            if len(partes) != 4 or not partes[0].isdigit() or not partes[1]:
                raise ValueError(f"línea {n}: no tiene el formato número | nombre | de dónde sale | guía")
            numero, nombre, origen, guia = partes
            if "," in nombre or '"' in nombre:
                raise ValueError(f"línea {n}: el nombre no puede llevar comas ni comillas")
            if numero in numeros or nombre in nombres:
                raise ValueError(f"línea {n}: número o nombre repetido")
            numeros.add(numero)
            nombres.add(nombre)
            if origen.startswith("TDTChannels:"):
                origen = origen.split(":", 1)[1]
            opciones = [o.strip() for o in origen.split(";") if o.strip()]
            if not opciones:
                raise ValueError(f"línea {n}: no dice de dónde sale el canal")
            canales.append((numero, nombre, opciones, guia))
    if not canales:
        raise ValueError("no hay ningún canal")
    return canales


def leer_lista(texto):
    entradas = []
    lineas = [l.strip() for l in texto.splitlines()]
    for i, linea in enumerate(lineas):
        m = NOMBRE_EXTINF.match(linea)
        if not m:
            continue
        # El enlace es la primera línea que no empieza por # (puede haber #EXTVLCOPT en medio).
        url = next((l for l in lineas[i + 1:i + 5] if l and not l.startswith("#")), "")
        if not url.startswith("http"):
            continue
        logo = re.search(r'tvg-logo="([^"]*)"', linea)
        entradas.append((m.group(1).strip(), url, logo.group(1) if logo else ""))
    return entradas


def lista_anterior():
    try:
        with open(DESTINO, encoding="utf-8") as f:
            return {n: (u, l) for n, u, l in leer_lista(f.read())}
    except FileNotFoundError:
        return {}


def escribir(destino, datos):
    fd, temporal = tempfile.mkstemp(dir=os.path.dirname(destino), prefix=".nuevo-")
    with os.fdopen(fd, "wb") as f:
        f.write(datos)
    os.chmod(temporal, 0o644)
    os.replace(temporal, destino)


def actualizar_guia():
    try:
        datos = descargar(GUIA_ORIGEN, 120)
    except Exception as e:
        print(f"No se pudo descargar la guía: {e}. Se queda la de ayer.")
        return False
    # Un .gz de verdad empieza por 1f 8b; si no, es una página de error.
    if len(datos) < 10000 or datos[:2] != b"\x1f\x8b":
        print("La guía descargada no es válida. Se queda la de ayer.")
        return False
    escribir(GUIA, datos)
    return True


def main():
    try:
        canales = leer_canales()
    except (OSError, ValueError) as e:
        print(f"Error en canales.txt: {e}. Se queda la lista de ayer.")
        return 1

    nueva = []
    if any(not o.startswith("http") for _, _, opciones, _ in canales for o in opciones):
        try:
            nueva = leer_lista(descargar(ORIGEN, 60).decode("utf-8", "replace"))
        except Exception as e:
            print(f"No se pudo descargar la lista de TDTChannels: {e}. Se queda la de ayer.")
            return 1
        if len(nueva) < 100:
            print(f"La lista de TDTChannels solo tiene {len(nueva)} canales. Se queda la de ayer.")
            return 1

    guia_bien = actualizar_guia()
    # Si el servidor aún no tiene su copia de la guía, la tele la pide a TDTChannels.
    url_guia = GUIA_LOCAL if GUIA_LOCAL and os.path.exists(GUIA) else GUIA_ORIGEN

    anterior = lista_anterior()
    salida = [f'#EXTM3U url-tvg="{url_guia}"']
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

    if len(salida) == 1:
        print("No ha salido ningún canal. Se queda la lista de ayer.")
        return 1
    escribir(DESTINO, ("\n".join(salida) + "\n").encode("utf-8"))

    if faltan:
        print("No encontrados hoy (se queda el enlace de ayer si lo había): " + ", ".join(faltan))
        return 2
    if not guia_bien:
        return 2
    print(f"Lista Casa preparada con {len(canales)} canales.")
    try:
        with open(AVISO, encoding="utf-8") as f:
            aviso = f.read().strip()
        if aviso:
            descargar(aviso, 10)
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"No se pudo avisar a Kuma: {e}")
    return 0


if __name__ == "__main__":
    # Que no corran dos a la vez y se pisen la lista.
    with open(CANALES, "rb") as bloqueo:
        try:
            fcntl.flock(bloqueo, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("Ya hay otra ejecución en marcha.")
            sys.exit(1)
        sys.exit(main())
