

import os
from pathlib import Path
import questionary
from component.test_template import test_template
from container.container_template import container_template

PATH_TO_DOORAY_PROJECT = (Path.home() / 'Projects/was-front-react')
PATH_TO_SERVICES = PATH_TO_DOORAY_PROJECT / '_services/main-services/src/services'
LOWER_CASE_ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
print(PATH_TO_SERVICES)

def container():
  current_path = PATH_TO_SERVICES
  service = questionary.select(
      "select services:",
      choices=os.listdir(current_path.as_posix()),
      default='home'
  ).ask()

  current_path = current_path / service / 'components'

  grid_choices = list(filter(lambda x: x[0] in LOWER_CASE_ALPHABET ,os.listdir(current_path.as_posix())))
  target_grid = questionary.select(
      "select grid system section of target component:",
      choices=grid_choices,
  ).ask()

  current_path = current_path / target_grid
  container_path = PATH_TO_SERVICES / service / 'containers'

  component_choices = list(filter(lambda x: x[0] in LOWER_CASE_ALPHABET ,os.listdir(current_path.as_posix())))
  component_choices = list(filter(lambda x: f'{x}-container' not in os.listdir(container_path.as_posix()), component_choices))

  target_component = questionary.select(
      "select target component: ",
      choices=component_choices,
  ).ask()


  container_dir = f"{target_component}-container"
  container_path = container_path / container_dir
  container_path.mkdir()
  tokens = container_dir.split('-')
  

  container_name_pascal = ''.join(map(lambda x: x.title(), tokens))
  target_component_pascal = ''.join(map(lambda x: x.title(), target_component.split('-')))
  target_component_path = current_path / target_component / f'{target_component_pascal}.tsx'

  component_props = get_props(target_component_path, target_component_pascal)
  # print(component_props)
  # print(f'interface {target_component_pascal}Props {props_for_interface(component_props)}')
  attrs = props_for_jsx(component_props)

  import_path = f'@{service}/components/{target_grid}/{target_component}/{target_component_pascal}'
  container_tsx_path = container_path / f"{container_name_pascal}.tsx"
  test_path = container_path / f"{container_name_pascal}.test.tsx"
  
  map(lambda path: path.touch(), [container_tsx_path, test_path])

  with container_tsx_path.open(mode='a') as f:
    f.write(container_template(target_component_pascal, import_path, attrs))
    f.close()
  with test_path.open(mode='a') as f:
    f.write(test_template(container_name_pascal))
    f.close()

  print(f'''CONTAINER CREATED!
  {service}
  ㄴcontainers
    ㄴ{container_dir}
      ㄴ{container_name_pascal}.test.tsx
      ㄴ{container_name_pascal}.tsx
  ''')


  # TODO - redux 모듈 삭제 툴 / sample 대신 읽어오는 방식으로 변경

CURLY_BRACES = ['{', '}']
PRIMITIVES = ['boolean', 'string', 'null', ]
NOOP = f'() => {{}}'

def get_props(path, component_name):
  with path.open() as f:
    file = f.read()
    prop_idx = file.find(f'{component_name}Props')
    start_idx = prop_idx + file[prop_idx:].find('{')
    parsed = parse_type(file[start_idx:])[0]

    return parsed


def parse_type(string): 
  it = 1
  pairs = []
  current_pair = []
  tmp = []
  while(it < len(string)):
    c = string[it]

    if c == ':':
      if (len(current_pair) == 0):
        current_pair.append(''.join(tmp))
        tmp = []
      else:
        tmp.append(c)
      it += 1
      continue
      
    if c.isspace():
      it += 1
      continue
    if c == ';':
      current_pair.append(''.join(tmp))
      it += 1
      tmp = []
      pairs.append(current_pair[:])
      current_pair = []
      continue
    if c not in CURLY_BRACES:
      tmp.append(c)
      it += 1
      continue
    if c == '{':
      parse_inner = parse_type(string[it:])
      current_pair.append(parse_inner[0])
      tmp = []
      pairs.append(current_pair[:])
      current_pair = []
      it += parse_inner[1] + 1
      continue
    else:
      return (pairs, it + 1)

  return (pairs, it + 1)
    
def props_for_interface(props):
  ret = '{\n'
  if isinstance(props, list):
    for prop in props:
      ret += f'{prop[0]}: {props_for_interface(prop[1])}\n'
    return ret + '}'
  else:
    return props
  


def props_for_jsx(props):
  ret = '\n'
  for prop in props:
    if isinstance(prop[1], list) :
      ret += f'{prop[0].rstrip("?")}={{{to_obj(prop[1])}}}\n'
    else:
      ret += f'{prop[0].rstrip("?")}={{{handle_type(prop[1])}}}\n'
  return ret

def to_obj(props):
  ret = '{\n'
  if isinstance(props, list):
    for prop in props:
      ret += f'{prop[0]}: {to_obj(prop[1])},\n'
    return ret + '}'
  else:
    return handle_type(props)
  


def handle_type(type):
  if type == 'number':
    return "0"
  if type == 'string':
    return "''"
  if type == 'boolean':
    return 'false'
  if type.endswith('[]'):
    return '[]'
  if '=>' in type:
    l, r = map(lambda x: x.strip(), type.split('=>'))
    if r == 'void':
      r = {}
    else:
      r = handle_type(r)
    return f'{l} => {r}'
  if '|' in type:
    return handle_type(type.split('|')[0])
  else:
    return '{}'