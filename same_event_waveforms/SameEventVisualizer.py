import json, re
import numpy as np
import matplotlib.pyplot as plt
from pygama.vis.waveform_browser import WaveformBrowser

def draw(lh5_file: str, channel_map: str, entries: list[int] = [0], channel_mask: list[int] = [], size: tuple = (14,14))-> None:
    
    if not re.findall('.lh5$', lh5_file):
        raise ValueError('lh5_file must be a LH5 file')
    if not re.findall('.json$', channel_map):
        raise ValueError('channel_map must be a JSON file')
        
    with open(channel_map,'r') as f:
        c_map=json.load(f)['hardware_configuration']['channel_map']

    plt.rcParams["figure.facecolor"] = "white"
    plt.rcParams["font.size"] = 12
    
    color=plt.cm.rainbow(np.linspace(0,1,len(c_map)))
    
    browsers= {int(re.findall('\d{3}', ch)[0]):WaveformBrowser(lh5_file, ch+'/raw', styles=[{'ls':['--'], 'c':[color[i-23]]}]) for i,ch in enumerate(c_map.keys())}
    to_be_drawn=list(set(browsers.keys())-set(channel_mask))
    
    for entry in entries:
        #clear=True
        fig=plt.figure(figsize=size)
        ax=fig.subplots(11,3)
        for i in range(len(to_be_drawn)):
            #browsers[to_be_drawn[i]].draw_entry(entry, clear=False)
            #clear=False
            #if i<len(to_be_drawn)-1:
                #browsers[to_be_drawn[i+1]].set_figure(browsers[to_be_drawn[i]])
        #plt.autoscale(axis='y')
            browsers[to_be_drawn[i]].set_figure(fig=fig, ax=ax[i//3,i%3])
            browsers[to_be_drawn[i]].draw_entry(entry, clear=False)
            ax[i//3,i%3].set_xticklabels([])
            ax[i//3,i%3].set_yticklabels([])
            ax[i//3,i%3].set_xlabel('')
            ax[i//3,i%3].set_ylabel('')
        #plt.autoscale(axis='y')
        #plt.show()
        fig.show()