import json
import websocket
from datetime import datetime
from confluent_kafka import Producer


class CryptoTracker:


    #Initialization vars
    def __init__(self, crypto_symbols):


        #Producer, send data to kafka
        conf = {'bootstrap.servers': "localhost:9092"}
        self.producer = Producer(conf)

        #list of simbols - always use USD from U.S.A
        self.crypto_symbols = [symbol.upper() + "-USD" for symbol in crypto_symbols]

        #Key's to counter crypto
        self.key_crypto_size = 'crypto_size'


    #Goal: open conexion with coinbase, and subscribe to the order flow and trades
    def on_open(self, ws):
        print(f"Successful connection, subscribe symbols: {', '.join(self.crypto_symbols)}")

        # Suscribe message 
        subscribe_message = {
            "type": "subscribe",
            "channels": [{"name": "ticker", "product_ids": self.crypto_symbols}]
        }

        #Send subscribe message to coinbase
        ws.send(json.dumps(subscribe_message))


    # Goal: receive data from Coinbase
    def on_message(self, ws, message):


        # Load data in dict
        data = json.loads(message)

        #data to count
        data_count = {
            'product_id' : data['product_id'],
            'price': float(data['price']),
            'last_size': float(data['last_size']),
        }

        #add 'trasacted_capital' in 'data_count'
        data_count['transacted_capital'] = data_count['price'] * data_count['last_size']

        self.count_crypto(data_count)


    #Goal: assing key to send message in specific partition of kafka
    def count_crypto(self,data_count):
        

        #convert the message to JSON - format: <str>
        message_json = json.dumps(data_count)
            
        #Send mesagge, with key
        self.producer.produce('crypto_price', value=message_json)

        self.producer.flush()  # Ensure the message is sent

        print(f"Sent to Kafka: {message_json}")


    #Goal: close connection
    def on_close(self, ws, close_status_code, close_msg):
        print("Conexión cerrada")

    #Goal: execute in case of error
    def on_error(self, ws, error):
        print(f"Error: {error}")

#Symbols
symbols = ['BTC','ETH']

#Create instance
tracker = CryptoTracker(crypto_symbols = symbols)

# URL web socket from coinbase
socket_url = "wss://ws-feed.exchange.coinbase.com"


#Create a websocket and define the functions, using methods from the class.
ws = websocket.WebSocketApp(socket_url,
                            on_open=tracker.on_open,
                            on_message=tracker.on_message,
                            on_close=tracker.on_close,
                            on_error=tracker.on_error)

#Run connection 
ws.run_forever()


"""
Paso a paso para ocupar kafka:

1 - encender zookoper (controlador de kafka)

    bin/zookeeper-server-start.sh config/zookeeper.properties

2 - Iniciar broker local

    bin/kafka-server-start.sh config/server.properties

    
3 - Crear topico

    bin/kafka-topics.sh --create --topic crypto_price --bootstrap-server localhost:9092  --replication-factor 1



"""