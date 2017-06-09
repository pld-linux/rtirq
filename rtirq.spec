Summary:	Realtime IRQ thread system tunning
Name:		rtirq
Version:	20150216
Release:	1
License:	GPL v2
Group:		Applications
Source0:	http://www.rncbc.org/jack/%{name}-%{version}.tar.gz
# Source0-md5:	59e8b012c16b1e879ce8648f537400c5
URL:		http://alsa.opensrc.org/Rtirq
Requires(post,preun):	/sbin/chkconfig
BuildRequires:	rpmbuild(macros) >= 1.647
Requires:	rc-scripts
Requires(post,preun,postun):	systemd-units >= 38
Requires:	systemd-units >= 0.38
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Startup scripts for tunning the realtime scheduling policy and
priority of relevant IRQ service threads, featured for a
realtime-preempt enabled kernel configuration.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/sysconfig,%{systemdunitdir}}

cp -p rtirq.sh $RPM_BUILD_ROOT/etc/rc.d/init.d/rtirq
cp -p rtirq.conf $RPM_BUILD_ROOT/etc/sysconfig/rtirq
cp -p rtirq.service $RPM_BUILD_ROOT%{systemdunitdir}/rtirq.service

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart
%systemd_post %{name}.service

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi
%systemd_preun %{name}.service

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%{systemdunitdir}/%{name}.service
