"""Generic bounded four-layer copper grid proposal; native DRC remains authority.

Copied geometry primitives from the native AFE repair with no AFE-specific masks.
Used for the 300 x 250 mm supervision reference board.
"""
from __future__ import annotations
import argparse
import hashlib
import heapq
import json
from pathlib import Path
import time
import numpy as np
import pcbnew as pcb

HERE=Path(__file__).resolve().parent
PKG=HERE.parent
PATH=PKG/'boards/recording-front-end/recording_front_end.kicad_pcb'
GRID=.1
LAYERS=[pcb.F_Cu,pcb.In1_Cu,pcb.In2_Cu,pcb.B_Cu]
WIDTH=.15
VIA=.6
CLEAR=.15
MARGIN=.025
NX,NY=3001,2501


def mm(x):return pcb.FromMM(float(x))
def point(x,y):return pcb.VECTOR2I(mm(x),mm(y))
def xy(v):return pcb.ToMM(v.x),pcb.ToMM(v.y)
def digest(path):return hashlib.sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
def cell(x,y):return int(round(x/GRID)),int(round(y/GRID))
def mark_rect(a,x0,y0,x1,y1,r=0):
    x0=max(0,int(np.ceil((x0-r)/GRID)));x1=min(NX-1,int(np.floor((x1+r)/GRID)))
    y0=max(0,int(np.ceil((y0-r)/GRID)));y1=min(NY-1,int(np.floor((y1+r)/GRID)))
    a[y0:y1+1,x0:x1+1]=True

def mark_line(a,start,end,r):
    sx,sy=start;ex,ey=end
    x0=max(0,int(np.floor((min(sx,ex)-r)/GRID)));x1=min(NX-1,int(np.ceil((max(sx,ex)+r)/GRID)))
    y0=max(0,int(np.floor((min(sy,ey)-r)/GRID)));y1=min(NY-1,int(np.ceil((max(sy,ey)+r)/GRID)))
    if x1<x0 or y1<y0:return
    yy,xx=np.ogrid[y0:y1+1,x0:x1+1];xx=xx*GRID;yy=yy*GRID
    dx,dy=ex-sx,ey-sy;den=dx*dx+dy*dy
    t=np.clip(((xx-sx)*dx+(yy-sy)*dy)/den,0,1) if den else 0
    distance=(xx-(sx+t*dx))**2+(yy-(sy+t*dy))**2
    a[y0:y1+1,x0:x1+1]|=distance<=r*r


def obstacles(board,net):
    blocked=np.zeros((4,NY,NX),dtype=np.bool_);via=np.zeros((NY,NX),dtype=np.bool_)
    for mask in list(blocked)+[via]:
        mask[:10,:]=True;mask[-10:,:]=True;mask[:,:10]=True;mask[:,-10:]=True
    for f in board.GetFootprints():
        for pad in f.Pads():
            if pad.GetNetCode()==net:continue
            box=pad.GetBoundingBox();x0,y0=xy(box.GetOrigin());x1,y1=xy(box.GetEnd())
            for index,layer in enumerate(LAYERS):
                if pad.IsOnLayer(layer):mark_rect(blocked[index],x0,y0,x1,y1,CLEAR+WIDTH/2+MARGIN)
            mark_rect(via,x0,y0,x1,y1,CLEAR+VIA/2+MARGIN)
    for track in board.GetTracks():
        start=xy(track.GetStart());end=xy(track.GetEnd())
        if isinstance(track,pcb.PCB_VIA):
            # Drilled vias require hole spacing even on the same electrical net.
            mark_line(via,start,start,.3+.25+MARGIN)
            if track.GetNetCode()!=net:
                for mask in blocked:mark_line(mask,start,start,pcb.ToMM(track.GetWidth(pcb.F_Cu))/2+CLEAR+WIDTH/2+MARGIN)
                mark_line(via,start,start,pcb.ToMM(track.GetWidth(pcb.F_Cu))/2+CLEAR+VIA/2+MARGIN)
        elif track.GetNetCode()!=net:
            layer=track.GetLayer()
            if layer in LAYERS:mark_line(blocked[LAYERS.index(layer)],start,end,pcb.ToMM(track.GetWidth())/2+CLEAR+WIDTH/2+MARGIN)
            mark_line(via,start,end,pcb.ToMM(track.GetWidth())/2+CLEAR+VIA/2+MARGIN)
    return blocked,via


def native_items(board):
    items={}
    for f in board.GetFootprints():
        for pad in f.Pads():items[pad.m_Uuid.AsString()]=pad
    for track in board.GetTracks():items[track.m_Uuid.AsString()]=track
    return items


