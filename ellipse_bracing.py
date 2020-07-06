import cadquery as cq # type: ignore

scale = 20
wt = 0.4
height = 2*scale
xAxis = 1.0*scale
yAxis = 0.5*scale

r1 = (
    cq.Workplane("XY", origin=(0, 0))#height/2))
    .ellipse(xAxis, yAxis)
    .extrude(height)
)
log(f'r1.isValid()={r1.val().isValid()}')
#show_object(r1)

cutter = (
    cq.Workplane("XY", origin=(0, 0))#(height+wt)/2))
    .ellipse(xAxis-wt, yAxis-wt)
    .extrude(height+wt)
)
log(f'cutter.isValid()={cutter.val().isValid()}')
#show_object(cutter)

r1 = r1.cut(cutter)
log(f'r1.isValid()={r1.val().isValid()}')
show_object(r1)

brace = (
    cq.Workplane("YZ", origin=(0, 0))
    .transformed(rotate=(-47, 0, ), offset=(0, height/2))
    .center(0, 0)
    .rect(25, 60)
    .circle(8)
    .center(0, -16)
    .circle(6)
    .center(0, 32)
    .circle(6)
    .extrude(wt)
)
log(f'brace.val().isValid={brace.val().isValid()}')
show_object(brace)

# This generates "IndexError: list index out of range"
r2 = r1.cutThruAll(brace)
#log(f'r2.isValid()={r2.val().isValid()}')
#show_object(r2)

