"""
Export track x,y coordinates created from a 2D object tracking
Creates a dataframe containing all tracks within the movieclips object
coordinates are % of image width / height
to get in units of length, multiply x-coordinates by image width in length units (meters)
and y-coordinates by image height in length units
"""

outputFolder= '<path>'
testName = 'test'

for clip in D.movieclips:
    # get clips from movieclips
    print(f'Clip Duration: {clip.frame_duration}')
    # create empty dataframe to fill with track coordinates
    df = pd.DataFrame.from_dict({'frame': list(range(0, clip.frame_duration))})

    print('')
    for ob in clip.tracking.objects:
        print(f'Processing object {ob.name}')
        if ob.name == 'Camera':
            continue
        trackNum = 1
        for track in ob.tracks:
            print(f'Processing track {trackNum}: {track.name}')
            for index, row in df.iterrows():
                marker = track.markers.find_frame(row.frame)
                if marker:
                    coords = marker.co.xy
                    df.loc[index, f'{ob.name} Track {trackNum} x'] = coords[0]
                    df.loc[index, f'{ob.name} Track {trackNum} y'] = coords[1]

                else:
                    continue
                
            del marker
            trackNum += 1 

# save
#df = df.replace('', np.nan)
#df = df.dropna()
df.to_csv(os.path.join(outputFolder, f'{testName}_{clipCount}.csv'), index=False)

# create file with info
info = pd.DataFrame.from_records({'pixel_width': D.movieclips[0].size[0],
                               'pixel_height': D.movieclips[0].size[1]}, index=[0])

info.to_csv(os.path.join(outputFolder, f'{testName}_{clipCount}_info.csv'), index=False)