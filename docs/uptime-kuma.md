# Uptime Kuma

Uptime Kuma vigila cada servicio desde dentro del servidor: cada minuto comprueba que responde y, si deja de hacerlo, me avisa por Telegram con un bot propio.

## Qué vigila

- **DNS de AdGuard:** le pregunta por `cloudflare.com` y espera una IP. Si falla, el filtrado de la casa ha caído (la casa sigue navegando con el DNS de respaldo del router).
- **Panel de AdGuard:** que la web del panel abre.
- Cada servicio nuevo entra aquí en cuanto existe. Es una regla del proyecto: ningún servicio sin vigilancia, sin copia y sin límite de memoria.

## Dos capas de vigilancia

Kuma no puede avisar de su propia caída: si el servidor se apaga, se apaga con él. Para eso está el latido externo de Healthchecks, que avisa si la máquina entera deja de dar señales. El latido cubre la caída total y Kuma cada servicio por separado.

## Decisiones

- **Docker con `network_mode: host`:** el contenedor usa la red del sistema, así que UFW sí se aplica (con un puerto publicado normal, Docker se saltaría UFW). Su puerto solo está abierto a la red de casa y por Tailscale.
- **Versión exacta fijada** (`2.5.8`), no la etiqueta `2`, que cambia sola. Las actualizaciones las hago yo a mano cada mes.
- **Límite de 512 MB de memoria.** En reposo usa unos 110 MB.
- **Base de datos SQLite:** un solo fichero, sin otro servidor de base de datos que mantener.
- **Dentro de la copia:** `/opt/servicios`, donde vive su configuración, entra en la copia diaria cifrada.
