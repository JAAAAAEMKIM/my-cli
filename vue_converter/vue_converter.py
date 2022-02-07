from questionary import questionary

COMPONENT_NAME = ['COMPONENT_NAME']
USE_TRANSLATE = [0]

def convert_into_react():

  component_name = convert_kebab_to_pascal(questionary.text(
      "Name of this component in kebab-case:",
  ).ask())
  COMPONENT_NAME[0] = component_name

  sample = open('/Users/nhn/Projects/blog/dooray-react-frontend-cli/vue_converter/sample.vue', 'r')

  file_string = sample.read()
  template_start = file_string.find('<template>') + 10
  template_end = file_string.rfind('</template>')

  print(template_end)

  template_string = " ".join(file_string[template_start : template_end].strip().split())

  i = 0
  start_idx = 0
  close_idx = 0
  open_bracket = 0
  text_node = 0
  parsed = []

  for i, c in enumerate(template_string):
    if c == '<':
      start_idx = i + 1
      open_bracket = 1
      if text_node:
        parsed.append(('text_node', 'text', template_string[close_idx + 1: i]))
        text_node = 0
      continue
    if c == '>':
      close_idx = i
      open_bracket = 0
      parsed.append(parse(template_string[start_idx: close_idx].strip()))

    elif not open_bracket and c != ' ':
      text_node = 1

  parsed_jsx = reactify(parsed)

  import_translation = "import { useTranslation } from 'react-i18next';" if USE_TRANSLATE[0] else ''
  translate_hook = 'const { t } = useTranslation();' if USE_TRANSLATE[0] else ''
    

  result = f'''
    {import_translation}
    
    interface {component_name}Props {{}}
    
    const {component_name}: React.FC<{component_name}Props> = ({{}}) => {{
      {translate_hook}
      
      // undefined variables

      return (
        {parsed_jsx}
      )
    }}

    export default {component_name};
  '''
  print(result)
  return result



def parse(component_string):
  tag_open_close_type = 'open'
  if component_string.startswith('/'):
    tag_open_close_type = 'close'
  elif component_string.endswith('/'):
    tag_open_close_type = 'self-close'

  component_name = ''

  if tag_open_close_type == 'close':
    return (convert_kebab_to_pascal(component_string[1:]), tag_open_close_type, None)

  attr_idx = 0
  for i in range(len(component_string)):
    if component_string[i] == ' ':
      attr_idx = i
      component_name = component_string[:i]
      break
    if  i == len(component_string) - 1:
      component_name = component_string

  component_name = convert_kebab_to_pascal(component_name)
  if attr_idx == 0:
    return (component_name, tag_open_close_type, None)

  attr_string = component_string[attr_idx: ]

  open_quote = 0
  quote_start = 0
  quote_end = -1

  attrs = []
  temp = []

  for i, c in enumerate(attr_string):
    if c == '"' and open_quote == 0:
      temp.append(attr_string[quote_end + 2: i - 1])
      open_quote = 1
      quote_start = i
    elif c == '"' and open_quote == 1:
      open_quote = 0
      quote_end = i
      temp.append(attr_string[quote_start + 1: quote_end])
      attrs.append(temp[:])
      temp = []

      # TODO: close quote가 끝과 다를 때 single attribute인 경우 체크
  
  return (component_name, tag_open_close_type, attrs)

def reactify(nodes):
  stack = []
  strings = []
  for node in nodes:
    if node[0] == 'translate':
      USE_TRANSLATE[0] = 1
      if node[1] == 'open':
        strings.append('{t(')
        stack.append(node[0])
      if node[1] == 'close':
        strings.append(')}')
        stack.pop()
      continue

    if node[1] == 'text':
      if stack[-1] == 'translate': 
        __, value = node[2].split('~~')
        strings.append(f"'{COMPONENT_NAME[0]}~~{value}'")
        
      else:
        tmp = node[2].replace(f'{{{{', '{')
        tmp = tmp.replace(f'}}}}', '}')

        strings.append(tmp)
      continue

    if node[1] == 'close':
      top = stack.pop()
      if top.endswith('v-for'):
        strings.append(f'</{node[0]}>))}}')
      elif top.endswith('v-if'):
        strings.append(f'</{node[0]}>)}}')
      elif top.endswith('v-show'):
        strings.append(f'</{node[0]}>)}}')
      else:
        strings.append(f'</{node[0]}>')
      continue


    starting_bracket = '<'
    closing_bracket = '>' if node[1] == 'open' else '/>'
    attr_string = '' if not node[2] else ' '+' '.join(map(set_attr, node[2]))

    v_directive = find_vue_directives(node[2])
    if v_directive:
      if v_directive[0] == 'v-if':  # TODO: v-else, v-else-if 처리
        starting_bracket = f'{{{v_directive[1]} && (<'
        if node[1] == 'self-close':
          closing_bracket = f'/>)}}'
      elif v_directive[0] == 'v-show':
        starting_bracket = f'{{{v_directive[1]} && (<'
        if node[1] == 'self-close':
          closing_bracket = f'/>)}}'
      else: # v-for
        iterators, collection = v_directive[1].split(' in ')
        starting_bracket = f'{{{collection}.map({iterators} => (<'
        if node[1] == 'self-close':
          closing_bracket = f'/>))}}'

    strings.append(f'{starting_bracket}{node[0]}{attr_string}{closing_bracket}')

    if node[1] == 'open':
      directive = v_directive[0] if v_directive else ''
      stack.append(node[0] + directive)
      continue

  return ''.join(strings)

def convert_kebab_to_pascal(kebab):
  if '-' not in kebab:
    return kebab
  return ''.join(map(lambda x: x.title(), kebab.split('-')))

def set_attr(attr):
  if ' ' in attr[0]:
    return 
  if attr[0] == 'class':
    return f'className="{attr[1]}"'
  if attr[0].startswith(':'):
    if attr[0][1:] == 'class':
      return f'className={{{attr[1]}}}'
    return f'{attr[0][1:]}={{{attr[1]}}}'
  if attr[0].startswith('@'):
    event = convert_kebab_to_pascal(attr[0][1:]) if '-' in attr[0][1:] else attr[0][1:].title()
    return f'on{event}={{{attr[1]}}}'
  if attr[0].startswith('v-'):
    return ''
  if attr[0] == 'slot':
    return ''
  return f'{attr[0]}="{attr[1]}"'


def find_vue_directives(attrs):
  if not attrs: return False
  for attr in attrs:
    if attr[0] in ['v-if', 'v-show', 'v-for']:
      return attr

  return False