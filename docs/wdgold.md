# El disco de 10 TB

Un WD Gold de 10 TB en una caja USB, para las fotos, las películas y una segunda copia del servidor. El servidor no depende de él: si falta, arranca igual.

## Cómo está montado

- Una sola partición ext4 en `/srv/wdgold`, montada por su UUID y sin cifrar, para que el servidor se encienda solo después de un corte.
- `nofail` en `fstab`: si el disco no está, el servidor arranca sin él.
- `chattr +i` en la carpeta vacía, para que nada escriba en el NVMe si el disco no está montado.
- Formateado con `-m 0`, porque es solo de datos y no necesita espacio reservado para root.
- Si enciendo la caja con el servidor ya arrancado, una regla de udev lo monta solo.

## El ruido

Suena bastante, así que de 23:30 a 8:30 está parado: `hd-idle` lo para a los 20 minutos sin uso y su copia va a las 13:00. Lo saqué de `smartd` y le puse un filtro en LVM, porque los dos lo despertaban.

## Las copias

- La configuración del servidor se copia cada día con restic a Cloudflare R2 y a este disco.
- Las fotos y las películas no van en ninguna copia.
- El archivo de fotos viejas solo está en este disco. Si SMART avisa, lo primero es sacarlo a otro sitio.

## Los avisos

Telegram si el disco se desmonta o se llena, y Healthchecks si SMART ve algo raro o falla una copia.
