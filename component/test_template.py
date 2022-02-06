test_template = lambda fullname: f'''
import {{ render }} from '@testing-library/react';

import {fullname} from './{fullname}';

describe('{fullname}', () => {{
  it('renders a component', () => {{
    render(
      <{fullname} />,
    );
  }});
}});

'''