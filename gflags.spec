Summary:	A commandline flags library that allows for distributed flags
Summary(pl.UTF-8):	Biblioteka flag linii poleceń pozwalająca na rozproszone flagi
Name:		gflags
Version:	1.5
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: http://code.google.com/p/google-gflags/downloads/list
Source0:	http://google-gflags.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	0e66a83014efcd395d936c7fb7e71fd8
URL:		http://code.google.com/p/google-gflags/
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gflags is Google's commandline flags library. It differs from other
libraries, such as getopt(), in that flag definitions can be scattered
around the source code, and not just listed in one place such as
main().

%description -l pl.UTF-8
gflags to biblioteka flag linii poleceń stworzona przez Google. Różni
się od innych bibliotek, takich jak getopt(), tym, że definicje flag
mogą być rozproszone po kodzie źródłowym, a nie wypisane tylko w
jednym miejscu, takim jak main().

%package devel
Summary:	Header files for gflags library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki gflags
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for gflags library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki gflags.

%package static
Summary:	Static gflags library
Summary(pl.UTF-8):	Statyczna biblioteka gflags
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static gflags library.

%description static -l pl.UTF-8
Statyczna biblioteka gflags.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
# <google/gflags*.h> inclusion is obsolete, directory belongs to other package
%{__rm} -r $RPM_BUILD_ROOT%{_includedir}/google

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/gflags_completions.sh
%attr(755,root,root) %{_libdir}/libgflags.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgflags.so.0
%attr(755,root,root) %{_libdir}/libgflags_nothreads.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgflags_nothreads.so.0

%files devel
%defattr(644,root,root,755)
%doc doc/{gflags.html,designstyle.css}
%attr(755,root,root) %{_libdir}/libgflags.so
%attr(755,root,root) %{_libdir}/libgflags_nothreads.so
%{_includedir}/gflags
%{_pkgconfigdir}/libgflags.pc
%{_pkgconfigdir}/libgflags_nothreads.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libgflags.a
%{_libdir}/libgflags_nothreads.a
