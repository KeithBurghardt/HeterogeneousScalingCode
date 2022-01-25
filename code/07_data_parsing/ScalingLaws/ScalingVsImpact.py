import pandas as pd
import numpy as np
import os,glob,shutil
#from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from scipy.optimize import curve_fit
import scipy as sp
sp.special.seterr(all='ignore')
np.seterr(all='print')

nlm_fit = False

def fit_log(np_array):
    size = np.array(np_array[:,0])
    y = np.array(np_array[:,1])

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
        print(residuals)

    else:
        size = sm.add_constant(size)
        model = sm.OLS(y, size)
        results = model.fit()
        params = results.params
        errors = results.bse
        residuals = y - results.predict()
        #print(size)
        size = size[:,1]

    return [[params,errors],[size,residuals]]

def power_law(x,a,b):
    return a*x**b

def create_log_size_data(df,attr,cumulQ):
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
    #print(params)
    # if there is no variance, give fit a low weight
    eps=1
    for attr in params.keys():
        params_std = np.array(params[attr])
        if len(params_std) > 0:
            
            p = np.array(params_std[:,0])
            param_const = p[:,0]
            param_slope = p[:,1]
            var = np.array(params_std[:,1])**2
            var[var==0] = eps
            w = 1/var
            w_const = w[:,0]
            w_slope = w[:,1]
            # weighted mean
            mean_const = np.average(param_const,weights=w_const)
            mean_slope = np.average(param_slope,weights=w_slope)
            mean_params[attr] = [mean_const,mean_slope]
        else:
            mean_params[attr] = [None,None]
    return mean_params

def find_null_params(mean_params,residuals):
    # recreate data with randomized residuals
    null_params = {}
    for attr in mean_params.keys():
        null_params[attr] = [];
        mean_const,mean_slope = mean_params[attr]
        num_neg = 0
        for size,res in residuals[attr]:

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
                [params,errors],[size,res] =fit_log(xy)
                null_params[attr].append([params,errors])
            else:
                [params,errors],[size,res] =fit_log(xy)
                null_params[attr].append([params,errors])
        print("number of bad data")
        print(num_neg)

    return null_params
def add_folder(folder):
    # delete old folder and contents
    if os.path.exists(folder+"/"):
        shutil.rmtree(folder+"/")
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
def parse_data(field,latest_year):
    directory = 'InstituteCollaborationData/'+field+'/institution_description/'
    # read all (compressed) files
    num_files = 0;
    num = 0;
    files = glob.glob(directory + "*.csv")
    pre_keys = ['size_','int_collab_','ext_collab_']
    params = set_keys(files[0],pre_keys)
    params['2012impact']=[]
    params['2012impact_oneauthor']=[]
    params['2012impact_twoauthor']=[]
    params['2012impact_three2sixauthor']=[]
    residuals=set_keys(files[0],pre_keys)
    for file in files:
            num_files += 1
            if num_files % 1000==0:
                print(num_files)
                print(num)
            
            df = pd.read_csv(file)
            df = df.loc[df['year']<=latest_year,]
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
                init_size = df.iloc[-1,df.columns.get_loc('cumul_size')]
                final_size = df.iloc[0,df.columns.get_loc('cumul_size')]
                
                if final_size - init_size > 50:# and len(df) > 50:
                    
                    num = num + 1
                    for attr in df.columns:
                        
                        if attr not in ['year','size','cumul_size']:
                            
                            
                            log_data_types,pre_keys = find_log_datatypes(df,attr)
                            for index,log_data in enumerate(log_data_types):
                               
                                pre_key = pre_keys[index]
                                
                                key = pre_key + attr
                                forbidden_keys = ['int_collab_ext_collabs_per_researcher','int_collab_int_collabs_per_researcher','int_collab_int_cumul_collabs_per_researcher','int_collab_ext_cumul_collabs_per_researcher']
                                if key not in forbidden_keys:
                                    min_size = 50
                                        
                                    if len(log_data) > min_size:
                                        [const_slope,errors],[size,res] = fit_log(log_data)
                                        params[key].append([const_slope,errors])
                                        residuals[key].append([size,res])
                                        params['2012impact'].append(df.loc[df['year']==2012,'avg_impact'].values)
                                        params['2012impact_oneauthor'].append(df.loc[df['year']==2012,'avg_impact_oneauthor'].values)
                                        params['2012impact_twoauthor'].append(df.loc[df['year']==2012,'avg_impact_twoauthor'].values)
                                        params['2012impact_three2sixauthor'].append(df.loc[df['year']==2012,'avg_impact_three2sixauthor'].values)
    
    return [params,residuals]


def parse_sim():
    directory = '../Simulation/WithinInstituteScaling/'
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
        
        if final_size - init_size > 50 and len(df) > 50:
            num = num + 1
            for attr in list(df):
                if attr not in ['num_researchers','p','q']:
                    log_size_data = create_log_size_sim(df,attr)
                    attr_dat = np.array(log_size_data[:,1])
                    
                    min_size = 50
                    if len(attr_dat[attr_dat>0]) > min_size:
                        [const_slope,errors],[size,res] = fit_log(log_size_data)

                        params[attr].append([const_slope,errors])
                        residuals[attr].append([size,res])
    
    return [params,residuals]
            
def save_params(params,file,field):
    print(params.keys())
    for attr in params.keys():
        save_file = 'Institution Densification/'+field+'/'+'nlm_fit='+str(nlm_fit)+'_'+attr+'_'+file
        if len(params[attr]) > 0:
            const_slope = np.array(np.array(params[attr])[:,0])
            errors=np.array(np.array(params[attr])[:,1])
            d = {'const':const_slope[:,0],'slope':const_slope[:,1],'error_const':errors[:,0],'error_slope':errors[:,1]}
            df = pd.DataFrame(data=d)
            df.to_csv(save_file,index=False)
        
    
def main():
    latest_year = 2012
    for field in ["Physics"]:#["CS","Math","Physics","Sociology"]:
        params,residuals = parse_data(field,latest_year)
        save_params(params,'data_params.csv',field)
        mean_params = find_mean_params(params)
        null_params = find_null_params(mean_params,residuals)
        save_params(null_params,'null_params.csv',field)
if __name__ == "__main__":
    main()
