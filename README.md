# hakoniwa-iot

## 前提とする環境

- docker-compose がインストーするされている環境

## インストール方法

### git clone する
```
git clone https://github.com/toppers/hakoniwa-iot.git
```

### docker-compose をビルドする
```
cd hakoniwa-iot
```

```
docker-compose build
```

### ビルド確認

```
$ docker-compose images
Container       Repository         Tag       Image Id       Size  
------------------------------------------------------------------
client      hakoniwa-iot_client   latest   10ff7161c664   466.4 MB
server      hakoniwa-iot_server   latest   506ddea8967e   465.9 MB
```

## 環境起動方法

```
docker-compose up
```

うまく起動するとこうなります．（mosquitto が自動起動します）
```
Starting client ... done
Starting server ... done
Attaching to client, server
server    | [ 2248.512756]~DLT~    1~INFO     ~FIFO /tmp/dlt cannot be opened. Retrying later...
server    | 1663224379: mosquitto version 1.6.9 starting
server    | 1663224379: Using default config.
server    | 1663224379: Opening ipv4 listen socket on port 1883.
server    | 1663224379: Opening ipv6 listen socket on port 1883.
```


## 環境停止方法

起動しているコンソールで，`CTRL+C` してください．

正常に停止するとこうなります．
```
^CGracefully stopping... (press Ctrl+C again to force)
Stopping client ... done
Stopping server ... done
```

## MQTTを使ってみよう

`docker-compose up` してから，端末を２個(サーバー用とクライアント用)起動してください．

### サーバー起動

サーバーに入ります．
```
docker-compose exec server /bin/bash
```

TLS通信でやりたい場合は，１回だけ，以下の操作を実行してください．

```
CURDIR=`pwd`
```

```
cd config/tls
```

```
bash ../tls_conf.bash
```

```
cd ${CURDIR}
```

ご覧の通り，TLS向けの各種暗号化用のファイル群が作成されます．
```
# ls config/tls
ca.crt  ca.key  ca.srl  client.crt  client.csr  client.key  server.crt  server.csr  server.key
```

サンプル用のMQTTサブスクライバを起動します．

```
bash src/sample_sub.bash
```

なお，TLS通信でやる場合は，`tls`を付けてください

```
bash src/sample_sub.bash tls
```


成功するとこうなります．

```
Client mosq-M4uLqJfOKmXvtFwieV sending CONNECT
Client mosq-M4uLqJfOKmXvtFwieV received CONNACK (0)
Client mosq-M4uLqJfOKmXvtFwieV sending SUBSCRIBE (Mid: 1, Topic: topicA, QoS: 0, Options: 0x00)
Client mosq-M4uLqJfOKmXvtFwieV received SUBACK
Subscribed (mid: 1): 0
```

### クライアント起動

クライアントに入ります．

```
docker-compose exec client /bin/bash
```

サンプル用のMQTTトピックを送信します．
ただし，トピック送信の仕方は２種類あります．

1. mosquitto_pub コマンドで実行する方法
2. python プログラムで実行する方法

#### mosquitto_pub コマンドで実行する方法

```
bash src/sample_pub.bash 'hello world'
```

なお，TLS通信でやる場合は，`tls`を付けてください

```
bash src/sample_pub.bash 'hello world' tls
```


#### python プログラムで実行する方法

```
python3 src/sample_pub.py 
```

なお，TLS通信でやる場合は，`tls`を付けてください

```
python3 src/sample_pub.py tls
```


成功するとこうなります．

##### クライアント側のログ(mosquitto_pub)

```
Client mosq-QVrbCAEGBGqZ8MPUG8 sending CONNECT
Client mosq-QVrbCAEGBGqZ8MPUG8 received CONNACK (0)
Client mosq-QVrbCAEGBGqZ8MPUG8 sending PUBLISH (d0, q0, r0, m1, 'topicA', ... (11 bytes))
Client mosq-QVrbCAEGBGqZ8MPUG8 sending DISCONNECT
```


#### サーバー側のログ

```
Client mosq-M4uLqJfOKmXvtFwieV sending PINGREQ
Client mosq-M4uLqJfOKmXvtFwieV received PINGRESP
Client mosq-M4uLqJfOKmXvtFwieV received PUBLISH (d0, q0, r0, m0, 'topicA', ... (11 bytes))
hello world
Client mosq-M4uLqJfOKmXvtFwieV sending PINGREQ
Client mosq-M4uLqJfOKmXvtFwieV received PINGRESP
```

# 今後について
- [ ] BLE スタブデバイスの追加
- [ ] GCPと同じような認証手順の追加
- [ ] [サーバー側の箱庭環境RDBOX](https://github.com/fukuta-tatsuya-intec/rdbox_hakoniwa_iot)との結合
