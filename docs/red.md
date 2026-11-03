# La red

## La casa

Del router salen tres Deco X20 en modo punto de acceso, que dan el WiFi a toda la casa. De uno de ellos cuelga un switch con el mini PC y mi PC por cable.

Cada aparato recibe del router dos DNS: el del servidor y 1.1.1.1. Si el servidor se apaga, los aparatos pasan solos a 1.1.1.1 y la casa sigue con internet, aunque sin filtrar.

El router no reenvía ningún puerto al servidor. El túnel de Tailscale lo abre el propio servidor hacia fuera, así que desde internet no se puede llegar a él.

## Dentro del mini PC

AdGuard pregunta a Cloudflare por DNS sobre HTTPS y, si no responde, a Quad9. El propio servidor resuelve con 1.1.1.1 y, de reserva, 9.9.9.9.

Los temporizadores de systemd hacen cuatro cosas: cada 5 minutos el latido le pregunta a AdGuard y a Uptime Kuma y avisa a Healthchecks, a las 04:00 se hace la copia en R2, a las 04:45 se preparan la lista de canales y su guía, y a las 09:00 se mira la salud del disco.

## Quién llega a qué

| Puerto | Servicio | Desde dónde |
| --- | --- | --- |
| 22 | SSH | Casa y Tailscale |
| 53 y 853 | DNS de AdGuard (normal y cifrado) | Casa y Tailscale |
| 3000 | Panel de AdGuard | Casa y Tailscale |
| 443 | Caddy (`kuma.lab`, `grafana.lab` y `ha.lab`) | Solo Tailscale |
| 8123 | Home Assistant | Solo Tailscale (normalmente por Caddy) |
| 34400 | Lista Casa | Solo casa |
| 3001, 3002, 9090 y 9100 | Uptime Kuma, Grafana, Prometheus y node_exporter | Solo el propio servidor (Kuma y Grafana, por Caddy) |

UFW solo deja pasar lo de esta tabla. Docker se salta UFW, así que los puertos de contenedores con red propia los publico en la IP de casa del servidor o en `127.0.0.1`, según quién tenga que llegar. Los que usan la red del sistema, como Home Assistant, sí pasan por UFW. Kuma y Grafana escuchan solo en `127.0.0.1`, así que la única forma de llegar a ellos es Caddy.
