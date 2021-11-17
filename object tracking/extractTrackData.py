import pandas as pd
import numpy as np
import bpy
import os

D = bpy.data

"""
Export track x,y coordinates created from a 2D object tracking
Creates a dataframe containing all tracks within the movieclips object
"""

outputFolder= "<path>"
testName = 'test'

for clip in D.movieclips:
    # get clips from movieclips
    print(f'Clip Duration: {clip.frame_duration}')
    # create empty dataframe to fill with track coordinates
    df = pd.DataFrame.from_dict({'frame': list(range(0, clip.frame_duration))})
    
    print('')
    for ob in clip.tracking.objects:
        print(f'Processing object {ob.name}')
        trackNum = 1
        for track in ob.tracks:
            print(f'Processing track {trackNum}: {track.name}')          
            for frame in list(range(0, clip.frame_duration)):
                marker = track.markers.find_frame(frame)
                if marker:
                    coords = marker.co.xy
                    df.loc[frame, f'{ob.name} Track {trackNum} x'] = coords[0]
                    df.loc[frame, f'{ob.name} Track {trackNum} y'] = coords[1]

                else:
                    continue
                
            del marker
            trackNum += 1 

# save
df = df.replace('', np.nan)
df = df.dropna()
df.to_csv(os.path.join(outputFolder, f'{testName}.csv'), index=False)
