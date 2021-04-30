
# record voice
cd /home/pi/IntelligenceHomeSys/SoundFunction
sudo arecord -D hw:2,0 -d 5 -f cd -r 44100 -c 1 -t wav voice/test.wav

# play voice
# sudo arecord -D hw:2,0 -d 10 -f S16_LE -r 44100 -c 1 -t wav test.wav

# tansform
ffmpeg -y -i voice/test.wav -acodec pcm_s16le -f s16le -ac 1 -ar 16000 voice/test.pcm

# upload and recognition
python3 /home/pi/IntelligenceHomeSys/SoundFunction/srs_Recognition_speed.py
