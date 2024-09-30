from confluent_kafka import Consumer, KafkaException
import time
import json

class ClasePrueba:
    
    def __init__(self):

        # Configuración del consumidor
        conf = {
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'crypto_group',
            'auto.offset.reset': 'earliest'
        }

        # Crear el consumidor
        self.consumer = Consumer(conf)

        # Suscribirse al tópico
        self.consumer.subscribe(['crypto_price'])

        # === VARS ACUMULADORAS Y DE LOGICA

        # Tamaños
        self.btc_size = 0
        self.eth_size = 0

        # Capital transaccionado
        self.btc_capital = 0
        self.eth_capital = 0

        # Contador de mensajes recibidos
        self.count_message = 0

    def update_vars(self):
        
        try: 
            # Consumir hasta 10 mensajes a la vez con un timeout de 1 segundo
            messages = self.consumer.consume(num_messages=100, timeout=1.0)

            for msg in messages:

                if msg is None:
                    print("Mensaje vacío")
                    continue

                else:
                    
                    #DEcodificar datos
                    data = json.loads(msg.value().decode("utf-8"))

                    #detectar y contar criptomonedas
                    if data['product_id'] == 'BTC-USD':
                        self.btc_size += data['last_size']
                        self.btc_capital += data['transacted_capital']

                    elif data['product_id'] == 'ETH-USD':
                        self.eth_size += data['last_size']
                        self.eth_capital += data['transacted_capital']

                        print(" === BTC === ")
                        print(f"Total de criptomonedas trasnferidas: {self.btc_size}")
                        print(f"Total de capital trasnferido: {self.btc_size}")

                        print(" === ETH === ")
                        print(f"Total de criptomonedas trasnferidas: {self.eth_size}")
                        print(f"Total de capital trasnferido: {self.eth_capital}")


                if msg.error():
                    print(f"Error en el mensaje: {msg.error()}")
                    continue

                # Imprimir información del mensaje
                print(f"Mensaje recibido: {msg.value().decode('utf-8')}")
                print("--")


                #Contar cantidad de mensajes
                self.count_message += 1
                

        except:
            pass
