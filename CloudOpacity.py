import random
import simpy

cloud_count = []

RANDOM_SEED = 12
NUM_SLOTS = 10  # Number of "slots" for a cloud
LIFETIME = random.randint(10,30)    # Minutes the for which cloud lasts
T_INTER = 5       # Create a cloud every ~5 minutes
SIM_TIME = 1440     # Simulation time in minutes, min per day
cloudList = []
cloudCount = []

class CloudModel(object):
    """A carwash has a limited number of machines (``NUM_MACHINES``) to
    clean cars in parallel.
    Cars have to request one of the machines. When they got one, they
    can start the washing processes and wait for it to finish (which
    takes ``washtime`` minutes).
    """
    def __init__(self, env, num_slots, lifetime):
        self.env = env
        self.machine = simpy.Resource(env, num_slots)
        self.lifetime = lifetime

    def wash(self, cloud):
        """The washing processes. It takes a ``car`` processes and tries
        to clean it."""
        yield self.env.timeout(LIFETIME)
        #print("%s is no longer over head at %.2f." % (cloud, env.now))


def cloud(env, name, cw):
    """The car process (each car has a ``name``) arrives at the carwash
    (``cw``) and requests a cleaning machine.
    It then starts the washing process, waits for it to finish and
    leaves to never come back ...
    """

    # print('%s arrives in the sky at %.2f.' % (name, env.now))
    with cw.machine.request() as request:
        yield request
        cloud_count.append(len(cloudList))
        # print('%s blocks the sun at %.2f.' % (name, env.now))
        cloudList.append(name)
        yield env.process(cw.wash(name))

        # print('%s is no longer in the sky at %.2f.' % (name, env.now))
        cloudList.remove(name)


def setup(env, num_machines, washtime, t_inter):
    """Create a sky, a number of initial clouds and keep creating clouds
    approx. every ``t_inter`` minutes."""
    # Create the cloudmodel
    cloudmodel = CloudModel(env, num_machines, washtime)

    start_time = env.now

    # Create 4 initial clouds
    for i in range(4):
        env.process(cloud(env, 'Cloud %d' % i, cloudmodel))

    # Create more clouds while the simulation is running
    while True:
        yield env.timeout(random.randint(t_inter-4, t_inter+4))
        i += 1
        env.process(cloud(env, 'Cloud %d' % i, cloudmodel))

        print ((cloudList))
        cloudCount.append(len(cloudList))


# Setup and start the simulation
# random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, NUM_SLOTS, LIFETIME, T_INTER))

# Execute!
env.run(until=SIM_TIME)
print()
print('The average cloud count was ' + str(round(sum(cloud_count)/len(cloud_count),3)) + ' clouds.')

def cloudOpacity():
    if len(cloudCount) > 289:
        del cloudCount[290:]
    elif len(cloudCount) < 289:
        while len(cloudCount) < 289:
            cloudCount.append(1)
            
    return (cloudCount)
