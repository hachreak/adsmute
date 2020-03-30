# Ads Mute

A utility to manage advertising blacklist files on linux.

### How install

Download updated version of the ads server blacklists and create on dnsmasq
configuration file.

```
cd adsmute
# install the utils
pip install -e .
mkdir raw
# Download the blacklist files inside a "raw" directory
adsmute-cli download data/sources.json raw/
# Extract server list from them into a unique file
adsmute-cli servers data/sources.json raw/ servers.list
# Create a dnsmasq config file
adsmute-cli dnsmasq servers.list 00-adsmute.conf
# Install new configuration
sudo mv 00-adsmute.conf /etc/dnsmasq.d/
# restart dnsmasq
sudo systemctl restart dnsmasq

```

### DnsMasq vs Network Manager know issues

To install into dnsmasq, please remember that (at least in debian) could go
in conflict with network manager dnsmasq plugin and set manually the dns
`127.0.0.1`.
It's recommended to disable network manager plugin and restart both,
because network manager is not able to manage correctly dnsmasq.

### Acknowledgment
See original [source file](https://github.com/hectorm/hmirror/).
