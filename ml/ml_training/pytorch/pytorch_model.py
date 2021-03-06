import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

"""code is built from video tutorial mentioned in reference mat links file"""


class Linear_QNet(nn.Module):
    # we want to configure our model params here
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        # for tetris we should experiment with more layers here
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, hidden_size)
        self.linear3 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        # here x is our tensor, relu activation is good for this case with feed forward structure
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name='pytorch_model.pth'):
        # saves our model in specified folder, if it doesn't exist we create it
        model_folder_path = './models'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

class DeepQNetwork(nn.Module):
    """slightly modified from github project by uvipen"""
    def __init__(self, input_size, hidden_size, output_size):
        super(DeepQNetwork, self).__init__()
        self.conv1 = nn.Sequential(nn.Linear(input_size, hidden_size), nn.ReLU(inplace=True))
        self.conv2 = nn.Sequential(nn.Linear(hidden_size, hidden_size), nn.ReLU(inplace=True))
        self.conv3 = nn.Sequential(nn.Linear(hidden_size, output_size))

        self._create_weights()

    def _create_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                nn.init.constant_(m.bias, 0)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        return x

    def save(self, file_name='pytorch_model.pth'):
            # saves our model in specified folder, if it doesn't exist we create it
            model_folder_path = './models'
            if not os.path.exists(model_folder_path):
                os.makedirs(model_folder_path)

            file_name = os.path.join(model_folder_path, file_name)
            torch.save(self.state_dict(), file_name)
 

class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        # (n, x)

        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # 1: predicted Q values with current state
        pred = self.model(state)

        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(action[idx]).item()] = Q_new
    
        # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
        # pred.clone()
        # preds[argmax(action)] = Q_new
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()