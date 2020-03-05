#Julio Herrera 19402
#Hoja de Trabajo 5
import random
import simpy
import math
import statistics

#environment configuration
interval = 1
RANDOM_SEED = 10
random.seed(RANDOM_SEED)
env = simpy.Environment()
#New
MemoryRAM = simpy.Container(env, init=100, capacity=100)
#Ready
numbersCPU = 1
#Running
velocityCPU = 3 #Instructios per cicle
#queues
cpus = simpy.Resource(env, capacity = 2)
timesPassed = []
#procesos
numberProcess = 200

def newProcess():
    for i in range(numberProcess):
        randomTimeToNewProcess = random.expovariate(1.0 / interval)
        processMemory = random.randint(1, 10)
        processInstructions = random.randint(1, 10)
        env.process(processNow(i, processMemory, processInstructions))
        yield env.timeout(randomTimeToNewProcess)

def processNow(id, processMemory, processInstructions):
    arrive = env.now
    print("----------------------------------------------------------------------")
    print("New Process ", id, " created at time ", arrive)
    with MemoryRAM.get(processMemory) as get:
        isFree = yield get | env.timeout(1)
        print("Process ", id, " waiting for ", processMemory," RAM at ", env.now)
        if get in isFree:
            print("RAM assigned to Process ", id)
            with cpus.request() as req:
                print("Process ", id, " waiting for free CPU at time ", env.now)
                isUsable = yield req | env.timeout(1)
                if req in isUsable:
                    print("CPU take Process ", id, " at time ", env.now)
                    terminated = False
                    while terminated == False:

                        nextState = 0
                        for i in range(velocityCPU):
                            processInstructions -= 1
                            if processInstructions > velocityCPU:
                                yield env.timeout(1)
                            else:
                                processInstructions = 0
                                nextState = random.randint(1, 2)

                        print("Left ", processInstructions, " instructions to finish the Process ", id, " at time ", env.now)

                        if processInstructions == 0:
                            terminated = True

                        if nextState == 1:
                            print("Process ", id, " waiting for Input Output at time ", env.now)
                            yield env.timeout(1)

        print("Process ", id, " finished at time ", env.now)
        MemoryRAM.put(processMemory)
    timePassed = int(env.now - arrive)
    timesPassed.append(timePassed)

#ejecucion
env.process(newProcess())
env.run()

#mostrando estadisticas
average = statistics.mean(timesPassed)
standardDev = statistics.stdev(timesPassed)

print("The average of times of all the process is ", average)
print("The standard deviation of all the process is ", standardDev)