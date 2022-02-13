def container_template(target_component, import_path, attrs): 
  
  return f'''
import {target_component} from '{import_path}';

interface {target_component}ContainerProps {{}}

const {target_component}Container: React.FC<
  {target_component}ContainerProps
> = () => {{
  return (
    <{target_component} {attrs}/>
  );
}};

export default {target_component}Container;
'''