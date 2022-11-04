import KicadModTree as kmt

# Total length of the linear input
LENGTH = 40.0 # mm
# The size of the flat on the point of each tooth
POINT_FLAT = 0.3 # mm
# The width of the solid (non interlaced) part of each segment
SOLID_SIZE = 3.2 # mm
# Space between interleaved electrodes
ELECTRODE_GAP = 0.25
# Tangential pitch of the teeth
TOOTH_PITCH = 4.8
NUM_TEETH = 3

HEIGHT = NUM_TEETH * TOOTH_PITCH
SEGMENT_LENGTH = LENGTH / 3

def make_right_side(x_offset): 
    pts = []
    # origin is the center of the solid band
    x_minor = x_offset + SOLID_SIZE / 2 
    x_major = x_offset + SEGMENT_LENGTH - SOLID_SIZE / 2 - ELECTRODE_GAP
    
    clearance_flat = POINT_FLAT + ELECTRODE_GAP * 2

    y = -HEIGHT / 2
    pts.append([x_offset, y])
    pts.append([x_major, y])
    pts.append([x_major, y + POINT_FLAT / 2])

    for n in range(NUM_TEETH):
        y += TOOTH_PITCH / 2
        pts.append([x_minor, y - clearance_flat / 2])
        pts.append([x_minor, y + clearance_flat / 2])
        y += TOOTH_PITCH / 2
        pts.append([x_major, y - POINT_FLAT / 2])
        # Halfway on last point on last tooth
        if n < NUM_TEETH - 1:
            pts.append([x_major, y + POINT_FLAT / 2])
        else:
            pts.append([x_major, y])
        
    pts.append([x_offset, y])
    return pts

def make_left_side(x_offset):
    pts = []
    # origin is the center of the solid band
    x_minor = x_offset - SOLID_SIZE / 2
    x_major = x_offset - SEGMENT_LENGTH + SOLID_SIZE / 2 + ELECTRODE_GAP
    
    clearance_flat = POINT_FLAT + ELECTRODE_GAP * 2
    y = HEIGHT / 2
    pts.append([x_offset, y])
    pts.append([x_minor, y])
    pts.append([x_minor, y - clearance_flat / 2])
    
    for n in range(NUM_TEETH):
        y -= TOOTH_PITCH / 2
        pts.append([x_major, y + POINT_FLAT / 2])
        pts.append([x_major, y - POINT_FLAT / 2])
        y -= TOOTH_PITCH / 2
        pts.append([x_minor, y + clearance_flat / 2])
        if n < NUM_TEETH - 1:
            pts.append([x_minor, y - clearance_flat / 2])
        else:
            pts.append([x_minor, y])
    
    pts.append([x_offset, y])
    return pts

def make_combined(x_offset):
    right = make_right_side(x_offset)
    left = make_left_side(x_offset)

    # Remove the duplicate points
    right = right[0:-1]
    left = left[0:-1]

    return right + left

polygons = [
    make_right_side(0.0),
    make_combined(0.0),
    make_combined(0.0),
    make_left_side(0.0)
]

positions = [
    0.0,
    SEGMENT_LENGTH * 1,
    SEGMENT_LENGTH * 2,
    SEGMENT_LENGTH * 3,
]

pad_centers = [
    0.0,
    0.0,
    0.0,
    -0.0,
]

footprint_name = f'linear_touch_{LENGTH}mm'

mod = kmt.Footprint(footprint_name)
mod.setDescription('An interlaced touch sensitive linear slider')

for i, p in enumerate(polygons):
    poly = kmt.Polygon(nodes=p, layer='F.Cu', width = 0.0001)
    pad = kmt.Pad(
        number=i+1,
        type=kmt.Pad.TYPE_SMT,
        shape=kmt.Pad.SHAPE_CUSTOM,
        at=[positions[i], 0],
        size=0.1,
        layers=["F.Cu"],
        primitives=[poly],
    )
    mod.append(pad)

file_handler = kmt.KicadFileHandler(mod)
file_handler.writeFile(footprint_name + '.kicad_mod')