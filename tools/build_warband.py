"""Stylized, solid 28 mm frog warband. Coordinates and STL dimensions are mm."""
from pathlib import Path
import json
import numpy as np
import trimesh as t

OUT = Path(__file__).resolve().parents[1] / 'models'
OUT.mkdir(exist_ok=True)

def ball(p, r):
    m = t.creation.icosphere(subdivisions=2)
    m.apply_scale(r if np.ndim(r) else [r]*3)
    m.apply_translation(p)
    return m

def rod(a,b,r):
    a,b=np.array(a,float),np.array(b,float)
    m=t.creation.cylinder(radius=r,height=np.linalg.norm(b-a),sections=16)
    m.apply_transform(t.geometry.align_vectors([0,0,1], b-a))
    m.apply_translation((a+b)/2)
    return m

def link(parts, points, r):
    for a,b in zip(points,points[1:]): parts.append(rod(a,b,r))
    for p in points: parts.append(ball(p,r))

def build(kind):
    p=[]
    base=t.creation.cylinder(radius=12.5,height=2,sections=96)
    base.apply_translation([0,0,1]); p.append(base)
    # Low crouched legs, broad webbed feet, and a rounded frog torso.
    for s in [-1,1]:
        link(p,[(s*3,0,12),(s*5,0,8),(s*4,-1,3.5)],1.65)
        p.append(ball([s*4,-1.5,3],[2.4,2.7,1.2]))
        for dx in [-1,0,1]:
            link(p,[(s*4+dx*.6,-2,3),(s*4+dx,-4,2.7)],.55)
    p.extend([ball([0,0,15],[4.4,3,6]),ball([0,.1,20],[4.7,3.2,3]),
              ball([0,-1,24],[5,3.7,3.2]),ball([0,-2.6,22.7],[4.6,2.3,1.25])])
    # Raised eye sockets and strongly defined eyes look toward negative Y.
    for s in [-1,1]:
        p.extend([ball([s*3,-1.5,26.4],[1.9,2,1.6]),
                  ball([s*3,-3,26.5],[1.15,.8,1]),
                  ball([s*3,-3.65,26.5],[.4,.25,.65])])
    # Continuous raised lip line and paired nostrils.
    link(p,[(-4,-3.2,23.5),(-2.5,-4.7,23.2),(0,-5,23.1),(2.5,-4.7,23.2),(4,-3.2,23.5)],.32)
    for s in [-1,1]: p.append(ball([s*1.3,-4.25,25],[.45,.35,.3]))
    # Belt, diagonal straps, rear garment panels and front loincloth.
    belt=t.creation.torus(major_radius=3.55,minor_radius=.55)
    belt.apply_scale([1,.78,1]); belt.apply_translation([0,0,12]); p.append(belt)
    for s in [-1,1]:
        link(p,[(s*3,-1.8,20),(s*1,-3,16),(-s*3,-1.8,12)],.42)
        link(p,[(s*3,1.8,20),(s*1,2.9,16),(-s*3,1.8,12)],.42)
        p.append(ball([s*2.4,1.7,10],[1.9,1.2,3.2]))
    p.append(ball([0,-2,9.7],[2,1.1,3.5]))
    p.append(ball([3.8,-.8,12],[1.3,1.3,1.7]))
    # Back warts and shoulder details, attached to the skin.
    for z in [15,17,19,21]:
        for x in [-2,0,2]: p.append(ball([x,2.5 if abs(x)<1 else 2.2,z],.65))
    for s in [-1,1]:
        for z in [8,9,10]:
            p.append(ball([s*4.6,0,z],[1.65,1.65,.35]))
    if kind=='archer':
        arms=[[(3,0,19),(6,-1,18),(8,-2,19)], [(-3,0,19),(-5,-3,20),(-1,-4,21)]]
    elif kind=='swamp_shaman':
        arms=[[(-3,0,19),(-6,-1,17),(-7,-2,18)],[(3,0,19),(6,-1,19),(8,-2,21)]]
    else:
        arms=[[(-3,0,19),(-6,0,18),(-7,-1,20)],[(3,0,19),(5,-1,16),(7,-2,16)]]
    for points in arms:
        link(p,points,1.2); p.append(ball(points[-1],1.45))
    if kind=='spearman':
        link(p,[(-7,-1,2),(-7,-1,33)],.65)
        spear=t.creation.cone(radius=1.5,height=6,sections=4)
        spear.apply_translation([-7,-1,32]); p.append(spear)
        p.append(ball([7,-2,15],[1.3,3.4,6]))
        for y in [-4,-2,0]: link(p,[(7,y,10),(7,y,20)],.4)
        for z in [12,18]: link(p,[(7,-4,z),(7,0,z)],.55)
    if kind=='cleaver_warrior':
        link(p,[(-7,-1,18),(-7,-1,27)],.7)
        blade=t.creation.box(extents=[3,1.2,7]); blade.apply_translation([-7,-1,29]); p.append(blade)
    if kind=='club_warrior':
        link(p,[(-7,-1,18),(-7,-1,31)],.8)
        p.append(ball([-7,-1,29],[2,1.9,4]))
        for z in [27,29,31]:
            for s in [-1,1]: link(p,[(-7+s,-1,z),(-7+s*2.8,-1,z+.7)],.55)
    if kind=='archer':
        bow=[(6,-2,9),(8.5,-2,13),(9,-2,19),(8.5,-2,25),(6,-2,29)]
        link(p,bow,.65)
        link(p,[bow[0],(7.9,-2,19),bow[-1]],.4)
        link(p,[(-1,-4,21),(10,-2.2,21)],.45)
        p.append(ball([10,-2.2,21],[1,.65,.65]))
        link(p,[(-2,2,13),(-2,3,22)],1.2)
        for x in [-3,-2,-1]: link(p,[(x,3,20),(x,3,25)],.35)
    if kind=='swamp_shaman':
        link(p,[(-7,-2,2),(-7,-2,33)],.8)
        p.append(ball([-7,-2,32],[2.2,1.6,2]))
        for s in [-1,1]: link(p,[(-7+s,-2,32),(-7+s*2.8,-2,34)],.65)
        # Thick hood rim and a connected magical orb rather than unsupported wisps.
        for s in [-1,1]: link(p,[(s*4,1,18),(s*5,1,24),(s*3,1,28),(0,1,29)],.85)
        p.append(ball([8,-2,23],[1.5,1.5,1.7]))
        for s in [-1,1]: link(p,[(8+s*.7,-2,23),(8+s,-2,25)],.5)
    # Union every overlapping component into printable solid shells.
    mesh=t.boolean.union(p,engine='manifold')
    assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0
    mesh.export(OUT/f'{kind}_28mm.stl')
    reloaded=t.load_mesh(OUT/f'{kind}_28mm.stl')
    # STL stores float32 vertices; weld coincident export vertices at 0.00001 mm.
    reloaded.merge_vertices(digits_vertex=5)
    reloaded.update_faces(reloaded.nondegenerate_faces())
    reloaded.remove_unreferenced_vertices()
    assert reloaded.is_watertight
    reloaded.export(OUT/f'{kind}_28mm.stl')
    mesh=t.load_mesh(OUT/f'{kind}_28mm.stl')
    assert mesh.is_watertight and len(mesh.split())==1
    return dict(model=kind,triangles=len(mesh.faces),dimensions_mm=mesh.extents.tolist(),
                watertight=bool(mesh.is_watertight),shells=len(mesh.split()))

if __name__=='__main__':
    results=[build('spearman')]
    (OUT/'validation.json').write_text(json.dumps(results,indent=2))
    print(json.dumps(results,indent=2))
