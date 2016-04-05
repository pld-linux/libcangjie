#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Library implementing the Cangjie input method
Summary(pl.UTF-8):	Biblioteka implementująca metodę wprowadzania znaków Cangjie
Name:		libcangjie
Version:	1.3
Release:	1
License:	LGPL v3+
Group:		Libraries
#Source0Download: https://github.com/Cangjians/libcangjie/releases
Source0:	https://github.com/Cangjians/libcangjie/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	e50ed193b0e82b07d2d32ee6e62720b9
URL:		https://github.com/Cangjians/libcangjie
BuildRequires:	pkgconfig
BuildRequires:	sqlite3-devel >= 3
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a C library implementing the Cangjie input method (for
Chinese).

%description -l pl.UTF-8
Ten pakiet zawiera bibliotekę C z implementacją metody wprowadzania
znaków chińskich Cangjie.

%package devel
Summary:	Header files for libcangjie library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libcangjie
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	sqlite3-devel >= 3

%description devel
Header files for libcangjie library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libcangjie.

%package static
Summary:	Static libcangjie library
Summary(pl.UTF-8):	Statyczna biblioteka libcangjie
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libcangjie library.

%description static -l pl.UTF-8
Statyczna biblioteka libcangjie.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libcangjie.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md
%attr(755,root,root) %{_bindir}/libcangjie_bench
%attr(755,root,root) %{_bindir}/libcangjie_cli
%attr(755,root,root) %{_bindir}/libcangjie_dbbuilder
%attr(755,root,root) %{_libdir}/libcangjie.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcangjie.so.2
%{_datadir}/libcangjie

%files devel
%defattr(644,root,root,755)
%doc docs/*.md
%attr(755,root,root) %{_libdir}/libcangjie.so
%{_includedir}/cangjie
%{_pkgconfigdir}/cangjie.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcangjie.a
%endif
