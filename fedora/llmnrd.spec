%bcond_with sourcegit

Name:           llmnrd
Version:        0.7
Release:        1%{?dist}
Summary:        Link-Local Multicast Resolution Daemon

License:        GPLv2
URL:            https://github.com/tklauser/llmnrd
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        llmnrd.service

BuildRequires:  gcc
BuildRequires:  make
%if %{with sourcegit}
BuildRequires:  git-core
%endif
BuildRequires:  systemd-rpm-macros
%systemd_requires

%description
llmnrd is a daemon implementing the Link-Local Multicast Name Resolution (LLMNR)
protocol according to RFC 4795.

llmnrd will respond to name resolution queries sent by Windows clients in
networks where no DNS server is available. It supports both IPv4 and IPv6.

%prep
%autosetup -p1


%build
%set_build_flags
%make_build prefix=%{_usr}


%install
%make_install prefix=%{_usr}
install -Dp %{SOURCE1} ${RPM_BUILD_ROOT}%{_unitdir}/llmnrd.service

%check
llmnr-query $(hostname)

%post
%systemd_post %{name}

%preun
%systemd_preun %{name}

%postun
%systemd_postun_with_restart %{name}


%files
%doc README*
%license COPYING
%{_bindir}/llmnr-query
%{_sbindir}/llmnrd
%{_unitdir}/llmnrd.service
%{_mandir}/man1/llmnr-query.1*
%{_mandir}/man8/llmnrd.8*

%changelog
* Wed Sep 30 2020 Petr Menšík <pemensik@redhat.com> - 0.7-1
- Initial release
