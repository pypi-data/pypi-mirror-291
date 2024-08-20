# https://github.com/kuangliu/pytorch-cifar/blob/master/models/resnet.py

import torch
import torch.nn as nn
import torch.nn.functional as F


class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, in_planes, planes, stride=1):
        super(BasicBlock, self).__init__()
        self.conv1 = nn.Conv2d(
            in_planes,
            planes,
            kernel_size=3,
            stride=stride,
            padding=1,
            bias=False
        )
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(
            planes,
            planes,
            kernel_size=3,
            stride=1,
            padding=1,
            bias=False
        )
        self.bn2 = nn.BatchNorm2d(planes)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_planes != self.expansion * planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_planes, self.expansion * planes,
                          kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(self.expansion * planes)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out


class Bottleneck(nn.Module):
    expansion = 4

    def __init__(self, in_planes, planes, stride=1):
        super(Bottleneck, self).__init__()
        self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3,
                               stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv3 = nn.Conv2d(planes, self.expansion *
                               planes, kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm2d(self.expansion * planes)

        self.shortcut = nn.Sequential()
        if stride != 1 or in_planes != self.expansion * planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_planes, self.expansion * planes,
                          kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(self.expansion * planes)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = F.relu(self.bn2(self.conv2(out)))
        out = self.bn3(self.conv3(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out


class ResNet(nn.Module):
    """
    ResNet class.
    """

    def __init__(self, c, h, w, block, num_blocks, n_hidden=100, n_outputs=10):
        """

        :param c: number of input image channels.
        :param h: input image height.
        :param w: input image width.
        :param block: block class for ResNet.
        :param num_blocks: List of block numbers for each of the four layers.
        :param n_hidden: number of hidden units at the last linear layer.
        :param n_outputs: number of outputs.
        """
        if h % 4 != 0:
            raise ValueError('Image height must be divisible by 4.')
        if w % 4 != 0:
            raise ValueError('Image width must be divisible by 4.')

        super(ResNet, self).__init__()
        self.in_planes = 64

        self.conv1 = nn.Conv2d(c, 64, kernel_size=3,
                               stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.layer1 = self._make_layer(block, 64, num_blocks[0], stride=1)
        self.layer2 = self._make_layer(block, 128, num_blocks[1], stride=1)
        self.layer3 = self._make_layer(block, 256, num_blocks[2], stride=1)
        self.layer4 = self._make_layer(block, 512, num_blocks[3], stride=1)
        self.linear1 = nn.Linear(512 * h * w // 16, n_hidden)
        self.linear2 = nn.Linear(n_hidden, n_outputs)

    def _make_layer(self, block, planes, num_blocks, stride):
        strides = [stride] + [1] * (num_blocks - 1)
        layers = []
        for stride in strides:
            layers.append(block(self.in_planes, planes, stride))
            self.in_planes = planes * block.expansion
        return nn.Sequential(*layers)

    def forward(self, x):
        """
        :param x: tensor with shape (*b, channels, height, width). Height and width must be equal.
        :return:
        """
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = F.avg_pool2d(out, 4)
        out = out.flatten(start_dim=1, end_dim=-1)
        out = F.relu(self.linear1(out))
        out = self.linear2(out)
        return out


def make_resnet18(image_shape, n_outputs):
    return ResNet(*image_shape, BasicBlock, num_blocks=[2, 2, 2, 2], n_outputs=n_outputs)


def make_resnet34(image_shape, n_outputs):
    return ResNet(*image_shape, BasicBlock, num_blocks=[3, 4, 6, 3], n_outputs=n_outputs)


def make_resnet50(image_shape, n_outputs):
    # TODO fix error regarding image shape
    return ResNet(*image_shape, Bottleneck, num_blocks=[3, 4, 6, 3], n_outputs=n_outputs)


def make_resnet101(image_shape, n_outputs):
    # TODO fix error regarding image shape
    return ResNet(*image_shape, Bottleneck, num_blocks=[3, 4, 23, 3], n_outputs=n_outputs)


def make_resnet152(image_shape, n_outputs):
    # TODO fix error regarding image shape
    return ResNet(*image_shape, Bottleneck, num_blocks=[3, 8, 36, 3], n_outputs=n_outputs)


if __name__ == '__main__':
    n_images = 2
    event_shape = (5, 8 * 7, 4 * 7)

    net = make_resnet18(event_shape, 15)
    y = net(torch.randn(n_images, *event_shape))
    print(y.size())
