from confluent_kafka import Consumer, KafkaException
import time
import json

class CryptoConsumer:
    
    def __init__(self):

        #Conf to consumer
        conf = {
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'crypto_group',
            'auto.offset.reset': 'earliest'
        }

        # Create consumer with conf
        self.consumer = Consumer(conf)

        #Subscribe to the topic
        self.consumer.subscribe(['crypto_price'])

        # === Accumulator vars

        #sizes
        self.btc_size = 0
        self.eth_size = 0

        #transacted capital
        self.btc_capital = 0
        self.eth_capital = 0

        #counter messages
        self.count_message = 0


    #Goal: update vars 
    def update_vars(self):
        
        try: 
            #Consume to up 100 message for each second
            messages = self.consumer.consume(num_messages=100, timeout=1.0)

            #scroll through list looking for data
            for msg in messages:

                if msg is None:
                    print("Mensaje vacío")
                    continue

                else:
                    
                    #decode data
                    data = json.loads(msg.value().decode("utf-8"))

                    #detect and updte vars
                    if data['product_id'] == 'BTC-USD':
                        self.btc_size += data['last_size']
                        self.btc_capital += data['transacted_capital']

                    elif data['product_id'] == 'ETH-USD':
                        self.eth_size += data['last_size']
                        self.eth_capital += data['transacted_capital']

                        print(" === BTC === ")
                        print(f"Total number of cryptocurrencies transferred: {self.btc_size}")
                        print(f"Total capital transferred: {self.btc_size}")

                        print(" === ETH === ")
                        print(f"Total number of cryptocurrencies transferred: {self.eth_size}")
                        print(f"Total capital transferred: {self.eth_capital}")


                #Control errors
                if msg.error():
                    print(f"Error with message: {msg.error()}")
                    continue

                #Print message receive
                print(f"message received: {msg.value().decode('utf-8')}")


                #Count message
                self.count_message += 1
                

        except:
            pass