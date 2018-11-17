# トレーナーbot
## 要件定義
- 筋トレを開始する前に、筋トレ項目を選択する
- 回数と重さを入力して送信
- db上に保存する
- 自分で、新しい種目を送信でき、以後、選択できるようにする

## 目的
既存手法では、技名を入力し、その後重さ・回数を入力していた。
しかし、
- 技名を入力するのが面倒
- 宣言したトレーニングを行えなかった時の修正ができない。


## シナリオ
- 記録の登録
  - 「登録」と入力
  - 種目のリストがLINE botによって帰ってくる
  - 種目を選択
  - 「重さ rep数 set数」    を入力
  - 登録した内容をLINE botが出力する

- 記録の除去
  - 「削除」と入力
  - 今日のトレーニング内容一覧を出力
  - 消したいidを入力
  - そのレコードを消す
  - 登録した内容をLINE botが出力する

- 種目の追加
  - 「追加」と入力
  - 種目名の追加を促すアラート
  - 種目名を入力
  - 登録した内容をLINE botが出力する

## dbのテーブル
- training_record  
|キー名|型|その他|
|-|-|-|
|id|INT|primary key, auto_increment|
|usr_id|INT|NOT NULL|  
|tr_date|DATE|NOT NULL|  
|tr_name|CHAR(32)|NOT NULL|  
|tr_weight|Int|-|  
|tr_rep|INT|NOT NULL|  

- training_kind  
|キー名|型|その他|
|-|-|-|
|uid|INT|primary key|
|tr_name|CHAR(32)|NOT NULL|

## ロジック
- actionフラグを入力
- actionフラグがすでにある場合は、変更
- actionフラグがないのにaction_list以外の入力があったらキャンセル処理
- actioにより、リストを返す。
- idが入力される
- idを保存 入力が整数じゃない もしくはリストの範囲外ならキャンセル処理
- rep数、set数の出力を促す
- actionフラグが入力されていて、かつidが入力されていれば、入力されたテキストを入力。フォーマットが間違えていたらキャンセル処理正しけれdbに保存
