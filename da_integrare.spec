Summary: apache/mod_php stack for Doraemon
Name: doraemon
Version: 1.3.0.1
Release: 1%{?dist}
License: GPL
URL: %{url_prefix}/%{name}
BuildArch: noarch

Source0: %{name}-%{version}.tar.gz


BuildRequires: nethserver-devtools

BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Requires: httpd, php, sudo, php-xml, php-mcrypt, nethserver-httpd-admin
Requires: nethserver-base, nethserver-php
Requires: nethserver-lang-en

%description
Runs an Apache instance on port 3000 that serves
the doraemon web application

%prep
%setup


# Nethgui:
cd %{_builddir}/nethgui-%{nethgui_commit}

%build
perl createlinks
mkdir -p root/%{_nseventsdir}/%{name}-update

%install
(cd root ; find . -depth -print | cpio -dump %{buildroot})
rm -f %{name}-%{version}-%{release}-filelist
%{genfilelist} %{buildroot} \
    > %{name}-%{version}-%{release}-filelist
mkdir -p %{buildroot}/%{_localstatedir}/log/doraemon
mkdir -p %{buildroot}/%{_localstatedir}/cache/doraemon

# Copy the server-manager dir
mkdir -p %{buildroot}%{_nsuidir}
cp -av nethserver-manager %{buildroot}%{_nsuidir}/nethserver-manager

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%doc %{extradocs}

%{_nsuidir}/nethserver-manager


%dir %{_nseventsdir}/%{name}-update
%dir %{_sysconfdir}/httpd/doraemon.d

%attr(0750,srvmgr,srvmgr) %dir %{_localstatedir}/cache/doraemon
%attr(0644,root,root) %ghost %{_sysconfdir}/init/doraemon.conf
%attr(0644,root,root) %ghost %{_sysconfdir}/httpd/doraemon/httpd.conf
%attr(0700,root,root) %dir %{_localstatedir}/log/doraemon
%attr(0644,root,root) %config %ghost %{_localstatedir}/log/doraemon/access_log
%attr(0644,root,root) %config %ghost %{_localstatedir}/log/doraemon/error_log
%config(noreplace) /etc/sysconfig/doraemon

%post
%systemd_post doraemon.service

%preun
%systemd_preun doraemon.service

%postun
%systemd_postun

%changelog
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
