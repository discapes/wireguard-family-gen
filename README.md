# wireguard-family-gen

> Tool to generate scripts to configure a Wireguard server and clients.

This tool is useful when you have lots of devices that are all behind different routers/NATs/firewalls, and you want to connect them together. It only requires that one of the devices is able to expose any UDP port to the internet. A VPS is a good choice for that (the smallest EC2 instance t4g.nano works fine, and it's only 3€/m). 

How this tool works is it first creates a Wireguard configuration for the "server" (the device with the exposed UDP port), which has all the other devices as peers with AllowedIPs like "10.0.0.2/32", "10.0.0.3/32" etc.

It also creates Wireguard configurations for the other devices, which have only one peer, the server, with AllowedIPs set to a network prefix like 10.0.0.0/24. So whenever a device (like 10.0.0.2) wants to access another device (10.0.0.3), the request is sent to the server since it falls under the network prefix. Then, the server node routes it to the correct destination, and vice versa.

Finally, the tool packages the Wireguard configurations into scripts that install Wireguard and the respective configurations. 

### Warning!!!
The generated client scripts also open a netcat listener that listens on port 3000 that executes received commands in bash!!!!
The purpose of it is to allow for an ssh server to be configured. The netcat listener runs 10 times, so after configuring the ssh server, reopen the connection until it doens't open anymore.
Note: do not use this tool for malicious purposes! 

The script is configured via a file named config.yml. Here's an example:

```yml
server:
  sk: IAW/U437Jcxxxx # set your own secret key
  pk: rKDhEjxxxxx # set your own public key
  port: 51000 # don't need to change this, just make sure port 51000 is unblocked on the vps
  ip: 10.0.0.1 # don't need to change this
  endpoint_ip: 16.16.123.12 # this should be the vps box's external IP
  network: 10.0.0.0/24 # don't need to change this
  filename: server # the script will be placed in scripts/server.sh
  wg_install_cmd: apt install wireguard netcat-traditional

clients:
  - filename: desktop
    sk: 6Ku/bU4Xxxxxx # set your own secret key
    pk: cXdwVxxxx # set your own public key
    ip: 10.0.0.2 # don't need to change this
    wg_install_cmd: pacman -S --noconfirm --needed wireguard-tools gnu-netcat
  - filename: laptop
    sk: 6C4pxxxx
    pk: TJ0rxxxx
    ip: 10.0.0.3
    wg_install_cmd: pacman -S --noconfirm --needed wireguard-tools gnu-netcat

# generate keys with
# sk=$(wg genkey); pk=$(wg pubkey <<< $sk); echo -e "sk: $sk\npk: $pk"
```

After configuring the tool, you can generate the scripts with 
```bash
python main.py
```
If you don't have ssh access, you can upload the scripts to paste.rs or similar services
```bash
curl --data-binary @scripts/server.sh paste.rs -L
```
And run them on the new device with
```bash
curl <url> | bash
```
Note: after adding a new device, the server script needs to be run again.
