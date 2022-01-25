import pandas as pd
import numpy as np
import os,glob,shutil,time
#from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from scipy.optimize import curve_fit
import scipy as sp
sp.special.seterr(all='ignore')
np.seterr(all='print')
#with np.warnings.catch_warnings():
#    np.warnings.filterwarnings('ignore', r'divide by zero encountered in log10')
    
nlm_fit = False

def fit_log(np_array):
    size = np.array(np_array[:,0])
    y = np.array(np_array[:,1])
    max_size = max(size)

    if nlm_fit:
        #size = 10**size;
        #y = 10**y;
        params = [-1,-1]
        errors = [0,0]
        try:
            params, pcov = curve_fit(power_law, size, y,maxfev = 1000)#,bounds=(0, np.inf)
            
            errors = np.sqrt(np.diag(pcov))
        except RuntimeError:
            print("Error - curve_fit failed")
        a,b = params
        
        best_fit = a*size**b
        residuals = y - best_fit
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((y-np.mean(y))**2)
        r_squared = 1 - (ss_res / ss_tot)
        #print(residuals)

    else:
        #print(size)
        size = sm.add_constant(size)
        #print(size)
        inst_sizes = size[:,1]
        model = sm.OLS(y, size)
        results = model.fit()
        params = results.params
        errors = results.bse
        residuals = y - results.predict()
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((y-np.mean(y))**2)
        r_squared = 1 - (ss_res / ss_tot)

    return [[params,errors],[inst_sizes,residuals],r_squared,max_size]

def power_law(x,a,b):
    return a*x**b
    
def create_log_size_data(df,attr,cumulQ):
    #print(attr)
    if nlm_fit:
        # no log of data. this avoids issue of removing good data
        log_data = df.loc[:,['size',attr]].values
        if cumulQ:
            log_data = df.loc[:,['cumul_size',attr]].values

    else:
        log_data = np.log10(df.loc[df[attr]>0,['size',attr]].values)

        if cumulQ:
            log_data = np.log10(df.loc[df[attr]>0,['cumul_size',attr]].values)
    return log_data
def create_log_int_collabs_data(df,attr,cumulQ):
    if nlm_fit:
        # no log of data. this avoids issue of removing good data
        log_data = df.loc[:,['int_collabs_per_researcher',attr]].values
        if cumulQ:
            log_data = df.loc[:,['int_cumul_collabs_per_researcher',attr]].values

    else:
        with np.errstate(divide='ignore'):
            log_data = np.log10(df.loc[df[attr]>0,['int_collabs_per_researcher',attr]].values)
            if cumulQ:
                log_data = np.log10(df.loc[df[attr]>0,['int_cumul_collabs_per_researcher',attr]].values)
            log_data = log_data[~np.isinf(log_data).any(axis=1)]
    return log_data
def create_log_ext_collabs_data(df,attr,cumulQ):
    if nlm_fit:
        # no log of data. this avoids issue of removing good data
        log_data = df.loc[:,['ext_collabs_per_researcher',attr]].values
        if cumulQ:
            log_data = df.loc[:,['ext_cumul_collabs_per_researcher',attr]].values
    else:
        with np.errstate(divide='ignore'):
            log_data = np.log10(df.loc[df[attr]>0,['ext_collabs_per_researcher',attr]].values)
            if cumulQ:
                log_data = np.log10(df.loc[df[attr]>0,['ext_cumul_collabs_per_researcher',attr]].values)
            log_data = log_data[~np.isinf(log_data).any(axis=1)]
        
    return log_data

def create_log_size_sim(df,attr):
    log_data = np.log10(df.loc[df[attr]>0,['num_researchers',attr]].values)
    return log_data

