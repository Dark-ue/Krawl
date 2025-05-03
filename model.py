import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
import torchvision.datasets as datasets
from torch.utils.data import DataLoader
import os

# CONFIG
BATCH_SIZE = 128
EPOCHS = 100
PATIENCE = 10
LR = 1e-3
MODEL_PATH = "alphabet_model.pth"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Data Augmentation & Normalization
transform = transforms.Compose([
    transforms.RandomAffine(degrees=15, translate=(0.1, 0.1), scale=(0.9, 1.1)),
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

# Load EMNIST Dataset (balanced split)
train_set = datasets.EMNIST(root="data", split="balanced", train=True, download=True, transform=transform)
test_set = datasets.EMNIST(root="data", split="balanced", train=False, download=True, transform=transform)
train_loader = DataLoader(train_set, batch_size=BATCH_SIZE, shuffle=True)
test_loader = DataLoader(test_set, batch_size=BATCH_SIZE)

NUM_CLASSES = len(train_set.classes)

#  Residual-style CNN
class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.skip = nn.Conv2d(in_channels, out_channels, 1) if in_channels != out_channels else nn.Identity()

    def forward(self, x):
        identity = self.skip(x)
        out = self.bn1(self.conv1(x))
        out = self.bn2(self.conv2(torch.relu(out)))
        return torch.relu(out + identity)

class EMNISTModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            ResidualBlock(32, 64),
            nn.MaxPool2d(2),
            ResidualBlock(64, 128),
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Linear(128, NUM_CLASSES)
        )

    def forward(self, x):
        return self.net(x)

#  Training loop

def train(model, optimizer, criterion):
    model.train()
    total_loss = 0
    total_images = len(train_loader.dataset)
    images_seen = 0

    for i, (inputs, labels) in enumerate(train_loader):
        inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

        #  Count images
        images_seen += inputs.size(0)
        percent = images_seen / total_images * 100

        print(f"\r{images_seen}/{total_images} images processed ({percent:.2f}%)", end='')

    print()
    return total_loss / len(train_loader)


#  Evaluation
def evaluate(model, loader):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, labels in loader:
            inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    return correct / total

#  Full Training Script with Early Stopping
def train_until_perfection():
    model = EMNISTModel().to(DEVICE)
    optimizer = optim.AdamW(model.parameters(), lr=LR)
    criterion = nn.CrossEntropyLoss()

    best_acc = 0
    patience_counter = 0

    for epoch in range(EPOCHS):
        loss = train(model, optimizer, criterion)
        acc = evaluate(model, test_loader)

        print(f"Epoch {epoch+1}: Loss={loss:.4f}, Accuracy={acc*100:.2f}%")

        if acc > best_acc:
            best_acc = acc
            torch.save(model.state_dict(), MODEL_PATH)
            patience_counter = 0
            print(" New best model saved!")
        else:
            patience_counter += 1
            if patience_counter >= PATIENCE:
                print(" Early stopping triggered.")
                break

    print(f"Best Accuracy: {best_acc*100:.2f}%")

if __name__ == "__main__":
    train_until_perfection()
