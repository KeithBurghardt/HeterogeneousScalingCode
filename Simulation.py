import time

from classes.GDSimulation import densify_and_grow

def simulation(params):
    
    final_time,rho,nu,eta,mu_p,sigma_p = params
    simulation = densify_and_grow(final_time,rho,nu,eta,mu_p,sigma_p)
    simulation.run_simulation()
    simulation.export_data()
    

def main():
    ###################################################################
    ###############              Parameters             ############### 
    ###################################################################
    # integers
    #range > 0
    final_time = 500000
    # range > 0
    rho = 4
    # range > 0
    nu = 2
    # range: 0-1
    eta = 1.0
    # range: 0-1
    mu_p = 0.6
    # range: >0
    sigma_p = 0.0
    ###################################################################
    params = [final_time,rho,nu,eta,mu_p,sigma_p]
    sim_obj = densify_and_grow(final_time,rho,nu,eta,mu_p,sigma_p)
    start_time = time.time()
    simulation(params)
    print("--- %s seconds ---" % (time.time() - start_time))
    
    
if __name__ == "__main__":
    main()





    
