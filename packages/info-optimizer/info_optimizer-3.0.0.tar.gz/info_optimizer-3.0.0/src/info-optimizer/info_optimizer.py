import numpy as np   
import time


class solution:  
    def __init__(self):  
        self.startTime = None  
        self.endTime = None  
        self.executionTime = None  
        self.convergence = None  
        self.optimizer = None  
        self.BestCost = None  
        self.Best_X = None  

# Function to initialize the solutions  
def initialization(nP, dim, ub, lb):  
    if np.isscalar(ub) and np.isscalar(lb):  
        return np.random.rand(nP, dim) * (ub - lb) + lb  
    else:  
        X = np.zeros((nP, dim))  
        for i in range(dim):  
            ub_i = ub[i]  
            lb_i = lb[i]  
            X[:, i] = np.random.rand(nP) * (ub_i - lb_i) + lb_i  
        return X  

def handle_constraints(x, lb, ub, method, dim):  
    # Check if lb and ub are scalars; if so, expand them to vectors  
    if np.isscalar(lb):  
        lb = np.full(dim, lb)  
    if np.isscalar(ub):  
        ub = np.full(dim, ub)  
    
    if method == "RI":  # Random Initialization method  
        for j in range(dim):  
            if x[j] < lb[j] or x[j] > ub[j]:  
                x[j] = lb[j] + (ub[j] - lb[j]) * np.random.rand()  
    else:  # Default to clipping method  
        x = np.clip(x, lb, ub)  
        
    return x 

