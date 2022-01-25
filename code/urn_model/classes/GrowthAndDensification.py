# simulation of method:

# institution growth = polya urn
#       - urn has colored balls, simulation gamma = nu/rho
# distribution of p,q: pick within-institution friends with probability p,
#   outside with probability q,epsilon
#   also check cross-institution scaling over time!!
import numpy as np
import scipy
import random

    
class densify:

    # each institution has:
    #   - number of researchers (updates)
    #   - set of researchers
    #   - # collaborators (determin from who connects to whom)
    def __init__(self,inst_id,p,q):
        # we make sure p,q are between 0 and 1
        p,q = self.in_range([p,q],[0,1])
        # institution ID
        self.id=inst_id
        # dict of researchers
        self.researchers = {}
        #self.researchers[new_researcher.id] = new_researcher
        # counts # researchers
        self.num_researchers = 0
        # this gets updated with densification
        self.num_internal_collaborations = 0
        self.num_external_collaborations = 0
        # densification parameters
        self.p = p
        self.q = q
        
    # class "researcher" is within each "institution":        
    class researcher:
        # each researcher has:
        #   - institution (number)
        #   - set of internal collaborators (updates)
        #   - set of external collaborators (updates)
        def __init__(self,res_id,institute):
            # researcher ID
            self.id = res_id
            # institution ID
            self.institution = institute
            # list of internal collaborator IDs
            self.internal_collaborators = set()
            # list of external collaborator IDs
            self.external_collaborators = []

    def in_range(self,array,limits):
        min_val,max_val = limits
        chopped_array = []
        for val in array:
            # if we are below range
            if val < min_val:
                chopped_array.append(min_val)
            # if we are above range
            elif val > max_val:
                chopped_array.append(max_val)
            # else we are within range
            else:
                chopped_array.append(val)
        return chopped_array        

    def find_researcher(self,researcher_id):
        # return researcher object
        if researcher_id in self.researchers.keys():
            res = self.researchers[researcher_id]
        else:
            res = None
        return res

    def find_first_internal_collab(self,res):
        # poisson distributed
        num_int = 1#np.random.poisson(1.0)
        if len(self.researchers) > 1:
            if num_int >= len(self.researchers):
                num_int = len(self.researchers) - 1;
            for i in range(num_int):
                random_id = self.pick_random_internal_collab(res)
                #print([res.id,random_id])
                # add researcher
                self.add_random_internal_collabs(res.id,random_id)
        
        
    def pick_random_internal_collab(self,res):
        
        # internal_collab_ids
        all_internal_researchers_ids = list(self.researchers.keys())
        # no self-loops: remove own id
        all_internal_researchers_ids.remove(res.id)
        # no multiple loops: do not connect to neighbors with whom we already collaborate
        for neighbor in res.internal_collaborators:
            all_internal_researchers_ids.remove(neighbor)
        # pick ID at random
        if len(all_internal_researchers_ids) > 0:
            random_id = np.random.choice(all_internal_researchers_ids)
        else:
            random_id = None
        return random_id

    def add_random_internal_collabs(self,res_id,random_id):
        if random_id is not None and random_id != res_id:
            # i->j
            self.researchers[res_id].internal_collaborators.add(random_id)
            # j->i
            self.researchers[random_id].internal_collaborators.add(res_id)
        
    def find_new_internal_collaborators(self,res):
        # connect with internal collaborators
        # "meat" of the densification simulation
        if len(self.researchers) > 1:
            # find collaborator of collaborators
            in_collab_candidates = self.find_internal_neighbors_neighbors(res)
            # add new neighbors
            self.add_internal_densification_neighbors(res.id,in_collab_candidates)
            
    def make_connections(self,candidates,p):
        # make connection with neighbors
        # 1: successful collaboration
        # 0: unsuccessful collaboration
        collab_rand = np.random.binomial(1,p,len(candidates))
        # ID of new collaborators
        new_collabs = candidates[collab_rand==1].tolist()
        if len(new_collabs) == 0:
            new_collabs = None
        return new_collabs
        
    def add_internal_densification_neighbors(self,res_id,candidates):
        # new collaborators
        new_collabs =self.make_connections(candidates,self.p)
        if new_collabs is not None:
            # add new collaborators
            # i->j
            self.researchers[res_id].internal_collaborators.update(new_collabs)
            # j->i
            self.add_incoming_internal_collabs(new_collabs,res_id)

    def add_incoming_internal_collabs(self,new_collabs,res_id):
        #print(len(new_collabs))
        for collab in new_collabs:
            self.researchers[collab].internal_collaborators.add(res_id)
        
    def find_internal_neighbors_neighbors(self,res):
        neighbors_neighbors = set()
        # search through internal collaborators
        # use the following to help parallelize
        #pool = multiprocessing.Pool(4)
        #neighbors_neighbors = zip(*pool.map(calc_stuff, res.internal_collaborators))
        for collab_id in res.internal_collaborators:
            # get collaborator object
            collab = self.find_researcher(collab_id)
            # find neighbors neighbors
            collab_neighbors = collab.internal_collaborators
            #collab_neighbors.remove(res.id)
            neighbors_neighbors.update(collab_neighbors)
        # neighbors not already a collaborator
        neighbors_neighbors = neighbors_neighbors - res.internal_collaborators - set([res.id])
        
        neighbors_neighbors = np.array(list(neighbors_neighbors))
        return neighbors_neighbors
    

    # densification statistics
    def find_num_collaborations(self):
        self.num_internal_collaborations = 0
        self.num_external_collaborations = 0
        #last_institute
        for r in self.researchers.keys():
            res = self.researchers[r]
            self.num_internal_collaborations += len(res.internal_collaborators)
            self.num_external_collaborations += len(res.external_collaborators)
        # we double-count internal collaborators
        # we therefore divide by 2
        self.num_internal_collaborations /= 2;
    def find_num_researchers(self):
        self.num_researchers = len(self.researchers)

    
