
# assume there is data of the form:
# sequence = [1,2,6,3,7,...]
# each number corresponds to a unique institute ID
import numpy as np
import pandas as pd
import shutil,os,time
import pickle as pk
from glob import glob

def unique_colors(sequence,n):
    return set(sequence[:n])
def total_num_researchers(sequence):
    return len(sequence)
def total_num_institutes(sequence):
    return len(unique_colors(sequence,len(sequence)))
                                                            
def record_entropy(sequence,institute):
    event_pos=np.argwhere(np.array(sequence)==institute).ravel()
    k = len(event_pos)
    if k==1:
        return [1,0]

    total_events = len(sequence)-min(event_pos)
    
    bin_width=int(round(total_events/k))
    
    bins = range(min(event_pos),len(sequence),bin_width)
    events_per_bin = np.histogram(event_pos,bins)[0]
    probability = events_per_bin/k
    probability = probability[probability>0]
    entropy = -np.sum(probability*np.log(probability))
    norm_entropy = entropy/np.log(k)
    
    return [k,norm_entropy]
                                                            
def record_mean_entropy(sequence):
    # unique institutes
    unique_institutes = set(sequence)
    #print(len(unique_institutes))
    entropy_institute=[]
    for institute in unique_institutes:
        k,norm_entropy = record_entropy(sequence,institute)
        #print([k,norm_entropy])
        if norm_entropy is not None:
            entropy_institute.append([k,norm_entropy])
    entropy_institute = np.array(entropy_institute)
    
    #print(entropy_institute)
    max_k = np.max(entropy_institute[:,0])
    delta_k = 0.05
    bin_array = [10**x for x in np.arange(0,np.log10(max_k)+delta_k,delta_k)]
    bin_vals = np.array([bin_array[i:i+2] for i in range(0,len(bin_array),1) if len(bin_array[i:i+2])>1])
    #print(bin_vals)
    mean_entropy_k =[]
    for b1,b2 in bin_vals:
        binned_entropy=entropy_institute[b1<entropy_institute[:,0]]
        binned_entropy=binned_entropy[binned_entropy[:,0]<=b2]
        if len(binned_entropy) > 0:
            mean_entropy = np.mean(binned_entropy[:,1])
        else:
            mean_entropy = np.nan
        mean_entropy_k.append(mean_entropy)
    #mean_entropy_k = [np.mean(np.argwhere(b1<entropy_institute[:,1]<=b2).ravel()) for b1,b2 in bin_vals]
    #print(mean_entropy_k)
    entropy_data = {'entropy_k':mean_entropy_k,'bin_low':list(bin_vals[:,0]),'bin_high':list(bin_vals[:,1])}
    return entropy_data
def record_local_mean_entropy(entropy_institute):
    
    entropy_institute = np.array(entropy_institute)
    max_k = np.max(entropy_institute[:,0])
    delta_k = 0.05
    bin_array = [10**x for x in np.arange(0,np.log10(max_k)+delta_k,delta_k)]
    bin_vals = np.array([bin_array[i:i+2] for i in range(0,len(bin_array),1) if len(bin_array[i:i+2])>1])
    #print(bin_vals)
    mean_entropy_k =[]
    for b1,b2 in bin_vals:
        binned_entropy=entropy_institute[b1<entropy_institute[:,0]]
        binned_entropy=binned_entropy[binned_entropy[:,0]<=b2]
        #print(binned_entropy)
        if len(binned_entropy) > 0:
            mean_entropy = np.mean(binned_entropy[:,1])
        else:
            mean_entropy = np.nan
        mean_entropy_k.append(mean_entropy)
    entropy_data = {'entropy_k':mean_entropy_k,'bin_low':list(bin_vals[:,0]),'bin_high':list(bin_vals[:,1])}
    return entropy_data

def inter_event_times(sequence,institute):
    # find the distribution for 1 institute
    event_pos=np.argwhere(np.array(sequence)==institute).ravel()
    interevent_times = event_pos[1:]-event_pos[:-1]
    return interevent_times
def flatten(lol):
    return [s for l in lol for s in l];
def inter_event_time_dist(sequence):
    # unique institutes
    unique_institutes = set(sequence)
    # find the pos
    events = [inter_event_times(sequence,institute) for institute in unique_institutes]
    events = flatten(events)
    delta_t=0.05
    bin_array = [10**x for x in np.arange(0,np.log10(max(events))+delta_t,delta_t)]
    bin_vals  = np.array([bin_array[i:i+2] for i in range(0,len(bin_array),1) if len(bin_array[i:i+2])>1])
    hist = np.histogram(events,bin_array)
    EventHist = {'histogram':list(hist[0]),'bin_low':list(bin_vals[:,0]),'bin_high':list(bin_vals[:,1])}
    return EventHist
def local_inter_event_time_dist(events):
    events=np.array(events)
    delta_t=0.05
    bin_array = [10**x for x in np.arange(0,np.log10(len(events)),delta_t)]
    bin_vals  = np.array([bin_array[i:i+2] for i in range(0,len(bin_array),1) if len(bin_array[i:i+2])>1])
    hist = np.histogram(events,bin_array)
    EventHist = {'histogram':list(hist[0]),'bin_low':list(bin_vals[:,0]),'bin_high':list(bin_vals[:,1])}
    return EventHist

def randomize_globally(sequence):
    rand_seq = sequence[:];
    np.random.shuffle(rand_seq)
    return rand_seq

