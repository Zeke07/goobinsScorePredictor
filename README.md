# goobinsScorePredictor Proposal!
Working set for an ML-based music score generator

## Basic Idea:
The plan is to take mp3 files and convert them into sheet music in the MusicXML format (readily available) and perhaps generate a MIDI with that information so we can listen to see if the model is training well.
Once the audio is converted to MusicXML, there is the possibility of visualizing it using Sheet Music or perhaps a modification of the Synthesia format, which would enhance the visual experience by emphasizing nuanced characteristics of the music such as dynamics, rhythm, and tempo
NOTE: Hoping to open source this and consolidate our findings into something like a Python module

We are thinking of web-scraping the data from various online sources (i.e., Musescore’s “OpenScore”, or some other sources from this website): https://www.musicxml.com/music-in-musicxml/)

## Overall Plan and Timeframe:
- Collect Data - Winter Break prior
- Make VM - Winter Break prior
- Get Access to HPC - Winter Break prior
- Parse/Convert Data - Winter Break prior/during
- Train Model - During or After Winter Break
- Test Model - During or After Winter Break
- Frontend - TBD
- Profit (Debt?) - Whenever we’re done.

## Potential Frameworks/Dependencies:
Python MusicXML Parser: https://github.com/qsdfo/musicxml_parser, this we plan to use to convert the sheet music into MIDI for testing and for potential use in our loss function (take CS 540 for more information, lo).
Model Training: HPC, disk quota is 100 GB per user! (super-computer used by Skunkworks) - https://chtc.cs.wisc.edu/uw-research-computing/hpc-overview.html 
Some sort of virtual machine to store the data and model temporarily, and potentially for us to host the model if we plan to make a website for it. In regards to storing the data for the music and such, we can use an Amazon EC2 instance or a GCP instance to store the data.

We plan to use a Sequence to Sequence Network for this project, as recommended by our professor. We might look into using a Convolutional Neural Network for this, but this is less likely.

## Type of Data (Space Constraints):
Our input data is going to be WAV, and the model will output MIDI for testing the veracity of the model.
WAV data is roughly 10MB per minute of footage, we estimate that the average piano miniature in the dataset is 5 minutes, so roughly 50MB per feature.  For approximately 1,000 features, we project 50GB of storage requirements, but this will likely increase.

Audio must correspond to the sheet music that we are training on since disparities between sheet and audio will create problems (MuseScore is pretty good for this).  Essentially, the timing of the audio must correspond to the data that MusicXML gives us (for instance, the ‘pianoroll’ function in the git library captures the frame count that a note is played for, so lining these up in a strict manner is quite feasible).

The audio itself must be converted into a sequence (notes and other parameters) to feed into the model, we plan to reference the Hugging Face Sequence to Sequence model for reference. The training data initially will be "fake" data to train the model on specific aspects of music rather than trying to do it all at once. So, we plan to first design a tool to generate fake note data for the model to train on before trying to add more complexity such as dynamics, accidentals, etc.

Output data is going to JUST be the MusicXML data, and will be flattened to make analysis easier. Each time we would like to measure how good the network is, we can generate a MIDI using the git library above (musicXML to piano roll) to listen to it to more easily gauge how it's doing. This will not be done on every iteration because that would use a lot of space. We plan to use either a predefined loss function, or make our own.
Example of musicXML data encoding: https://www.musicxml.com/publications/makemusic-recordare/notation-and-analysis/a-sample-musicxml-encoding/ 

## Future Plans:
If all goes well and the model is good or bad (We don’t really expect for it to be 100% accurate), hopefully, we can create a simple website to allow people to upload WAV files and we can return the musicXML or sheet music to them. No details about this are set in stone, but I plan for our frontend to be React.js with an EC2 instance to store the mp3 file temporarily and generate the XML file with our model weights. 
