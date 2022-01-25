import numpy as np
import pandas as pd
import os,glob



def main():
    # number of insitutes in time/unique institues in time
    yearpos = 1;
    sizepos = 2;
    init_year = 1800
    final_year = 2018
    out_directory = "/Users/keithab/Desktop/Dropbox/InstitutionScaling/DataAnalysis/InstituteCollaborationData/";
    for field in ["CS","Physics","Math","Sociology"]:
        # input directory
        directory = "/Users/keithab/Desktop/Dropbox/InstitutionScaling/DataAnalysis/InstituteCollaborationData/" + field+ "/institution_description/";
        os.chdir(directory)
        # all institution files
        files = [f for f in glob.glob("*.csv") if "num" not in f]

        #number of institutes
        num_inst = {str(year):[0] for year in range(init_year,final_year)}
        #number of new institutes
        num_new_inst = {str(year):[0] for year in range(init_year,final_year)}
        #number of researchers
        num_researchers = {str(year):[0] for year in range(init_year,final_year)}
        inst_per_year = {str(year):[] for year in range(init_year,final_year)}
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
                        
                        num_res = line['size']
                        num_inst[str(year)][0]+=1
                        num_researchers[str(year)][0] += num_res
                        inst_per_year[str(year)].append(inst)

        # once we collect all this data...
        num_new_inst = {}
        for year in range(init_year,final_year):
            old_institutes = set()
            if year > init_year:
                old_institutes = set().union(*[inst_per_year[str(y)] for y in range(init_year,year)])
            num_new_inst[str(year)] = [len(set(inst_per_year[str(year)]) - old_institutes)]
        df_num_inst = pd.DataFrame(data=num_inst)
        df_num_new_inst = pd.DataFrame(data=num_new_inst)
        df_num_researchers = pd.DataFrame(data=num_researchers)
        
        df_num_inst.to_csv(out_directory+field+"_num_inst.csv",index=False)
        df_num_new_inst.to_csv(out_directory+field+"_num_new_inst.csv",index=False)
        df_num_researchers.to_csv(out_directory+field+"_num_researchers.csv",index=False)
            


if __name__ == "__main__":
    main()
