#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	ARIB STD-B24 library
Summary(pl.UTF-8):	Biblioteka ARIB STD-B24
Name:		aribb24
Version:	1.0.3
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/nkoriyama/aribb24/releases
Source0:	https://github.com/nkoriyama/aribb24/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	5ef0a6d1d72f294666ee1489b7ebb8c5
Patch0:		%{name}-pc.patch
Patch1:		link-libm.patch
URL:		https://github.com/nkoriyama/aribb24
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake
BuildRequires:	libpng-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A library for ARIB STD-B24, decoding JIS 8-bit characters and parsing
MPEG-TS stream.

%description -l pl.UTF-8
Biblioteka ARIB STD-B24, służąca do dekodowania 8-bitowych znaków JIS
oraz analizy strumieni MPEG-TS.

%package devel
Summary:	Header files for ARIB STD-B24 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ARIB STD-B24
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libpng-devel

%description devel
Header files for ARIB STD-B24 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ARIB STD-B24.

%package static
Summary:	Static ARIB STD-B24 library
Summary(pl.UTF-8):	Statyczna biblioteka ARIB STD-B24
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ARIB STD-B24 library.

%description static -l pl.UTF-8
Statyczna biblioteka ARIB STD-B24.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	%{?with_static_libs:--enable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libaribb24.la
# COPYING is just GPL text, the rest packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/aribb24/{COPYING,README.md}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libaribb24.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libaribb24.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libaribb24.so
%{_includedir}/aribb24
%{_pkgconfigdir}/aribb24.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libaribb24.a
%endif
