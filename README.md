# Demo utilizando bottle.py

Esto es un ejemplo básico para el uso de `bottle`, para escribir un `API` y el modulo estándar de Python `http.server` para levantar un servidor que tenga nuestras paginas estáticas.

> Este proyecto utiliza `pipenv`
> Antes de iniciar hay que copiar el archivo `example.env` a el archivo `.env` como `cp example.env .env`

Este ejemplo, esta diseñado para correr dos servidores de desarrollo, uno para un sitio estático, dicho sitio, y otro con un servidor que sirve como un API que sera consumido por el sitio estático.


## Ejecución

Para iniciar este proyecto, hay que instalarlo con el comando `pipenv install`.


Para correr el servidor de archivos estáticos ejecutar el siguiente comando.

```
pipenv run www
```

Para levantar el servidor de datos hay que ejecutar 

```
pipenv run server
```

## Notas

Este ejemplo fue construido durante una demostración en vivo durante la clase de _Cómputo en la nube_ en la _Universidad Tecnológica de Tijuana_.
