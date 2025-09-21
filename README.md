# FSUB

# 📡 Install via Linux (VPS)
Ini Panduan buat install bot fsub di linux (VPS) 

## 1. Pastikan update & upgrade vps nya
```
apt update && apt upgrade -y
```

## 2. Clone repository
```
git clone https://github.com/Raja009988/Fsub-Gacor
```
kalau mau nama directory sesuai yg lu mau, tambahin nama directory dibelakang link repo `(opsional)`

Contoh :
```
git clone https://github.com/Raja009988/Fsub-Gacor fsub
```

## 3. Change Directory
```
cd Fsub-Gacor
```
kalau nama directory nya `fsub` :
```
cd fsub
```

## 4. Buat screen baru
sesuai nama directory ya! biar ga bingung kalau banyak bot yg mau di deploy
```
screen -S Fsub-Gacor
```

## 5. Install venv
```
apt install -y python3-venv
```

## 6. Buat venv dan aktifkan environment 
```
python3 -m venv venv && source venv/bin/activate
```

## 7. Install requirements
```
pip install -r req*
```

## 8. Install pyrogram (khusus buat bot ini)
```
pip install git+https://github.com/naya1503/mypyrogram@dev
```

## 9. run bot
```
bash start.sh
```
