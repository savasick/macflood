# MAC Flood

>Mac Address Flooding Attack may slow and make unavailable LAN network

This python script is a tool for performing MAC Flood attacks using multithreading. It generates random MAC addresses and sends ARP packets to the local network, which can lead to overloading of switches.


### install

```bash
git clone https://github.com/savasick/macflood.git
cd macflood
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
or just need python3 and scapy

### run

```bash
sudo python3 macflood.py
```