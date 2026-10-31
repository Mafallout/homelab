# Prometheus y Grafana

Gráficas del servidor (temperatura, CPU, RAM, disco y red) y un aviso al móvil si la CPU se calienta demasiado.

Son tres contenedores en cadena: node_exporter lee los datos del sistema, Prometheus los recoge cada 15 segundos y los guarda 30 días, y Grafana los dibuja con el panel "Node Exporter Full".

## El aviso de temperatura

Si la CPU pasa de 90 °C durante 2 minutos, Grafana me avisa por Telegram. En la prueba de carga del principio llegó a 87 °C, así que si salta es que algo va mal: primero se limpia el polvo del ventilador y, si sigue igual, se cambia la pasta térmica.

La alerta está en un fichero de configuración y no creada a mano, así que vuelve sola si reinstalo Grafana. La probé con el umbral en 30 °C para ver que el aviso llegaba de verdad.

Me pasó que la alerta apuntaba a un aviso de Telegram que todavía no había creado en el panel, y Grafana no arrancaba. Primero tiene que existir el aviso y después la alerta.

## Cómo está montado

- node_exporter y Prometheus solo escuchan en `127.0.0.1`, porque no tienen contraseña.
- Grafana va en el puerto 3002 (el 3000 es de AdGuard) y solo se llega por Tailscale: UFW no abre ese puerto a casa.
- Versiones exactas fijadas y límites de memoria: 512 MB para Prometheus, 512 MB para Grafana y 64 MB para node_exporter.
- La configuración y los paneles entran en la copia diaria. Los datos de Prometheus no, porque se vuelven a generar solos.
- Uptime Kuma comprueba que Grafana responde.
