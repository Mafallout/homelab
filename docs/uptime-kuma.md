# Uptime Kuma

Uptime Kuma comprueba cada minuto que cada servicio responde y, si alguno cae, me avisa por Telegram con un bot mío.

Ahora vigila el DNS de AdGuard (le pregunta por `cloudflare.com` y espera una IP), el panel de AdGuard, Grafana, Caddy y su certificado, y la lista de canales de la tele. Cada servicio nuevo entra aquí en cuanto existe.

Kuma está dentro del servidor, así que si el servidor se apaga no avisa nadie. Para eso está el latido de Healthchecks, que avisa desde fuera si la máquina deja de dar señales. Otro aviso de Healthchecks salta si Kuma deja de responder.

## Cómo está montado

- En Docker con `network_mode: host`, para que UFW se aplique. Su puerto solo está abierto por Tailscale y entro por `kuma.lab.jdsantana.com`.
- Versión exacta fijada (2.5.8). La actualizo yo a mano.
- Límite de 512 MB de memoria. En reposo usa unos 130 MB.
- Sin permisos de más: sin `NET_RAW` y con `no-new-privileges`. Sus datos, que llevan el token del bot de Telegram, solo los lee root.
- Base de datos SQLite, que es un solo fichero. Antes de la copia diaria se vuelca con `VACUUM INTO`, para copiarla entera aunque Kuma esté escribiendo en ella.