# polya urn growth model
class ball_color:
    def __init__(self,new_color,trigger_color):
        # number of balls with color
        self.num_balls = 1
        # color of group
        self.color = new_color
        # weight we give to most/all elements with label
        self.weight = 1
        # triggered s_t-1 color
        self.triggered_last_color = False
        # color of ball that triggered this color
        self.trigger_color = trigger_color
        
class grow:            
    def __init__(self,N0):
        self.sequence = []
        self.balls = []
        #print(N0)
        for color in range(N0):
            new_ball = ball_color(color,-1)
            self.balls.append(new_ball)
                                                            
    def add_ball(self,color,trigger_color):
        # if new color
        if color >= len(self.balls):
            self.balls.append(ball_color(color,trigger_color))
        else:
            self.balls[color].num_balls += 1
                                                            
    def urn_weight(self):
        total_weight = 0;
        ball_weights = []
        #print(len(self.balls))
        for color in self.balls:
            # number of balls with given color
            num_balls = color.num_balls
            # weight of each ball (except ball that triggered last color)
            color_weight = color.weight
            # if element triggered the color of the ball in timestep t-1
            trigger_weight = 0
            if color.triggered_last_color:
                num_balls -= 1
                trigger_weight = 1
            color_weight = color_weight*num_balls + trigger_weight
            total_weight += color_weight
            ball_weights.append(color_weight)
        return [np.array(ball_weights),total_weight]

    def grow_institutes(self,rho,nu,eta,sim_time):
        for t in range(sim_time):
            self.add_ball_to_sequence(rho,nu,eta)


    def add_ball_to_sequence(self,rho,nu,eta):
        picked_ball = self.pick_ball()
        self.sequence.append(picked_ball.color)
        self.copy_balls(picked_ball,rho)
        trigger = self.trigger_ball(picked_ball,nu)
        self.new_weights(picked_ball,trigger,nu,eta)
                                                            
    def pick_ball(self):
        # pick balls proportional to their weight
        # weight of each ball, total_weight
        ball_weights,total_weight = self.urn_weight()
        # weighted probability
        p_array = ball_weights/total_weight
        # ball chosen at random
        random_ball = np.random.choice(self.balls,p=p_array)
        return random_ball
                                                            
    def copy_balls(self,picked_ball,rho):
        # add rho new balls to urn with ball color
        color = picked_ball.color
        trigger_color = picked_ball.trigger_color
        # rho is an integer
        for ball in range(rho):
            self.add_ball(color,trigger_color)
                                                            
    def unique_colors(self,n):
        return set(self.sequence[:n])
    def total_num_researchers(self):
        return len(self.sequence)
    def total_num_institutes(self):
        return len(self.unique_colors(len(self.sequence)))
                                                                
    def trigger_ball(self,new_ball,nu):
        # if ball color is new to sequence...
        # i.e., only appears at the very end of the sequence
        # then we trigger

        # unique institutes before this point
        unique_institutes = self.unique_colors(len(self.sequence)-1)
        # assume not trigger
        trigger = False
        # if new ball
        if new_ball.color not in unique_institutes:
            trigger = True
             # add new colors
            # latest color
            latest_color = len(self.balls)
            trigger_color = new_ball.color
            for new_color in range(latest_color,latest_color+nu+1):
                self.add_ball(new_color,trigger_color)                                                    
        return trigger
    def new_weights(self,picked_ball,trigger, nu,eta):
        
        for color in range(len(self.balls)):
            # unless noted otherwise, colors have weight eta
            self.balls[color].weight = eta
            # unless otherwise noted,
            # assume color did not trigger last element's color
            self.balls[color].triggered_last_color = False

        # weight 1 to the following:

        # weight 1 to colors same as picked ball
        self.balls[picked_ball.color].weight = 1
                                                            
        # weight 1 to elements triggered by ball
        if trigger:
            for color in range(len(self.balls)-nu-1,len(self.balls)):
                self.balls[color].weight = 1
        
        # weight 1 to element that triggered ball
        trigger_color = picked_ball.trigger_color
        self.balls[trigger_color].triggered_last_color = True

    def record_entropy(self,sequence,institute):

        event_pos=np.argwhere(np.array(sequence)==institute).ravel()
        
        k = len(event_pos)
        #print(k)
        total_events = len(sequence)-min(event_pos)
        if k==1:
            return [1,0]
        bin_width=int(round(total_events/k))
        
        bins = range(min(event_pos),len(sequence),bin_width)
        events_per_bin = np.histogram(event_pos,bins)[0]
        probability = events_per_bin/k
        probability = probability[probability>0]
        entropy = -np.sum(probability*np.log(probability))
        norm_entropy = entropy/np.log(k)
        return [k,norm_entropy]
                                                                
    def record_mean_entropy(self,sequence):
        # unique institutes
        unique_institutes = set(sequence)
        entropy_institute=[]
        for institute in unique_institutes:
            k,norm_entropy = self.record_entropy(sequence,institute)
            if norm_entropy is not None:
                entropy_institute.append([k,norm_entropy])
        entropy_institute = np.array(entropy_institute)
        max_k = np.max(entropy_institute[:,0])
        delta_k = 0.05
        bin_array = [10**x for x in np.arange(0,np.log10(max_k)+delta_k,delta_k)]
        bin_vals = np.array([bin_array[i:i+2] for i in range(0,len(bin_array),1) if len(bin_array[i:i+2])>1])
        mean_entropy_k =[]
        for b1,b2 in bin_vals:
            binned_entropy=entropy_institute[b1<entropy_institute[:,0]]
            binned_entropy=binned_entropy[binned_entropy[:,0]<=b2]
            if len(binned_entropy) > 0:
                mean_entropy = np.mean(binned_entropy[:,1])
            else:
                mean_entropy = np.nan
            mean_entropy_k.append(mean_entropy)
        entropy_data = {'entropy_k':mean_entropy_k,'bin_low':list(bin_vals[:,0]),'bin_high':list(bin_vals[:,1])}
        return entropy_data
    def record_local_mean_entropy(self,entropy_institute):
        entropy_institute = np.array(entropy_institute)
        max_k = np.max(entropy_institute[:,0])
        delta_k = 0.05
        bin_array = [10**x for x in np.arange(0,np.log10(max_k)+delta_k,delta_k)]
        bin_vals = np.array([bin_array[i:i+2] for i in range(0,len(bin_array),1) if len(bin_array[i:i+2])>1])
        mean_entropy_k =[]
        for b1,b2 in bin_vals:
            binned_entropy=entropy_institute[b1<entropy_institute[:,0]]
            binned_entropy=binned_entropy[binned_entropy[:,0]<=b2]
            if len(binned_entropy) > 0:
                mean_entropy = np.mean(binned_entropy[:,1])
            else:
                mean_entropy = np.nan
            mean_entropy_k.append(mean_entropy)
        entropy_data = {'entropy_k':mean_entropy_k,'bin_low':list(bin_vals[:,0]),'bin_high':list(bin_vals[:,1])}
        return entropy_data
    
    def inter_event_times(self,sequence,institute):
        # find the distribution for 1 institute
        event_pos=np.argwhere(np.array(sequence)==institute).ravel()
        interevent_times = event_pos[1:]-event_pos[:-1]
        return interevent_times
    def flatten(self,lol):
        return [s for l in lol for s in l];
    def inter_event_time_dist(self,sequence):
        # unique institutes
        unique_institutes = set(sequence)
        # find the pos
        events = self.flatten([self.inter_event_times(sequence,institute) for institute in unique_institutes])
        delta_t=0.05
        bin_array = [10**x for x in np.arange(0,np.log10(max(events))+delta_t,delta_t)]
        bin_vals  = np.array([bin_array[i:i+2] for i in range(0,len(bin_array),1) if len(bin_array[i:i+2])>1])
        hist = np.histogram(events,bin_array)
        EventHist = {'histogram':list(hist[0]),'bin_low':list(bin_vals[:,0]),'bin_high':list(bin_vals[:,1])}
        return EventHist
    def local_inter_event_time_dist(self,events):
        events=np.array(events)
        delta_t=0.05
        bin_array = [10**x for x in np.arange(0,np.log10(max(events))+delta_t,delta_t)]
        bin_vals  = np.array([bin_array[i:i+2] for i in range(0,len(bin_array),1) if len(bin_array[i:i+2])>1])
        hist = np.histogram(events,bin_array)
        EventHist = {'histogram':list(hist[0]),'bin_low':list(bin_vals[:,0]),'bin_high':list(bin_vals[:,1])}
        return EventHist

    def randomize_globally(self):
        rand_seq = self.sequence[:];
        np.random.shuffle(rand_seq)
        return rand_seq
    
    def randomize_locally(self,institute):
        # find first occurence of institute
        first_pos = self.sequence.index(institute)
        if first_pos == len(self.sequence)-1:
            return self.sequence
        else:
            reshuffled = self.sequence[first_pos:]
            np.random.shuffle(reshuffled)
            return self.sequence[:first_pos]+reshuffled
    def record_growth_statistics(self,sequence):
        # record:
        #       - Zipf's law: log-binned research size distribution
        #       - Heap's law: {# researchers, # institutions}
        #       - sequence entropy(k)
        #       - times between researchers join institutes
        
        # Zipf's law
        delta_n = 0.05
        bin_array = [10**x for x in np.arange(0,np.log10(len(sequence))+delta_n,delta_n)]
        bin_vals  = np.array([bin_array[i:i+2] for i in range(0,len(bin_array),1) if len(bin_array[i:i+2])>1])
        num_res_per_institute = [sequence.count(institute) for institute in set(sequence)]
        hist = np.histogram(num_res_per_institute,bin_array)
        
        ZipfLaw = {'histogram':list(hist[0]),'bin_low':list(bin_vals[:,0]),'bin_high':list(bin_vals[:,1])}
        
        # Heap's law: {# researchers,#institutes}
        HeapsLaw ={'num_researchers':list(range(len(sequence))),'num_institutes':[len(set(sequence[:n])) for n in range(len(sequence))]}
        
        # entropy
        EntropyK = self.record_mean_entropy(sequence)
        # inter-event times
        InterEventTimes = self.inter_event_time_dist(sequence)
        data = {'ZipfLaw':ZipfLaw,'HeapsLaw':HeapsLaw,'EntropyK':EntropyK,'InterEventTimes':InterEventTimes}
        return data                                                                       
