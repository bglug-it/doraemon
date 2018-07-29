# doraemon #

## Progetto Scuola [<img src="https://avatars1.githubusercontent.com/u/12886037?v=3&s=200" width="25" height="25" /> BgLUG][bglug] - Scenery 1 ##

`doraemon` is a helper daemon that provides information to [Ubuntu][] network
clients, to correctly join in a [SAMBA][] 3.0 domain served by [NethServer][]
with [custom configurations][server-config].

It is a webserver (based on [Python Bottle][bottle]) responding on port 3000
to requests from client during provisioning phase with [Ansible][].

This repo contains the server itself (`doraemon.py`) plus all the other files
needed to package a RPM installable on a [NethServer][] 6.0 server.

It stores the configuration for the hosts inside a [SQLite][] database, plus
providing some other information from well-known files inside the filesystem.

Please see `doraemon.ini` for configuration of the server.

It is licensed under [GPLv2][] license.

Thanks to the initial developer, [Enrico Bacis][].

## Routes served ##

Actually, the server responds to the following routes:

* `/mac2hostname`: responds to the client stating the hostname based on MAC
  address. Actually requires following parameters:
    - `mac`: the MAC address for which create the hostname.
  Optional parameters:
    - `base`: basename of the client. Can be any string. Defaulting to "lab".
    - `role`: role of the client to be created. Can be any string (default:
      "client").
* `/whatsmyhostname`: returns hostname for the client that requested the
  route. May accept the following optional parameters:
    - `base`: basename of the client.
    - `role`: role of the client.
* `/hosts`: returns a dictionary of all hosts registered, each with its role,
  hostname and MAC address. 
* `/domain`: returns YAML-formatted output for domain information.
* `/mgmtkey`: returns the SSH public key for the management user inside the
  network.
* `/vaultpass`: provides encrypted password for the decription of vaulted
  files within [Ansible configuration repository][client-pull-installation].
* `/ansible_list`: replies with the hostname list to be used with a dynamic
  inventory script for Ansible, please see [this
page][ansible-dynamic-inventory].
* `/ansible_host`: receives a `host` parameter, but returns anyways additional
  variables based on the MAC address of the client contacting it, to be used
with dynamic inventory script for Ansible and `ansible-pull`.
* `/epoptes-srv`: replies with the hostname of the local [Epoptes][epoptes] controller.

[bglug]: http://bglug.it "BgLUG Homepage"
[ubuntu]: http://www.ubuntu.com
[samba]: http://www.samba.org
[nethserver]: http://www.nethserver.org
[server-config]: https://github.com/bglug-it/server-config
[client-pull-installation]: https://github.com/bglug-it/client-pull-installation
[bottle]: http://bottlepy.org/docs/dev/index.html
[ansible]: http://www.ansible.com
[sqlite]: https://www.sqlite.org/
[gplv2]: https://www.gnu.org/licenses/gpl-2.0.html
[enrico bacis]: https://github.com/enricobacis
[ansible-dynamic-inventory]: http://docs.ansible.com/ansible/developing_inventory.html
[epoptes]: http://www.epoptes.org/
