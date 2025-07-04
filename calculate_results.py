import re
import matplotlib.pyplot as plt

# 初始化存储列表
train_losses = []
train_accs = []
test_losses = []
test_accs = []
test_ious = []
time_costs = []

# 正则表达式模式
train_pattern = re.compile(
    r'Train (\d+), loss: ([\d.]+), train acc: ([\d.]+), train avg acc: ([\d.]+), IoU: ([\d.]+)'
)
test_pattern = re.compile(
    r'Test (\d+), loss: ([\d.]+), test acc: ([\d.]+), test avg acc: ([\d.]+), IoU: ([\d.]+), time: ([\d.]+) s'
)

# 读取日志文件
with open('run.log', 'r') as f:
    for line in f:
        line = line.strip()
        # 处理训练数据
        train_match = train_pattern.match(line)
        if train_match:
            epoch = int(train_match.group(1))
            loss = float(train_match.group(2))
            acc = float(train_match.group(3))
            # 动态扩展列表长度以适应epoch编号
            if epoch >= len(train_losses):
                train_losses.extend([None] * (epoch - len(train_losses) + 1))
                train_accs.extend([None] * (epoch - len(train_accs) + 1))
            train_losses[epoch] = loss
            train_accs[epoch] = acc
        # 处理测试数据
        test_match = test_pattern.match(line)
        if test_match:
            epoch = int(test_match.group(1))
            loss = float(test_match.group(2))
            acc = float(test_match.group(3))
            iou = float(test_match.group(5))
            time = float(test_match.group(6))
            # 动态扩展列表长度以适应epoch编号
            if epoch >= len(test_losses):
                test_losses.extend([None] * (epoch - len(test_losses) + 1))
                test_accs.extend([None] * (epoch - len(test_accs) + 1))
                test_ious.extend([None] * (epoch - len(test_ious) + 1))
                time_costs.extend([None] * (epoch - len(time_costs) + 1))
            test_losses[epoch] = loss
            test_accs[epoch] = acc
            test_ious[epoch] = iou
            time_costs[epoch] = time

# 计算总训练时间
total_time = sum(time_costs)

# 找到最佳测试准确率的epoch
max_test_acc = max(test_accs)
best_epoch = test_accs.index(max_test_acc)
best_train_acc = train_accs[best_epoch]
best_test_iou = test_ious[best_epoch]

# 打印结果
print(f"最佳测试准确率出现在轮次 {best_epoch}:")
print(f"测试准确率: {max_test_acc:.4f}")
print(f"训练准确率: {best_train_acc:.4f}")
print(f"测试IoU: {best_test_iou:.4f}")
print(f"总训练时长: {total_time:.2f} 秒")

# 创建子图
plt.figure(figsize=(18, 8))

# 绘制损失曲线
plt.subplot(1, 2, 1)
plt.plot(train_losses, label='Train Loss', color='blue', linewidth=1)
plt.plot(test_losses, label='Test Loss', color='red', linewidth=1)
plt.xlabel('Epoch', fontsize=14)
plt.ylabel('Loss', fontsize=14)
plt.title('Loss Curve', fontsize=16)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

# 绘制准确率曲线
plt.subplot(1, 2, 2)
plt.plot(train_accs, label='Train Accuracy', color='green', linewidth=1)
plt.plot(test_accs, label='Test Accuracy', color='orange', linewidth=1)
plt.xlabel('Epoch', fontsize=14)
plt.ylabel('Accuracy', fontsize=14)
plt.title('Accuracy Curve', fontsize=16)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()