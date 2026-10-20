# homelab

Estoy montando un pequeño servidor en casa que protege la red de mi familia. Ya filtra la publicidad y los rastreadores y puedo administrarlo a distancia de forma segura. Le falta guardar copias de seguridad cifradas.

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
- AdGuard Home como DNS de toda la casa, con listas de bloqueo suaves y las consultas cifradas hacia fuera (DNS sobre HTTPS).
- Un aviso desde fuera: cada 5 minutos el servidor le pregunta a su propio AdGuard y, si no recibe una IP, me salta una alarma en el móvil.

## Siguiente

DNS secundario de respaldo y copias cifradas diarias con restic.

El estado al día y la bitácora de cada sesión están en [jdsantana.com/homelab](https://jdsantana.com/homelab).
