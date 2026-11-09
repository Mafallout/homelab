# homelab

Estoy montando un pequeño servidor en casa que protege la red de mi familia. Ya filtra la publicidad y los rastreadores, guarda copias de seguridad cifradas de su configuración y puedo administrarlo a distancia de forma segura.

## Hardware

HP EliteDesk 800 G4 Mini (i5-8500T, 16 GB, NVMe de 1 TB), un disco WD Gold de 10 TB en una caja USB y un switch Netgear GS308E.

## Cómo está montado

El router de casa reparte dos DNS: el del servidor y 1.1.1.1 de respaldo. Así, si el servidor se apaga, la casa sigue teniendo internet. Lo he probado apagando el servidor algunos ratos.

En el servidor, AdGuard Home va instalado directamente en Debian, sin Docker, porque es la pieza de la que depende la familia y así arranca aunque Docker falle. Caddy también va en el sistema. Los demás servicios van en contenedores, cada uno con su versión fijada y su límite de memoria. Desde fuera de casa solo se llega por Tailscale: el router no reenvía ningún puerto al servidor.

El esquema de la red y qué puerto se abre a quién están en [docs/red.md](docs/red.md).

## Qué hay montado

- Debian 13 sin entorno gráfico y con IP fija. Todo lo hago por SSH.
- Antes de fiarme de él: memtest con 12 pasadas sin errores, SMART limpio y Secure Boot activado.
- SSH con llave FIDO2, en dos YubiKey por si pierdo una. Sin contraseña, sin login de root y solo para mi usuario. El móvil tiene su propia clave, que solo vale desde casa o por Tailscale.
- Tailscale para entrar desde fuera de casa sin abrir puertos en el router.
- Cortafuegos con UFW: bloquea todo lo que entra salvo SSH, lo que llega por Tailscale y, solo desde la red de casa, el DNS (normal y cifrado) y el panel de AdGuard.
- Actualizaciones de seguridad automáticas.
- Se enciende solo cuando vuelve la luz después de un corte, y se reinicia solo si se cuelga (watchdog de la placa).
- AdGuard Home como DNS de toda la casa, con listas de bloqueo suaves y las consultas cifradas hacia fuera (DNS sobre HTTPS). El router reparte también 1.1.1.1 de respaldo por si el servidor se cae.
- DNS cifrado también dentro de casa (DNS sobre TLS).
- Un aviso desde fuera: cada 5 minutos el servidor le pregunta a su propio AdGuard y, si no recibe una IP, me salta una alarma en el móvil. Otro aviso igual salta si se caen Docker o Uptime Kuma, y otro si el disco da señales de fallo.
- Copias diarias cifradas con restic en Cloudflare R2 y en el disco de 10 TB, con otro aviso si una falla. Ya he probado a restaurarlas.
- Docker listo para los servicios, con su propio espacio en disco y logs acotados. Detalles en [docs/docker.md](docs/docker.md).
- Registro del uso de CPU, memoria y disco cada 10 minutos con sysstat.
- La CPU va sin turbo y, de 23:30 a 8:30, a media velocidad, para que el ventilador no se oiga de noche. Con un núcleo al máximo se queda en 43 °C en vez de 51 °C.
- Uptime Kuma vigila cada servicio y me avisa por Telegram si alguno cae. Detalles en [docs/uptime-kuma.md](docs/uptime-kuma.md).
- Gráficas del servidor con Prometheus y Grafana, y avisos al móvil si se calienta, si se llena un disco o si se queda sin RAM. Detalles en [docs/monitorizacion.md](docs/monitorizacion.md).
- Una lista con 12 canales de TDT para la tele, que se prepara sola cada día y no depende del servidor para verse. Detalles en [docs/lista-casa.md](docs/lista-casa.md).
- Caddy con nombres propios y candado para Uptime Kuma, Grafana y Home Assistant, con un certificado comodín de Let's Encrypt. Solo responde por Tailscale. Detalles en [docs/caddy.md](docs/caddy.md).
- Home Assistant para la domótica de casa, de momento sin aparatos. Detalles en [docs/home-assistant.md](docs/home-assistant.md).
- El disco de 10 TB para las fotos y las películas, montado de forma que el servidor arranca igual si falta. De noche está parado para que no se oiga. Detalles en [docs/wdgold.md](docs/wdgold.md).

## Lo que he medido

AdGuard da servicio a 16 aparatos de casa. Los móviles Android aceptan su DNS cifrado, pero aun así mandan casi todas sus consultas a 1.1.1.1. Para arreglarlo tendría que quitar el DNS de respaldo, y entonces la casa se quedaría sin internet si se cae el servidor, así que lo dejo así.

## Lo que me ha costado

- Docker se salta UFW: un puerto publicado por un contenedor queda abierto aunque `ufw status` no lo diga. Por eso lo que es solo de casa lo publico en la IP de casa del servidor o en `127.0.0.1`.
- Docker 29 guardaba las imágenes fuera de su volumen, en el disco del sistema. Lo vi al medir cuánto ocupaba cada sitio y lo moví.
- El servicio de Caddy de Debian escribía en el log todas sus variables, también el token de Cloudflare. Lo quité y cambié el token.
- La alerta de temperatura de Grafana apuntaba a un aviso de Telegram que todavía no existía, y Grafana no arrancaba. Primero tiene que existir el aviso y después la alerta.
- Los días de fútbol la operadora bloquea parte de Cloudflare, y con eso a veces no llegaban ni la lista de canales ni las copias. La lista se prepara de madrugada, y si falla se queda la del día anterior.

## Siguiente

Immich para las fotos y Jellyfin para las películas, y las luces de mi cuarto en Home Assistant.

El estado al día y la bitácora de cada sesión están en [jdsantana.com/homelab](https://jdsantana.com/homelab).
