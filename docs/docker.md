# Docker

Docker es la base de los servicios que vienen después (Uptime Kuma, Jellyfin, Immich, Home Assistant...). Cada servicio corre en su contenedor, aislado del resto y con su configuración en `/opt/servicios/<servicio>/compose.yaml`.

## Cómo está montado

- **Volumen propio de 150 GiB** en `/var/lib/docker`, creado con LVM en el espacio libre del disco. Si un contenedor se desboca y llena el disco, llena el suyo y no el del sistema, así que AdGuard sigue respondiendo.
- **Repositorio oficial de Docker**, no el de Debian, porque va más al día. Se actualiza solo con las actualizaciones automáticas, igual que Tailscale.
- **Mi usuario no está en el grupo `docker`.** Estar en ese grupo es como ser root sin contraseña, así que uso siempre `sudo docker`.
- **Logs acotados antes del primer contenedor:** driver `local`, que rota y comprime los logs de cada contenedor (unos 100 MB como máximo). El de fábrica, `json-file`, crece sin límite.
- **Reglas para cada contenedor:** versión de la imagen fijada (nunca `latest`, para que nada cambie sin que yo lo decida) y un límite de memoria, para que ninguno le quite RAM a AdGuard.

## Docker se salta UFW

Cuando un contenedor publica un puerto, Docker mete sus propias reglas en iptables y ese tráfico no pasa por las reglas de UFW. El puerto queda abierto aunque `ufw status` no lo diga. Por eso:

- Lo que es solo de casa se publica en la IP de casa del servidor, y no responde por Tailscale.
- Lo que solo usa el propio servidor se publica en `127.0.0.1`.
- Los servicios con `network_mode: host` usan la red del sistema, y ahí UFW sí aplica.
- Para cerrar de verdad un puerto de un contenedor, la regla va en la cadena `DOCKER-USER`.

La frontera real es que el router no reenvía ningún puerto y que por Tailscale solo entran mis aparatos.

## sysstat

Además, el servidor guarda cada 10 minutos el uso de CPU, memoria y disco con sysstat. Con `sar` veo qué pasaba a una hora concreta, por ejemplo si el ventilador suena fuerte sin motivo aparente.
