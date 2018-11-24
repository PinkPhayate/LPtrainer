class Training(object):
    name = ''
    vd_url = ''
    def __init__(self, name, vd_url=None):
        self.name = name
        self.vd_url = vd_url

class Record():
    id = None
    user_id = None
    tr_date = None
    tr_name = None
    tr_weight = None
    tr_rep = None
    tr_set = None

    has_delete_button = None
    def __init__(self, tr):
        self.get_training_record(tr)

    def get_training_record(self, tr):
        self.id = tr[0]
        self.user_id = tr[1]
        self.tr_date = tr[2]
        self.tr_name = tr[3]
        self.tr_weight = tr[4]
        self.tr_rep = tr[5]
        self.tr_set = tr[6]

    def set_delete_button(self):
        self.has_delete_button = 1
