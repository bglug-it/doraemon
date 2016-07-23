Summary: Helps client to join domain and maintain itself
Name: doraemon
Version: 1.3.0
Release: 1.ns6
URL: https://github.com/bglug-it/doraemon/
License: GPLv2+
Group: System Environment/Daemons
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: nethserver-devtools > 1.0.1
Requires: httpd, php, sudo, php-xml, php-mcrypt
Requires: nethserver-base, nethserver-php
Requires: upstart
Source0: doraemon-1.3.0.tar.gz
BuildArch: noarch

%description
Helps client on a domain network to get information for its maintenance.

%prep
%setup -q

%build

%install
(cd root ; find . -depth -print | cpio -dump %{buildroot})
rm -f %{name}-%{version}-%{release}-filelist
%{genfilelist} %{buildroot} > %{name}-%{version}-%{release}-filelist
mkdir -p %{buildroot}%{_localstatedir}/log/doraemon
mkdir -p %{buildroot}%{_localstatedir}/cache/doraemon

# Copy the webroot dir
# mkdir -p %{buildroot}%{_datarootdir}/%{name}
# cp -av doraemon/* %{buildroot}%{_datadir}/%{name}

%post
if [ "$1" = 1 ]; then
  /sbin/e-smith/db configuration set %{name} service status enabled TCPPort 3000 access private DefaultRole client DomainFile /etc/domain.yml ManagementKeyFile /home/amgmt/.ssh/id_rsa.pub NamingBase lab NamingDigits 2 VaultPassFile /home/amgmt/.ansible/vault.txt
  /sbin/start %{name} >/dev/null 2>&1 || :
  /sbin/e-smith/signal-event runlevel-adjust
  /sbin/e-smith/signal-event firewall-adjust
fi

%preun
if [ "$1" = 0 ]; then
  /sbin/stop %{name} >/dev/null 2>&1 || :
  /sbin/e-smith/db configuration delete %{name}
  /sbin/e-smith/signal-event runlevel-adjust
  /sbin/e-smith/signal-event firewall-adjust
fi

%clean
rm -rf %{buildroot}

%files -f %{name}-%{version}-%{release}-filelist
%files
%defattr(644,root,root,755)
# %doc README.md LICENSE.txt
# %attr(755,-,-) %{_initrddir}/%{name}
# %{_sysconfdir}/logrotate.d/%{name}
# %dir %{_sysconfdir}/httpd/doraemon
%attr(0750,srvmgr,srvmgr) %dir %{_localstatedir}/cache/doraemon
#  %attr(0644,root,root) %ghost %{_sysconfdir}/init/doraemon.conf
#  %attr(0644,root,root) %ghost %{_sysconfdir}/httpd/doraemon/httpd.conf
%attr(0700,root,root) %dir %{_localstatedir}/log/doraemon
%attr(0644,root,root) %config %ghost %{_localstatedir}/log/doraemon/access_log
%attr(0644,root,root) %config %ghost %{_localstatedir}/log/doraemon/error_log


%changelog
* Mon Jul 18 2016 Paolo Asperti <paolo-AT-asperti.com> - 1.3.0-1.ns6
- PHP porting
- Added a basic UI

* Tue Oct 27 2015 Emiliano Vavassori <syntaxerrormmm-AT-gmail.com> - 1.2.1-2.ns6
- Packing corrections to rpm to fix upgrading issue

* Tue Oct 27 2015 Emiliano Vavassori <syntaxerrormmm-AT-gmail.com> - 1.2.1-1.ns6
- Packing new minor correction on how packages are extracted from db

* Mon Sep 11 2015 Emiliano Vavassori <syntaxerrormmm-AT-gmail.com> - 1.2.0-1.ns6
- Packing new version with ansible dynamic inventory support, epoptes server role support.

* Mon Sep 07 2015 Emiliano Vavassori <syntaxerrormmm-AT-gmail.com> - 1.1.1-1.ns6
- Packing new version with correct roles.

* Sun Sep 06 2015 Emiliano Vavassori <syntaxerrormmm-AT-gmail.com> - 1.1.0-1.ns6
- Packing new version with new functionalities.

* Wed Jul 15 2015 Emiliano Vavassori <syntaxerrormmm-AT-gmail.com> - 1.0.0-2.ns6
- Added logrotate file.

* Mon Jul 13 2015 Emiliano Vavassori <syntaxerrormmm-AT-gmail.com> - 1.0.0-1.ns6
- Unique binary for both ansiblehelper and mac2hostname.
