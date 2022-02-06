

import os
from pathlib import Path
import questionary
from component.story_template import story_template
from component.style_template import style_template
from component.test_template import test_template
from component.component_template import component_template

PATH_TO_DOORAY_PROJECT = (Path.home() / 'Projects/was-front-react')
PATH_TO_SERVICES = PATH_TO_DOORAY_PROJECT / '_services/main-services/src/services'
print(PATH_TO_SERVICES)

def component(path):
  print()
  current_path = PATH_TO_SERVICES
  service = questionary.select(
      "select services:",
      choices=os.listdir(current_path.as_posix()),
      default='home'
  ).ask()

  current_path = current_path / service / 'components'


  grid_choices = list(filter(lambda x: x[0] in 'abcdefghijklmnopqrstuvwxyz' ,os.listdir(current_path.as_posix())))
  target_grid = questionary.select(
      "select grid system section:",
      choices=grid_choices,
  ).ask()

  current_path = current_path / target_grid

  name = questionary.text(
      "Name of this component in kebab-case:",
  ).ask()

  tokens = name.split('-')

  component_dir = f"{service}-{target_grid}-{name}"
  current_path = current_path / component_dir
  current_path.mkdir()

  component_name_pascal = ''.join(map(lambda x: x.title(), tokens))
  full_name_token = [service, target_grid] + tokens
  full_name_pascal = ''.join(map(lambda x: x.title(), full_name_token))

  print('fullpath', current_path.as_posix())
  print(full_name_pascal)

  # TODO: y/N style

  component_path = current_path / f"{full_name_pascal}.tsx"
  style_path = current_path / f"{full_name_pascal}.styles.ts"
  story_path = current_path / f"{full_name_pascal}.stories.tsx"
  test_path = current_path / f"{full_name_pascal}.test.tsx"
  
  map(lambda path: path.touch(), [component_path, style_path, story_path, test_path])
  
  print(component_path.as_posix())

  # TODO: props도 받기

  with component_path.open(mode='a') as f:
    f.write(component_template(full_name_pascal))
    f.close()
  with story_path.open(mode='a') as f:
    f.write(story_template(service, target_grid, component_name_pascal, full_name_pascal))
    f.close()
  with style_path.open(mode='a') as f:
    f.write(style_template)
    f.close()
  with test_path.open(mode='a') as f:
    f.write(test_template(full_name_pascal))
    f.close()

  print(f'''COMPONENT CREATED!
  {service}
  ㄴcomponents
    ㄴ{target_grid}
      ㄴ{component_dir}
        ㄴ{full_name_pascal}.stories.tsx
        ㄴ{full_name_pascal}.styles.tsx
        ㄴ{full_name_pascal}.test.tsx
        ㄴ{full_name_pascal}.tsx
  ''')


  # TODO - redux 모듈 삭제 툴