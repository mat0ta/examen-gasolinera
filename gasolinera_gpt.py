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
