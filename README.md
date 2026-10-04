# homelab

Estoy montando un pequeño servidor en casa que protegerá la red de mi familia: filtrará publicidad y rastreadores, guardará copias de seguridad cifradas, y podré administrarlo a distancia de forma segura.

## Hardware

HP EliteDesk 800 G4 Mini (i5-8500T, 16 GB, NVMe de 1 TB) y un switch Netgear GS308E.

## Qué hay montado

- Debian 13 sin entorno gráfico y con IP fija. Todo lo hago por SSH.
- SSH solo con llave, en dos YubiKey por si pierdo una. Sin contraseña y sin login de root.
- Tailscale para entrar desde fuera de casa sin abrir puertos en el router.
- UFW: solo deja pasar SSH y Tailscale.
- Actualizaciones de seguridad automáticas.
- Se enciende solo cuando vuelve la luz después de un corte.

## Siguiente

AdGuard Home como DNS de toda la casa.