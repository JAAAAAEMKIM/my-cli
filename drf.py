import argparse
import os
from component.component import component
from container.container import container
from vue_converter.vue_converter import convert_into_react

def redux():
  pass

parser = argparse.ArgumentParser()
parser.add_argument("-src",
                  required=False,
                  help="path to some folder",
                  type=os.path.abspath,
                  default='./')
parser.add_argument("type",
                  help="What to do",
                  default='component')

if __name__ == '__main__':
  args = parser.parse_args()
  if args.type == 'component':
    component()
  elif args.type == 'container':
    container()
  elif args.type == 'redux':
    redux()
  elif args.type == 'vue':
    convert_into_react()
  else:
    raise ValueError('Invalid type')

# TODO - BASH 단으로 넘기기