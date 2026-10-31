# Docker

Docker es la base de los servicios del homelab. Cada servicio va en su contenedor, con su configuración en `/opt/servicios/<servicio>/compose.yaml`.

## Cómo está montado

- Volumen propio de 150 GiB en `/var/lib/docker`, creado con LVM. Si un contenedor llena el disco, llena el suyo y AdGuard sigue respondiendo.
- Instalado desde el repositorio oficial de Docker, y se actualiza solo como el resto del sistema.
- Mi usuario no está en el grupo `docker`, porque estar en él es como ser root sin contraseña. Uso `sudo docker`.
- Logs con el driver `local`, que los rota y los comprime (unos 100 MB por contenedor como mucho). Lo puse antes del primer contenedor porque solo se aplica a los que se crean después.
- Cada contenedor lleva la versión de la imagen fijada y un límite de memoria, para que nada cambie sin que yo lo decida y ninguno le quite RAM a AdGuard.

## Docker se salta UFW

Cuando un contenedor publica un puerto, Docker mete sus propias reglas en iptables y ese tráfico no pasa por UFW. El puerto queda abierto aunque `ufw status` no lo diga. Por eso lo que es solo de casa se publica en la IP de casa del servidor, lo que solo usa el propio servidor en `127.0.0.1`, y los servicios con `network_mode: host` usan la red del sistema, donde UFW sí se aplica. Para cerrar de verdad un puerto de un contenedor, la regla va en la cadena `DOCKER-USER`.

## sysstat

El servidor guarda cada 10 minutos el uso de CPU, memoria y disco con sysstat. Con `sar` veo qué pasaba a una hora concreta, por ejemplo si el ventilador suena fuerte sin motivo.
