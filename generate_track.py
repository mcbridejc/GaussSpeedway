"""KiCad plugin to generate linear stepper track traces in KiCad"""


import pcbnew
import curvycad as cc
import os

WIDTH=10.0
PITCH=4.0
WIDTH_MARGIN = 1.2
LINE_WIDTH = 0.3
VIA_DRILL = 0.3
VIA_PAD = 0.6
GUIDE_RAIL_WIDTH = 1.25
GUIDE_RAIL_SPACE = 6 + GUIDE_RAIL_WIDTH
CU_CLEARANCE = 0.2
OUTER_MARKING_WIDTH = 2.0

# def pcbpoint(p):
#     return pcbnew.wxPointMM(float(p[0]), float(p[1]))

# Define a single cycle of a periodic pattern which is projected along the
# path. Points along the track are normalized to the range (0, 1), and they are
# expanded based on the computed pitch later. 
# Transverse distances -- positions left and right of the track are absolute and
# in millimeters. 
# This definition defines two tracks, one on the left of the centerline and one
# on the right. Each track has two guard rails on the bottom layer, and two 
# alternating drive phases.
TRACK_CENTER = 0.0
TRACK_MINOR = WIDTH / 2
TRACK_MAJOR = WIDTH / 2 + VIA_PAD / 2 + CU_CLEARANCE + LINE_WIDTH / 2
segment = [
    
    # Silkscreen
    cc.ParallelLine(0.0, 1.0, TRACK_CENTER + TRACK_MAJOR + OUTER_MARKING_WIDTH / 2, OUTER_MARKING_WIDTH, pcbnew.F_SilkS),
    cc.ParallelLine(0.0, 1.0, -(TRACK_CENTER + TRACK_MAJOR + OUTER_MARKING_WIDTH / 2), OUTER_MARKING_WIDTH, pcbnew.F_SilkS),
    #cc.ParallelLine(0.25, 0.75, 0.0, LANE_SEPARATOR_WIDTH, pcbnew.F_SilkS),

    # Guard rails
    cc.ParallelLine(0.0, 1.0, -GUIDE_RAIL_SPACE / 2, GUIDE_RAIL_WIDTH, pcbnew.F_Cu),
    cc.ParallelLine(0.0, 1.0, GUIDE_RAIL_SPACE / 2, GUIDE_RAIL_WIDTH, pcbnew.F_Cu),
    
    # Track 1 Phase A
    cc.TransverseLine(
        start=-(TRACK_CENTER - TRACK_MINOR),
        end=-(TRACK_CENTER + TRACK_MAJOR),
        offset=0,
        width=LINE_WIDTH,
        layer=pcbnew.In1_Cu,
    ),
    cc.ParallelLine(
        start=0,
        end=0.5,
        offset=-(TRACK_CENTER + TRACK_MAJOR),
        width=LINE_WIDTH,
        layer=pcbnew.In1_Cu,
    ),
    cc.TransverseLine(
        start=-(TRACK_CENTER + TRACK_MAJOR),
        end=-(TRACK_CENTER - TRACK_MINOR),
        offset=0.5,
        width=LINE_WIDTH,
        layer=pcbnew.In1_Cu,
    ),
    cc.Via(0.5, -(TRACK_CENTER - TRACK_MINOR)),
    cc.ParallelLine(
        start=0.5, 
        end=1.0,
        offset=-(TRACK_CENTER - TRACK_MINOR),
        width=LINE_WIDTH,
        layer=pcbnew.In2_Cu,
    ),
    cc.Via(1.0, -(TRACK_CENTER - TRACK_MINOR)),
    
    # Track 1 Phase B
    cc.ParallelLine(
        start=0.0, 
        end=0.25,
        offset=-(TRACK_CENTER - TRACK_MAJOR),
        width=LINE_WIDTH,
        layer=pcbnew.In1_Cu,
    ),
    cc.TransverseLine(
        start=-(TRACK_CENTER - TRACK_MAJOR),
        end=-(TRACK_CENTER + TRACK_MINOR),
        offset=0.25,
        width=LINE_WIDTH,
        layer=pcbnew.In1_Cu,
    ),
    cc.Via(0.25, -(TRACK_CENTER + TRACK_MINOR)),
    cc.ParallelLine(
        start=0.25,
        end=0.75,
        offset=-(TRACK_CENTER + TRACK_MINOR),
        width=LINE_WIDTH,
        layer=pcbnew.In2_Cu,
    ),
    cc.Via(0.75, -(TRACK_CENTER + TRACK_MINOR)),
    cc.TransverseLine(
        start=-(TRACK_CENTER + TRACK_MINOR),
        end=-(TRACK_CENTER - TRACK_MAJOR),
        offset=0.75,
        width=LINE_WIDTH,
        layer=pcbnew.In1_Cu,
    ),
    cc.ParallelLine(
        start=0.75, 
        end=1.00,
        offset=-(TRACK_CENTER - TRACK_MAJOR),
        width=LINE_WIDTH,
        layer=pcbnew.In1_Cu,
    ),
]

class TrackLayout(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Layout two-lane race track"
        self.category = "Modify PCB"
        self.description = "Layout two-lane race track"
        self.show_toolbar_button = True

    def Run(self):
        board = pcbnew.GetBoard()
        projdir = os.path.dirname(os.path.abspath(board.GetFileName()))
        guide = cc.read_dxf(os.path.join(projdir, 'track.dxf'))
        for el in guide:
            print(el)
        track = cc.KicadTrackBuilder(PITCH, segment, board)
        track.draw_path(guide)
   

TrackLayout().register()
