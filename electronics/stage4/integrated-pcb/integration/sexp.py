"""Small lossless-type S-expression reader for native KiCad saved files."""
import json,re
class Quoted(str): pass
def loads(text):
    tokens=re.findall(r'"(?:\\.|[^"\\])*"|\(|\)|[^\s()]+',text); stack=[]; root=None
    for t in tokens:
        if t=='(':
            v=[]
            if stack: stack[-1].append(v)
            else: root=v
            stack.append(v)
        elif t==')': stack.pop()
        else: stack[-1].append(Quoted(json.loads(t)) if t.startswith('"') else t)
    assert not stack
    return root
def dumps(x):
    if isinstance(x,list): return '('+' '.join(dumps(y) for y in x)+')'
    if isinstance(x,Quoted): return json.dumps(str(x),ensure_ascii=False)
    return str(x)
def sub(x,name): return next((y for y in x if isinstance(y,list) and y and y[0]==name),None)
def subs(x,name): return [y for y in x if isinstance(y,list) and y and y[0]==name]
def walk(x):
    if isinstance(x,list):
        yield x
        for v in x: yield from walk(v)
