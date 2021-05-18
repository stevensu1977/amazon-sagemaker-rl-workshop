# learn
from mlagents.trainers.learn import parse_command_line

from mlagents.trainers import learn
import os

if __name__ == '__main__':
    env_list = ['SM_OUTPUT_DATA_DIR', 'SM_OUTPUT_DIR', 'SM_MODEL_DIR']
    for _ in env_list:
        print(_, os.getenv(_))
    # learn.run_cli(parse_command_line(['SoccerTwos.yaml', '--env', '/Users/jty/Desktop/3dball/3dball', '--tensorflow', '--resume']))
    learn.run_cli(parse_command_line(['config.yaml', '--env', '/src/soccer6v6.x86_64', '--tensorflow']))
