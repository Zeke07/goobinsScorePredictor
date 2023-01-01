import os
import torch
import torch.nn as nn
import torchaudio as ta


class GoobinsNN(nn.Module):
    def __init__(self, training_wav_fp, training_text_fp, hidden_size):
        super(GoobinsNN, self).__init__()
        self.training_wav = []
        self.training_text = []

        for file in os.listdir(training_wav_fp):
            f = os.path.join(training_wav_fp, file)
            if os.path.isfile(f):
                try:
                    self.training_wav.append(ta.load(f))
                except:
                    pass

        for file in os.listdir(training_text_fp):
            f = os.path.join(training_text_fp, file)
            if os.path.isfile(f):
                self.training_text.append(f)

        # Model structure
        self.hidden_size = hidden_size




def main():
    nn = GoobinsNN("wav_data", "text_data", 1)
    print(nn.training_wav)



if __name__ == "__main__":
    main()