%define product_name leechcraft
%define plugin_dir %{_libdir}/%{product_name}/plugins
%define translations_dir %{_datadir}/%{product_name}/translations
%define settings_dir %{_datadir}/%{product_name}/settings
%define full_version %{version}-%{release}

Name:           leechcraft-bittorrent
Summary:        BitTorrent Client for LeechCraft
Version:        0.6.70
Release:        1%{?dist}
License:        GPLv2+
Url:            http://leechcraft.org
Source0:        http://dist.leechcraft.org/LeechCraft/0.6.70/leechcraft-0.6.70.tar.xz 


BuildRequires: cmake
BuildRequires: boost-devel
BuildRequires: qt4-devel
BuildRequires: qt-webkit-devel
BuildRequires: bzip2-devel
BuildRequires: qwt-devel
BuildRequires: pcre-devel
BuildRequires: rb_libtorrent-devel
BuildRequires: leechcraft-devel >= %{version}


%description
BitTorrent Client for LeechCraft.


%prep
%setup -qn %{product_name}-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DLEECHCRAFT_VERSION="%{version}" \
    $(cat ../src/CMakeLists.txt | egrep "^option \(ENABLE" | awk '{print $2}' | sed 's/(//g;s/.*/-D\0=False/g;s/TORRENT=False/TORRENT=True/g' | xargs) \
    $(cat ../src/CMakeLists.txt | grep cmake_dependent_option | grep ENABLE | awk '{print $2}' | sed 's/(//g;s/.*/-D\0=False/g' | xargs) \
    ../src

cd plugins/bittorrent
make %{?_smp_mflags} 
popd


%install
rm -rf $RPM_BUILD_ROOT
cd %{_target_platform}/plugins/bittorrent/
make install/fast DESTDIR=$RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files

%changelog
* Thu Dec 26 2014 Minh Ngo <minh@fedoraproject.org> - 0.6.70-1
- 0.6.70

