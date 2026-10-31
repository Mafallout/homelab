# Lista de canales de la tele

En la tele del salón usamos TiviMate, y le he preparado una lista "Casa" con 12 canales de TDT en abierto (La 1, La 2, 24h, Teledeporte, los de Canal Sur, los de Huelva, Trece y Clan), numerados del 1 al 12 y con su guía de programación.

## Cómo funciona

1. Los canales están en `canales.txt`, uno por línea: número, nombre, de dónde sale y su guía.
2. Cada día a las 04:45, el script `lista-casa.py` descarga la lista de [TDTChannels](https://www.tdtchannels.com), busca esos canales y prueba cada enlace como lo haría la tele. Se queda con el primero que funciona.
3. Un nginx en Docker sirve la lista resultante a la red de casa, y TiviMate la recoge de ahí. La propia lista dice dónde está la guía de TDTChannels, así que TiviMate la carga solo.

El vídeo no pasa por el servidor: los enlaces de la lista van directos a RTVE, Canal Sur y las teles locales. Si el servidor se apaga, TiviMate sigue con la última lista que cargó y los canales siguen funcionando.

## Lo que me encontré

- Algunos canales de RTVE salen dos veces en TDTChannels, y una de las dos mete anuncios (`ottera.tv`). El script la descarta siempre.
- El enlace de Canal Sur Andalucía que sale primero responde a un navegador, pero a la tele le da error 403. Por eso el script prueba cada enlace con el identificador de TiviMate, igual que lo pediría la tele.
- Programas como Threadfin, que se suelen usar para esto, hacen de intermediario: la tele pasa por el servidor para abrir cada canal. Yo quería que la tele no dependa de él, así que lo hice con un script.

## Si algo falla

- Si un canal no aparece en TDTChannels o ninguno de sus enlaces funciona, se queda el enlace del día anterior y nada desaparece de la tele.
- Si el script no termina bien, no avisa a Uptime Kuma, y Kuma me escribe por Telegram al día siguiente. Otro monitor comprueba que la lista se sirve.
- Los días de fútbol, las operadoras bloquean parte de Cloudflare por orden de LaLiga, y la web de TDTChannels puede no responder. Me pasó un sábado por la tarde. Por eso el script corre a las 04:45, cuando no hay partidos.

## Cómo está montado

- nginx sin root (`nginx-unprivileged`), con el disco del contenedor en solo lectura y 32 MB de memoria como mucho.
- El puerto solo se publica en la IP de casa del servidor, así que por Tailscale no responde.
- El script corre con mi usuario desde un temporizador de systemd, no como root.
