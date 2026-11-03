# Prometheus y Grafana

Gráficas del servidor (temperatura, CPU, RAM, disco y red) y avisos al móvil cuando algo se sale de lo normal.

Son tres contenedores en cadena: node_exporter lee los datos del sistema, Prometheus los recoge cada 15 segundos y los guarda 30 días, y Grafana los dibuja con el panel "Node Exporter Full".

## Los avisos

Grafana me avisa por Telegram si la CPU pasa de 90 °C durante 2 minutos, si el NVMe pasa de 70 °C, si a un disco le queda menos del 15 % libre o si queda menos del 10 % de RAM.

La CPU llegó a 87 °C en la prueba de carga del principio, así que si salta ese aviso es que algo va mal: primero se limpia el polvo del ventilador y, si sigue igual, se cambia la pasta térmica.

Las alertas están en ficheros de configuración y no creadas a mano, así que vuelven solas si reinstalo Grafana. La de la CPU la probé con el umbral en 30 °C para ver que el aviso llegaba de verdad.

Me pasó que la alerta apuntaba a un aviso de Telegram que todavía no había creado en el panel, y Grafana no arrancaba. Primero tiene que existir el aviso y después la alerta.

## Cómo está montado

- node_exporter y Prometheus solo escuchan en `127.0.0.1`, porque no tienen contraseña.
- Grafana va en el puerto 3002 (el 3000 es de AdGuard), solo en `127.0.0.1`. Se entra por Caddy en `grafana.lab.jdsantana.com`, que solo responde por Tailscale.
- Los tres contenedores sin capacidades de Linux (`cap_drop: ALL`) y con `no-new-privileges`. No les hace falta ninguna.
- Grafana trae de serie plugins para muchas bases de datos y cada uno arranca su propio proceso. Solo uso Prometheus, así que los demás están desactivados, y Grafana gasta bastante menos RAM.
- Versiones exactas fijadas y límites de memoria: 256 MB para Prometheus, 768 MB para Grafana y 64 MB para node_exporter.
- La configuración y los paneles entran en la copia diaria. Los datos de Prometheus no, porque se vuelven a generar solos.
- Uptime Kuma comprueba que Grafana responde.
