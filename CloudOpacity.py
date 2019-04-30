import random
import simpy

wait_time = []

RANDOM_SEED = 12
NUM_SLOTS = 10  # Number of "slots" for a cloud
LIFETIME = random.randint(10,40)    # Minutes the cloud lasts for
T_INTER = 5       # Create a car every ~7 minutes
SIM_TIME = 1440     # Simulation time in minutes


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
        print("%s is no longer over head at %.2f." % (cloud, env.now))


def cloud(env, name, cw):
    """The car process (each car has a ``name``) arrives at the carwash
    (``cw``) and requests a cleaning machine.

    It then starts the washing process, waits for it to finish and
    leaves to never come back ...

    """
    print('%s arrives in the sky at %.2f.' % (name, env.now))
    with cw.machine.request() as request:
        start_waiting = env.now
        yield request
        waiting_time = env.now-start_waiting
        wait_time.append(waiting_time)
        print('%s blocks the sun at %.2f.' % (name, env.now))
        yield env.process(cw.wash(name))

        print('%s is no longer in the sky at %.2f.' % (name, env.now))


def setup(env, num_machines, washtime, t_inter):
    """Create a carwash, a number of initial cars and keep creating cars
    approx. every ``t_inter`` minutes."""
    # Create the cloudmodel
    cloudmodel = CloudModel(env, num_machines, washtime)

    # Create 4 initial people
    for i in range(4):
        env.process(cloud(env, 'Cloud %d' % i, cloudmodel))

    # Create more cars while the simulation is running
    while True:
        yield env.timeout(random.randint(t_inter - 2, t_inter + 2))
        i += 1
        env.process(cloud(env, 'Cloud %d' % i, cloudmodel))


# Setup and start the simulation
# random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, NUM_SLOTS, LIFETIME, T_INTER))

# Execute!
env.run(until=SIM_TIME)
print()
print('The average wait time was ' + str(round(sum(wait_time)/len(wait_time),3)) + ' minutes.')