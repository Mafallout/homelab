# Caddy

Caddy recibe las visitas por el puerto 443 y las reparte a cada servicio por su nombre: `kuma.lab.jdsantana.com` va a Uptime Kuma y `grafana.lab.jdsantana.com` a Grafana. Así entro con un nombre y con candado en vez de con IP y puerto.

## El certificado

Uso un certificado comodín de Let's Encrypt para `*.lab.jdsantana.com`, que vale para todos los servicios a la vez. Para darlo, Let's Encrypt pide demostrar que el dominio es mío, y Caddy lo hace creando un registro temporal en el DNS de Cloudflare (reto DNS-01). No hace falta abrir ningún puerto a internet.

Caddy lo pide y lo renueva solo, y Uptime Kuma me avisa si se acerca la caducidad.

## Los nombres

En Cloudflare hay un registro `*.lab.jdsantana.com` que apunta a la IP de Tailscale del servidor, sin el proxy de Cloudflare. Así cualquier nombre `lab` funciona en el móvil, en casa o fuera, sin tocar AdGuard. Esa IP solo sirve dentro de mi red de Tailscale, así que aunque sea pública no abre nada.

## Solo por Tailscale

Los nombres del Caddyfile solo responden si la conexión viene de `100.64.0.0/10`, el rango que usa Tailscale, y cualquier otro nombre se corta. Desde la red de casa no llega ni a Caddy, porque UFW no abre el 443 a casa.

## Cómo está montado

- Caddy viene del repositorio oficial, pero el de apt no trae el módulo de Cloudflare. Uso el binario de su web con ese módulo y lo dejo por encima del de apt con `dpkg-divert` y `update-alternatives`, para que una actualización no lo pise. Cuando sale una versión nueva, lo actualizo a mano.
- El token de Cloudflare solo puede tocar el DNS de `jdsantana.com`. Está en un fichero que solo lee root y el servicio lo carga con `EnvironmentFile`, así no aparece en la configuración ni lo ve otro usuario.
- La API de administración de Caddy no escucha en un puerto, sino en un socket que solo puede abrir el propio Caddy. Con ella se podría sacar el token, y en un puerto la podría usar cualquier programa del servidor.
- Si Caddy se cae, systemd lo vuelve a arrancar solo.

## Lo que me encontré

El servicio de Caddy de Debian arranca con `--environ`, que escribe en el log todas sus variables, también el token. Lo quité con un drop-in de systemd y cambié el token.
