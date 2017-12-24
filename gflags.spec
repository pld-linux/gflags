Summary:	A commandline flags library that allows for distributed flags
Summary(pl.UTF-8):	Biblioteka flag linii poleceń pozwalająca na rozproszone flagi
Name:		gflags
Version:	2.2.1
Release:	2
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/gflags/gflags/releases
Source0:	https://github.com/schuhschuh/gflags/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b98e772b4490c84fc5a87681973f75d1
Patch0:		%{name}-pc-nothreads.patch
URL:		http://gflags.github.io/gflags/
BuildRequires:	cmake >= 2.8.12
BuildRequires:	libstdc++-devel
BuildRequires:	sed >= 4.0
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
%patch0 -p1

%build
install -d build
cd build
%cmake .. \
	-DBUILD_STATIC_LIBS=ON
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# disable completeness check incompatible with split packaging
%{__sed} -i -e '/^foreach(target .*IMPORT_CHECK_TARGETS/,/^endforeach/d' $RPM_BUILD_ROOT%{_libdir}/cmake/gflags/gflags-targets.cmake

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS.txt COPYING.txt ChangeLog.txt README.md
%attr(755,root,root) %{_bindir}/gflags_completions.sh
%attr(755,root,root) %{_libdir}/libgflags.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgflags.so.2.2
%attr(755,root,root) %{_libdir}/libgflags_nothreads.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgflags_nothreads.so.2.2

%files devel
%defattr(644,root,root,755)
# not present in 2.2.0
#%doc doc/{index.html,designstyle.css}
%attr(755,root,root) %{_libdir}/libgflags.so
%attr(755,root,root) %{_libdir}/libgflags_nothreads.so
%{_includedir}/gflags
%{_pkgconfigdir}/gflags.pc
%{_pkgconfigdir}/gflags_nothreads.pc
%{_libdir}/cmake/gflags

%files static
%defattr(644,root,root,755)
%{_libdir}/libgflags.a
%{_libdir}/libgflags_nothreads.a
