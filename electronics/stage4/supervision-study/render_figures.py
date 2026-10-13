"""Render scientific figures from saved results; explicit --write-figures only."""
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--write-figures',action='store_true',required=True);ap.parse_args()
    d=json.loads((HERE/'analog-results.json').read_text(encoding='utf-8'))
    out=HERE/'figures';out.mkdir(exist_ok=True)
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,
                         'svg.fonttype':'none','figure.facecolor':'white'})
    fig,ax=plt.subplots(2,2,figsize=(12,7),layout='constrained')
    colors=['#086f8c','#cc6430','#5e5896']
    with np.load(HERE/'analog-traces.npz') as data:
        for name,label,col in zip(['normal_single_phase','primary_timer_stuck_secondary_healthy','rail_fault_at_80us'],
                                  ['Normal request ends','Primary stuck; secondary healthy','Rail fault + assumed delay'],colors):
            trace=data[name]
            ax[0,0].step(trace[:,0]*1e6,trace[:,1]*1e3,where='post',label=label,color=col)
            ax[0,1].plot(trace[:,0]*1e3,trace[:,2],label=label,color=col)
    ax[0,0].set(xlim=(0,350),xlabel='Time (µs)',ylabel='External current (mA)',title='Healthy guard interrupts the external path')
    ax[0,0].legend(fontsize=8)
    ax[0,1].set(xlim=(0,12),xlabel='Time (ms)',ylabel='Artificial load voltage (V)',title='Stored energy persists after disconnection')
    rows=d['interruptions'];labels=['Normal','Primary stuck','Secondary stuck','Rail fault','Monitor fault','Both timers stuck','Welded guards*']
    positions=np.arange(len(rows))
    ax[1,0].barh(positions,[r['external_port_charge_C']*1e6 for r in rows],color=colors[0])
    ax[1,0].set(yticks=positions,yticklabels=labels,xscale='log',xlabel='Absolute external charge (µC; log scale)',title='A heartbeat alone is far too slow for phase limiting')
    ax[1,0].invert_yaxis()
    ax[1,1].barh(positions,[r['stored_energy_at_observation_end_J']*1e6 for r in rows],color=colors[1])
    ax[1,1].set(yticks=positions,yticklabels=labels,xlabel='Stored load energy at observation end (µJ)',title='Finite fault witnesses retain their consequences')
    ax[1,1].invert_yaxis()
    fig.suptitle('Independent shutdown — artificial 1 kΩ ‖ 2 µF load, 3 mA; declared 5 µs guard edges',fontsize=13)
    fig.text(.5,-.025,'*Welded trace ends at 5 ms with current still flowing. No later cutoff is inferred. Edge injection is accounted separately.',ha='center',fontsize=9)
    for suffix in ('svg','png'):fig.savefig(out/f'shutdown-and-residual.{suffix}',dpi=170,bbox_inches='tight')
    plt.close(fig)
    fig,axes=plt.subplots(1,3,figsize=(12,4),layout='constrained')
    quiet=d['comparator_windows'][0];pair=d['difference_amplifier'];afe=d['AFE_blank_observation']
    cases=[(quiet['accepted_union'],quiet['accepted_intersection'],1e6,'Current window (µA)','Measured quiescence'),
           (pair['accepted_union_V'],pair['accepted_intersection_V'],1,'Internal A − B (V)','Pair-voltage window'),
           (afe['pin_voltage_accepted_union_V'],afe['pin_voltage_accepted_intersection_V'],1e3,'RHD-side pin voltage (mV)','Recording blank observation')]
    for ax,(union,intersection,scale,xlabel,title) in zip(axes,cases):
        ax.plot(np.array(union)*scale,[1,1],color='#cc6430',linewidth=10,solid_capstyle='butt',label='Accepted in at least one corner')
        ax.plot(np.array(intersection)*scale,[.5,.5],color='#086f8c',linewidth=10,solid_capstyle='butt',label='Accepted in every chosen corner')
        ax.axvline(0,color='gray',linewidth=.7)
        ax.set(ylim=(0,1.4),yticks=[],xlabel=xlabel,title=title)
        ax.grid(axis='x',alpha=.2)
    axes[0].legend(loc='lower center',fontsize=8,bbox_to_anchor=(.5,-.4))
    fig.suptitle('Stable threshold envelopes under declared component limits and allowances',fontsize=13)
    fig.text(.5,-.03,'These are finite DC windows. They do not prove zero current, guard position, AC linearity, recovery or biological efficacy.',ha='center',fontsize=9)
    for suffix in ('svg','png'):fig.savefig(out/f'threshold-envelopes.{suffix}',dpi=170,bbox_inches='tight')
    plt.close(fig)
    print('Rendered two saved-data figures as SVG and PNG')


if __name__=='__main__':main()
