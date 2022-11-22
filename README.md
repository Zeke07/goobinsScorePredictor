# goobinsScorePredictor

Working set for an ML-based music score generator
Basic Idea:

The plan is to take mp3 files and convert them into sheet music in the MusicXML (readily available) format and perhaps generate a MIDI with that information so we can listen to see if the model is training well.
Once the audio is converted to MusicXML, there is the possibility of visualizing it using Sheet Music or perhaps a modification of the Synthesia format, which would enhance the visual experience by emphasizing nuanced characteristics of the music such as dynamics, rhythm, and tempo
NOTE: Hoping to open source this and consolidate our findings into something like a Python module

We are thinking of web-scraping the data from various online sources (i.e., Musescore’s “OpenScore”, or some other sources from this website): https://www.musicxml.com/music-in-musicxml/)

Overall Plan and Timeframe:
Collect Data - Winter Break prior
Make VM - Winter Break prior
Get Access to HPC - Winter Break prior
Parse/Convert Data - Winter Break prior/during
Train Model - During or After Winter Break
Test Model - During or After Winter Break
Frontend - TBD
Profit (Debt?) - Whenever we’re done.

Potential Frameworks/Dependencies:
Python MusicXML Parser: https://github.com/qsdfo/musicxml_parser, this we plan to use to convert the sheet music into MIDI for testing and for potential use in our loss function (take CS 540 for more information, lo).
Model Training: HPC, disk quota is 100 GB per user! (super-computer used by Skunkworks) - https://chtc.cs.wisc.edu/uw-research-computing/hpc-overview.html 
Some sort of virtual machine to store the data and model temporarily, and potentially for us to host the model if we plan to make a website for it. In regards to storing the data for the music and such, we can use an Amazon EC2 instance or a GCP instance to store the data. We can’t use the free tiers for either of these because we’ll have too much data, so if you haven’t registered your $300 credit for GCP, please tell Ankit!
Not sure about what ML framework or type of Neural Network to use, Ankit plans to talk with Sala about this for help.
ReactJS for Frontend

Type of Data (Space Constraints):
Our input data is going to be mp3 most likely (I wanted to use .wav, but most sources provided mp3 and this might act as our dimensionality reduction anyway since it's compressed).
Higher-end mp3 data is roughly 2MB per minute of footage, we estimate that the average piano miniature in the dataset is 5 minutes, so roughly 10MB per feature.  For approximately 1,000 features, we project 10GB of storage requirements → Standard Persistent Disk for free-tier GCP VM is 10 GB, so we can upgrade to 50GB to be safe
Audio must correspond to the sheet music that we are training on since disparities between sheet and audio will create problems (MuseScore is pretty good for this).  Essentially, the timing of the audio must correspond to the data that MusicXML gives us (for instance, the ‘pianoroll’ function in the git library captures the frame count that a note is played for, so lining these up in a strict manner is quite feasible)
Output data is going to JUST be the MusicXML data, unless Sala tells me something else. Each time we would like to measure how good the network is, we can generate a MIDI using the git library above (musicXML to piano roll) to listen to it to more easily gauge how it's doing. This will not be done on every iteration because that would use a lot of space.
Example of musicXML data encoding: https://www.musicxml.com/publications/makemusic-recordare/notation-and-analysis/a-sample-musicxml-encoding/ 

Future Plans:
If all goes well and the model is good or bad (I don’t really care for it to be 100% accurate), hopefully, we can create a simple website to allow people to upload mp3 files and we can return the musicXML or sheet music to them. No details about this are set in stone, but I plan for our frontend to be React.js with an EC2 instance to store the mp3 file temporarily and generate the XML file with our model weights. This is not set in stone, so if you have suggestions on the backend or frontend when we get to this point, tell Ankit or Zayn (except please no Angular.js). 


Meeting Notes (SALA, 10-20-2022):


We need a sequence-to-sequence Model. Should be using an uncompressed format.
Audio to continuous sequence model (sequence to sequence model, use some public repo maybe?)
We should convert the audio into a sequence, then feed it into our model. 
Flatten the XML format (in other words, flatten a tree)
Use a pre-defined Loss Function 
First focus on designing “Fake” data that uses randomly generated note sequences with XML we already have before trying to use an actual song.
Hugging Face Sequence to Sequence Model (Google This)!
Encoding, Data Loaders, Training Loop, then run. (Pytorch tutorial)
Maybe try initially with MIDI
