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