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

%define siauser sia
%define siagroup sia

Name:           sia-renterd
Version:        1.0.7
Release:        %mkrel 1
Summary:        Blockchain-based marketplace for file storage - Renter daemon
License:        MIT
URL:            https://github.com/SiaFoundation/renterd
Group:          System/Servers
Source0:	  renterd-%{version}.tar.gz
Source1:        sia-renterd.service
Source3:        sia-renterd.sysconfig
Source4:        sia-renterd-tmpfiles.conf
BuildRequires:  golang
BuildRequires:  git
Requires(pre):    rpm-helper >= %{rpmhelper_required_version}
Requires(post):   rpm-helper >= %{rpmhelper_required_version}
Requires(post):   systemd >= %{systemd_required_version}
Requires(preun):  rpm-helper >= %{rpmhelper_required_version}
Requires(postun): rpm-helper >= %{rpmhelper_required_version}
Obsoletes:	sia-server

%description
Sia is a new decentralized cloud storage platform that radically alters the
landscape of cloud storage. By leveraging smart contracts, client-side
encryption, and sophisticated redundancy (via Reed-Solomon codes), Sia allows
users to safely store their data with hosts that they do not know or trust. The
result is a cloud storage marketplace where hosts compete to offer the best
service at the lowest price. And since there is no barrier to entry for hosts,
anyone with spare storage capacity can join the network and start making money.
%if %{?_with_testnet:1}%{!?_with_testnet:0}
THIS %{name} USES THE TESTNET
%endif

%prep
%setup -n renterd-%{version}
# -c -T

%build
#go generate ./...
%if %{?_with_testnet:1}%{!?_with_testnet:0}
CGO_ENABLED=1 go build -o bin/ -tags='testnet netgo timetzdata' -trimpath -a -ldflags '-s -w'  ./cmd/renterd
%else
CGO_ENABLED=1 go build -o bin/ -tags='netgo timetzdata' -trimpath -a -ldflags '-s -w'  ./cmd/renterd
%endif

%install
%{__mkdir_p} %{buildroot}/%{_localstatedir}/lib/sia/renterd
%{__mkdir_p} %{buildroot}/%{_bindir}
%{__mkdir_p} %{buildroot}/%{_sbindir}
%{__mkdir_p} %{buildroot}/%{_var}/log/sia/
export GOPATH=$(pwd)
%{__install} -p -m 0755 $GOPATH/bin/renterd %{buildroot}%{_sbindir}/%{name}
#{__mkdir_p} %{buildroot}/%{_sysconfdir}/bash_completion.d

#pushd $GOPATH/bin
#PATH=.:$PATH siac bash-completion siac.bash
#popd

#{__install} $GOPATH/bin/siac.bash %{buildroot}/%{_sysconfdir}/bash_completion.d/siac
%{__mkdir_p} %{buildroot}/%{_sysconfdir}/sysconfig
%{__install} %{SOURCE3} %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
%{__mkdir_p} %{buildroot}%{_unitdir}
%{__install} -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}
%{__install} -D -p -m 0644 %{SOURCE4} %{buildroot}%{_tmpfilesdir}/%{name}.conf

%clean

%pre
%_pre_useradd %{siauser} /var/lib/sia/ /bin/false

%post
if ! /usr/bin/id %{siauser} &>/dev/null; then
       /usr/sbin/useradd -r -g %{siagroup} -s /bin/false -c "Sia" -d /var/lib/sia %{siauser}
fi
%_tmpfilescreate %{name}
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
%_postun_userdel %{name}

%files
%config (noreplace) /etc/sysconfig/%{name}
%{_unitdir}/%{name}.service
%{_sbindir}/*
%{_tmpfilesdir}/%{name}.conf
%dir %attr(0750, sia,sia) %{_localstatedir}/lib/sia
%dir %attr(0750, sia,sia) %{_localstatedir}/lib/sia/renterd
%dir %attr(0755, sia,sia) %{_var}/log/sia
