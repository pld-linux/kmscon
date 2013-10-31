# TODO
# - allow to use systemd-enabled version without systemd running
# - modules can be put to subpackages
#
# Conditional build:
%bcond_without	systemd		# systemd-based multi-seat support
%bcond_without	udev		# udev-based hotplug support
%bcond_without	unifont		# Unifont backend (could make kmscon GPLed)

Summary:	Simple terminal emulator based on Linux Kernel Mode Setting (KMS)
Summary(pl.UTF-8):	Prosty emulator terminala oparty na linuksowym KMS (Kernel Mode Setting)
Name:		kmscon
Version:	8
Release:	1
License:	MIT (code), GPL (Unifont)
Group:		Applications/Terminal
Source0:	http://www.freedesktop.org/software/kmscon/releases/%{name}-%{version}.tar.xz
# Source0-md5:	90d39c4ef53a11c53f27be4a7e9acee4
Patch1:		%{name}-link.patch
URL:		http://www.freedesktop.org/wiki/Software/kmscon/
BuildRequires:	Mesa-libEGL-devel
# glesv2
BuildRequires:	Mesa-libGLES-devel
BuildRequires:	Mesa-libgbm-devel
BuildRequires:	autoconf >= 2.68
BuildRequires:	automake >= 1:1.11
BuildRequires:	libdrm-devel
BuildRequires:	libtsm-devel
BuildRequires:	libtool >= 2:2.2
BuildRequires:	pango-devel
BuildRequires:	pixman-devel
BuildRequires:	pkgconfig
%{?with_systemd:BuildRequires:	systemd-devel}
BuildRequires:	udev-devel >= 1:172
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libxkbcommon-devel >= 0.2.0
BuildRequires:	xz
Requires:	udev-libs >= 1:172
Obsoletes:	kmscon-devel
Obsoletes:	kmscon-libs
Obsoletes:	kmscon-static
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

%prep
%setup -q
%patch1 -p1

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
	%{?with_unifont:--enable-unifont}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# modules dlopened, so static modules do not make sense
%{__rm} $RPM_BUILD_ROOT%{_libdir}/kmscon/mod-*.a
%{__rm} $RPM_BUILD_ROOT%{_libdir}/kmscon/mod-*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING NEWS README
%attr(755,root,root) %{_bindir}/kmscon
%{_mandir}/man1/kmscon.1*
%dir %{_libdir}/kmscon
%attr(755,root,root) %{_libdir}/kmscon/mod-bbulk.so
%attr(755,root,root) %{_libdir}/kmscon/mod-gltex.so
%attr(755,root,root) %{_libdir}/kmscon/mod-pango.so
%attr(755,root,root) %{_libdir}/kmscon/mod-unifont.so
