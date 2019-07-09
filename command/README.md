初期設定に使うコマンドファイルたちです．
macにて動作確認済み

kidou.file  :ラズベリーパイが自動でbitnixを動かすための設定ファイル  
setup.command   :SDカード初期設定（使わない）  
setupzeroWH.sh  :ラズベリーパイ本体初期設定ファイル  
shoki.command   :SDカード初期設定  
sshpi.command   :ユーザー未設定のラズベリーパイとssh接続  
sshusr.command  :ユーザー設定済みのラズベリーパイとssh接続  
wpa_supplicant.conf :ラズベリーパイのWi-Fi初期設定用ファイル  

### SDカード初期設定方法
##### 設定を吹っ飛ばしてしまった時用
1. microSDカードをmacに挿す
2. shoki.commandを実行（20分ほどかかる）
3. microSDカードを抜く＋ラズベリーパイに挿す
4. 電源を入れる
5. sshpi.commandを実行（下記参照），繋がらないなら少し待つ
6. /Volumes/boot/kidou.fileを実行
7. 最初のパッケージ導入でyesを入力
8. あとは残りのパッケージを勝手にインストールしてくれるので待つ
9. 自動的に再起動してBitNixのプログラムが起動

### SSH接続の仕方
#### ユーザー設定（上記初期設定）が終わってない場合
1. sshpi.commandを実行
2. yesを入力＋エンター
3. SSH接続成功

#### ユーザー設定が終わっている場合
1. sshusr.commandを実行
2. yesを入力＋エンター
3. パスワード入力（デフォルトは「nixrsp11」）＋エンター
4. SSH接続成功
5.
