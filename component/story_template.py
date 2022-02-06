story_template = lambda service, grid, component, fullname: f'''
import {{ ComponentMeta, ComponentStory }} from '@storybook/react';

import {fullname} from './{fullname}';

export default {{
  title: '{service.title()}/Components/{grid.title()}/{component.title()}',
  component: {fullname},
  argTypes: {{}},
}} as ComponentMeta<typeof {fullname}>;

const Template: ComponentStory<typeof {fullname}> = (args) => {{
  return <{fullname} {{...args}} />;
}};

export const Default = Template.bind({{}});
Default.args = {{
}};
'''