import numpy as np
import pandas as pd
import os,glob



def main():
    # number of insitutes in time/unique institues in time
    yearpos = 1;
    sizepos = 2;
    init_year = 1800
    final_year = 2018
    out_directory = "/Users/keithab/Desktop/Dropbox/InstitutionScaling/DataAnalysis/Author Collaboration Data/";
    for field in ["CS","Physics","Math","Sociology"]:
        # input directory
        directory = "/Users/keithab/Desktop/Dropbox/InstitutionScaling/DataAnalysis/Author Collaboration Data/" + field+ "/author_collab/";
        os.chdir(directory)
        # all institution files
        files = [f for f in glob.glob("*.csv") if "num" not in f]

        #researchers per year
        res_per_year = {str(year):[] for year in range(init_year,final_year)}
        #number of new researchers
        num_new_res = {str(year):[0] for year in range(init_year,final_year)}
        count = 0
        for file in files:
            count+=1;
            if count % 1000 == 0:
                print(count/len(files));
            inst = file.replace('.csv','')
            df = pd.read_csv(file);
            if len(df) > 0:
                for index,line in df.iterrows():
                    
                    year = int(float(line['year']))
                    if year < final_year:
                        
                        author_id = line['authorId']#df.loc[df['year'] == year,['size']]
                        res_per_year[str(year)].append(author_id)
        # once we collect all this data...
        num_new_res = {}
        for year in range(init_year,final_year):
            old_res = set()
            if year > init_year:
                old_res = set().union(*[res_per_year[str(y)] for y in range(init_year,year)])
            num_new_res[str(year)] = [len(set(res_per_year[str(year)]) - old_res)]

        df_num_new_res = pd.DataFrame(data=num_new_res)
        df_num_new_res.to_csv(out_directory+field+"_num_new_res.csv",index=False)            


if __name__ == "__main__":
    main()
