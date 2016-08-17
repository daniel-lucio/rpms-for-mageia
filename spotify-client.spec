%global         debug_package %{nil}
%global	        __strip /bin/true

# Remove bundled libraries from requirements/provides
%global         __requires_exclude ^(libcef\\.so.*|libffmpegsumo\\.so.*|libcrypto\\.so\\..*|libssl\\.so\\..*|.*(CURL_OPENSSL_3).*)$
%global         __provides_exclude ^(libcef\\.so.*|libffmpegsumo\\.so.*|libcrypto\\.so\\..*|libssl\\.so\\..*)$

Name:           spotify-client
Summary:        Spotify music player native client
Version:        1.0.19.106.gb8a7150f
Release:        %mkrel 2
License:        https://www.spotify.com/legal/end-user-agreement
URL:            http://www.spotify.com/
Group:          Sound/Players
ExclusiveArch:  x86_64 %{ix86}

Source0:        http://repository.spotify.com/pool/non-free/s/%{name}/%{name}_%{version}_amd64.deb
Source1:        http://repository.spotify.com/pool/non-free/s/%{name}/%{name}_%{version}_i386.deb
# Debian libraries, required by the binaries. Ugh.
Source2:        http://de.archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.0.0_1.0.2d-0ubuntu1_amd64.deb
Source3:        http://de.archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.0.0_1.0.2d-0ubuntu1_i386.deb

Provides:       spotify = %{version}-%{release}
# Libraries linked in the package (no auto require) and Debian libraries
Provides:       bundled(libssl-Debian) = 1.0.0

# Obsoletes old data subpackage
Provides:       spotify-client-data = %{version}-%{release}
Obsoletes:      spotify-client-data < %{version}-%{release}

BuildRequires:  desktop-file-utils
#BuildRequires:  chrpath
Requires:       libffmpeg
Requires:       hicolor-icon-theme
Requires:	zenity

%if 0%{?fedora} >= 21 || 0%{?rhel} >= 8
Requires:       compat-libgcrypt
%endif

# Libraries linked in the package (no auto require) and Debian libraries
Provides:       bundled(libssl-Debian) = 1.0.0

%prep
%setup -q -c -T

%ifarch x86_64
ar x %{SOURCE0}
tar -xzf data.tar.gz
ar x %{SOURCE2}
tar -xJf data.tar.xz
%endif

%ifarch %{ix86}
ar x %{SOURCE1}
tar -xzf data.tar.gz
ar x %{SOURCE3}
tar -xJf data.tar.xz
%endif

# chrpath -d spotify Data/SpotifyHelper

%description
Think of Spotify as your new music collection. Your library. Only this time your
collection is vast: millions of tracks and counting. Spotify comes in all shapes
and sizes, available for your PC, Mac, home audio system and mobile phone.
Wherever you go, your music follows you. And because the music plays live,
there’s no need to wait for downloads and no big dent in your hard drive.

%install
mkdir -p %{buildroot}%{_libdir}/%{name}
cp -frp .%{_datadir}/spotify/* %{buildroot}%{_libdir}/%{name}
rm -fr %{buildroot}%{_libdir}/%{name}/*.{sh,txt,desktop}
chmod +x %{buildroot}%{_libdir}/%{name}/*.so

mkdir -p %{buildroot}%{_bindir}
ln -sf %{_libdir}/%{name}/spotify %{buildroot}%{_bindir}/spotify

install -m 0644 -D -p .%{_datadir}/spotify/spotify.desktop \
    %{buildroot}%{_datadir}/applications/spotify.desktop

# Also leave icons along main executable as they are needed by the client. We
# can't just symlink them or RPM will complain with the broken links.
for size in 16 22 24 32 48 64 128 256 512; do
    install -p -D -m 644 .%{_datadir}/spotify/icons/spotify-linux-${size}.png \
        %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/%{name}.png
done

desktop-file-validate %{buildroot}%{_datadir}/applications/spotify.desktop

# Extra libraries: the binaries expects the libraries along with the main
# "spotify" binary or in the "Data" folder. "SpotifyHelper" expects them only in
# the "Data" folder. So put everything in the "Data" folder.
cp -f ./lib/*-linux-gnu/lib*.so* %{buildroot}%{_libdir}/%{name}/
chmod 0755 %{buildroot}%{_libdir}/%{name}/lib*.so*

%post
%{_bindir}/update-mime-database %{_datadir}/mime &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
%{_bindir}/update-desktop-database &> /dev/null || :

%postun
%{_bindir}/update-mime-database %{_datadir}/mime &> /dev/null || :
%{_bindir}/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    %{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
%{_bindir}/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
%{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc .%{_datadir}/spotify/README.txt
%{_bindir}/spotify
%{_libdir}/%{name}
%{_datadir}/applications/spotify.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

