from flaskr import db
from datetime import datetime
class StatusSession(db.Model):
    __tablename__ = "session_table"
    user_id = db.Column(db.String(120), primary_key=True, nullable=False)
    action_mode = db.Column(db.String(120))
    tr_name = db.Column(db.String(120))
    tr_strength = db.Column(db.String(120))
    last_datetime = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


    def __init__(self, user_id):
        self._set_cuttrnt_date()
        self.user_id = user_id

    def _set_cuttrnt_date(self):
        self.last_datetime = datetime.now()

    def set_action_mode(self, action_mode):
        self.action_mode = action_mode
        self._set_cuttrnt_date()

    def set_tr_name(self, tr_name):
        self.tr_name = tr_name
        self._set_cuttrnt_date()

    def set_tr_strength(self, tr_strength):
        self.tr_strength = tr_strength
        self._set_cuttrnt_date()

    def is_invalid_session(self):
        if self.last_datetime is None:
            return False
        dt_now = datetime.now()
        diff_time = dt_now - self.last_datetime
        if diff_time.days > 0:
            return True
        if diff_time.seconds > 60 * 10:
            return True
        return False

    def print_session_vars(self):
        print("user_id: "+ self.user_id)
        _am = self.action_mode if self.action_mode is not None else ' '
        print("action_mode: "+ _am)
        _tn = self.tr_name if self.tr_name is not None else ' '
        print("tr_name: "+ _tn)
        _ts = self.tr_strength if self.tr_strength is not None else ' '
        print("tr_strength: "+ _ts)
        _ts = self.last_datetime if self.last_datetime is not None else ' '
        print("last_datetime: "+ str(_ts))
