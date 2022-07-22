import gym

import os

from gym.wrappers.monitoring.video_recorder import VideoRecorder
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.ppo import MlpPolicy



class RewScale(gym.RewardWrapper):
    def __init__(self, env, scale):
        gym.RewardWrapper.__init__(self, env)
        self.scale = scale

    def reward(self, _reward):
        return _reward * self.scale


class SagemakerStableBaselinesLauncher():
    """
    Sagemaker's Stable Baselines Launcher.
    """

    def __init__(self, env, output_path, model, num_timesteps):
        self._env = env
        self._output_path = output_path
        self._model = model
        self._num_timesteps = num_timesteps

    def _train(self):
        """Train the RL model
        """
        print("train...")
        self._model.learn(total_timesteps=self._num_timesteps)

    def _predict(self, model, video_path):
        """Run predictions on trained RL model.
        """
        vr = VideoRecorder(env=self._env, path="{}/rl_out.mp4".format(video_path, str(1)),
                           enabled=True)
        obs = self._env.reset()
        for i in range(1000):
            action, _states = model.predict(obs)
            obs, rewards, dones, info = self._env.step(action)
            if dones:
                obs = self._env.reset()
            self._env.render(mode='rgb_array')
            vr.capture_frame()
        vr.close()
        self._env.close()
        print("Predict and video record was completed, {}/rl_out.mp4".format(video_path))
        
    def _save(self, model):
        model.save("{}/rl_model".format(self._output_path))
        print("model saved: {}/rl_model".format(self._output_path))
        

    def run(self):

        self._train()
        self._predict(self._model, self._output_path)
        self._save(self._model)


class SagemakerStableBaselines3PPOLauncher(SagemakerStableBaselinesLauncher):
    """
    Sagemaker's Stable Baselines3 PPO Launcher.
    """

    def __init__(self, env, output_path, n_steps,
                 clip_range, ent_coef, n_epochs,
                 learning_rate, batch_size,
                 gamma, gae_lambda, 
                 verbose, num_timesteps):
        print(
            "Initializing PPO with output_path: {} and Hyper Params [n_steps: {},clip_range: {}, "
            "ent_coef: {}, n_epochs: {}, learning_rate: {}, batch_size: {}, gamma: {}, lam: {}, "
            "verbose: {}, num_timesteps: {}]".format(output_path, n_steps,
                                                                   clip_range, ent_coef, n_epochs,
                                                                   learning_rate, batch_size,
                                                                   gamma, gae_lambda, 
                                                                   verbose, num_timesteps))

        super().__init__(env, output_path,
                         PPO(policy=MlpPolicy,
                              env=env,
                              gamma=gamma,
                              n_steps=n_steps,
                              clip_range=clip_range,
                              ent_coef=ent_coef,
                              n_epochs=n_epochs,
                              learning_rate=learning_rate,
                              batch_size=batch_size,
                              gae_lambda=gae_lambda,
                              verbose=verbose),
                         num_timesteps)


def create_env(env_id, output_path, seed=0):
    rank = 1
    env = gym.make(env_id)
    env = Monitor(env, os.path.join(output_path, str(rank)), allow_early_resets=True)
    env.seed(seed)
    return env