def find_mean_params(params):
    # mean params weighted by inverse variance
    mean_params = {}
    # if there is no variance, give fit a low weight
    eps=1#10**6
    for attr in params.keys():
        params_std = np.array(params[attr])
        if len(params_std) > 0:
            
            p = np.array(params_std[:,0])
            param_const = np.array([p[i][0] for i in range(len(p))])
            param_slope = np.array([p[i][1] for i in range(len(p))])
            var = np.array(params_std[:,1])**2
            #if np.sum([int(var==0)]) > 0:
            #    var[var==0] = eps
            #var[var<10**-8] = eps
            w = 1/var
            w_const = np.array([w[i][0] for i in range(len(w))])
            w_slope = np.array([w[i][1] for i in range(len(w))])
            # weighted mean
            param_const_temp = param_const[(~np.isnan(param_const)) & (~np.isnan(w_const)) & ~np.isinf(param_const) & ~np.isinf(w_const)]
            w_const_temp = w_const[~np.isnan(param_const) & ~np.isnan(w_const) & ~np.isinf(param_const) & ~np.isinf(w_const)]
            param_slope_temp = param_slope[~np.isnan(param_slope) & ~np.isnan(w_slope) & ~np.isinf(param_slope) & ~np.isinf(w_slope)]
            w_slope_temp = w_slope[~np.isnan(param_slope) & ~np.isnan(w_slope)& ~np.isinf(param_slope) & ~np.isinf(w_slope)]
            mean_const = np.average(param_const_temp,weights=w_const_temp)
            mean_slope = np.average(param_slope_temp,weights=w_slope_temp)
            #if 'size_#cumul_external' in attr:
            #    print(attr)
            #    print(mean_const)
            #    print(mean_slope)
            #    print(param_const_temp)
            #    print(w_const_temp)
            #    print(param_slope_temp)
            #    print(w_slope_temp)
            print(['MEAN VALUES: ',attr,mean_const,mean_slope])
            mean_params[attr] = [1,1.2]#[mean_const,mean_slope]
        else:
            mean_params[attr] = [None,None]
    return mean_params

def find_null_params(mean_params,residuals):
    # recreate data with randomized residuals
    null_params = {}
    for attr in mean_params.keys():
        null_params[attr] = [];
        mean_const,mean_slope = mean_params[attr]
        if 'internal' in attr or 'external' in attr:
            print(mean_slope)
        num_neg = 0
        if attr not in residuals.keys():
            print(attr+' NOT FOUND')
            continue
        #else:
        #    print(attr)
        if 'size_#' in attr:
            print(attr)
        for size,res in residuals[attr]:
            if 'size_#' in attr:
                print(res)
            # randomize residuals
            rand_res = np.random.permutation(res)
            X = size[:]
            # residuals are the "error" terms in each datapoint
            y = (mean_const + X*mean_slope) + rand_res
            if nlm_fit:
                # no log
                # if y < 0, fit is so bad that we ignore it anyway
                y = mean_const*X**mean_slope + rand_res
                if np.sum(y) != np.sum(np.abs(y)):
                    y[y<0] = 0
                    num_neg += 1

            xy = np.transpose([X,y])
            if nlm_fit and len(y[y<0])/float(len(y)) < 0.9:                
                # refit
                [params,errors],[size,res],r_squared,max_size = fit_log(xy)
                null_params[attr].append([params,errors,r_squared,max_size])
            else:
                [params,errors],[size,res],r_squared,max_size =fit_log(xy)
                null_params[attr].append([params,errors,r_squared,max_size])
        print("number of bad data")
        print(num_neg)

    return null_params
def add_folder(folder):
    # delete old folder and contents
    if os.path.exists(folder+"/"):
        shutil.rmtree(folder+"/")
    #if not os.path.exists(folder+"/"):
    os.mkdir(folder+"/");
def set_keys(file,pre_keys):
    df = pd.read_csv(file)
    keys = [x+col for x in pre_keys for col in df.columns if col not in ['year','size','cumul_size']]
    keys+=['size_int_collabs_per_researcher','size_int_cumul_collabs_per_researcher','size_ext_collabs_per_researcher','size_ext_cumul_collabs_per_researcher']
    dict_data = {};
    for key in keys:
        dict_data[key]= []
    return dict_data
