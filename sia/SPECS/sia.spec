%global debug_package %{nil}

%ifarch x86_64
%global altarch amd64
%endif
%ifarch %{ix86}
%global altarch 386
%endif
%ifarch %{arm}
%global altarch arm
%endif

Name:           sia
Version:        1.3.0
Release:        %mkrel 0.20170714
Summary:        Blockchain-based marketplace for file storage
License:        MIT
URL:            https://github.com/NebulousLabs/Sia/
Group:          System/Servers
Source1:        sia.service
Source3:        sia.sysconfig
Source4:        sia-tmpfiles.conf
BuildRequires:  golang
BuildRequires:  git
Requires(pre):    rpm-helper >= %{rpmhelper_required_version}
Requires(post):   rpm-helper >= %{rpmhelper_required_version}
Requires(post):   systemd >= %{systemd_required_version}
Requires(preun):  rpm-helper >= %{rpmhelper_required_version}
Requires(postun): rpm-helper >= %{rpmhelper_required_version}

%description
Sia is a new decentralized cloud storage platform that radically alters the
landscape of cloud storage. By leveraging smart contracts, client-side
encryption, and sophisticated redundancy (via Reed-Solomon codes), Sia allows
users to safely store their data with hosts that they do not know or trust. The
result is a cloud storage marketplace where hosts compete to offer the best
service at the lowest price. And since there is no barrier to entry for hosts,
anyone with spare storage capacity can join the network and start making money.

%package        server
Summary:        Blockchain-based marketplace for file storage daemon
Group:          System/Servers

%description    server
Sia is a new decentralized cloud storage platform that radically alters the
landscape of cloud storage. By leveraging smart contracts, client-side
encryption, and sophisticated redundancy (via Reed-Solomon codes), Sia allows
users to safely store their data with hosts that they do not know or trust. The
result is a cloud storage marketplace where hosts compete to offer the best
service at the lowest price. And since there is no barrier to entry for hosts,
anyone with spare storage capacity can join the network and start making money.
SIA server daemon

%package        client
Summary:        Blockchain-based marketplace for file storage client
Group:          System/Servers

%description    client
Sia is a new decentralized cloud storage platform that radically alters the
landscape of cloud storage. By leveraging smart contracts, client-side
encryption, and sophisticated redundancy (via Reed-Solomon codes), Sia allows
users to safely store their data with hosts that they do not know or trust. The
result is a cloud storage marketplace where hosts compete to offer the best
service at the lowest price. And since there is no barrier to entry for hosts,
anyone with spare storage capacity can join the network and start making money.
SIA server daemon

%prep
%setup -c -T

%build
export GOPATH=$(pwd)
go get -u github.com/NebulousLabs/Sia/...

%install
%{__mkdir_p} %{buildroot}/%{_localstatedir}/lib/sia
%{__mkdir_p} %{buildroot}/%{_bindir}
%{__mkdir_p} %{buildroot}/%{_sbindir}

export GOPATH=$(pwd)
%{__install} -p -m 0755 $GOPATH/bin/siac %{buildroot}%{_bindir}
%{__install} -p -m 0755 $GOPATH/bin/siad %{buildroot}%{_sbindir}

%{__mkdir_p} %{buildroot}/%{_sysconfdir}/sysconfig
%{__install} %{SOURCE3} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
%{__mkdir_p} %{buildroot}%{_unitdir}
%{__install} -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}
%{__install} -D -p -m 0644 %{SOURCE4} %{buildroot}%{_tmpfilesdir}/%{name}.conf

%clean

%pre server
%_pre_useradd %{name} /dev/null /bin/false

%post server
if ! /usr/bin/id sia &>/dev/null; then
       /usr/sbin/useradd -r -g sia -s /bin/false -c "Sia" -d /var/run/sia sia
fi
%_tmpfilescreate %{name}
%_post_service %{name}

%preun server
%_preun_service %{name}

%postun server
%_postun_userdel %{name}

%files server
%config (noreplace) /etc/sysconfig/%{name}
%{_unitdir}/%{name}.service
%{_sbindir}/*
%{_tmpfilesdir}/%{name}.conf

%files client
%{_bindir}/*
