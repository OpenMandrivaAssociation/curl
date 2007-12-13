%define major 4
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name}-devel

Summary:	Gets a file from a FTP, GOPHER or HTTP server
Name:		curl
Version:	7.17.1
Release:	%mkrel 5
Epoch:		1
License:	MIT
Group:		Networking/Other
URL:		http://curl.haxx.se
Source:		http://curl.haxx.se/download/%{name}-%{version}.tar.bz2
Patch1:		curl-7.10.4-compat-location-trusted.patch
Provides:	webfetch
Requires:	%{libname} = %{epoch}:%{version}
BuildRequires:	groff-for-man
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRequires:	libidn-devel
BuildRequires:	libssh2-devel
BuildRequires:	openldap-devel
# (misc) required for testing
BuildRequires:	stunnel
Requires:	rootcerts
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
curl is a client to get documents/files from servers, using any of the
supported protocols. The command is designed to work without user
interaction or any kind of interactivity.

curl offers a busload of useful tricks like proxy support, user
authentication, ftp upload, HTTP post, file transfer resume and more.

This version is compiled with SSL (https) support.

%package -n %{libname}
Summary:	A library of functions for file transfer
Group:		Networking/Other

%description -n %{libname}
libcurl is a library of functions for sending and receiving files through
various protocols, including http and ftp.

You should install this package if you plan to use any applications that
use libcurl.

%package -n %{develname}
Summary:	Header files and static libraries for libcurl
Group:		Development/C
Requires:	%{libname} = %{epoch}:%{version}
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	lib%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	libcurl%{major}-devel = %{epoch}:%{version}-%{release}
Obsoletes:	%{name}-devel
Obsoletes:	%mklibname %{name} 4 -d
Provides:	%mklibname %{name} 4 -d

%description -n %{develname}
libcurl is a library of functions for sending and receiving files through
various protocols, including http and ftp.

You should install this package if you wish to develop applications that
use libcurl.

%package examples
Summary:	Example files for %{name} development
Group:		Development/C
Requires:	%{develname} = %{epoch}:%{version}-%{release}

%description examples
Example files for %{name} development.

%prep
%setup -q
%patch1 -p1

%build
%configure2_5x \
	--with-ssl \
	--with-zlib \
	--with-libidn \
	--with-ssh2 \
	--with-random \
	--enable-hidden-symbols \
	--enable-libgcc \
	--enable-ldaps \
	--with-ca-bundle=%{_sysconfdir}/pki/tls/certs/ca-bundle.crt
%make

# disable tests that want to connect/run sshd, which is quite impossible
%check
make test TEST_Q='-a -p !SCP !SFTP !SOCKS4 !SOCKS5'

%install
rm -rf %{buildroot}
%makeinstall_std

rm -rf docs/examples/.libs
rm -rf docs/examples/.deps
rm -rf docs/examples/*.o

# (tpg) use rootcerts's certificates
find %{buildroot} -name ca-bundle.crt -exec rm -f '{}' \;

%clean
rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/curl
%{_mandir}/man1/curl.1*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%docdir docs/
%doc docs/BUGS docs/KNOWN_BUGS docs/CONTRIBUTE docs/FAQ CHANGES
%doc docs/FEATURES docs/RESOURCES docs/TODO docs/THANKS docs/INTERNALS
%{_bindir}/curl-config
%{_libdir}/libcurl.so
%{_includedir}/curl
%{_libdir}/libcurl*a
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/curl-config.1*
%{_mandir}/man3/*

%files examples
%defattr(-,root,root,644)
%doc docs/examples