def add_densification(df):
    df2 = df.copy()
    size = df2['size'].values
    num_int_collabs = df2['#internal_collab'].values
    num_ext_collabs = df2['#external_collab'].values
    cumul_size = df2['cumul_size'].values
    num_cumul_int_collabs = df2['#cumul_internal_collab'].values
    num_cumul_ext_collabs = df2['#cumul_external_collab'].values
    with np.errstate(divide='ignore'):

        int_collabs_per_researcher = num_int_collabs/size
        ext_collabs_per_researcher = num_ext_collabs/size
        int_cumul_collabs_per_researcher = num_cumul_int_collabs/cumul_size
        ext_cumul_collabs_per_researcher = num_cumul_ext_collabs/cumul_size

    df2['int_collabs_per_researcher'] = pd.Series(int_collabs_per_researcher, index=df2.index)
    df2['ext_collabs_per_researcher'] = pd.Series(ext_collabs_per_researcher, index=df2.index)
    df2['int_cumul_collabs_per_researcher'] = pd.Series(int_cumul_collabs_per_researcher, index=df2.index)
    df2['ext_cumul_collabs_per_researcher'] = pd.Series(ext_cumul_collabs_per_researcher, index=df2.index)
    return df2

def find_log_datatypes(df,attr):
    log_size_data = create_log_size_data(df,attr,'cumul' in attr)
    pre_keys = ['size_']
    
    if 'collabs_per_researcher' in attr:
        return [[log_size_data],pre_keys]
    else:
        log_int_collab_data = create_log_int_collabs_data(df,attr,'cumul' in attr)
        log_ext_collab_data = create_log_ext_collabs_data(df,attr,'cumul' in attr)
        log_data = [log_size_data,log_int_collab_data,log_ext_collab_data]
        pre_keys = ['size_','int_collab_','ext_collab_']
        return [log_data,pre_keys]

def parse_data(field,first_year,latest_year,folder,min_data_size,min_size_diff):
    #add_folder('InstituteCollaborationData/'+field)
    directory = folder+'/'+field+'/institution_description/'
    # read all (compressed) files
    #min_size_diff = the minimum change in institution size for fitting scaling law
    #min_data_size = the minimum number of datapoints

    num_files = 0;
    num = 0;
    files = glob.glob(directory + "*.csv")
    #print(files)
    pre_keys = ['size_','int_collab_','ext_collab_']
    params = set_keys(files[0],pre_keys)#{'#internal_collab':[],'#external_collab':[],'#cumul_internal_collab':[],'#cumul_external_collab':[]}
    params['institution'] = []
    residuals=set_keys(files[0],pre_keys)#{'#internal_collab':[],'#external_collab':[],'#cumul_internal_collab':[],'#cumul_external_collab':[]}
    for file in files:
            num_files += 1
            if num_files % 1000==0:
                print(num_files)
                print(num)
                #for key in params.keys():
                #    print([key,len(params[key])])
            
            df = pd.read_csv(file)
            #df.astype('float32')

            #print(len(df))
            df = df.loc[(df['year']>=first_year)&(df['year']<=latest_year),]
            #print(len(df))
            if len(df) > 0:
                # add densification column
                df = add_densification(df)

                # we record
                #   - year
                #   - size
                #   - #internal_collab
                #   - #external_collab
                #   - cumul_size
                #   - #cumul_internal_collab
                #   - #cumul_external_collab

                # look at scaling for subset of data:
                #init_size = df.iloc[-1,df.columns.get_loc('cumul_size')]
                #final_size = df.iloc[0,df.columns.get_loc('cumul_size')]
                num = num + 1
                    
                for attr in df.columns:
                        
                    if attr not in ['year','size','cumul_size','aff_name']:                    
                        log_data_types,pre_keys = find_log_datatypes(df,attr)
                        for index,log_data in enumerate(log_data_types):
                            pre_key = pre_keys[index]#[pk for pk,dat in zip(pre_keys,log_data_types) if dat == log_data][0]
                            key = pre_key + attr
                            forbidden_keys = ['int_collab_ext_collabs_per_researcher','int_collab_int_collabs_per_researcher','int_collab_int_cumul_collabs_per_researcher','int_collab_ext_cumul_collabs_per_researcher']
                            if key not in forbidden_keys:
                                if len(log_data) < np.log10(min_data_size): continue
                                size = np.array(log_data[:,0])
                                init_size = np.min(size)
                                final_size = np.max(size)
                                if final_size - init_size < np.log10(min_size_diff): continue
                                
                                [const_slope,errors],[size,res],r_squared,max_size = fit_log(log_data)
                                params[key].append([const_slope,errors,r_squared,max_size,file[:-4]])
                                residuals[key].append([size,res])
                                av_impact = -1
                                av_impact_oneauthor = -1
                                av_impact_twoauthor = -1
                                av_impact_three2sixauthor = -1
                                production = -1
                                productivity = -1
                                if len(df.loc[df['year']==2012,]) > 0:
                                    av_impact = df.loc[df['year']==2012,'avg_impact'].values[0]
                                    av_impact_oneauthor = df.loc[df['year']==2012,'avg_impact_oneauthor'].values[0]
                                    av_impact_twoauthor = df.loc[df['year']==2012,'avg_impact_twoauthor'].values[0]
                                    av_impact_three2sixauthor = df.loc[df['year']==2012,'avg_impact_three2sixauthor'].values[0]
                                    production = df.loc[df['year']==2012,'production'].values[0]
                                    productivity =df.loc[df['year']==2012,'productivity'].values[0]
                                params[key][-1]+=[av_impact,av_impact_oneauthor,av_impact_twoauthor,av_impact_three2sixauthor,production,productivity]
    
    return [params,residuals]


