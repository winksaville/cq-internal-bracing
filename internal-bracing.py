import cadquery as cq # type: ignore

length = 40.0
height = 10 
base = 3
top = 5 
wallThickness = 0.50

outline = [
      (-top/2, height)
    , (-base/2, 0)
    , (base/2, 0)
    , (top/2, height)
]

# Create outside solid
thing = (
    cq.Workplane("XZ", origin=(0, length/2))
    .polyline(outline).close()
    .extrude(length)
)
log(f'thing.val().isValid={thing.val().isValid()}')
#show_object(thing)

cutterOutline = [
      (-(top-wallThickness)/2, height+wallThickness)
    , (-(base-wallThickness)/2, 0-wallThickness)
    , ((base-wallThickness)/2, 0-wallThickness)
    , ((top-wallThickness)/2, height+wallThickness)
]

# Create cutter solid
cutter = (
    cq.Workplane("XZ", origin=(0, (length+wallThickness)/2))
    .polyline(cutterOutline).close()
    .extrude(length+wallThickness)
)
log(f'cutter.val().isValid={cutter.val().isValid()}')
#show_object(cutter)

# Remove cutter
thing = thing.cut(cutter)
log(f'thing.val().isValid={thing.val().isValid()}')
show_object(thing)

planarBrace = (
    cq.Workplane("XZ", origin=(0, 0))
    .transformed(rotate=(-45, 0, ), offset=(0, 0))
    .center(0, height/2)
    .rect(20, 20)
    .center(0, -3)
    .circle(1)
    .center(0, 2.8)
    .circle(1.15)
    .center(0, 2.9)
    .circle(1.3)
    .center(0, 3.3)
    .circle(1.5)
    .extrude(wallThickness)
)
print(f'planarBrace.val().isValid={planarBrace.val().isValid()}')
show_object(planarBrace)

