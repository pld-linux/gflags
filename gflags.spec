Summary:	A commandline flags library that allows for distributed flags
Summary(pl.UTF-8):	Biblioteka flag linii poleceń pozwalająca na rozproszone flagi
Name:		gflags
Version:	2.1.1
Release:	4
License:	BSD
Group:		Libraries
Source0:	https://github.com/schuhschuh/gflags/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	18acc0ae270672a70a86b33ebbe9761b
Source1:	libgflags.pc
Source2:	libgflags_nothreads.pc
Patch0:		%{name}-libversion.patch
Patch1:		%{name}-nothreads.patch
URL:		http://code.google.com/p/gflags/
BuildRequires:	cmake >= 2.8.4
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
%patch0 -p1
%patch1 -p1

%{__sed} -i \
	-e 's|LIBRARY_INSTALL_DIR lib|LIBRARY_INSTALL_DIR %{_lib}|g' \
	-e 's|CONFIG_INSTALL_DIR  lib/cmake|CONFIG_INSTALL_DIR  %{_lib}/cmake|g' \
	CMakeLists.txt

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

# .pc files used to be provided before gflags 2.1; reintroduce them
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
for f in %{SOURCE1} %{SOURCE2} ; do
	sed -e "s|@prefix@|%{_prefix}|;s|@libdir@|%{_libdir}|" "$f" \
		>$RPM_BUILD_ROOT%{_pkgconfigdir}/$(basename $f)
done

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS.txt COPYING.txt ChangeLog.txt NEWS.txt README.txt
%attr(755,root,root) %{_bindir}/gflags_completions.sh
%attr(755,root,root) %{_libdir}/libgflags.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgflags.so.2
%attr(755,root,root) %{_libdir}/libgflags_nothreads.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgflags_nothreads.so.2

%files devel
%defattr(644,root,root,755)
%doc doc/{gflags.html,designstyle.css}
%attr(755,root,root) %{_libdir}/libgflags.so
%attr(755,root,root) %{_libdir}/libgflags_nothreads.so
%{_includedir}/gflags
%{_pkgconfigdir}/libgflags.pc
%{_pkgconfigdir}/libgflags_nothreads.pc
%{_libdir}/cmake/gflags

%files static
%defattr(644,root,root,755)
%{_libdir}/libgflags.a
%{_libdir}/libgflags_nothreads.a