def parse_sim(field,min_data_size,min_size_diff):

    directory = field+'/WithinInstituteScaling/'#'../Simulations/Simulation_'+str(i)+'/WithinInstituteScaling/'
    # read all (compressed) files
    num_files = 0;
    num = 0;
    params = {'internal_collaborators':[],'external_collaborators':[]}
    residuals = {'internal_collaborators':[],'external_collaborators':[]}
    for file in glob.glob(directory + "*.csv"):
        #print(file)
        num_files += 1
        if num_files % 100==0:
            print(num_files)
            print(num)
        df = pd.read_csv(file)
        # we record
        #   - year
        #   - size
        #   - #internal_collab
        #   - #external_collab
        #   - cumul_size
        #   - #cumul_internal_collab
        #   - #cumul_external_collab

        # look at scaling for subset of data:
        init_size = df.iloc[0,df.columns.get_loc('num_researchers')]
        final_size = df.iloc[-1,df.columns.get_loc('num_researchers')]
        #print(final_size - init_size)
        
        if final_size - init_size > min_size_diff:#50 and len(df) > 50:
            #print(len(df))
            
            num = num + 1
            for attr in list(df):
                if attr not in ['num_researchers','p','q']:
                    #print(attr)
                    log_size_data = create_log_size_sim(df,attr)
                    attr_dat = np.array(log_size_data[:,1])
                    
                    #min_size = 50
                    if len(attr_dat[attr_dat>0]) > min_data_size:#np.sum(log_size_data[:,1]) > 1:
                        [const_slope,errors],[size,res],r_squared,max_size = fit_log(log_size_data)

                        params[attr].append([const_slope,errors,r_squared,max_size])
                        residuals[attr].append([size,res])
    
    return [params,residuals]
            