def endpoint(item,reported):
    if isinstance(item,pcb.PAD):
        pos=xy(item.GetPosition());layers=[i for i,l in enumerate(LAYERS) if item.IsOnLayer(l)]
    elif isinstance(item,pcb.PCB_VIA):pos=xy(item.GetStart());layers=list(range(4))
    else:
        # DRC's item position is a real endpoint in these saved reports.
        options=[xy(item.GetStart()),xy(item.GetEnd())]
        pos=min(options,key=lambda p:(p[0]-reported['x'])**2+(p[1]-reported['y'])**2)
        layers=[LAYERS.index(item.GetLayer())]
    return pos,layers


def route(blocked,via,start,end,max_nodes=300000):
    (sx,sy),sl=start;(ex,ey),el=end
    ax,ay=cell(sx,sy);bx,by=cell(ex,ey)
    # Endpoints on their own copper are safe; a large obstacle margin may have
    # consumed one sampled cell. Never open a corridor through foreign copper.
    for l in sl:
        if blocked[l,ay,ax]:raise RuntimeError(('blocked start',sx,sy,l))
    for l in el:
        if blocked[l,by,bx]:raise RuntimeError(('blocked end',ex,ey,l))
    target={(l,bx,by) for l in el}
    def heuristic(x,y):
        dx=abs(x-bx);dy=abs(y-by)
        return 1.5*(max(dx,dy)+.41421356237*min(dx,dy))
    heap=[];cost={};prev={}
    for l in sl:
        key=(l,ax,ay);cost[key]=0.;heapq.heappush(heap,(heuristic(ax,ay),0.,key))
    n=0
    moves=[(1,0,1.),(-1,0,1.),(0,1,1.),(0,-1,1.),(1,1,1.41421356237),(1,-1,1.41421356237),(-1,1,1.41421356237),(-1,-1,1.41421356237)]
    while heap:
        _,g,key=heapq.heappop(heap)
        if g!=cost.get(key):continue
        if key in target:
            path=[key]
            while path[-1] in prev:path.append(prev[path[-1]])
            return path[::-1],n
        n+=1
        if n>max_nodes:raise RuntimeError(('route expansion bound',n))
        l,x,y=key
        for dx,dy,c in moves:
            nx=x+dx;ny=y+dy
            if nx<0 or nx>=NX or ny<0 or ny>=NY or blocked[l,ny,nx]:continue
            if dx and dy and (blocked[l,y,nx] or blocked[l,ny,x]):continue
            nk=(l,nx,ny);ng=g+c
            if ng<cost.get(nk,float('inf')):
                cost[nk]=ng;prev[nk]=key;heapq.heappush(heap,(ng+heuristic(nx,ny),ng,nk))
        if not via[y,x]:
            for nl in range(4):
                if nl==l or blocked[nl,y,x]:continue
                nk=(nl,x,y);ng=g+35
                if ng<cost.get(nk,float('inf')):
                    cost[nk]=ng;prev[nk]=key;heapq.heappush(heap,(ng+heuristic(x,y),ng,nk))
    raise RuntimeError(('no geometric route',start,end,n))


def copper(board,net,path,start,end):
    # Compress collinear grid steps, retaining a vertex at every layer change.
    simplified=[path[0]]
    for i in range(1,len(path)-1):
        a,b,c=path[i-1:i+2]
        if a[0]!=b[0] or b[0]!=c[0] or (b[1]-a[1],b[2]-a[2])!=(c[1]-b[1],c[2]-b[2]):simplified.append(b)
    simplified.append(path[-1])
    tracks=0;vias=0
    def segment(a,b,layer):
        nonlocal tracks
        if a==b:return
        t=pcb.PCB_TRACK(board);t.SetStart(point(*a));t.SetEnd(point(*b));t.SetWidth(mm(WIDTH));t.SetLayer(LAYERS[layer]);t.SetNetCode(net);board.Add(t);tracks+=1
    segment(start[0],(path[0][1]*GRID,path[0][2]*GRID),path[0][0])
    for a,b in zip(simplified,simplified[1:]):
        if a[0]!=b[0]:
            v=pcb.PCB_VIA(board);v.SetPosition(point(a[1]*GRID,a[2]*GRID));v.SetWidth(mm(VIA));v.SetDrill(mm(.3));v.SetViaType(pcb.VIATYPE_THROUGH);v.SetLayerPair(pcb.F_Cu,pcb.B_Cu);v.SetNetCode(net);board.Add(v);vias+=1
        else:segment((a[1]*GRID,a[2]*GRID),(b[1]*GRID,b[2]*GRID),a[0])
    segment((path[-1][1]*GRID,path[-1][2]*GRID),end[0],path[-1][0])
    return tracks,vias
