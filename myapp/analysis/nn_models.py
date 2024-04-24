# nn_models.py
import torch
import torch.nn as nn
class CNNModel(nn.Module):
    def __init__(self, input_channels, input_length, num_classes):
        super(CNNModel, self).__init__()
        self.conv1 = nn.Conv1d(input_channels, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool1d(2)
        self.conv2 = nn.Conv1d(64, 128, kernel_size=3, padding=1)
        self.flatten = nn.Flatten()

        # Calculate the correct dimension for the linear layer input
        # Assuming one pooling operation
        correct_dimension = self._get_correct_dimension(input_length)

        self.fc1 = nn.Linear(correct_dimension, 128)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = torch.relu(self.conv2(x))  # Remove the pooling operation here
        x = self.flatten(x)
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

    def _get_correct_dimension(self, input_length):
        # Adjust the calculation based on the revised architecture
        pooled_length = (input_length // 2)  # After first pooling
        final_output_length = pooled_length * 128  # Assuming 128 channels after last conv layer
        return final_output_length

