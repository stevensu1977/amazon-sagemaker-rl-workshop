# 使用 Stable baselines 在 Amazon SageMaker 上进行强化学习训练

<img src="https://stable-baselines.readthedocs.io/en/master/_static/logo.png" width="300">

[OpenAI Gym](https://gym.openai.com) 是一个开源的强化学习工具包,它提供了标准的接口和一组环境, 通过这些环境我们可以快速的进行强化学习实验. 

[Stable baselines](https://stable-baselines.readthedocs.io/en/master/) 是在OpenAI Baselines 基础算法上进行增强的开源强化学习算法项目. 

本次实验我们将使用stable baselines 自带的算法进行对OpenAI Gym自带的雅达利游戏 '吃豆人' [**MsPacman-v0**](https://gym.openai.com/envs/MsPacman-v0/) 进行训练.


## Contents

* `rl_gym_stable_baselines.ipynb`: Notebook demonstrating the code to make *MsPacman* bot
* `Dockerfile`: Dockerfile building the container with Roboschool, OpenMPI, stable-baselines and their dependencies by using SageMaker's RL tensorflow container as base.
* `src/`
  * `preset-pacman-sb3.py`: Preset for MsPacman distributed training with Stable-Baselines PPI1. 
  * `train_stable_baselines.py`: Training Stable-Baselines launcher script.
* `resources`: Files required as part of docker build.
* * 

