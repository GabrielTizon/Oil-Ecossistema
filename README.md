API 1 – Módulo de Sensores em Node

Finalidade:

Cria uma simulação de dados de temperatura e pressão, como se viessem de poços de petróleo reais.

Permite gerar dados via GET /sensor-data e enviar alertas via POST /alert.

API 2 – Módulo de Eventos Críticos em Python

O que faz:

Atua como um receptor de alertas via HTTP, encaminha esses alertas via RabbitMQ e os armazena como eventos.

Disponibiliza um POST /event para inserir eventos manualmente e GET /events para a visualização completa do histórico de eventos.

API 3 – Módulo de Logística em PHP

O que faz:

Lista equipamentos disponíveis via GET /equipments.

Publica mensagens de despacho urgente na fila do RabbitMQ, utilizando um POST para o endpoint /dispatch.

A comunicação é variada: alertas usam HTTP diretamente para a API Event, enquanto os pedidos passam pelo RabbitMQ, garantindo que cheguem mesmo que algum serviço esteja fora do ar. O Redis serve como um cache na API Sensor (10 s para /sensor-data) e como um banco de dados rápido na API Event. Já o RabbitMQ separa o envio do processamento dos pedidos.
