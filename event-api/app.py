from flask import Flask, request, jsonify
import redis
import os
import threading
import pika

app = Flask(__name__)

# Conexão com Redis (cache de eventos)
redis_client = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379)
events_key = 'events:list'

# Endpoint HTTP para receber alerta da API Node.js
@app.route('/event', methods=['POST'])
def receive_event():
    data = request.json
    redis_client.rpush(events_key, str(data))
    return '', 204

# Endpoint HTTP para listar todos os eventos
@app.route('/events', methods=['GET'])
def list_events():
    raw = redis_client.lrange(events_key, 0, -1)
    return jsonify([eval(x) for x in raw])

# Função que fica consumindo a fila 'logistics' do RabbitMQ
def consume():
    params = pika.URLParameters(os.getenv('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/'))
    conn = pika.BlockingConnection(params)
    ch = conn.channel()
    ch.queue_declare(queue='logistics', durable=True)

    def callback(ch, method, properties, body):
        redis_client.rpush(events_key, body.decode())
        ch.basic_ack(delivery_tag=method.delivery_tag)

    ch.basic_consume(queue='logistics', on_message_callback=callback)
    ch.start_consuming()

if __name__ == '__main__':
    # Inicia o consumidor RabbitMQ em background
    t = threading.Thread(target=consume, daemon=True)
    t.start()
    app.run(host='0.0.0.0', port=5000)
