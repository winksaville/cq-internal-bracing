import cadquery as cq # type: ignore

scale = 20
height = 2*scale
xAxis = 1.0*scale
yAxis = 0.5*scale
wt = 0.4 # "Single Layer"

collarThickness = wt + 0.1 # At wt of 0.4 this one layer
                           # and prusa-slicer shows a gap
                           # between collar and lip.
                           # Adding 0.1 makes it two layers
                           # and there is no gap

braceAngle = 41
braceZoffset = height/2
lenBraceCollar = wt * 6
lenBraceLip = wt * 6
widthBraceLip = 2 * wt

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
    cq.Workplane("XY", origin=(0, 0))
    .ellipse(xAxis-wt, yAxis-wt)
    .extrude(height+wt)
)
log(f'cutter.isValid()={cutter.val().isValid()}')
#show_object(cutter)

# Create a tube using the cutter to hollow it out
ellipticalTube = ellipticalRod.cut(cutter)
log(f'ellipticalTube.isValid()={ellipticalTube.val().isValid()}')
#show_object(ellipticalTube)

# Create a plate for the collar
plate = (
    cq.Workplane("XY", origin=(0, 0, braceZoffset))
    .transformed(
        rotate=(0, braceAngle, 0),
    )
    .rect(60, 25)
    .extrude(collarThickness) # At 0.5 this is two layers, one layer at 0.4 but gaps
)
log(f'plate.val().isValid={plate.val().isValid()}')
#show_object(plate)

# Cut the plate leaving a brace which fits the inside of the tube
brace = plate.cut(ellipticalTube).solids().last()
log(f'brace.isValid()={brace.val().isValid()}')
#show_object(brace)

# brace collar
braceCollarCutter = (
    cq.Workplane("XY", origin=(0, 0))
    .ellipse(xAxis-lenBraceCollar, yAxis-lenBraceCollar)
    .extrude(height)
)
log(f'braceCollarCutter.isValid()={braceCollarCutter.val().isValid()}')
#show_object(braceCollarCutter)
#)
braceCollar = brace.cut(braceCollarCutter)
show_object(braceCollar)

# Brace lip Rod. Initially "braceLipRod=braceCollarCutter" but
# prusa-slicer ended up with a gap between the collar and lip
# So I make the braceLipRod slightly bigger
#braceLipRod = braceCollarCutter
braceLipRod = (
    cq.Workplane("XY", origin=(0, 0))
    #.ellipse(xAxis-lenBraceCollar+(1*wt), yAxis-lenBraceCollar+(1*wt))
    .ellipse(xAxis-lenBraceCollar+0.5, yAxis-lenBraceCollar+0.5)
    .extrude(height)
)
log(f'braceLipRod.isValid()={braceLipRod.val().isValid()}')
#show_object(braceLipRod)

# Brace lip cutter
braceLipCutter = (
    cq.Workplane("XY", origin=(0, 0))
    .ellipse(xAxis-lenBraceCollar-widthBraceLip, yAxis-lenBraceCollar-widthBraceLip)
    .extrude(height)
)
log(f'braceLipCutter.isValid()={braceLipCutter.val().isValid()}')
#show_object(braceLipCutter)

# Brace lib tube
braceLipTube = braceLipRod.cut(braceLipCutter)
log(f'braceLipTube.isValid()={braceLipTube.val().isValid()}')
#show_object(braceLipTube)
#show_object(braceCollar)

## Brace lip Splitters
braceLipTop = (
    braceLipTube
    .faces(">Z")
    .workplane(-height/2)
    .transformed(
        rotate=(0, braceAngle),
    )
    .split(keepTop=True, keepBottom=False)
)
log(f'braceLipTop.isValid()={braceLipTop.val().isValid()}')
#show_object(braceLipTop)

braceLip = (
    braceLipTop
    .faces(">Z")
    .workplane(-height/2 + lenBraceLip)
    .transformed(
        rotate=(0, braceAngle),
    )
    .split(keepTop=False, keepBottom=True)
)
log(f'braceLip.isValid()={braceLip.val().isValid()}')
#show_object(braceLip)

bracedTube = ellipticalTube.union(braceCollar).union(braceLip)
log(f'bracedTube.isValid()={bracedTube.val().isValid()}')
show_object(bracedTube)
