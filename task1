import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt

 transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))   
])

print("Downloading MNIST dataset...")

train_dataset = torchvision.datasets.MNIST(
    root='./data', train=True, download=True, transform=transform
)
test_dataset = torchvision.datasets.MNIST(
    root='./data', train=False, download=True, transform=transform
)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader  = DataLoader(test_dataset,  batch_size=64, shuffle=False)

print(f"Training samples : {len(train_dataset)}")
print(f"Testing  samples : {len(test_dataset)}")


def show_samples(dataset, n=10):
    """Display the first n sample images with their labels."""
    fig, axes = plt.subplots(1, n, figsize=(15, 2))
    fig.suptitle("MNIST Sample Images (digits 0-9)", fontsize=14)
    for i in range(n):
        image, label = dataset[i]
        axes[i].imshow(image.squeeze(), cmap='gray')
        axes[i].set_title(f"Label: {label}")
        axes[i].axis('off')
    plt.tight_layout()
    plt.savefig("mnist_samples.png")
    plt.show()
    print("Sample image saved to mnist_samples.png")

show_samples(train_dataset)


class DigitClassifier(nn.Module):
    """
    A simple fully-connected neural network for digit classification.
    Architecture: 784 → 256 → 128 → 10
    """
    def __init__(self):
        super(DigitClassifier, self).__init__()
        self.network = nn.Sequential(
            nn.Flatten(),               
            nn.Linear(784, 256),        
            nn.ReLU(),
            nn.Dropout(0.2),           
            nn.Linear(256, 128),       
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 10)          
        )

    def forward(self, x):
        return self.network(x)



def train(model, loader, criterion, optimiser, epoch):
    """Train the model for one epoch and return average loss."""
    model.train()
    total_loss = 0
    for batch_idx, (images, labels) in enumerate(loader):
        optimiser.zero_grad()           # Clear previous gradients
        outputs = model(images)         # Forward pass
        loss = criterion(outputs, labels)
        loss.backward()                 # Backpropagation
        optimiser.step()                # Update weights
        total_loss += loss.item()

    avg_loss = total_loss / len(loader)
    print(f"Epoch {epoch:2d} | Training Loss: {avg_loss:.4f}")
    return avg_loss


def evaluate(model, loader):
    """Evaluate the model on a dataset and return accuracy (%)."""
    model.eval()
    correct = 0
    total   = 0
    with torch.no_grad():               # No gradient needed during evaluation
        for images, labels in loader:
            outputs    = model(images)
            _, predicted = torch.max(outputs, 1)
            total   += labels.size(0)
            correct += (predicted == labels).sum().item()
    accuracy = 100 * correct / total
    return accuracy


EPOCHS       = 5
LEARNING_RATE = 0.001

model     = DigitClassifier()
criterion = nn.CrossEntropyLoss()         
optimiser = optim.Adam(model.parameters(), lr=LEARNING_RATE)

print("\nTraining the digit classifier...")
print("-" * 40)

loss_history = []
for epoch in range(1, EPOCHS + 1):
    avg_loss = train(model, train_loader, criterion, optimiser, epoch)
    loss_history.append(avg_loss)
    acc = evaluate(model, test_loader)
    print(f"         Test  Accuracy : {acc:.2f}%\n")

print("-" * 40)
final_acc = evaluate(model, test_loader)
print(f"Final Test Accuracy: {final_acc:.2f}%")


plt.figure(figsize=(7, 4))
plt.plot(range(1, EPOCHS + 1), loss_history, marker='o', color='steelblue')
plt.title("Training Loss over Epochs")
plt.xlabel("Epoch")
plt.ylabel("Average Loss")
plt.grid(True)
plt.tight_layout()
plt.savefig("mnist_training_loss.png")
plt.show()
print("Training loss plot saved to mnist_training_loss.png")


def predict_samples(model, dataset, n=10):
    """Show predictions for the first n test images."""
    model.eval()
    fig, axes = plt.subplots(1, n, figsize=(15, 2))
    fig.suptitle("Model Predictions vs True Labels", fontsize=13)
    with torch.no_grad():
        for i in range(n):
            image, true_label = dataset[i]
            output    = model(image.unsqueeze(0))     
            _, predicted = torch.max(output, 1)
            pred_label = predicted.item()
            colour = 'green' if pred_label == true_label else 'red'
            axes[i].imshow(image.squeeze(), cmap='gray')
            axes[i].set_title(f"P:{pred_label}\nT:{true_label}", color=colour, fontsize=9)
            axes[i].axis('off')
    plt.tight_layout()
    plt.savefig("mnist_predictions.png")
    plt.show()
    print("Prediction image saved to mnist_predictions.png")

predict_samples(model, test_dataset)
