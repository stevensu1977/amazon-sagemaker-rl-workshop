import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--RLSTABLEBASELINES_PRESET', required=True, type=str)
    parser.add_argument('--output_path', default="/opt/ml/output/intermediate/", type=str)
    parser.add_argument('--instance_type', type=str)
    parser.add_argument('--num_timesteps', default=1e4) #default 1e4
    parser.add_argument('--timesteps_per_actorbatch', default=2048, type=int)
    parser.add_argument('--clip_param', default=0.2, type=float)
    parser.add_argument('--entcoeff', default=0.0, type=float)
    parser.add_argument('--optim_epochs', default=10, type=int)
    parser.add_argument('--optim_stepsize', default=3e-4)
    parser.add_argument('--optim_batchsize', default=64, type=int)
    parser.add_argument('--gamma', default=0.99, type=float)
    parser.add_argument('--lam', default=0.95, type=float)
    parser.add_argument('--schedule', default="linear", type=str)
    parser.add_argument('--verbose', default=1, type=int)

    return parser.parse_known_args()


def main():
    args, unknown = parse_args()
    print(args)
    print("Launching training script with stable baselines PPO1")
    test_parameters=dict()
    test_parameters['output_path']=args.output_path
    test_parameters['timesteps_per_actorbatch']=int(args.timesteps_per_actorbatch)
    test_parameters['clip_param']=float(args.clip_param)
    test_parameters['entcoeff']=float(args.entcoeff)
    test_parameters['optim_epochs']=int(args.optim_epochs)
    test_parameters['optim_stepsize']=float(args.optim_stepsize)
    test_parameters['optim_batchsize']=int(args.optim_batchsize)
    test_parameters['gamma']=args.gamma
    test_parameters['lam']=float(args.lam)
    test_parameters['schedule']=args.schedule
    test_parameters['verbose']=int(args.verbose)
    test_parameters['num_timesteps']=float(args.num_timesteps)
    print(test_parameters)
        
    
    
if __name__ == "__main__":
    args, unknown_args = parse_args()
    print("Launching train script with MPI: {} and arguments: {}".format(args.RLSTABLEBASELINES_PRESET,
                                                                         str(unknown_args)))
    main()
