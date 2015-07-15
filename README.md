# doraemon #

`doraemon` is a helper daemon that provides information to network clients
based on Ubuntu system, to correctly join in a SAMBA 3.0 domain served by
NethServer with [custom configurations](https://github.com/bglug-it/ps-srvmgmt).

It is a webserver (based on [Python
Bottle](http://bottlepy.org/docs/dev/index.html)) responding on port 3000 to
requests from client during provisioning phase with
[Ansible](http://www.ansible.com/).

This repo contains the server itself (`doraemon.py`) plus all the other files
needed to package a RPM installable on a
[NethServer](http://www.nethserver.org) 6.0 server.

It stores the configuration for the hosts inside a [SQLite](https://www.sqlite.org/) database.

Please see `doraemon.ini` for configuration of the server.

It is licensed under [GPLv2](https://www.gnu.org/licenses/gpl-2.0.html) license.

Thanks to the initial developer, [Enrico
Bacis](https://github.com/enricobacis).

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
  files within [Ansible configuration
repository](https://github.com/bglug-it/client-pull-installation).


### TODO List ###

* Implement methods for dynamic inventory for Ansible
* Verify RPM packaging to automatically start daemon as soon as it is
  installed
* Verify NethServer script for `runlevel-adjust`
