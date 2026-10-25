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
- DNS cifrado también dentro de casa (DNS sobre TLS), para que los móviles Android lo usen en vez de irse al de Cloudflare.
- Un aviso desde fuera: cada 5 minutos el servidor le pregunta a su propio AdGuard y, si no recibe una IP, me salta una alarma en el móvil.
- Copias diarias cifradas con restic en Cloudflare R2, con otro aviso si una falla. Ya he probado a restaurarlas.

## Siguiente

Pasar un día entero con el servidor apagado para comprobar que la casa sigue con internet, y después Docker.

El estado al día y la bitácora de cada sesión están en [jdsantana.com/homelab](https://jdsantana.com/homelab).
