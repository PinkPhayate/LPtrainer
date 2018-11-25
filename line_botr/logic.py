from line_botr import repository
from line_botr import carousel_creater as cc
from line_botr.training import Training
ACTION_LIST = ['追加', '記録' , '削除', '参照']

def is_invalid_action_mode(msg):
    if msg not in ACTION_LIST:
        return True
    return False

def select_1st_action(user_id, input_mode):
    """ 1回目の返信を決めるロジック
    LINE botに返してもらう文字列を決定する。形式は問わない。
    決定したモード: str、返す文字列を返す: str
    """
    # action mode判定し、相応しくなければメッセージを返して終わり
    if is_invalid_action_mode(input_mode):
        return None, 'その操作はできません'

    # 相応しければaction modeを返す準備
    # モード別の処理を書く
    if input_mode == '記録':
        lst = repository.get_training_menu(user_id)
        trainig_menu = [Training(t) for t in lst]
        output_msg = cc.items2tra_car(trainig_menu)

    elif input_mode == '参照':
        lst = repository.get_records(user_id)
        output_msg = cc.items2record_car(lst)
        action_mode = None

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
        output_msg = '追加しました'
    elif action_mode == '削除':
        repository.drop_record(resource['postback']['data'])
        action_mode = None
        output_msg = '削除しました'

    return action_mode, output_msg
