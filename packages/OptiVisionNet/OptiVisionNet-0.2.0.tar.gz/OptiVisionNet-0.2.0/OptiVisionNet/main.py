from OptiVisionNet.model import CNN_BiLSTM_MLP
from OptiVisionNet.utils import train_cnn_bilstm, evaluate_model
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import torch.optim as optim
import torch.nn as nn

# Data preparation
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

train_data = datasets.CIFAR10(root="data", train=True, download=True, transform=transform)
test_data = datasets.CIFAR10(root="data", train=False, download=True, transform=transform)

train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=64, shuffle=False)

# Initialize model
model = CNN_BiLSTM_MLP(input_channels=3, lstm_hidden_size=128, lstm_layers=2, output_size=10)

# Train CNN + BiLSTM
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
train_cnn_bilstm(model, train_loader, criterion, optimizer, epochs=5)

# Evaluate the model
accuracy, f1 = evaluate_model(model, test_loader)
print(f"Test Accuracy: {accuracy:.2f}%")
print(f"Test F1 Score: {f1:.2f}")
