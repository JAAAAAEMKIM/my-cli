component_template = lambda fullname: f'''
import * as styles from './{fullname}.styles';

interface {fullname}Props {{}}

const {fullname}: React.FC<
  {fullname}Props
> = () => {{
  return (
    <div></div>
  );
}};

export default {fullname};
'''