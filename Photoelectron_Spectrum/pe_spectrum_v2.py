import numpy as np
from pygama.lgdo import LH5Store
from pygama.dsp.processors.histogram import histogram, histogram_stats
import matplotlib.pyplot as plt
import copy

store=LH5Store()

def draw(lh5_file: str, channels: list[str], dt: float | int = 16, draw_spectrum : bool = True, draw_tp_hist : bool = False, size : tuple = (8,5)):
    
    plt.rcParams["figure.figsize"] = size
    plt.rcParams["figure.facecolor"] = "white"
    plt.rcParams["font.size"] = 12
    
    for ch in channels:
        
        trigger_pos=store.read_object(ch+'/dsp/trigger_pos', lh5_file)[0].nda*dt/1000
        energies=store.read_object(ch+'/dsp/energies', lh5_file)[0].nda
        
        #trigger_pos histogram
        hist_weights=np.zeros(1000)
        hist_borders=np.zeros(1001)
        histogram(trigger_pos[~np.isnan(trigger_pos)], hist_weights, hist_borders)
        if draw_tp_hist:
            plt.stairs(hist_weights, edges=hist_borders, fill=True, label=ch)
            plt.legend()
            plt.show()
        
        #Getting the trigger time
        max_idx=np.zeros(1)
        histogram_stats(hist_weights, hist_borders, max_idx, np.zeros(1), np.zeros(1), np.nan)
        trigg_time=hist_borders[np.int64(max_idx[0])]
        
        #p.e. spectrum
        pe_energy=np.array([])
        for i in range(len(energies)):
            
            mask=trigger_pos[i]>trigg_time-0.5
            tp=trigger_pos[i][mask]
            ens=energies[i][mask]
            
            if np.size(ens)>0:
                en=copy.copy(ens)
                for j in range(1,len(ens)):
                    diffs=tp[j:]-tp[:-j]
                    en=np.concatenate(([en[k]+ens[k+j] if diffs[k]<5.5 else en[k] for k in range(len(diffs))], en[len(en)-j:]))
                pe_energy=np.concatenate((pe_energy, en))
            
        if draw_spectrum:
            hist_weights=np.zeros(15000)
            hist_borders=np.zeros(15001)
            histogram(pe_energy, hist_weights, hist_borders)
            plt.stairs(hist_weights, edges=hist_borders, fill=True, label=ch)
            plt.xlim(0, 100)
            plt.legend()
            plt.show()