def save_params(params,file,field,first_year,folder):
    for attr in params.keys():
            #if '2012impact' not in attr:
        if field in ["CS","Math","Physics","Sociology"]:
            # Institution Densification
            save_file = folder + '/' + field+'/'+'nlm_fit='+str(nlm_fit)+'_'+attr+'_y>='+str(first_year)+'_'+file
        else:
            #save_file = folder + '/' + field+
            save_file = folder + '/nlm_fit='+str(nlm_fit)+'_'+attr+'_y>='+str(first_year)+'_'+file
        if len(params[attr]) > 0:
            const_slope = np.array(np.array(params[attr])[:,0])
            const = [const_slope[i][0] for i in range(len(const_slope))]
            slope = [const_slope[i][1] for i in range(len(const_slope))]
            errors=np.array(np.array(params[attr])[:,1])
            err_const = [errors[i][0] for i in range(len(errors))]
            err_slope = [errors[i][1] for i in range(len(errors))]
            r2 = np.array(np.array(params[attr])[:,2])
            n = np.array(np.array(params[attr])[:,3])
            inst = np.array([None]*len(params[attr]))
            if len(np.array(params[attr][0]))>4:
                inst = np.array(np.array(params[attr])[:,4])
            
            d = {'const':const,'slope':slope,'error_const':err_const,'error_slope':err_slope,'r2':r2,'final_n':n,'institution':inst};#,'2012impact':av_impact,'2012impact_oneauthor':av_impact_oneauthor,'2012impact_twoauthor':av_impact_twoauthor,'2012impact_three2sixauthor':av_impact_three2sixauthor,'production':production,'productivity':productivity}
            df = pd.DataFrame(data=d)
            #print(save_file)
            df.to_csv(save_file,index=False)
        
def analyze_data(folder,first_year,latest_year,min_data_size,min_size_diff):

    for field in ["Sociology","Physics","CS","Math"]:
        params,residuals = parse_data(field,first_year,latest_year,folder,min_data_size,min_size_diff)
        save_params(params,'data_params_minsize='+str(min_data_size)+'_mindiff='+str(min_size_diff)+'.csv',field,first_year,folder)
        mean_params = find_mean_params(params)
        #print(mean_params)
        null_params = find_null_params(mean_params,residuals)
        save_params(null_params,'null_params_minsize='+str(min_data_size)+'_mindiff='+str(min_size_diff)+'.csv',field,first_year,folder)

def analyze_sims(min_data_size,min_size_diff):
    os.chdir("/Users/keithab/Desktop/Dropbox/InstitutionScaling/Simulations/OriginalSimulations/")
    sim_folders = ["Rho=4;Nu=2;Mu=0.6;Sigma=0.25"]#glob.glob("Rho=*")#['Rho=4;Nu=2;Mu=0.6;Sigma=0.01/','Rho=4;Nu=2;Mu=0.6;Sigma=0.25/','Rho=4;Nu=2;Mu=0.4;Sigma=0.0/','Rho=4;Nu=2;Mu=0.8;Sigma=0.0/']#,'Rho=4;Nu=2;Mu=0.6;Sigma=0.0/','Rho=3;Nu=2;Mu=0.6;Sigma=0.0/','Rho=4;Nu=3;Mu=0.6;Sigma=0.0/']
    for sim_folder in sim_folders:
        os.chdir('/Users/keithab/Desktop/Dropbox/InstitutionScaling/Simulations/OriginalSimulations/'+sim_folder)
        folders = glob.glob("Simulation*")
        #print(folders)
        for folder in folders:#sim in ["CS","Physics","Math","Sociology"]:
            field = '/Users/keithab/Desktop/Dropbox/InstitutionScaling/Simulations/OriginalSimulations/'+sim_folder+'/'+folder
            start_time = time.time()
            params,residuals = parse_sim(field,min_data_size,min_size_diff)
            first_year = 0
            save_params(params,'sim_data_params_minsize='+str(min_data_size)+'_mindiff='+str(min_size_diff)+'.csv',field,first_year,folder)
            mean_params = find_mean_params(params)
            null_params = find_null_params(mean_params,residuals)
            save_params(null_params,'sim_null_params_minsize='+str(min_data_size)+'_mindiff='+str(min_size_diff)+'.csv',field,first_year,folder)
            
            print("--- %s seconds ---" % (time.time() - start_time))
            
def main():
    first_year = 1800
    latest_year = 2017
    min_data_size=5
    min_size_diff=10

    folder ='institutions_all_data' #'institutions_all_data'#'InstituteCollaborationData'
    analyze_data(folder,first_year,latest_year,min_data_size,min_size_diff)
    analyze_sims(min_data_size,min_size_diff)

if __name__ == "__main__":
    main()

