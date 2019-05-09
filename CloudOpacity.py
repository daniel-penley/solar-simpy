import random
import simpy

cloud_count = []

RANDOM_SEED = 12
NUM_SLOTS = 10  # Number of "slots" for a cloud
LIFETIME = random.randint(10,30)    # Minutes the for which cloud lasts
T_INTER = 5       # Create a cloud every ~5 minutes
SIM_TIME = 2000     # Simulation time in minutes
cloudList = []
cloudCount = []

class CloudModel(object):
    """The sky has a limited number of slots for clouds (``NUM_SLOTS``) for
    clouds to 'exist'.
    When a cloud fills a slot, they reside there for their LIFETIME.
    """
    def __init__(self, env, num_slots, lifetime):
        self.env = env
        self.machine = simpy.Resource(env, num_slots)
        self.lifetime = lifetime

    def life(self, cloud):
        """Cloud is overhead. It takes a ``cloud`` process and lets it sit
        for its life."""
        yield self.env.timeout(LIFETIME)

def cloud(env, name, st):
    """The cloud process (each cloud has a ``name``) arrives at the slot
    (``st``) and requests a spot in the sky.
    It then starts its lifetime, waits for it to finish and
    leaves to never come back ...
    """

    with st.machine.request() as request:
        yield request
        cloud_count.append(len(cloudList))
        cloudList.append(name)
        yield env.process(st.life(name))

        cloudList.remove(name)

def setup(env, num_slots, lifetime, t_inter):
    """Create a sky, a number of initial clouds and keep creating clouds
    approx. every ``t_inter`` minutes."""
    # Create the cloudmodel
    cloudmodel = CloudModel(env, num_slots, lifetime)

    start_time = env.now

    # Create 4 initial clouds
    for i in range(4):
        env.process(cloud(env, 'Cloud %d' % i, cloudmodel))

    # Create more clouds while the simulation is running
    while True:
        yield env.timeout(random.randint(t_inter-4, t_inter+4))
        i += 1
        env.process(cloud(env, 'Cloud %d' % i, cloudmodel))

        cloudCount.append(len(cloudList))

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, NUM_SLOTS, LIFETIME, T_INTER))

# Execute!
env.run(until=SIM_TIME)

def cloudOpacity():
    if len(cloudCount) > 289:
        del cloudCount[290:]
    elif len(cloudCount) < 289:
        while len(cloudCount) < 289:
            cloudCount.append(1)
            
    return (cloudCount)
