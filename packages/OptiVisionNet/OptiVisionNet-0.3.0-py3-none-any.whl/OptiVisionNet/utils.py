import torch
import torch.optim as optim
from tqdm import tqdm
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt

def train_cnn_bilstm(model, train_loader, criterion, optimizer, epochs):
    model.train()
    train_losses = []
    train_accuracies = []
    train_f1_scores = []

    for epoch in range(epochs):
        running_loss = 0.0
        correct = 0
        total = 0
        all_labels = []
        all_predictions = []
        
        for images, labels in tqdm(train_loader, desc=f'Epoch {epoch+1}/{epochs}'):
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

            # Collect predictions and labels for accuracy and F1 score calculation
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            all_labels.extend(labels.cpu().numpy())
            all_predictions.extend(predicted.cpu().numpy())

        avg_loss = running_loss / len(train_loader)
        accuracy = 100 * correct / total
        avg_f1 = f1_score(all_labels, all_predictions, average='weighted')

        train_losses.append(avg_loss)
        train_accuracies.append(accuracy)
        train_f1_scores.append(avg_f1)

        print(f'Epoch [{epoch+1}/{epochs}], Loss: {avg_loss:.4f}, Accuracy: {accuracy:.2f}%, F1 Score: {avg_f1:.4f}')
    
    plot_learning_curves(train_losses, train_accuracies, train_f1_scores)

def evaluate_model(model, test_loader):
    model.eval()
    correct = 0
    total = 0
    all_labels = []
    all_predictions = []
    
    with torch.no_grad():
        for images, labels in test_loader:
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

            # Collect predictions and labels for F1 score calculation
            all_labels.extend(labels.cpu().numpy())
            all_predictions.extend(predicted.cpu().numpy())

    accuracy = 100 * correct / total
    f1 = f1_score(all_labels, all_predictions, average='weighted')
    return accuracy, f1

def plot_learning_curves(losses, accuracies, f1_scores):
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 3, 1)
    plt.plot(losses, label='Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Training Loss')
    plt.legend()
    
    plt.subplot(1, 3, 2)
    plt.plot(accuracies, label='Accuracy', color='g')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy (%)')
    plt.title('Training Accuracy')
    plt.legend()
    
    plt.subplot(1, 3, 3)
    plt.plot(f1_scores, label='F1 Score', color='r')
    plt.xlabel('Epochs')
    plt.ylabel('F1 Score')
    plt.title('Training F1 Score')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
