# docker-handbrake-cli
Docker container based upon Ubuntu 14.04 with Python 3.4 and the latest HandbrakeCLI from apt repository whose purpose si to post-process MKV videos and store them to my NAS automatically.

I plan to add some common settings files, scripts, etc. that I use to automatically post-process videos in my environment.

Enjoy!

# Building Docker Image
```
# Full Build (with Latest Handbrake)
docker build --no-cache=true -t redwolf3/handbrake-cli:latest .

# Dev Build (with last built version of Handbrake)
docker build -t redwolf3/handbrake-cli:latest .

# Push to Repository
docker push redwolf3/handbrake-cli:latest
```

# Running Docker Image (REAL)
```
docker run -it --rm -v /Volumes/Videos/MKV_Ripping:/input -v /Volumes/Videos:/output redwolf3/handbrake-cli:latest
```

# Running Docker Image (TEST)
```
docker run -it --rm -v /Volumes/Videos/MKV_Ripping:/input -v /Volumes/Videos/HandrakeTest:/output redwolf3/handbrake-cli:latest
```

# Running Docker Image (DEBUG)
```
docker run -it --rm redwolf3/handbrake-cli:latest python3 handbrake-proc.py DEBUG
```

# Credits

## Encoding Settings
This project includes some custom HandbrakeCLI presets which I use for encoding various video formats. These settings were based upon recommendations from (http://www.rokoding.com/ "ROKODING"). Check them out!

## Sample Video Files
This project includes a handful of MKV files enccoded at different bitrates which you can use to test this docker container. These videos were obtained from (http://www.jell.yfish.us/ "Jellyfish Bitrate Test Files"). They have example files in lots of other formats and bitrates, included some Ultra 4K files.
