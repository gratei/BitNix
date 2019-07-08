date
sudo diskutil unmountDisk /dev/disk2
sudo dd bs=1m if=/Users/Snowfox/Downloads/2018-11-13-raspbian-stretch-full.img of=/dev/disk2
sudo touch /Volumes/boot/ssh
sudo mkdir /Volumes/boot/work
sudo cp /Users/Snowfox/work/NixBTC/Nix_BTC/main7.py /Volumes/boot/work/main.py
sudo cp /Users/Snowfox/work/NixBTC/Nix_BTC/wpa_supplicant.conf /Volumes/boot
sudo cp /Users/Snowfox/work/NixBTC/Nix_BTC/cmdline.txt /Volumes/boot/cmdline.txt
sudo cp /Users/Snowfox/work/NixBTC/Nix_BTC/config.txt /Volumes/boot/config.txt
sudo cp /Users/Snowfox/work/NixBTC/Nix_BTC/setupzeroWH.sh /Volumes/boot/setup.sh
sudo cp /Users/Snowfox/work/NixBTC/Nix_BTC/kidou.file /Volumes/boot/kidou.file
sudo diskutil unmountDisk /dev/disk2
read num
