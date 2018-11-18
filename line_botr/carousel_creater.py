from jinja2 import Environment, FileSystemLoader, select_autoescape
from line_botr.training import Training

def create_carousel():
    return [
        Training('クランチ', None), Training('プランク', None), Training('リバースプッシュアップ', None), Training('プッシュアップ', None)]

template_env = Environment(
    loader=FileSystemLoader('template/json'),
    autoescape=select_autoescape(['html', 'xml', 'json'])
)

def get_carousel_json():
    items = create_carousel()
    template = template_env.get_template('training.json')
    data = template.render(dict(items=items))
    return data
