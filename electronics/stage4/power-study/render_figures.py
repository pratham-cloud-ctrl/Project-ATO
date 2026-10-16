"""Render saved power-budget figures; explicit write flag required."""
from pathlib import Path
import argparse,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write-figures',action='store_true',required=True);p.parse_args()
    d=json.loads((HERE/'budget-results.json').read_text(encoding='utf-8'));a=d['operating_cases'][-1]
    out=HERE/'figures';out.mkdir(exist_ok=True)
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    fig,ax=plt.subplots(1,2,figsize=(12,4.6),layout='constrained')
    values=[a['rail_useful_load_W'],a['LDO_loss_W'],a['isolated_module_loss_W'],
            sum(c['loss_W'] for c in a['converter_stages']),a['battery_cases'][1]['diode_W']]
    labels=['Rail loads','AFE linear regulators','Isolated converter','Bucks / boosts','Input diode']
    colors=['#086f8c','#397d6b','#ab8648','#cc6430','#705e92'];start=0.
    for val,label,col in zip(values,labels,colors):
        ax[0].barh(0,val,left=start,color=col,label=f'{label}: {val:.3f} W');start+=val
    ax[0].set(yticks=[],xlabel='Battery input power allocation (W)',title=f'Conditional active allocation: {a["battery_nominal_W"]:.3f} W')
    ax[0].legend(loc='upper left',bbox_to_anchor=(0,-.25),fontsize=9)
    bs=sorted({r['buck_efficiency_assumed'] for r in d['efficiency_sensitivity']})
    iso=sorted({r['iso_efficiency_assumed'] for r in d['efficiency_sensitivity']})
    matrix=np.array([[next(r['runtime_h'] for r in d['efficiency_sensitivity'] if r['buck_efficiency_assumed']==b and r['iso_efficiency_assumed']==i) for b in bs] for i in iso])
    im=ax[1].imshow(matrix,origin='lower',cmap='Blues',aspect='auto')
    for row in range(len(iso)):
        for col in range(len(bs)):ax[1].text(col,row,f'{matrix[row,col]:.2f} h',ha='center',va='center',color='white' if matrix[row,col]>matrix.mean() else '#162f42')
    ax[1].set(xticks=range(len(bs)),xticklabels=[f'{b:.0%}' for b in bs],yticks=range(len(iso)),yticklabels=[f'{i:.0%}' for i in iso],xlabel='Assumed buck load efficiency',ylabel='Assumed isolated load efficiency',title='Runtime sensitivity; 80% of 19.24 Wh')
    fig.suptitle('Power reference — declared load ceilings and efficiencies, not measured hardware',fontsize=13)
    save(fig,out/'power-and-runtime')
    fig,ax=plt.subplots(1,3,figsize=(12,4),layout='constrained')
    for C,label in [(2e-6,'2 µF rejected witness'),(30e-6,'30 µF selected effective bank')]:
        rows=[r for r in d['reservoir']['cases'] if r['effective_C_F']==C and r['sources']==2]
        rows=sorted(rows,key=lambda r:r['integrated_on_time_s'])
        ax[0].plot([r['integrated_on_time_s']*1e6 for r in rows],[r['final_V'] for r in rows],marker='o',label=label)
    ax[0].axhline(22.8,color='#b14939',linestyle='--',label='Nominal UV comparison')
    ax[0].set(xlabel='Integrated phase on-time (µs)',ylabel='24 V bank after pulse (V)',title='Two aligned 3 mA sources')
    ax[0].legend(fontsize=8)
    r=d['resources'];labels=['Monitor conversion target','Continuous framed raw link','RAM / 80% allocation']
    ratios=[r['old_planned_monitor_words_per_s']/r['actual_aggregate_ADC_words_per_s'],r['raw4k_framed_bits_per_s']/1e6,r['RAM_total_bytes']/(.8*r['RAM_capacity_bytes'])]
    ax[1].barh(labels,ratios,color=['#cc6430' if x>1 else '#086f8c' for x in ratios]);ax[1].axvline(1,color='black',linestyle='--')
    ax[1].set(xlabel='Requested allocation / capacity',title='Retained resource constraints');ax[1].invert_yaxis()
    heat=d['thermal_sensitivity']
    ax[2].plot([r['assumed_system_thermal_resistance_K_per_W'] for r in heat],[r['steady_rise_K'] for r in heat],marker='o',color='#cc6430')
    ax[2].axhline(2,color='black',linestyle='--',label='Selected 2 K allocation')
    ax[2].set(xlabel='Assumed lumped resistance (K/W)',ylabel='Linear steady rise (K)',title='Compact thermal closure unearned');ax[2].legend(fontsize=8)
    fig.suptitle('Finite electrical and resource witnesses; thermal curve is a sensitivity model',fontsize=13)
    save(fig,out/'power-constraints')
    print('Saved two scientific power figures (PNG/SVG)')


def save(fig,path):
    for suffix in ('png','svg'):fig.savefig(path.with_suffix('.'+suffix),dpi=170,bbox_inches='tight')
    plt.close(fig)
    svg=path.with_suffix('.svg');svg.write_text(''.join(l.rstrip()+'\n' for l in svg.read_text(encoding='utf-8').splitlines()),encoding='utf-8')


if __name__=='__main__':main()
