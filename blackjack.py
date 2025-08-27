
import copy
import random

from game import Game, states

HIT = 0
STAND = 1
DISCOUNT = 0.95 #This is the gamma value for all value calculations

class Agent:
    def __init__(self):

        # For MC values
        self.MC_values = {} # Dictionary: Store the MC value of each state
        self.S_MC = {}      # Dictionary: Store the sum of returns in each state
        self.N_MC = {}      # Dictionary: Store the number of samples of each state
        # MC_values should be equal to S_MC divided by N_MC on each state (important for passing tests)

        # For TD values
        self.TD_values = {}  # Dictionary: Store the TD value of each state
        self.N_TD = {}       # Dictionary: Store the number of samples of each state

        # For Q-learning values
        self.Q_values = {}   # Dictionary: Store the Q-Learning value of each state and action
        self.N_Q = {}        # Dictionary: Store the number of samples of each state for each action

        # Initialization of the values
        for s in states:
            self.MC_values[s] = 0
            self.S_MC[s] = 0
            self.N_MC[s] = 0
            self.TD_values[s] = 0
            self.N_TD[s] = 0
            self.Q_values[s] = [0,0] # First element is the Q value of "Hit", second element is the Q value of "Stand"
            self.N_Q[s] = [0,0] # First element is the number of visits of "Hit" at state s, second element is the Q value of "Stand" at s

        # Game simulator
        # NOTE: see the comment of `init_cards()` method in `game.py` for description of the initial game states
        self.simulator = Game()

    # NOTE: do not modify this function
    # This is the fixed policy given to you, for which you need to perform MC and TD policy evaluation.
    @staticmethod
    def default_policy(state):
        user_sum = state[0]
        user_A_active = state[1]
        actual_user_sum = user_sum + user_A_active * 10
        if actual_user_sum < 14:
            return 0
        else:
            return 1

    # NOTE: do not modify this function
    # This is the fixed learning rate for TD and Q learning.
    @staticmethod
    def alpha(n):
        return 10.0/(9 + n)


    def make_one_transition(self, action):
        # if(self.simulator.game_over()):
        #     return None;

        if action == 0:
            self.simulator.act_hit();
            return self.simulator.state,self.simulator.check_reward()
        elif action == 1:
            self.simulator.act_stand();
            return self.simulator.state,self.simulator.check_reward()

    #TODO: Implement MC policy evaluation
    def MC_run(self, num_simulation, tester=False):

        # Perform num_simulation rounds of simulations in each cycle of the overall game loop
        for simulation in range(num_simulation):
            if tester:
                self.tester_print(simulation, num_simulation, "MC")
            self.simulator.reset()  # The simulator is already reset for you for each new trajectory

            holdingCheck2=[];
            if(self.simulator.game_over()):
                holdingCheck2.append((self.simulator.state,self.simulator.check_reward()))
            else:
                while not self.simulator.game_over():
                    holdingCheck2.append((self.simulator.state,self.simulator.check_reward()))
                    self.make_one_transition(self.default_policy(self.simulator.state))
                holdingCheck2.append((self.simulator.state,self.simulator.check_reward()))
                #print(holdingCheck2)
                for i in range(len(holdingCheck2)):
                    total=0;
                    for j in range(len(holdingCheck2)):
                        total+=(DISCOUNT**j)*holdingCheck2[j][1]
                    self.S_MC[holdingCheck2[0][0]]+=total;
                    self.N_MC[holdingCheck2[0][0]]+=1;
                    self.MC_values[holdingCheck2[0][0]]=self.S_MC[holdingCheck2[0][0]]/self.N_MC[holdingCheck2[0][0]]
                    del holdingCheck2[0]




    #TODO: Implement TD policy evaluation
    def TD_run(self, num_simulation, tester=False):

        # Perform num_simulation rounds of simulations in each cycle of the overall game loop
        for simulation in range(num_simulation):

            # Do not modify the following three lines
            if tester:
                self.tester_print(simulation, num_simulation, "TD")
            self.simulator.reset()

            holdingCheck2=[];
            if(self.simulator.game_over()):
                holdingCheck2.append((self.simulator.state,self.simulator.check_reward()))
            else:
                while not self.simulator.game_over():
                    holdingCheck2.append((self.simulator.state,self.simulator.check_reward()))
                    self.make_one_transition(self.default_policy(self.simulator.state))
                holdingCheck2.append((self.simulator.state,self.simulator.check_reward()))


            for i in range(len(holdingCheck2)):
                 if(i!=len(holdingCheck2)-1):
                    self.TD_values[holdingCheck2[i][0]]=self.TD_values[holdingCheck2[i][0]] + self.alpha(self.N_TD[holdingCheck2[i][0]])*(holdingCheck2[i][1]+
                    (DISCOUNT*self.TD_values[holdingCheck2[i+1][0]]) - self.TD_values[holdingCheck2[i][0]]  )
                    self.N_TD[holdingCheck2[i][0]]+=1;
                    #print(holdingCheck2[i][0], "  ",self.TD_values[holdingCheck2[i][0]], " current state and value")
                    #print(holdingCheck2[i+1][0], "  ",self.TD_values[holdingCheck2[i+1][0]], " next state and value")
                 else:
                    self.TD_values[holdingCheck2[i][0]]=holdingCheck2[i][1];
                    self.N_TD[holdingCheck2[i][0]]+=1;
                    #print(holdingCheck2[i][0], "  ",self.TD_values[holdingCheck2[i][0]], " current state and value")



    #TODO: Implement Q-learning
    def Q_run(self, num_simulation, tester=False, epsilon=0.4):

        # Perform num_simulation rounds of simulations in each cycle of the overall game loop
        for simulation in range(num_simulation):
            # Do not modify the following three lines
            if tester:
                self.tester_print(simulation, num_simulation, "Q")
            self.simulator.reset()

            #holdingCheck2=[];
            trackingAction=0;
            while(not self.simulator.game_over()):
                a=self.pick_action(self.simulator.state,0.4)
                prev_state=self.simulator.state;
                prev_stateReward=self.simulator.check_reward();
                self.make_one_transition(a)
                self.Q_values[prev_state][a]=self.Q_values[prev_state][a]+ self.alpha(self.N_Q[prev_state][a])*(
                prev_stateReward+ DISCOUNT*(max(self.Q_values[self.simulator.state][HIT],self.Q_values[self.simulator.state][STAND])) - self.Q_values[prev_state][a])
                self.N_Q[prev_state][a]+=1;
                trackingAction=a;
            self.Q_values[self.simulator.state][trackingAction]=self.simulator.check_reward();
            #self.Q_values[self.simulator.state][1]=self.simulator.check_reward();
            self.N_Q[self.simulator.state][trackingAction]+=1;
            #self.N_Q[self.simulator.state][1]+=1;
               


    #TODO: Implement epsilon-greedy policy
    def pick_action(self, s, epsilon):
        # TODO: Replace the following random value with an action following the epsilon-greedy strategy
         if(random.uniform(0, 1))< epsilon:
             return random.randint(0,1)
         else:
             return self.autoplay_decision(s);

    ####Do not modify anything below this line####

    #Note: do not modify
    def autoplay_decision(self, state):
        hitQ, standQ = self.Q_values[state][HIT], self.Q_values[state][STAND]
        if hitQ > standQ:
            return HIT
        if standQ > hitQ:
            return STAND
        return HIT #Before Q-learning takes effect, just always HIT

    # NOTE: do not modify
    def save(self, filename):
        with open(filename, "w") as file:
            for table in [self.MC_values, self.TD_values, self.Q_values, self.S_MC, self.N_MC, self.N_TD, self.N_Q]:
                for key in table:
                    key_str = str(key).replace(" ", "")
                    entry_str = str(table[key]).replace(" ", "")
                    file.write(f"{key_str} {entry_str}\n")
                file.write("\n")

    # NOTE: do not modify
    def load(self, filename):
        with open(filename) as file:
            text = file.read()
            MC_values_text, TD_values_text, Q_values_text, S_MC_text, N_MC_text, NTD_text, NQ_text, _  = text.split("\n\n")

            def extract_key(key_str):
                return tuple([int(x) for x in key_str[1:-1].split(",")])

            for table, text in zip(
                [self.MC_values, self.TD_values, self.Q_values, self.S_MC, self.N_MC, self.N_TD, self.N_Q],
                [MC_values_text, TD_values_text, Q_values_text, S_MC_text, N_MC_text, NTD_text, NQ_text]
            ):
                for line in text.split("\n"):
                    key_str, entry_str = line.split(" ")
                    key = extract_key(key_str)
                    table[key] = eval(entry_str)

    # NOTE: do not modify
    @staticmethod
    def tester_print(i, n, name):
        print(f"\r  {name} {i + 1}/{n}", end="")
        if i == n - 1:
            print()
