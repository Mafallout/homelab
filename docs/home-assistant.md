# Home Assistant

Home Assistant es el centro de la domótica de casa: junta los aparatos, sean de la marca que sean, y deja controlarlos y automatizarlos desde el móvil sin depender de la nube de cada fabricante. De momento está listo para las luces de mi cuarto, y más adelante irán la tele del salón y un asistente de voz para la familia.

## Cómo está montado

- En Docker, con la versión exacta fijada y un límite de 1,5 GB de memoria y 2 núcleos, para que nunca le quite recursos a AdGuard. Recién instalado usa unos 450 MB.
- Con la red del sistema (`network_mode: host`). Home Assistant tiene que oír los avisos que los aparatos mandan a toda la red para descubrirlos, y dentro de una red de Docker no los oye. Además, así UFW sí se aplica.
- Su puerto no está abierto a la red de casa. Entro por Caddy, en `ha.lab.jdsantana.com`, con candado y solo por Tailscale, igual que en Uptime Kuma y Grafana. La app del móvil usa esa misma dirección, en casa y fuera. Si Caddy se cae, puedo entrar directo por la IP de Tailscale.
- Solo se fía de la cabecera `X-Forwarded-For` cuando llega de Caddy, desde el propio servidor. Si no se lo dices, rechaza todo lo que pasa por un proxy con un error 400.
- Uptime Kuma comprueba que responde por su nombre, así que también me avisa si falla Caddy.

## La copia

La configuración entra en la copia diaria. El historial (estados y gráficas) va en una base SQLite que cambia cada segundo, así que antes de la copia se vuelca con `VACUUM INTO`, como las de Kuma y Grafana, y la original se excluye. Los logs y la caché de voz se quedan fuera porque se vuelven a generar.

## Lo que me encontré

Desde la versión 2026.8, los ajustes de HTTP (como en qué proxy confiar) ya no van en `configuration.yaml`, sino en el panel. Si están en el YAML, Home Assistant los importa en el primer arranque, pero los deja pendientes hasta que un administrador los confirme. En una instalación nueva todavía no hay administrador, así que a los 5 minutos los deshizo. Al final creé la cuenta entrando directo por la IP de Tailscale y activé el proxy desde el panel.
