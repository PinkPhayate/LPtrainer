from flaskr import db

class Training(db.Model):
    __tablename__ = "training_kind"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    tr_name = db.Column(db.String(120))

    def __init__(self, uid, tr_name):
        self.user_id = uid
        self.tr_name = tr_name

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
