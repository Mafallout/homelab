# Uptime Kuma

Uptime Kuma comprueba cada minuto que cada servicio responde y, si alguno cae, me avisa por Telegram con un bot mío.

Ahora vigila el DNS de AdGuard (le pregunta por `cloudflare.com` y espera una IP), el panel de AdGuard, Grafana y la lista de canales de la tele. Cada servicio nuevo entra aquí en cuanto existe.

Kuma está dentro del servidor, así que si el servidor se apaga no avisa nadie. Para eso está el latido de Healthchecks, que avisa desde fuera si la máquina deja de dar señales.

## Cómo está montado

- En Docker con `network_mode: host`, para que UFW se aplique. Su puerto solo está abierto a la red de casa y por Tailscale.
- Versión exacta fijada (2.5.8). La subo yo a mano cada mes.
- Límite de 512 MB de memoria. En reposo usa unos 130 MB.
- Base de datos SQLite, que es un solo fichero y entra en la copia diaria con el resto de `/opt/servicios`.
