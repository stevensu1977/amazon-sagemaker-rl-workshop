# learn
from mlagents.trainers.learn import parse_command_line

from mlagents.trainers import learn
import os

if __name__ == '__main__':
    env_list = ['SM_OUTPUT_DATA_DIR', 'SM_OUTPUT_DIR', 'SM_MODEL_DIR']
    for _ in env_list:
        print(_, os.getenv(_))
        
    # 在预训练的模型上继续训练，超参数不可修改
    learn.run_cli(parse_command_line(['resume-config.yaml', '--env', '/src/soccer6v6.x86_64', '--tensorflow', '--resume', '--run-id', 'ppo-resume']))
    
