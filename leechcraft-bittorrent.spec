%define product_name leechcraft
%define plugin_dir %{_libdir}/%{product_name}/plugins-qt5
%define translations_dir %{_datadir}/%{product_name}/translations
%define settings_dir %{_datadir}/%{product_name}/settings
%define full_version %{version}-%{release}
%define git_version 3466-g864bd1a
%global optflags %(echo %{optflags} | sed 's/-D_FORTIFY_SOURCE=2 //')

Name:           leechcraft-bittorrent
Summary:        BitTorrent Client for LeechCraft
Version:        0.6.75
Release:        1%{?dist}
License:        GPLv2+
Url:            http://leechcraft.org
Source0:        http://dist.leechcraft.org/LeechCraft/%{version}/leechcraft-0.6.70-%{git_version}.tar.xz
Patch1:         001-fix-qwt-cmake-script.patch


BuildRequires: cmake
BuildRequires: boost-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qtwebkit-devel
BuildRequires: qt5-qtx11extras-devel
BuildRequires: qt5-qtscript-devel
BuildRequires: qt5-qttools-devel
BuildRequires: bzip2-devel
BuildRequires: qwt-qt5-devel
BuildRequires: pcre-devel
BuildRequires: rb_libtorrent-devel
BuildRequires: leechcraft-devel >= %{version}
BuildRequires: clang


%description
BitTorrent Client for LeechCraft.


%prep
%setup -qn %{product_name}-0.6.70-%{git_version}
%patch1 -p 0


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DLEECHCRAFT_VERSION="%{version}" \
    -DUSE_QT5=True \
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++ \
    $(cat ../src/CMakeLists.txt | egrep "^(cmake_dependent_)?option \(ENABLE" | awk '{print $2}' | sed 's/^(/-D/;s/$/=False/;s/TORRENT=False/TORRENT=True/' | xargs) \
    ../src

cd plugins/bittorrent
make %{?_smp_mflags} 
popd

%install
rm -rf $RPM_BUILD_ROOT
pushd %{_target_platform}/plugins/bittorrent/
make install/fast DESTDIR=$RPM_BUILD_ROOT
popd
%find_lang leechcraft_bittorrent  --with-qt --without-mo


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f leechcraft_bittorrent.lang
%{plugin_dir}/libleechcraft_*.so
%{settings_dir}/*.xml
%{_datadir}/applications/leechcraft-bittorrent-qt5.desktop

%changelog
* Sat Dec 30 2015 Minh Ngo <minh@fedoraproject.org> - 0.6.75-1
- 0.6.75-1, Qt5

* Fri Dec 26 2014 Minh Ngo <minh@fedoraproject.org> - 0.6.70-1
- 0.6.70-1

