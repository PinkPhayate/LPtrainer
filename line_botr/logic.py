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
