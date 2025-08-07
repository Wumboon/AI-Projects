from __future__ import print_function
from game import sd_peers, sd_spots, sd_domain_num, init_domains, \
    restrict_domain, SD_DIM, SD_SIZE
import random, copy

class AI:
    def __init__(self):
        pass

    def solve(self, problem):
        sigma={}
        domains = init_domains()
        stack = []
        nonAssigned=[]
        lastMove=()
        Delta=[]
        restrict_domain(domains, problem)
        #for x in domains:
            #print(type(domains[x]))
        #print(domains, " before")
        #print(sigma, " before")
        while True:
            nonAssigned=False;
            #Delta=[]
            #sigma=domains
            sigma[(99,99)]="11111"
            sigma,domains=self.propogate(sigma,domains)
            if sigma[(99,99)]=="Conflict":
                if len(Delta)==0:
                    print("in None")
                    return None;
                else:
                    # print(" Before Backtrace")
                    # print(sigma)
                    # print()
                    # print(domains)
                    # print(" BEFORE ELTA VAL")
                    #for x in Delta:
                        # print(x)
                        # print(" DELTA VAL")
                    sigma,domains=self.Backtrack(Delta)
                    # print(" After Backtrace")
                    # print(sigma)
                    # print()
                    # print(domains)
            else:

                for x in sigma:
                    #print(sigma)
                    if x!=(99,99) and len(sigma[x])>1:
                        nonAssigned=True
                if(len(sigma)==82 and nonAssigned==False):
                    #print(domains)
                    #print()
                    #print(sigma)
                    return domains;
                else:
                    #print(lastMove)
                    sigma,lastMove=self.MakeDecision(sigma,domains)
                    #print(" in delta")
                    Delta.append(copy.deepcopy(sigma))
                    Delta.append(lastMove)
                    Delta.append(copy.deepcopy(domains))
        #print(sigma)
        #print(domains)
            #print(sigma)
        #print(domains)

        # TODO: implement backtracking search.
        #print(sd_peers)
        # TODO: delete this block ->
        # Note that the display and test functions in the main file take domains as inputs.
        #   So when returning the final solution, make sure to take your assignment function
        #   and turn the value into a single element list and return them as a domain map.
        #print(sd_domain_num)
        # for spot in sd_spots:
        #     #print(domains[spot])
        #     domains[spot] = [1]
        # return domains
        # <- TODO: delete this block
        #return domains

    # TODO: add any supporting function you need

    def propogate(self,sigma,domains):
        #pass;
        #while True:
        #print('in')
        while True:
            somethingRemoved=False;
            for x in domains:
                if(len(domains[x])==1):
                    sigma[x]=domains[x]

            for x in sigma:
                if(x!=(99,99) and len(domains[x])>1):
                    domains[x]=sigma[x]

            for x in domains:
                if(len(domains[x])==0):
                    sigma[(99,99)]="Conflict"
                    return sigma,domains
            for x in domains:
                for y in sd_peers[x]:
                    if len(domains[y])==1 and domains[y][0] in domains[x]:
                        domains[x].remove(domains[y][0])
                        somethingRemoved=True;

            if(somethingRemoved==False):
                return sigma,domains;

        #pass;
    def MakeDecision(self,sigma,domains):
        smallest=99;
        currentTouple=();
        if(len(sigma)!=82):
            for x in domains:
                #print(domains[x])
                if len(domains[x])>1 and smallest>len(domains[x]):

                    currentTouple=x
                    smallest=len(domains[x]);
                    if(smallest==2):
                        break;
                    # val=[random.choice(domains[x])]
                    # sigma[x]=val
                    # return sigma,x
        val=[random.choice(domains[currentTouple])]
        sigma[currentTouple]=val
        return sigma,currentTouple

    def Backtrack(self,Delta):
        domains=Delta.pop()
        lastMove=Delta.pop()
        sigma=Delta.pop()
        lastValue=sigma[lastMove][0]
        sigma.pop(lastMove)
        domains[lastMove].remove(lastValue)
        return sigma,domains
    #### The following templates are only useful for the EC part #####

    # EC: parses "problem" into a SAT problem
    # of input form to the program 'picoSAT';
    # returns a string usable as input to picoSAT
    # (do not write to file)
    def sat_encode(self, problem):
        text = ""

        # TODO: write CNF specifications to 'text'

        return text

    # EC: takes as input the dictionary mapping
    # from variables to T/F assignments solved for by picoSAT;
    # returns a domain dictionary of the same form
    # as returned by solve()
    def sat_decode(self, assignments):
        # TODO: decode 'assignments' into domains

        # TODO: delete this ->
        domains = {}
        for spot in sd_spots:
            domains[spot] = [1]
        return domains
        # <- TODO: delete this