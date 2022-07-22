import argparse

from sagemaker_rl.stable_baselines3_launcher import SagemakerStableBaselines3PPOLauncher, create_env


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_path', default="/opt/ml/output/intermediate/", type=str)
    parser.add_argument('--instance_type', type=str)
    parser.add_argument('--num_timesteps', default=1e4) #default 1e4
    parser.add_argument('--n_steps', default=2048, type=int)
    parser.add_argument('--clip_range', default=0.2, type=float)
    parser.add_argument('--ent_coef', default=0.0, type=float)
    parser.add_argument('--n_epochs', default=10, type=int)
    parser.add_argument('--learning_rate', default=3e-4)
    parser.add_argument('--batch_size', default=64, type=int)
    parser.add_argument('--gamma', default=0.99, type=float)
    parser.add_argument('--gae_lambda', default=0.95, type=float)
    parser.add_argument('--schedule', default="linear", type=str)
    parser.add_argument('--verbose', default=1, type=int)
    parser.add_argument('--env_id', default="MsPacman-v0",type=str)

    return parser.parse_known_args()


def main():
    args, unknown = parse_args()
    print("Launching training script with stable baselines PPO1")
    test_parameters=dict()
    test_parameters['output_path']=args.output_path
    test_parameters['n_steps']=int(args.n_steps)
    test_parameters['clip_range']=float(args.clip_range)
    test_parameters['ent_coef']=float(args.ent_coef)
    test_parameters['n_epochs']=int(args.n_epochs)
    test_parameters['learning_rate']=float(args.learning_rate)
    test_parameters['batch_size']=int(args.batch_size)
    test_parameters['gamma']=args.gamma
    test_parameters['gae_lambda']=float(args.gae_lambda)
    test_parameters['verbose']=int(args.verbose)
    test_parameters['num_timesteps']=float(args.num_timesteps)
    print(f"test_parameter {test_parameters}")
    
    SagemakerStableBaselines3PPOLauncher(
        #env=create_env(env_id="CartPole-v1", output_path=args.output_path),
        #env=create_env(env_id="SpaceInvaders-v0", output_path=args.output_path),
        env=create_env(env_id=args.env_id, output_path=args.output_path),   
        output_path=args.output_path,
        n_steps=int(args.n_steps),
        clip_range=float(args.clip_range),
        ent_coef=float(args.ent_coef),
        n_epochs=int(args.n_epochs),
        learning_rate=float(args.learning_rate),
        batch_size=int(args.batch_size),
        gamma=args.gamma,
        gae_lambda=float(args.gae_lambda),
        verbose=int(args.verbose),
        num_timesteps=float(args.num_timesteps)).run()

    
if __name__ == "__main__":
    args, unknown_args = parse_args()
    print("Launching train script with SagemakerStableBaselines3PPOLauncher: and arguments: {}".format(args))
    main()
