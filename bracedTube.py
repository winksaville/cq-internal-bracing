import cadquery as cq # type: ignore

scale = 20
wt = 0.4
height = 2*scale
xAxis = 1.0*scale
yAxis = 0.5*scale

# Create a rod
ellipticalRod = (
    cq.Workplane("XY", origin=(0, 0))#height/2))
    .ellipse(xAxis, yAxis)
    .extrude(height)
)
log(f'ellipticalRod.isValid()={ellipticalRod.val().isValid()}')
#show_object(ellipticalRod)

# Cutter to hollow out the rod
cutter = (
    cq.Workplane("XY", origin=(0, 0))#(height+wt)/2))
    .ellipse(xAxis-wt, yAxis-wt)
    .extrude(height+wt)
)
log(f'cutter.isValid()={cutter.val().isValid()}')
#show_object(cutter)

# Create a tube using the cutter to hollow it out
ellipticalTube = ellipticalRod.cut(cutter)
log(f'ellipticalTube.isValid()={ellipticalTube.val().isValid()}')
#show_object(ellipticalTube)

# Create a plate with some holes in it to lighten it.
plate = (
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
log(f'plate.val().isValid={plate.val().isValid()}')
#show_object(plate)

# Cut the plate leaving a brace which fits the inside of the tube
brace = plate.cut(ellipticalTube).solids().last()
log(f'brace.isValid()={brace.val().isValid()}')
#show_object(brace)

bracedTube = brace.union(ellipticalTube)
log(f'bracedTube.isValid()={bracedTube.val().isValid()}')
show_object(bracedTube)
