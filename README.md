# Segundo proyecto DE: Tiempo de respuesta de páginas web más visitadas

El objetivo de este proyecto es hacer uso de las herramientas de GCP para crear dashboards actualizados que muestren la latencia del usuario contra las páginas más populares del país. La idea de este proyecto es poder adquirir experiencia trabajando con datos en streaming, es decir, que llegan constantemente y no tienen un final definido. Las herramientas utilizadas son:

-  Python
-  PubSub
-  Dataflow
-  BigQuery
-  Looker Studio

![Diagrama](https://github.com/sebakjal/ping_streaming/blob/main/FlowDiagram.png)

## Procedimiento

Para calcular la latencia de una página se usa el comando de bash "ping", que combinado con otros comandos produce una linea de texto con los siguientes datos:

Fecha y hora del momento de medición de ping, el ping promedio, máximo y mínimo durante la medición, y la desviación estándar durante esta.

El resto del código, escrito en Python, se encarga de correr este comando de bash continuamente, recibir la información, transformarla a formato JSON y enviar esta información ("mensaje" como se denomina en PubSub) hacia un tópico de PubSub.
Dentro de la plataforma de GCP se setea una pipeline en Dataflow que capta todos los mensajes JSON del tópico de PubSub y los parsea a filas, que son enviadas a una tabla de BigQuery.

Este proceso se realiza de forma ininterrumpida o hasta que manualmente se pare de correr el código.

Por último, los datos guardados en BigQuery se utilizan para crear un dashboard en Looker Studio, mostrando gráficos de serie temporal de la evolución de la latencia en el tiempo. En la imagen de ejemplo se muestran 2 gráficos, el primero tiene la línea de el ping promedio y máximo en la última hora, mientras que el segundo representa el ping promedio para todo el día.

![Ejemplo](https://github.com/sebakjal/ping_streaming/blob/main/ejemplo2.png)

El proyecto logró mostrar resultados para una página en tiempo real a través de Looker Studio, pero falta agregar más indicadores, ordenar más el código y agregar más páginas. 

A pesar de los resultados, el desarrollo del proyecto se dejó en pausa debido a los costos de mantener esta pipeline.