def randomize_locally(sequence,institute):
    # find first occurence of institute
    first_pos = sequence.index(institute)
    if first_pos == len(sequence)-1:
        return sequence
    else:
        reshuffled = sequence[first_pos:]
        np.random.shuffle(reshuffled)
        return sequence[:first_pos]+reshuffled
def record_growth_statistics(sequence):
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
    
    #hist[0]= hist[0]
    ZipfLaw = {'histogram':list(hist[0]),'bin_low':list(bin_vals[:,0]),'bin_high':list(bin_vals[:,1])}
    
    # Heap's law: {# researchers,#institutes}
    HeapsLaw ={'num_researchers':list(range(len(sequence))),'num_institutes':[len(set(sequence[:n])) for n in range(len(sequence))]}
    
    # entropy
    #EntropyK = record_mean_entropy(sequence)
    # inter-event times
    #InterEventTimes = inter_event_time_dist(sequence)
    data = {'ZipfLaw':ZipfLaw,'HeapsLaw':HeapsLaw}#,'EntropyK':EntropyK,'InterEventTimes':InterEventTimes}
    return data

def local_growth_statistics(sequence):
    # "Zipf's Law"
    # this distribution is no different than original data
    ZipfLaw = {'histogram':[None],'bin_low':[None],'bin_high':[None]}
    # "Heap's Law"
    # there is no obvious equivalent of Heap's Law for local randomization
    HeapsLaw ={'num_researchers':[None],'num_institutes':[None]}
    local_null_growth_data = {'ZipfLaw':ZipfLaw,'HeapsLaw':HeapsLaw ,'EntropyK':[],'InterEventTimes':[]}
    events = []
    entropy_institute= []
    for institute in set(sequence):#range(total_num_institutes(sequence)):
        null_local_data = randomize_locally(sequence,institute)
        # compute entropy for institute
        e_i = record_entropy(null_local_data,institute)
        e_i = list(e_i)
        entropy_institute.append(e_i)
        # compute inter-event times
        inter_events = inter_event_times(null_local_data,institute)
        inter_events = list(inter_events)
        events.append(inter_events)
    events = flatten(events)
    
    local_null_growth_data['EntropyK']=record_local_mean_entropy(entropy_institute)
    local_null_growth_data['InterEventTimes']=local_inter_event_time_dist(events)
    return local_null_growth_data
    
def finish_data_collection(sequence):
    
    #null_global_data = randomize_globally(sequence)
    growth_data = record_growth_statistics(sequence)
    print("real data analyzed")
    growth_data = {'data':growth_data}#{'data':growth_data,'local_null':local_null_growth_data,'global_null':global_null_growth_data}
    return growth_data
def export_growth_data(growth_data,field):
    if field != '':
        add_field_folder(field)
    for data in growth_data.keys():
        if field != '':
            add_folder(field+'/'+data+'-one_affil_per_author')
        else:
            add_folder(data)

        for data_type in ['ZipfLaw','HeapsLaw']:#,'EntropyK','InterEventTimes']:
            export_data=growth_data[data][data_type]
            df = pd.DataFrame(data=export_data)
            # export to folder "growth_data/", "local_null/", or "global_null/"
            if field != '':
                df.to_csv(field+'/'+data+'-one_affil_per_author'+"/"+data_type+".csv",index=False)
            else:
                df.to_csv(data+'/'+data_type+".csv",index=False)
        
def add_folder(folder):
    # delete old folder and contents
    if os.path.exists(folder+"/"):
        shutil.rmtree(folder+"/")
    os.mkdir(folder+"/");
def add_field_folder(folder):
    # delete old folder and contents
    if not os.path.exists(folder+"/"):
        os.mkdir(folder+"/");

def analyze_data(JC):
    for field in ["CS","Physics","Math","Sociology"]:
        print(field)
        file = 'SequenceData/'+field+'/authorId_affId_sequence.pkl'
        if JC:
            file = 'SequenceData/'+field+'/authorId_affId_sequence_journal_conf.pkl'
        with open(file, 'rb') as f:
            author_affil_seq = pk.load(f)
        seq = [i for a,i in author_affil_seq]
        print("new sequence created")
        
        start_time = time.time()
        growth_data = finish_data_collection(seq)
        export_growth_data(growth_data,field)
        print("--- %s seconds ---" % (time.time() - start_time))

def analyze_sims():
    sim_folders = ['Rho=3;Nu=1;Mu=0.6;Sigma=0.0/']#['Rho=3;Nu=1;Mu=0.6;Sigma=0.0/','Rho=4;Nu=2;Mu=0.6;Sigma=0.0/','Rho=3;Nu=2;Mu=0.6;Sigma=0.0/','Rho=4;Nu=3;Mu=0.6;Sigma=0.0/']
    for sim_folder in sim_folders:
        os.chdir('/Users/keithab/Desktop/Dropbox/InstitutionScaling/Simulations/OriginalSimulations/'+sim_folder)
        folders = glob("Simulation*")
        print(folders)
        for folder in folders:#sim in ["CS","Physics","Math","Sociology"]:
            os.chdir('/Users/keithab/Desktop/Dropbox/InstitutionScaling/Simulations/OriginalSimulations/'+sim_folder+'/'+folder)
            with open('SimulationSequence/simulation_sequence.pkl', 'rb') as f:
                seq = pk.load(f)

            start_time = time.time()
            growth_data = finish_data_collection(seq)
            export_growth_data(growth_data,'')
            print("--- %s seconds ---" % (time.time() - start_time))

        
def main():
    JC = True
    analyze_data(JC)
    analyze_sims()
if __name__ == "__main__":
    main()
