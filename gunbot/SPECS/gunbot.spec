%define        __spec_install_post %{nil}
%define          debug_package %{nil}
%define        __os_install_post %{_dbpath}/brp-compress
%ifarch %ix86
%define executable_name gunthy-linuxx86
%endif
%ifarch x86_64 amd64 ia32e
%define executable_name gunthy-linuxx64
%endif

Name:           gunbot
Version:        3.3.2
Release:        %mkrel 1
Summary:        Bot trader
License:        Commercial
Group:          Networking/Other
URL:            https://github.com/GuntharDeNiro/BTCT
Source0:        GUNBOT_v3.3.2_Poloniex_Bittrex_Patch.zip
Source2:        gunbot-tmpfiles.conf
Requires:       nodejs
BuildRequires:  unzip
BuildRequires:  systemd
Requires(pre):    rpm-helper >= %{rpmhelper_required_version}
Requires(post):   rpm-helper >= %{rpmhelper_required_version}
Requires(post):   systemd >= %{systemd_required_version}
Requires(preun):  rpm-helper >= %{rpmhelper_required_version}
Requires(postun): rpm-helper >= %{rpmhelper_required_version}

%description
Poloniex, Craken, Bittrex trader

%prep
rm -rf *
%{__mkdir_p} zipball
pushd zipball
unzip %{SOURCE0}
mv %{executable_name} ..
mv ALLPAIRS-params.js ..
mv bittrex-BTC_AMP-config.js ../exchange-XXX_YYY-config.js
popd
rm -rf zipball

%install
%{__install} -d %{buildroot}/opt/gunbot
%{__install} -d %{buildroot}%{_unitdir}

%{__install} -p -m 0755 %{executable_name} %{buildroot}/opt/gunbot
%{__install} -p -m 0644 ALLPAIRS-params.js %{buildroot}/opt/gunbot
%{__install} -D -p -m 0644 %{SOURCE2} %{buildroot}%{_tmpfilesdir}/%{name}.conf

cat > %{buildroot}%{_unitdir}/gunbot@.service <<EOF
[Unit]
Description=The Gunbot
After=network.target remote-fs.target nss-lookup.target

[Service]
Type=simple
User=gunbot
WorkingDirectory=/opt/gunbot
PIDFile=/run/gunbot/gunbot-%i.pid
ExecStart=/usr/bin/bash -c 'cd /opt/gunbot; /opt/gunbot/%{executable_name} \`/usr/bin/echo -n %%i | /usr/bin/cut -d- -f2\` \`/usr/bin/echo -n %%i | /usr/bin/cut -d- -f1\`'
ExecStop=/usr/bin/kill \$(/run/gunbot/gunbot-%i.pid)

[Install]
WantedBy=multi-user.target
EOF

#\${PAIR_EXCHANGE#*-} \${PAIR_EXCHANGE%%-*}'

%pre
%_pre_useradd %{name} /dev/null /bin/false

%post
%_tmpfilescreate %{name}

%preun
%_preun_service %{name}

%postun
%_postun_userdel %{name}

%files
%doc exchange-XXX_YYY-config.js
%{_unitdir}/%{name}@.service
%{_tmpfilesdir}/%{name}.conf
%attr(-, gunbot, gunbot) %dir /opt/gunbot
%config(noreplace) %attr(-, gunbot, gunbot) /opt/gunbot/ALLPAIRS-params.js
/opt/gunbot/gunthy-*
