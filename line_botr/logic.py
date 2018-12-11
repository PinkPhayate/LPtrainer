from line_botr import repository
from line_botr.session import StatusSession
from line_botr import carousel_creater as cc
ACTION_LIST = ['追加', '記録' , '削除', '参照']

def _is_invalid_action_mode(msg):
    if msg not in ACTION_LIST:
        return True
    return False

def select_1st_action(user_id, input_mode):
    """ 1回目の返信を決めるロジック
    LINE botに返してもらう文字列を決定する。形式は問わない。
    決定したモード: str、返す文字列を返す: str
    """
    # action mode判定し、相応しくなければメッセージを返して終わり
    if _is_invalid_action_mode(input_mode):
        return None, 'その操作はできません'

    # 相応しければaction modeを返す準備
    # モード別の処理を書く
    if input_mode == '記録':
        lst = repository.get_training_menu(user_id)
        output_msg = cc.items2tra_car(lst) if len(lst) > 0\
                            else "まだ登録されていません"

    elif input_mode == '参照':
        lst = repository.get_records(user_id)
        output_msg = cc.items2record_car(lst) if len(lst) > 0\
                            else "まだ記録がありません"
        input_mode = None

    elif input_mode == '追加':
        output_msg = '追加する種目名を入力してください'

    elif input_mode == '削除':
        lst = repository.get_records(user_id)
        [e.set_delete_button() for e in lst]
        output_msg = cc.items2record_car(lst)
    return input_mode, output_msg


def select_2nd_action(user_id, action_mode, resource):
    """ 2回目の返信を決めるロジック
    line botiに返してもらう文字列を決定する。形式は問わない。
    決定したモード: str、返す文字列を返す: str
    この段階でやりとりが終了するものがほとんど -> action_modeに値がなければ
    グローバル変数を初期化させる
    """
    if action_mode == '記録':
        action_mode = resource['postback']['data']
        output_msg = '[回数] [セット数] [重さ(kg)]　の形式で入力してください'
    elif action_mode == '追加':
        repository.insert_tr_menu(user_id, resource['message']['text'])
        action_mode = None
        repository.drop_session_record(user_id)
        output_msg = '追加しました'
    elif action_mode == '削除':
        repository.drop_record(resource['postback']['data'])
        action_mode = None
        repository.drop_session_record(user_id)
        output_msg = '削除しました'

    return action_mode, output_msg


def select_3rd_action(user_id, tr_name, input_msg):
    """ 2回目の返信を決めるロジック
    記録モードだけがこのメソッドにたどり着く
    書き込みが行えたかどうかを返す
    output_msg:str
    """
    if _is_invalid(input_msg):
        return  "入力の形式が正しくありません"
    try:
        repository.insert_record(user_id, tr_name, input_msg)
        tr_strength = _beautify(input_msg)
        output_msg = "{0} {1} \n登録完了".format(tr_name, tr_strength)
    except Exception as e:
        print(e)
        output_msg = 'DBへの書き込みに失敗しました'
    repository.drop_session_record(user_id)
    return output_msg

def get_session(user_id):
    previous_sess = repository.get_session_record(user_id)
    sess = previous_sess[0] if len(previous_sess) > 0 else StatusSession(user_id)
    sess = StatusSession(user_id) if sess.is_invalid_session() else sess
    return sess

def set_session(sess):
    sess.print_session_vars()
    repository.insert_session_record(sess)

def _is_invalid(msg):
    ary = msg.split(' ')
    if len(ary) < 2 or 3 < len(ary):
        return True
    not_digits = [x for x in ary if not x.isdigit()]
    if 0 < len(not_digits):
        return True
    return False

def _beautify(msg):
    ary = msg.split(' ')
    if len(ary) == 2:
        str = '{}rep {}set'.format(ary[0], ary[1])
    if len(ary) == 3:
        str = '{}rep {}set {}Kg'.format(ary[0], ary[1], ary[2])
    return str
