%define debug_package %{nil}

Summary:	File and archive manager
Name:		peazip
Version:	7.7.0
Release:	1
License:	LGPLv3+
Group:		File tools
Url:		http://peazip.sourceforge.net/peazip-linux.html
Source0:	http://download.sourceforge.net/%{name}/%{name}-%{version}.src.zip
# configure to run in users home appdata
Source1:	altconf.txt

BuildRequires:	dos2unix
BuildRequires:	icoutils
BuildRequires:	lazarus
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	p7zip
BuildRequires:	unzip

Requires:	p7zip
Requires:	upx >= 3.09

%description
PeaZip is a free cross-platform file archiver that provides an unified portable
GUI for many Open Source technologies like 7-Zip, FreeArc, PAQ, UPX...

%files
%doc readme copying.txt
%{_bindir}/*
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/applications/*.desktop
%{_datadir}/%{name}/

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}.src
chmod +w res/lang
dos2unix readme*

%build
lazbuild --lazarusdir=%{_libdir}/lazarus \
%ifarch %{x86_64}
	--cpu=x86_64 \
%endif
	--widgetset=gtk2 \
	-B project_peach.lpi project_pea.lpi

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/%{name}
rm -rf res/icons
cp -r res %{buildroot}%{_datadir}/%{name}
cp %{SOURCE1} %{buildroot}%{_datadir}/%{name}/res

#install helper apps
mkdir -p %{buildroot}%{_datadir}/%{name}/res/{7z,upx}
ln -s %{_bindir}/7z  %{buildroot}%{_datadir}/%{name}/res/7z
ln -s %{_bindir}/upx  %{buildroot}%{_datadir}/%{name}/res/upx

install pea %{buildroot}%{_datadir}/%{name}/res
ln -s %{_datadir}/%{name}/res/pea %{buildroot}%{_bindir}/pea
install %{name} %{buildroot}%{_datadir}/%{name}
ln -s %{_datadir}/%{name}/%{name} %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_iconsdir}/hicolor/256x256/apps
install -m 0644 FreeDesktop_integration/peazip.png %{buildroot}%{_iconsdir}/hicolor/256x256/apps/%{name}.png
rm -rf %{buildroot}%{_datadir}/%{name}/res/icons

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Encoding=UTF-8
Name=PeaZip
MimeType=application/x-gzip;application/x-lha;application/x-tar;application/x-tgz;application/x-tbz;application/x-tbz2;application/x-zip;application/zip;application/x-bzip;application/x-rar;application/x-tarz;application/x-archive;application/x-bzip2;application/x-jar;application/x-deb;application/x-ace;application/x-7z;application/x-arc;application/x-arj;application/x-compress;application/x-cpio;
Exec=%{name}
Icon=%{name}
Type=Application
Terminal=false
Categories=GTK;KDE;Utility;System;Archiving;
EOF
