# La red

## La casa

```mermaid
flowchart TD
    internet(("Internet"))
    router["Router de la operadora<br>DHCP · DNS1: el servidor · DNS2: 1.1.1.1"]
    decos["3 Deco X20 en modo AP<br>WiFi de toda la casa"]
    switch["Switch Netgear GS308E"]
    minipc["Mini PC homelab<br>Debian 13 · IP fija"]
    pc["Mi PC"]
    aparatos["Aparatos de casa<br>móviles, teles, PC y Mac"]
    respaldo["1.1.1.1 de Cloudflare"]
    fuera["Mi móvil y mi PC<br>fuera de casa"]

    internet --- router
    router ---|cable| decos
    decos ---|cable| switch
    switch --- minipc
    switch --- pc
    decos -.->|WiFi| aparatos
    aparatos -->|"DNS (53 y 853)"| minipc
    aparatos -.->|"si el servidor no responde"| respaldo
    fuera -.->|"túnel de Tailscale"| minipc
```

El switch cuelga de uno de los Deco, y de él salen el mini PC y mi PC. El resto de la casa va por WiFi.

Cada aparato recibe del router dos DNS: el del servidor y 1.1.1.1. Si el servidor se apaga, los aparatos pasan solos a 1.1.1.1 y la casa sigue con internet, aunque sin filtrar.

El router no reenvía ningún puerto al servidor. El túnel de Tailscale lo abre el propio servidor hacia fuera, así que desde internet no se puede llegar a él.

## Dentro del mini PC

```mermaid
flowchart LR
    casa["Red de casa"]
    ts["Tailscale<br>solo mis aparatos"]

    subgraph minipc["Mini PC"]
        subgraph sistema["Instalado en Debian"]
            ssh["SSH<br>solo con llave"]
            adguard["AdGuard Home<br>DNS 53 y 853 · panel 3000"]
            caddy["Caddy<br>443 · *.lab"]
            timers["Temporizadores de systemd<br>latido, copia, SMART y lista Casa"]
        end
        subgraph docker["Docker"]
            kuma["Uptime Kuma<br>3001"]
            grafana["Grafana<br>3002"]
            prom["Prometheus<br>solo 127.0.0.1"]
            nodeexp["node_exporter<br>solo 127.0.0.1"]
            lista["nginx con la lista Casa<br>34400 · solo red de casa"]
            ha["Home Assistant<br>8123"]
        end
    end

    subgraph nube["Fuera de casa"]
        cloudflare["Cloudflare<br>DNS sobre HTTPS"]
        quad9["Quad9<br>DNS de reserva"]
        r2["Cloudflare R2<br>copias cifradas"]
        hc["Healthchecks<br>latido, servicios, copias y SMART"]
        tdt["TDTChannels<br>lista y guía de canales"]
        telegram["Telegram<br>avisos al móvil"]
    end

    casa -->|DNS| adguard
    casa --> lista
    ts --> ssh
    ts --> adguard
    ts --> caddy
    ts -.->|"si cae Caddy"| kuma
    ts -.->|"si cae Caddy"| grafana
    ts -.->|"si cae Caddy"| ha
    caddy --> kuma
    caddy --> grafana
    caddy --> ha
    grafana --> prom
    prom --> nodeexp
    adguard --> cloudflare
    adguard -.->|"si Cloudflare falla"| quad9
    timers --> r2
    timers --> hc
    timers --> tdt
    timers -->|"escribe la lista y la guía"| lista
    kuma --> telegram
    grafana --> telegram
```

AdGuard y Caddy van instalados en el sistema, sin Docker. AdGuard es la pieza de la que depende la familia y así arranca aunque Docker falle. Pregunta a Cloudflare por DNS sobre HTTPS y, si no responde, a Quad9. El propio servidor resuelve con 1.1.1.1 y, de reserva, 9.9.9.9.

Los temporizadores hacen cuatro cosas: cada 5 minutos el latido le pregunta a AdGuard y a Uptime Kuma y avisa a Healthchecks, a las 04:00 se hace la copia en R2, a las 04:45 se preparan la lista de canales y su guía, y a las 09:00 se mira la salud del disco.

## Quién llega a qué

| Puerto | Servicio | Desde dónde |
| --- | --- | --- |
| 22 | SSH | Casa y Tailscale |
| 53 y 853 | DNS de AdGuard (normal y cifrado) | Casa y Tailscale |
| 3000 | Panel de AdGuard | Casa y Tailscale |
| 443 | Caddy (`kuma.lab`, `grafana.lab` y `ha.lab`) | Solo Tailscale |
| 3001 | Uptime Kuma | Solo Tailscale (normalmente por Caddy) |
| 3002 | Grafana | Solo Tailscale (normalmente por Caddy) |
| 8123 | Home Assistant | Solo Tailscale (normalmente por Caddy) |
| 34400 | Lista Casa | Solo casa |
| 9090 y 9100 | Prometheus y node_exporter | Solo el propio servidor |

UFW solo deja pasar lo de esta tabla. Docker se salta UFW, así que los puertos de contenedores con red propia los publico en la IP de casa del servidor o en `127.0.0.1`, según quién tenga que llegar. Los que usan la red del sistema, como Kuma, Grafana y Home Assistant, sí pasan por UFW.