def INFO(nP, MaxIt, lb, ub, dim, fobj, constraint_handling="clip", verbose=False):  
    # Initialization  
    Cost = np.zeros(nP)  
    M = np.zeros(nP)  
    
    X = initialization(nP, dim, ub, lb)  
    
    for i in range(nP):  
        Cost[i] = fobj(X[i, :])  
        M[i] = Cost[i]  
    
    ind = np.argsort(Cost)  
    Best_X = X[ind[0], :]  
    Best_Cost = Cost[ind[0]]  
    
    Worst_Cost = Cost[ind[-1]]  
    Worst_X = X[ind[-1], :]  
    
    I = np.random.randint(2, 6)  
    Better_X = X[ind[I], :]  
    Better_Cost = Cost[ind[I]]  
    
    # Main Loop of INFO  
    Convergence_curve = np.zeros(MaxIt)  
    s = solution()
    # Loop counter
    print('INFO is optimizing')

    timerStart = time.time()
    s.startTime = time.strftime("%Y-%m-%d-%H-%M-%S")      
    for it in range(MaxIt):  
        alpha = 2 * np.exp(-4 * (it / MaxIt))  
        
        M_Best = Best_Cost  
        M_Better = Better_Cost  
        M_Worst = Worst_Cost  
        
        for i in range(nP):  
            # Updating rule stage  
            del_val = 2 * np.random.rand() * alpha - alpha  
            sigm = 2 * np.random.rand() * alpha - alpha  
            
            A1 = np.random.permutation(nP)  
            A1 = A1[A1 != i]  
            a, b, c = A1[:3]  
            
            e = 1e-25  
            epsi = e * np.random.rand()  
            
            omg = np.max([M[a], M[b], M[c]])  
            MM = [M[a] - M[b], M[a] - M[c], M[b] - M[c]]  
            
            W = np.cos(np.array(MM) + np.pi) * np.exp(-np.abs(np.array(MM)) / omg)  
            Wt = np.sum(W)  
            
            WM1 = del_val * (W[0] * (X[a, :] - X[b, :]) + W[1] * (X[a, :] - X[c, :]) +  
                             W[2] * (X[b, :] - X[c, :])) / (Wt + 1) + epsi  
            
            omg = np.max([M_Best, M_Better, M_Worst])  
            MM = [M_Best - M_Better, M_Best - M_Better, M_Better - M_Worst]  
            
            W = np.cos(np.array(MM) + np.pi) * np.exp(-np.abs(np.array(MM)) / omg)  
            Wt = np.sum(W)  
            
            WM2 = del_val * (W[0] * (Best_X - Better_X) + W[1] * (Best_X - Worst_X) +  
                             W[2] * (Better_X - Worst_X)) / (Wt + 1) + epsi  
            
            # Determine MeanRule  
            r = np.random.uniform(0.1, 0.5)  
            MeanRule = r * WM1 + (1 - r) * WM2  
            
            if np.random.rand() < 0.5:  
                z1 = X[i, :] + sigm * (np.random.rand() * MeanRule) + \
                     np.random.randn() * (Best_X - X[a, :]) / (M_Best - M[a] + 1)  
                z2 = Best_X + sigm * (np.random.rand() * MeanRule) + \
                     np.random.randn() * (X[a, :] - X[b, :]) / (M[a] - M[b] + 1)  
            else:  
                z1 = X[a, :] + sigm * (np.random.rand() * MeanRule) + \
                     np.random.randn() * (X[b, :] - X[c, :]) / (M[b] - M[c] + 1)  
                z2 = Better_X + sigm * (np.random.rand() * MeanRule) + \
                     np.random.randn() * (X[a, :] - X[b, :]) / (M[a] - M[b] + 1)  
            
            # Vector combining stage  
            u = np.zeros(dim)  
            for j in range(dim):  
                mu = 0.05 * np.random.randn()  
                if np.random.rand() < 0.5:  
                    if np.random.rand() < 0.5:  
                        u[j] = z1[j] + mu * np.abs(z1[j] - z2[j])  
                    else:  
                        u[j] = z2[j] + mu * np.abs(z1[j] - z2[j])  
                else:  
                    u[j] = X[i, j]  
            
            # Local search stage  
            if np.random.rand() < 0.5:  
                L = np.random.rand() < 0.5  
                v1 = (1 - L) * 2 * np.random.rand() + L  
                v2 = np.random.rand() * L + (1 - L)  
                Xavg = (X[a, :] + X[b, :] + X[c, :]) / 3  
                phi = np.random.rand()  
                Xrnd = phi * (Xavg) + (1 - phi) * (phi * Better_X + (1 - phi) * Best_X)  
                Randn = L * np.random.randn(dim) + (1 - L) * np.random.randn()  
                if np.random.rand() < 0.5:  
                    u = Best_X + Randn * (MeanRule + np.random.randn() * (Best_X - X[a, :]))  
                else:  
                    u = Xrnd + Randn * (MeanRule + np.random.randn() * (v1 * Best_X - v2 * Xrnd))  
            
            # Check if new solution goes outside the search space and bring them back  
            New_X = handle_constraints(u, lb, ub, constraint_handling, dim)  
            New_Cost = fobj(New_X)  
            
            if New_Cost < Cost[i]:  
                X[i, :] = New_X  
                Cost[i] = New_Cost  
                M[i] = Cost[i]  
                if Cost[i] < Best_Cost:  
                    Best_X = X[i, :]  
                    Best_Cost = Cost[i]  
        
        # Determine the worst solution  
        ind = np.argsort(Cost)  
        Worst_X = X[ind[-1], :]  
        Worst_Cost = Cost[ind[-1]]  
        # Determine the better solution  
        I = np.random.randint(2, 6)  
        Better_X = X[ind[I], :]  
        Better_Cost = Cost[ind[I]]  
        
        # Update Convergence_curve  
        Convergence_curve[it] = Best_Cost  
        
        # Print to console if verbose is enabled  
        if verbose:  
            print(f'it : {it}, Best Cost = {Convergence_curve[it]}')  

    timerEnd = time.time()  
    s.endTime = time.strftime("%Y-%m-%d-%H-%M-%S")  
    s.executionTime = timerEnd - timerStart  
    s.convergence = Convergence_curve  
    s.optimizer = "INFO"   
    s.BestCost = Best_Cost  
    s.Best_X = Best_X  
    return s



