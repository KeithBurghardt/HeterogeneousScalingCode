import numpy as np
import pandas as pd
import os,glob



def main():
    # number of insitutes in time/unique institues in time
    yearpos = 1;
    sizepos = 2;
    years = [1970,1990,2010]
    out_directory = "/Users/keithab/Desktop/Dropbox/InstitutionScaling/DataAnalysis/InstituteCollaborationData/";
    for field in ["Sociology","CS","Physics","Math"]:
        # input directory
        directory = "/Users/keithab/Desktop/Dropbox/InstitutionScaling/DataAnalysis/InstituteCollaborationData/" + field+ "/institution_description/";
        os.chdir(directory)
        # all institution files
        files = [f for f in glob.glob("*.csv") if "num" not in f]
        size_dist = {str(year):[] for year in years};
        for year in years:
            # find insitute sizes at this particular time
            count = 0
            for file in files:
                count+=1;
                if count % 1000 == 0:
                    pct_done = count/len(files)*100;
                    print('{0}\t{1}\t{2}% done'.format(field,str(year),str(pct_done)[:4]))
                    
                df = pd.read_csv(file);

                if len(df) > 0:
                    for b in range(3):
                        if year+b in df['year'].values:
                            # find size that year
                            size = df.loc[df['year']==year+b,['size']].values[0][0] 
                            size_dist[str(year)].append(size)
            print(len(size_dist[str(year)]))
        out_df = pd.concat([pd.DataFrame(data=size_dist[str(year)]) for year in years], ignore_index=True, axis=1);
        out_df.columns = [str(year) for year in years]
        out_df.to_csv(out_directory+field+'_size_dist.csv',index=False)


if __name__ == "__main__":
    main()
