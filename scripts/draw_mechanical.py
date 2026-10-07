"""Nominal dimensional plate; functional tolerance testing is still required."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,Circle,Rectangle
ROOT=Path(__file__).resolve().parents[1]
fig,axs=plt.subplots(1,2,figsize=(12,5));fig.patch.set_facecolor('#f3f5f7')
for a in axs:a.set_facecolor('#f3f5f7');a.set_aspect('equal');a.axis('off')
a=axs[0];a.set_xlim(-65,65);a.set_ylim(-52,52)
a.add_patch(FancyBboxPatch((-50,-35),100,70,boxstyle='round,pad=0,rounding_size=4',fill=False,lw=1.8,ec='#0b1424'))
a.add_patch(FancyBboxPatch((-40,-25),80,50,boxstyle='round,pad=0,rounding_size=2',fill=False,lw=1.2,ec='#24a0a7',linestyle='--'))
for x in (-30,30):
    for y in (-15,15):a.add_patch(Circle((x,y),1.6,fill=False,color='#24a0a7'))
for x in (-43,43):
    for y in (-28,28):a.add_patch(Circle((x,y),1.6,fill=False,color='#0b1424'))
def dimension(ax,p1,p2,text):
    ax.annotate('',xy=p1,xytext=p2,arrowprops=dict(arrowstyle='<->',color='#536275',lw=.9))
    mid=((p1[0]+p2[0])/2,(p1[1]+p2[1])/2)
    ax.text(mid[0],mid[1]+2,text,ha='center',fontsize=9,color='#0b1424',bbox=dict(fc='#f3f5f7',ec='none',pad=1))
dimension(a,(-50,44),(50,44),'100 mm');dimension(a,(-58,-35),(-58,35),'70')
dimension(a,(-30,0),(30,0),'60 mm mounting pitch')
a.text(0,-45,'PCB envelope 80 × 50 mm  |  Mount holes Ø3.2 mm',ha='center',fontsize=9,color='#536275')
a.set_title('TOP / nominal mounting geometry',loc='left',fontweight='bold',color='#0b1424',fontsize=12)
b=axs[1];b.set_xlim(-65,65);b.set_ylim(-12,62)
b.add_patch(Rectangle((-50,0),100,30,fill=False,lw=1.8,ec='#0b1424'))
b.add_patch(Rectangle((-50,30),100,2,fill=False,lw=1.8,ec='#0b1424'))
b.add_patch(Rectangle((-47,26),94,4,fill=False,lw=1,ec='#0b1424',linestyle='--'))
b.add_patch(Rectangle((-40,8),80,1.6,facecolor='#24a0a7',edgecolor='none'))
dimension(b,(58,0),(58,32),'32');dimension(b,(-50,45),(50,45),'100 mm')
b.annotate('2 mm floor',xy=(-20,2),xytext=(-42,-8),arrowprops=dict(arrowstyle='->',color='#536275'),fontsize=9)
b.annotate('PCB bottom z = 8 mm',xy=(20,8),xytext=(-20,18),arrowprops=dict(arrowstyle='->',color='#536275'),fontsize=9)
b.text(0,54,'Wall 2.5 mm  |  Lid rim clearance 0.5 mm / side',ha='center',fontsize=9,color='#536275')
b.set_title('SIDE / assembly heights',loc='left',fontweight='bold',color='#0b1424',fontsize=12)
fig.tight_layout(pad=2)
for ext in ('png','svg'):fig.savefig(ROOT/'figures'/f'mechanical-drawing.{ext}',dpi=180,facecolor=fig.get_facecolor())
