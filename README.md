# Examen Gasolinera 17/04

Examen realizado por: [mat0ta](https://github.com/mat0ta)

[ [Link del repositorio](https://github.com/mat0ta/examen-gasolinera) ]
 
El examen realizado a continuación tiene el siguiente enunciado.

# Práctica 3: Simulador de gasolinera

## Objetivo

El objetivo de la práctica es simular una gasolinera bajo las siguientes premisas.
   A la gasolinera llegan coches a un intervalo aleatorio de hasta T minutos.
   La gasolinera consta de N surtidores de combustible.
   Cuando un coche se pone en la surtidor de combustible, el conductor se baja,
    elije el combustible de su elección y llena el depósito. Este trabajo le lleva un
    tiempo de entre 5 y 10 minutos.
    Tras llenar el depósito se acerca a la oficina de pago y se pone a la cola de la
    caja. Suponga que la caja es única.
    En pagar tarda 3 minutos.
    Tras terminar el pago retira el coche, dejando el surtidor libre para el siguiente
    coche.
    
## Realización

Se pide:
    Modelar el problema con los objetos apropiado indicando los estados en que
    puede estar cada elemento.
    Se modelarán los coches como Threads que genera el programa principal. A
    efectos del ejercicio se generan 50 coches.
    Realizar el problema para un tiempo T de 15 minutos y N de un surtidor de
    combustible.
    Calcular el tiempo medio que tarda un coche desde que llega a la gasolinera
    hasta que sale de ella.
    A efectos del problema los minutos se tratarán en el programa con centésimas
    de segundo.
    
Una vez realizada la parte anterior:

    Ampliar la gasolinera para que se disponga de 4 surtidores de combustible.
    Cuando llega un coche se pone en el primer surtidor que esté libre o en el que
    tiene menos coches en la cola. Pruebe con distintos tiempos de T para
    calcular los tiempos medios en repostar. 
    
    
El código empleado para resolver la tarea es el siguiente:

```py
import threading
import time
import random

class Gasolinera:
    def __init__(self, T, N, C):
        self.tiempo = [1, T]
        self.surtidores = N
        self.coches = C
        self.t_repostage = [5, 10]
        self.gasolinera = threading.Semaphore(N)
        self.cola = threading.Semaphore(0)
        self.mutex = threading.Semaphore(1)
        self.cochesEnCola = 0
        self.cochesAtendidos = 0
        self.tiempos = [0] * 50
    
    def coche(self, id, tiempo):
        while True:
            time.sleep(random.randint(1, 5))
            self.tiempos[id] = tiempo
            self.mutex.acquire()
            if self.cochesEnCola < self.coches:
                self.cochesEnCola += 1
                self.cola.release()
                self.mutex.release()
                self.gasolinera.acquire()
                print("Coche ", id, " está respostando.")
                t = random.randint(self.t_repostage[0], self.t_repostage[1])
                self.tiempos[id] += t
                time.sleep(t)
                print("Coche ", id, " ha terminado de respostar. Ha tardado " + str(t) + " minutos. Pagando...")
                self.tiempos[id] += 3
                time.sleep(3)
                print("Coche ", id, " ha terminado de pagar. Ha tardado 3 minutos. Saliendo...")
                self.gasolinera.release()
                self.cochesAtendidos += 1
                self.cochesEnCola -= 1
                if self.cochesAtendidos == self.coches:
                    break
            else:
                self.mutex.release()
                print("Coche ", id, " ha decidido irse.")
                break

    def main(self):
        for i in range(self.coches):
            threading.Thread(target=self.coche, args=(i, random.randint(self.tiempo[0], self.tiempo[1]))).start()
        for i in range(self.coches):
            self.cola.acquire()
        if self.cochesAtendidos == self.coches:
            print("Todos los coches han sido atendidos.")
            print("Tiempo medio de espera: " + str(self.get_average_time()))
    
    def get_average_time(self):
        av_time = 0
        for i in range(self.coches):
            av_time += self.tiempos[i]
        return av_time / self.coches

if __name__ == "__main__":
    gasolinera = Gasolinera(15, 1, 50)
    gasolinera.main()
```

Además, se ha generado código para resolver el examen através de la IA de Chat GPT.

```py
import threading
import queue
import random
import time

class Car(threading.Thread):
    def __init__(self, name, gas_station, payment_queue):
        threading.Thread.__init__(self)
        self.name = name
        self.gas_station = gas_station
        self.payment_queue = payment_queue

    def run(self):
        print(f"{self.name} arrives at the gas station")
        fuel_type = random.choice(["Regular", "Plus", "Premium"])
        print(f"{self.name} chooses {fuel_type} fuel")
        time_to_fill = random.randint(5, 10) * 10  # centiseconds
        self.gas_station.get_fuel(fuel_type, time_to_fill)
        print(f"{self.name} goes to pay")
        self.payment_queue.put(self)
        time.sleep(3 * 10)  # centiseconds
        print(f"{self.name} leaves the gas station")

class GasStation:
    def __init__(self, num_pumps):
        self.pumps = [True] * num_pumps
        self.queue = queue.Queue()

    def get_fuel(self, fuel_type, time_to_fill):
        while True:
            for i in range(len(self.pumps)):
                if self.pumps[i]:
                    self.pumps[i] = False
                    print(f"Start filling up at pump {i+1} ({fuel_type})")
                    time.sleep(time_to_fill)
                    print(f"Stop filling up at pump {i+1} ({fuel_type})")
                    self.pumps[i] = True
                    return

    def pay(self):
        car = self.queue.get()
        print(f"{car.name} starts paying")

if __name__ == "__main__":
    gas_station = GasStation(1)
    payment_queue = queue.Queue()
    cars = []
    for i in range(50):
        car = Car(f"Car {i+1}", gas_station, payment_queue)
        cars.append(car)
        car.start()

    for car in cars:
        car.join()

    total_time = 0
    for i in range(50):
        car = payment_queue.get()
        total_time += car.wait_time
    average_time = total_time / 50
    print(f"Average time: {average_time/10} seconds")

    gas_station = GasStation(4)
    payment_queue = queue.Queue()
    cars = []
    for i in range(50):
        car = Car(f"Car {i+1}", gas_station, payment_queue)
        cars.append(car)
        car.start()

    for car in cars:
        car.join()

    total_time = 0
    for i in range(50):
        car = payment_queue.get()
        total_time += car.wait_time
    average_time = total_time / 50
    print(f"Average time: {average_time/10} seconds")
```
