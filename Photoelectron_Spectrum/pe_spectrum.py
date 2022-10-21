import numpy as np
from pygama.lgdo import LH5Store
from pygama.dsp.processors.histogram import histogram
import matplotlib.pyplot as plt

def draw(lh5_file: str, channels: list[str], dt: float | int, draw_spectrum : bool = True, trigger_pos_hist : bool = False, size : tuple = (8,5)):
    
    plt.rcParams["figure.figsize"] = size
    plt.rcParams["figure.facecolor"] = "white"
    plt.rcParams["font.size"] = 12
    
    store=LH5Store()
    for ch in channels:
        
        trigger_pos=store.read_object(ch+'/dsp/trigger_pos', lh5_file)[0].nda*dt/1000
        energies=store.read_object(ch+'/dsp/energies', lh5_file)[0].nda
        
        #trigger_pos histogram
        if trigger_pos_hist:
            hist_weights=np.zeros(1000)
            hist_borders=np.zeros(1001)
            histogram(trigger_pos[~np.isnan(trigger_pos)], hist_weights, hist_borders)
            plt.stairs(hist_weights, edges=hist_borders, fill=True)
            plt.show()
            
        #p.e. spectrum
        if draw_spectrum:
            pe_energy=np.array([])
            for i in range(len(energies)):
                tp=trigger_pos[i][~np.isnan(trigger_pos[i])]
                mask=tp>9.5
                tp=tp[mask]
                ens=energies[i][~np.isnan(energies[i])][mask]
                if np.size(ens)>0:
                    for j in range(1,len(ens)):
                        diffs=tp[j:]-tp[:-j]
                        ens=np.concatenate(([ens[k]+ens[k+j] if diffs[k]<5.5 else ens[k] for k in range(len(diffs))], ens[len(ens)-j:]))
                pe_energy=np.concatenate((pe_energy, ens))
                
            hist_weights=np.zeros(15000)
            hist_borders=np.zeros(15001)
            histogram(pe_energy, hist_weights, hist_borders)
            plt.stairs(hist_weights, edges=hist_borders, fill=True)
            plt.xlim(0, 100)
            plt.show()