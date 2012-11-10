# TODO: allow to use systemd-enabled version without systemd running
#
# Conditional build:
%bcond_without	systemd		# systemd-based multi-seat support
%bcond_without	udev		# udev-based hotplug support
%bcond_without	unifont		# Unifont backend (could make kmscon GPLed)
%bcond_with	wayland		# wayland-based wlterm [needs update for wayland 1.0]
#
Summary:	Simple terminal emulator based on Linux Kernel Mode Setting (KMS)
Summary(pl.UTF-8):	Prosty emulator terminala oparty na linuksowym KMS (Kernel Mode Setting)
Name:		kmscon
Version:	5
Release:	1
License:	MIT (code), GPL (Unifont)
Group:		Applications/Terminal
#Source0Download: https://github.com/dvdhrm/kmscon/downloads
Source0:	https://github.com/downloads/dvdhrm/kmscon/%{name}-%{version}.tar.bz2
# Source0-md5:	d35014947a468d1a5e633d4221d2e4fa
Patch0:		%{name}-xkbcommon.patch
Patch1:		%{name}-link.patch
Patch2:		%{name}-format.patch
URL:		https://github.com/dvdhrm/kmscon/wiki/KMSCON
BuildRequires:	Mesa-libEGL-devel
BuildRequires:	Mesa-libGLES-devel
BuildRequires:	Mesa-libgbm-devel
BuildRequires:	autoconf >= 2.68
BuildRequires:	automake >= 1:1.11
BuildRequires:	dbus-devel
BuildRequires:	freetype-devel >= 2
BuildRequires:	libdrm-devel
BuildRequires:	libtool >= 2:2.2
BuildRequires:	pango-devel
BuildRequires:	pkgconfig
%{?with_systemd:BuildRequires:	systemd-devel}
BuildRequires:	udev-devel
# wayland-client wayland-server wayland-cursor
%{?with_wayland:BuildRequires:	wayland-devel}
BuildRequires:	xorg-lib-libxkbcommon-devel >= 0.2.0
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# log symbols in convenience libkmscon_core.la/main
%define		skip_post_check_so	libuterm.so.*

%description
Kmscon is a simple terminal emulator based on Linux kernel mode
setting (KMS). It is an attempt to replace the in-kernel VT
implementation with a userspace console.

%description -l pl.UTF-8
Kmscon to prosty emulator terminala oparty na linuksowym KMS (kernel
mode setting - ustawianiu trybów w jądrze). Jest to próba zastąpienia
implementacji VT z jądra konsolą w przestrzeni użytkownika.

%package libs
Summary:	Kmscon libraries
Summary(pl.UTF-8):	Biblioteki kmscon
Group:		Libraries

%description libs
Kmscon libraries.

%description libs -l pl.UTF-8
Biblioteki kmscon.

%package devel
Summary:	Header files for kmscon libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek kmscon
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for kmscon libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek kmscon.

%package static
Summary:	Static kmscon libraries
Summary(pl.UTF-8):	Statyczne biblioteki kmscon
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static kmscon libraries.

%description static -l pl.UTF-8
Statyczne biblioteki kmscon.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_systemd:--disable-systemd} \
	%{!?with_udev:--disable-udev} \
	%{?with_unifont:--enable-unifont} \
	%{?with_wayland:--enable-wlterm}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# keeping *.la because of missing all external dependencies in *.pc

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING NEWS README
%attr(755,root,root) %{_bindir}/kmscon

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libeloop.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libeloop.so.1
%attr(755,root,root) %{_libdir}/libtsm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtsm.so.1
%attr(755,root,root) %{_libdir}/libuterm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libuterm.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libeloop.so
%attr(755,root,root) %{_libdir}/libtsm.so
%attr(755,root,root) %{_libdir}/libuterm.so
%{_libdir}/libeloop.la
%{_libdir}/libtsm.la
%{_libdir}/libuterm.la
%{_includedir}/eloop.h
%{_includedir}/tsm_*.h
%{_includedir}/uterm.h
%{_pkgconfigdir}/libeloop.pc
%{_pkgconfigdir}/libtsm.pc
%{_pkgconfigdir}/libuterm.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libeloop.a
%{_libdir}/libtsm.a
%{_libdir}/libuterm.a
