# VirtualBox-to-Create-Multiple-VMs

## Install VirtualBox in linux
1. Update system
```bash
sudo apt update
```
2. Install VirtualBox
```bash
sudo apt install virtualbox
```
3. Verify installation
```bash
virtualbox
```

---
## Download alpine OS
download ios file from https://www.alpinelinux.org/downloads

---
## Create VM 
create VM using downloaded image
- add 1024 MB memory and 2 CPU processor
- Enable EFI
- keep 8 GB Hard Disk

setup network adapter to bridge for local machine access

---
## Configure VM
- start VM and login as 'root' user
- check ip address of the VM
    ```bash
    ip a
    ```
- if ip is not assigned, set the ethernet and request ip address from DHCP
    ```bash
    ip link set eth0 up
    udhcpc -i eth0
    ```
- check ip address again
    ```bash
    ip a
    ```
- verify network by ping to google stun server
    ```bash
    ping -c 3 8.8.8.8
    ```

---
## Update packages in VM
alpine does not come with repos added so add repos manually
```bash
vi /etc/apk/repositories
```
add main and community repos from alpine
```bash
https://dl-cdn.alpinelinux.org/alpine/latest-stable/main
https://dl-cdn.alpinelinux.org/alpine/latest-stable/community
```
add python package
```bash
apk update
apk add python3 py3-pip
```

---
## Deploy microservice in VM
add code from this repository to create a fastAPI based python servers and access it through REST API call.
