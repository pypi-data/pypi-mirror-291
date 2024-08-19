import torch
import matplotlib.pyplot as plt

class GreyWolfOptimizer:
    def __init__(self, num_agents, max_iter, model, train_loader):
        self.num_agents = num_agents
        self.max_iter = max_iter
        self.model = model
        self.train_loader = train_loader
        self.best_solution = None
        self.best_fitness = float('inf')
        self.alpha_pos = None
        self.beta_pos = None
        self.delta_pos = None
        self.alpha_score = float('inf')
        self.beta_score = float('inf')
        self.delta_score = float('inf')
        self.fitness_history = []

    def fitness(self, weights):
        with torch.no_grad():
            index = 0
            for param in self.model.parameters():
                num_params = param.numel()
                param.data.copy_(weights[index:index + num_params].view(param.size()))
                index += num_params
        
        criterion = torch.nn.CrossEntropyLoss()
        self.model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        for images, labels in self.train_loader:
            outputs = self.model(images)
            loss = criterion(outputs, labels)
            running_loss += loss.item()

            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        
        avg_loss = running_loss / len(self.train_loader)
        accuracy = 100 * correct / total
        fitness = avg_loss  # Use loss as fitness value
        return fitness, accuracy

    def optimize(self):
        num_params = sum(p.numel() for p in self.model.parameters())
        positions = [torch.randn(num_params) for _ in range(self.num_agents)]
        
        self.alpha_pos = positions[0]
        self.beta_pos = positions[1]
        self.delta_pos = positions[2]
        self.alpha_score, _ = self.fitness(self.alpha_pos)
        self.beta_score, _ = self.fitness(self.beta_pos)
        self.delta_score, _ = self.fitness(self.delta_pos)
        
        for t in range(self.max_iter):
            for i in range(self.num_agents):
                fitness, accuracy = self.fitness(positions[i])
                
                if fitness < self.alpha_score:
                    self.delta_score = self.beta_score
                    self.beta_score = self.alpha_score
                    self.alpha_score = fitness
                    self.delta_pos = self.beta_pos
                    self.beta_pos = self.alpha_pos
                    self.alpha_pos = positions[i]
                elif fitness < self.beta_score:
                    self.delta_score = self.beta_score
                    self.beta_score = fitness
                    self.delta_pos = positions[i]
                elif fitness < self.delta_score:
                    self.delta_score = fitness
                    self.delta_pos = positions[i]
            
            self.fitness_history.append(self.alpha_score)
            
            a = 2 - t * (2 / self.max_iter)
            for i in range(self.num_agents):
                r1 = torch.rand(num_params)
                r2 = torch.rand(num_params)
                A = 2 * a * r1 - a
                C = 2 * r2
                D_alpha = torch.abs(C * self.alpha_pos - positions[i])
                D_beta = torch.abs(C * self.beta_pos - positions[i])
                D_delta = torch.abs(C * self.delta_pos - positions[i])
                X1 = self.alpha_pos - A * D_alpha
                X2 = self.beta_pos - A * D_beta
                X3 = self.delta_pos - A * D_delta
                positions[i] = (X1 + X2 + X3) / 3
            
            print(f"Iteration {t+1}/{self.max_iter} - Best Fitness: {self.alpha_score:.4f}, Best Accuracy: {accuracy:.2f}%")
        
        self.best_solution = self.alpha_pos
        self.best_fitness = self.alpha_score
        self.best_accuracy = accuracy

        self.plot_convergence()

    def plot_convergence(self):
        plt.plot(self.fitness_history)
        plt.xlabel('Iteration')
        plt.ylabel('Best Fitness (Loss)')
        plt.title('Convergence Curve')
        plt.grid(True)
        plt.show()
