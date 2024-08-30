%define debug_package %{nil}

Summary:	File and archive manager
Name:		peazip
Version:	9.9.1
Release:	1
License:	LGPLv3+
Group:		File tools
Url:		https://peazip.sourceforge.net/peazip-linux.html
Source0:	https://download.sourceforge.net/%{name}/%{name}-%{version}.src.zip
# configure to run in users home appdata
Source1:	altconf.txt
# remove metadark dep as per instructions as it is unused on linux
Patch1:		metadark.patch
# use qt5 workarounds on qt6 to avoid crashes
Patch2:		qt6.patch
BuildRequires:	dos2unix
BuildRequires:	icoutils
BuildRequires:	lazarus
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	pkgconfig(libbrotlicommon)
BuildRequires:	7zip
BuildRequires:	unzip

Requires:	7zip
Requires:	upx
Requires:	brotli
Requires:	zstd


%description
PeaZip is a free cross-platform file archiver that provides an unified portable
GUI for many Open Source technologies like 7-Zip, FreeArc, PAQ, UPX...

%files
%{_bindir}/*
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/applications/*.desktop
%{_datadir}/%{name}/

#----------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-%{version}.src
#chmod +w ../res/lang
dos2unix readme*

%build
pushd dev
lazbuild --lazarusdir=%{_libdir}/lazarus \
%ifarch %{x86_64}
	--cpu=x86_64 \
%endif
	--widgetset=qt6 \
	-B project_peach.lpi project_pea.lpi

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/%{name}/res
rm -rf res/icons
cp -r res/share %{buildroot}%{_datadir}/%{name}/res
cp -r res/conf %{buildroot}%{_datadir}/%{name}/res
cp %{SOURCE1} %{buildroot}%{_datadir}/%{name}/res

#install helper apps
mkdir -p %{buildroot}%{_datadir}/%{name}/res/bin/{7z,upx}
ln -s %{_bindir}/7z  %{buildroot}%{_datadir}/%{name}/res/bin/7z/7z
ln -s %{_bindir}/upx  %{buildroot}%{_datadir}/%{name}/res/bin/upx/upx

install dev/pea %{buildroot}%{_datadir}/%{name}/res
ln -s %{_datadir}/%{name}/res/pea %{buildroot}%{_bindir}/pea
install dev/%{name} %{buildroot}%{_datadir}/%{name}
ln -s %{_datadir}/%{name}/%{name} %{buildroot}%{_bindir}/%{name}

#mkdir -p %{buildroot}%{_iconsdir}/hicolor/256x256/apps
#install -m 0644 FreeDesktop_integration/peazip.png %{buildroot}%{_iconsdir}/hicolor/256x256/apps/%{name}.png
#rm -rf %{buildroot}%{_datadir}/%{name}/res/icons

mkdir -p %{buildroot}%{_iconsdir}/hicolor/256x256/apps
pushd dev
icotool -x -i 1 -o %{buildroot}%{_iconsdir}/hicolor/256x256/apps/%{name}.png %{name}.ico

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
