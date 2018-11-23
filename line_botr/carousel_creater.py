from jinja2 import Environment, FileSystemLoader, select_autoescape
from line_botr.training import Training

template_env = Environment(
    loader=FileSystemLoader('template/json'),
    autoescape=select_autoescape(['html', 'xml', 'json'])
)

def items2tra_car(items):
    template = template_env.get_template('training.json')
    data = template.render(dict(items=items))
    return data

def items2record_car(items):
    template = template_env.get_template('record.json')
    data = template.render(dict(items=items))
    return data
