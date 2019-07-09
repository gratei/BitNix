#! /bin/sh
rootpw="nixrsproot"
nixpw="nixrsp11"
nixusr="nixdisp"
prog="main.py"
#export LANG=C
sudo apt-get install expect #対話自動化コマンドexpectをインストール
echo "\e[36m install expect \e[m"
sudo systemctl stop serial-getty@ttyAMA0.service #既存のシリアル通信サービスを停止
echo "\e[36m stop serial.service \e[m"
sudo systemctl disable serial-getty@ttyAMA0.service #既存のシリアル通信サービスを無効化
echo "\e[36m disable serial.service \e[m"
sudo timedatectl set-ntp yes #NTPサーバーを設定
echo "\e[36m set-ntp \e[m"
sudo timedatectl set-timezone Asia/Tokyo #タイムゾーンを日本に設定
echo "\e[36m timezone=TOKYO \e[m"
pip3 install pyserial #pythonからシリアル通信を扱うライブラリをインストール
echo "\e[36m install pyserial \e[m"
sudo cp /boot/kidou.file /etc/rc.local #起動時に自動で実行するファイルを設定
sudo sed -i -e "/python3/s/user/${nixusr}/" /etc/rc.local
sudo sed -i -e "/python3/s/program/${prog}/" /etc/rc.local
echo "\e[36m cp kidou.file \e[m"
#↓新しいユーザーを設定
expect -c "
set timeout 10
spawn sudo adduser ${nixusr}
expect \"Enter new UNIX password:\"
send -- \"${nixpw}\n\"
expect \"Retype new UNIX password:\"
send -- \"${nixpw}\n\"
expect \"Full Name\"
send -- \"\n\"
expect \"Room Number\"
send -- \"\n\"
expect \"Work Phone\"
send -- \"\n\"
expect \"Home Phone\"
send -- \"\n\"
expect \"Other\"
send -- \"\n\"
expect \"information\"
send -- \"y\n\"
interact
"
sudo usermod -G pi,adm,dialout,cdrom,sudo,audio,video,plugdev,games,users,input,netdev,spi,i2c,gpio ${nixusr} #新規ユーザーの権限を設定
echo \n
echo "\e[36m usermod ${nixusr} \e[m"
sleep 5s
sudo cp /boot/work/${prog} /home/${nixusr}/${prog} #メインプログラムをユーザーのホームディレクトリに移動
echo "\e[36m cp ${prog} \e[m"
sudo sed -i -e "/#PermitRootLogin/s/#//" /etc/ssh/sshd_config
sudo sed -i -e "/PermitRootLogin/s/prohibit-password/no/" /etc/ssh/sshd_config #rootでのログインを禁止する
echo "\e[36m PermitRootLogin->no \e[m"
sudo sed -i -e "/autologin-user=pi/s/autologin-user=pi/#autologin-user=pi/" /etc/lightdm/lightdm.conf #rootでのログインを禁止する
echo "\e[36m autologin=NO@root \e[m"
sudo cp -r /home/pi/* /home/${nixusr}/ #
echo "\e[36m cp pihomedir to ${nixusr} \e[m"
#ラズベリーパイのアップデート
expect -c "
set timeout 10
spawn sudo rpi-update
expect \"Would you like to proceed\"
send -- \"y\"
"
sudo apt-get update #同上
echo "\e[36m apt-get update \e[m"
#↓同上
expect -c "
set timeout 10
spawn sudo apt-get upgrade
expect \"Do you want to continue\"
send -- \"Y\n\"
expect \"Reading changelogs...\"
send -- \"q\n\"
expect \"press q to quit\"
send -- \"q\n\"
"
#rootのパスワード変更
expect -c "
set timeout 10
spawn sudo passwd root
expect \"Enter new UNIX password:\"
send -- \"${rootpw}\n\"
expect \"Retype new UNIX password:\"
send -- \"${rootpw}\n\"
"
echo "\e[36m reboot \e[m"
sudo reboot
