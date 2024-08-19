# OptiVisionNet/model.py

import torch
import torch.nn as nn

class CNN_BiLSTM_MLP(nn.Module):
    def __init__(self, input_channels, lstm_hidden_size, lstm_layers, output_size):
        super(CNN_BiLSTM_MLP, self).__init__()
        self.cnn = nn.Sequential(
            nn.Conv2d(input_channels, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(32),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(64),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Dropout(0.25)
        )
        self.lstm = nn.LSTM(64 * 8 * 8, lstm_hidden_size, lstm_layers, batch_first=True, bidirectional=True, dropout=0.5)
        self.mlp = nn.Sequential(
            nn.Linear(lstm_hidden_size * 2, 256),
            nn.ReLU(),
            nn.BatchNorm1d(256),
            nn.Dropout(0.5),
            nn.Linear(256, output_size)
        )

    def forward(self, x):
        x = self.cnn(x)
        x = x.view(x.size(0), -1)
        x = x.unsqueeze(1)  
        x, _ = self.lstm(x)
        x = x[:, -1, :]  # Take the output of the last time step
        x = self.mlp(x)
        return x
