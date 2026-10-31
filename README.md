# homelab

Estoy montando un pequeño servidor en casa que protege la red de mi familia. Ya filtra la publicidad y los rastreadores, guarda copias de seguridad cifradas de su configuración y puedo administrarlo a distancia de forma segura.

## Hardware

HP EliteDesk 800 G4 Mini (i5-8500T, 16 GB, NVMe de 1 TB) y un switch Netgear GS308E.

## Qué hay montado

- Debian 13 sin entorno gráfico y con IP fija. Todo lo hago por SSH.
- Antes de fiarme de él: memtest con 12 pasadas sin errores, SMART limpio y Secure Boot activado.
- SSH con llave FIDO2, en dos YubiKey por si pierdo una. Sin contraseña y sin login de root. El móvil tiene su propia clave, que solo vale desde casa o por Tailscale.
- Tailscale para entrar desde fuera de casa sin abrir puertos en el router.
- Cortafuegos con UFW: bloquea todo lo que entra salvo SSH, lo que llega por Tailscale y, solo desde la red de casa, el DNS y el panel de AdGuard.
- Actualizaciones de seguridad automáticas.
- Se enciende solo cuando vuelve la luz después de un corte.
- AdGuard Home como DNS de toda la casa, con listas de bloqueo suaves y las consultas cifradas hacia fuera (DNS sobre HTTPS). El router reparte también 1.1.1.1 de respaldo por si el servidor se cae.
- DNS cifrado también dentro de casa (DNS sobre TLS).
- Un aviso desde fuera: cada 5 minutos el servidor le pregunta a su propio AdGuard y, si no recibe una IP, me salta una alarma en el móvil.
- Copias diarias cifradas con restic en Cloudflare R2, con otro aviso si una falla. Ya he probado a restaurarlas.
- Docker listo para los servicios, con su propio espacio en disco y logs acotados. Detalles en [docs/docker.md](docs/docker.md).
- Registro del uso de CPU, memoria y disco cada 10 minutos con sysstat.
- Uptime Kuma vigila cada servicio y me avisa por Telegram si alguno cae. Detalles en [docs/uptime-kuma.md](docs/uptime-kuma.md).
- Gráficas del servidor con Prometheus y Grafana, y un aviso al móvil si la CPU pasa de 90 °C. Detalles en [docs/monitorizacion.md](docs/monitorizacion.md).
- Una lista con 12 canales de TDT para la tele, que se prepara sola cada día y no depende del servidor para verse. Detalles en [docs/lista-casa.md](docs/lista-casa.md).

## Lo que he medido

AdGuard da servicio a 16 aparatos de casa. Los móviles Android aceptan su DNS cifrado, pero aun así mandan casi todas sus consultas a 1.1.1.1. Para arreglarlo tendría que quitar el DNS de respaldo, y entonces la casa se quedaría sin internet si se cae el servidor, así que lo dejo así.

## Siguiente

Nombres internos con candado para entrar a cada servicio desde el móvil.

El estado al día y la bitácora de cada sesión están en [jdsantana.com/homelab](https://jdsantana.com/homelab).
