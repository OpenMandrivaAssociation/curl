%define name curl
%define version 7.16.0
%define release %mkrel 9
%define major 4
%define libname %mklibname %{name} %{major}

# Define to make check (default behavior)
%define do_check 1

%define __libtoolize /bin/true

# Enable --with[out] <feature> at rpm command line
%{?_with_CHECK: %{expand: %%define do_check 1}}
%{?_without_CHECK: %{expand: %%define do_check 0}}

Summary: Gets a file from a FTP, GOPHER or HTTP server
Name: %{name}
Version: %{version}
Release: %{release}
Epoch: 1
License: MIT
Group: Networking/Other
Source: http://curl.haxx.se/download/%{name}-%{version}.tar.bz2
Patch1: curl-7.10.4-compat-location-trusted.patch
Patch2: curl-7.13.0-64bit-fixes.patch
Patch3: curl-7.16.0-easy_magic.patch
Patch4: curl-7.16.0-fix-tests.patch
Patch5: curl-7.16.0-error-reporting.patch
URL: http://curl.haxx.se/
Provides: webfetch
Requires: %{libname} = %{epoch}:%{version}
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
BuildRequires: bison
BuildRequires: groff-for-man
BuildRequires: openssl-devel
BuildRequires: zlib-devel
BuildRequires: libidn-devel
# (misc) required for testing
BuildRequires: stunnel

%description
curl is a client to get documents/files from servers, using any of the
supported protocols. The command is designed to work without user
interaction or any kind of interactivity.

curl offers a busload of useful tricks like proxy support, user
authentication, ftp upload, HTTP post, file transfer resume and more.

This version is compiled with SSL (https) support.

%package -n %{libname}
Summary: A library of functions for file transfer
Group: Networking/Other
Provides: curl-lib = %{epoch}:%{version}-%{release}
Obsoletes: curl-lib

%description  -n %{libname}
libcurl is a library of functions for sending and receiving files through
various protocols, including http and ftp.

You should install this package if you plan to use any applications that
use libcurl.

%package -n %{libname}-devel
Summary: Header files and static libraries for libcurl
Group: Development/C
Requires: %{libname} = %{epoch}:%{version}
Provides: %{name}-devel = %{epoch}:%{version}-%{release}, lib%{name}-devel
Provides: libcurl%{major}-devel
Obsoletes: %{name}-devel
Obsoletes: %mklibname -d curl 3

%description -n %{libname}-devel
libcurl is a library of functions for sending and receiving files through
various protocols, including http and ftp.

You should install this package if you wish to develop applications that
use libcurl.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1
%patch3 -p1 -b .easy_magic
%patch4 -p1 -b .fix-tests
%patch5 -p1 -b .error-reporting

%if 0
%patch2 -p1 -b .64bit-fixes
# fix test517 with correct results according to curl_getdate() specs
cat > ptrsize.c << EOF
#include <time.h>
#include <stdio.h>
int main(void)
{
  printf("%d\n", sizeof(time_t));
  return 0;
}
EOF
%{__cc} -o ptrsize ptrsize.c
case `./ptrsize` in
4) ;;
8) mv -f ./tests/data/test517{.64,} ;;
*) exit 1 ;;
esac
%endif

%build
export LIBS="-L%{_libdir} $LIBS"
CFLAGS="$RPM_OPT_FLAGS -O0" \
	./configure \
	--prefix=%{_prefix} \
	--mandir=%{_mandir} \
	--datadir=%{_datadir} \
	--libdir=%{_libdir} \
	--includedir=%{_includedir} \
	--with-ssl
%make

skip_tests=
[ -n "$skip_tests" ] && {
  mkdir ./tests/data/skip/
  for t in $skip_tests; do
    mv ./tests/data/test$t ./tests/data/skip/
  done
}


%check 
%if %{do_check}
# At this stage, all tests must pass
make check
%endif

%install
rm -rf $RPM_BUILD_ROOT
%make install DESTDIR="$RPM_BUILD_ROOT"

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/curl
%attr(0644,root,root) %{_mandir}/man1/curl.1*
%{_datadir}/curl
%docdir docs/

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libcurl.so.%{major}*
%docdir docs/
%doc docs/BUGS docs/KNOWN_BUGS docs/CONTRIBUTE docs/FAQ CHANGES
%doc docs/FEATURES docs/RESOURCES docs/TODO docs/THANKS

%files -n %{libname}-devel
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/curl-config
%attr(0644,root,root) %{_mandir}/man1/curl-config.1*
%{_libdir}/libcurl.so
%{_includedir}/curl
%{_libdir}/libcurl*a
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*
%doc docs/examples docs/INTERNALS


