import pandas as pd;
import numpy as np
import os,glob
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
        if len(size) >0:
            if len(size[0])>1:
                size = size[:,1]

    return [[params,errors],[size,residuals]]
def create_log_size_data(df,attr,cumulQ):
    if nlm_fit:
        # no log of data. this avoids issue of removing good data
        log_data = df.loc[:,['size',attr]].values
        if cumulQ:
            log_data = df.loc[:,['cumul_size',attr]].values

    else:
        if not cumulQ:
            cleaned_df =df.loc[df[attr]>0,['size',attr]]
            cleaned_df = cleaned_df.loc[cleaned_df['size']>0,['size',attr]]
            log_data = np.log10(cleaned_df.values)
        if cumulQ:
            cleaned_df =df.loc[df[attr]>0,['cumul_size',attr]]
            cleaned_df = cleaned_df.loc[cleaned_df['cumul_size']>0,['cumul_size',attr]]
            log_data = np.log10(cleaned_df.values)
    return log_data


def collect_data(ParamsPerYear,cross_institute_df,cols,year):
    # year
    ParamsPerYear['year'].append(year)

    # total size:
    total_size = np.sum(cross_institute_df.loc[:,'size'].values)
    ParamsPerYear['size'].append(total_size)
    total_size = np.sum(cross_institute_df.loc[:,'cumul_size'].values)
    ParamsPerYear['cumul_size'].append(total_size)
    
    for c in cols:
        log_size_data = create_log_size_data(cross_institute_df,c,'cumul' in c)

        if np.sum(log_size_data[:,1]) > 1:
            [const_slope,errors],[size,res] = fit_log(log_size_data)
        else:
            const_slope = [None,None]
            errors = [None,None]
        for fit in ["const","slope"]:
            for err in ["","errors"]:
                if err == "":
                    val = const_slope[0]
                    if fit == "slope":
                        val = const_slope[1]
                else:
                    val = errors[0]
                    if fit == "slope":
                        val = errors[1]
                ParamsPerYear[c+'_'+fit+'_'+err].append(val)

def parse_data(field,folder):
    
    directory = folder + '/'+field+'/'+'institution_description/'
    # read all (compressed) files
    files = glob.glob(directory + "*.csv")
    num_files = 0;
    num = 0;
    cols = [c for c in (pd.read_csv(files[0])).columns if c not in ['year','size','cumul_size','aff_name']]
    
    ParamsPerYear ={c:[] for c in ['year','size','cumul_size']}
    for c in cols:
        for fit in ["const","slope"]:
            for err in ["","errors"]:
                ParamsPerYear[c+'_'+fit+'_'+err] = []

    
    df_list = []
    for file in files:
        num_files += 1
        if num_files % 1000==0:
            print(num_files)
        df_file = pd.read_csv(file)
        df_list.append(df_file)
    df = pd.concat(df_list)
    for year in range(1800,2013):
        print(year)
        cross_institute_data = {c:[] for c in cols+['year','size','cumul_size']}#{'year':year,'size':[],'cumul_size':[]};
        if year in df['year'].values:
            rows=df.loc[df['year']==year,];
            print(len(rows))
            # we record
            #   - year
            #   - size
            #   - #internal_collab
            #   - #external_collab
            #   - cumul_size
            #   - #cumul_internal_collab
            #   - #cumul_external_collab
            if len(rows) > 10:
                for i,row in rows.iterrows():
                    for c in cols+['year','size','cumul_size']:
                        cross_institute_data[c].append(row[c])
        cross_institute_df = pd.DataFrame(data=cross_institute_data)
        collect_data(ParamsPerYear,cross_institute_df,cols,year)
    
    Params_df = pd.DataFrame(data=ParamsPerYear)
    save_params(Params_df,field,folder)
                        
def save_params(df,field,folder):

        save_file = folder+'/'+field+'_CrossInstitution_nlm_fit='+str(nlm_fit)+'.csv'
        df.to_csv(save_file,index=False)

def main():
    folder = 'institutions_half_data'
    for folder in ['institutions_half_data','institutions_all_data']:
        for field in ["Sociology","Math","Physics","CS"]:
            parse_data(field,folder)
    
if __name__ == "__main__":
    main()

