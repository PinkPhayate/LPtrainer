from flaskr import db

class Training(db.Model):
    __tablename__ = "training_kind"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.String(120))
    tr_name = db.Column(db.String(120))

    def __init__(self, uid, tr_name):
        self.user_id = uid
        self.tr_name = tr_name

class Record(db.Model):
    __tablename__ = "training_record"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(120))
    tr_date = db.Column  (db.String(120))
    tr_name = db.Column  (db.String(120))
    tr_weight = db.Column(db.Integer)
    tr_rep = db.Column(db.Integer)
    tr_set = db.Column(db.Integer)


    def __init__(self, user_id, tr_date, tr_name, tr_weight, tr_rep, tr_set):
        self.user_id = user_id
        self.tr_date = tr_date
        self.tr_name = tr_name
        self.tr_weight = tr_weight
        self.tr_rep = tr_rep
        self.tr_set = tr_set

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
