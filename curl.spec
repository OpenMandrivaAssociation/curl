%define major 4
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Gets a file from a FTP, GOPHER or HTTP server
Name:		curl
Version:	7.28.1
Release:	2
Epoch:		1
License:	BSD-like
Group:		Networking/Other
URL:		http://curl.haxx.se
Source0:	http://curl.haxx.se/download/%{name}-%{version}.tar.lzma
Source1:	http://curl.haxx.se/download/%{name}-%{version}.tar.lzma.asc
Patch2:		curl-7.28.1-automake-1.13.patch
Patch3:		%{name}-7.27.0-privlibs.patch
Patch4:		%{name}-7.26.0-multilib.patch
Patch6:		%{name}-7.26.0-do-not-build-examples.patch
BuildRequires:	groff-for-man
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libidn)
BuildRequires:	pkgconfig(libssh2)
BuildRequires:	openldap-devel
BuildRequires:	krb5-devel
#BuildRequires:	c-ares-devel
# (misc) required for testing
BuildRequires:	stunnel
Provides:	webfetch
Requires:	%{libname} = %{EVRD}

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
Requires:	rootcerts >= 1:20070713.00

%description -n %{libname}
libcurl is a library of functions for sending and receiving files through
various protocols, including http and ftp.

You should install this package if you plan to use any applications that
use libcurl.

%package -n %{develname}
Summary:	Header files and static libraries for libcurl
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	lib%{name}-devel = %{EVRD}
Provides:	libcurl%{major}-devel = %{EVRD}
Obsoletes:	%{mklibname %{name} 4 -d} < %{version}
Provides:	%mklibname %{name} 4 -d

%description -n %{develname}
libcurl is a library of functions for sending and receiving files through
various protocols, including http and ftp.

You should install this package if you wish to develop applications that
use libcurl.

%package examples
Summary:	Example files for %{name} development
Group:		Development/C
Requires:       %{name}-devel = %{epoch}:%{version}-%{release}
BuildArch:	noarch

%description examples
Example files for %{name} development.

%prep
%setup -q
%patch2 -p1 -b .am113~
%patch3 -p1 -b .privlib~
%patch4 -p1 -b .multilib~
%patch6 -p1 -b .examples~

%build
autoreconf -fiv

%configure2_5x \
%if %{mdvver} >= 201200
	--disable-static \
%endif
	--with-ssl \
	--without-gnutls \
	--with-zlib \
	--with-lber-lib=lber \
	--with-libidn \
	--with-ssh2 \
	--with-random \
	--enable-hidden-symbols \
	--enable-optimize \
	--enable-nonblocking \
	--enable-thread \
	--enable-crypto-auth \
	--enable-libgcc \
	--enable-ldaps \
	--enable-ipv6 \
	--with-ca-bundle=%{_sysconfdir}/pki/tls/certs/ca-bundle.crt \
	--with-gssapi=%{_prefix} \
	--disable-ares

# we don't want them in curl-examples:
rm -r docs/examples/.deps

%make

# disable tests that want to connect/run sshd, which is quite impossible
%check
# Some tests fail at random inside ABF (timeouts?), but work in local builds.
# Let's make a test failure non-fatal for the moment.
make test TEST_Q='-a -p -v !SCP !SFTP !SOCKS4 !SOCKS5 !TFTP !198' || :

%install
%makeinstall_std

# [july 2008] HACK. to be replaced by a real fix
sed -i -e 's!-Wl,--as-needed!!' -e 's!-Wl,--no-undefined!!' %{buildroot}%{_bindir}/%{name}-config
sed -i -e 's!-Wl,--as-needed!!' -e 's!-Wl,--no-undefined!!' %{buildroot}%{_libdir}/pkgconfig/*.pc

%multiarch_binaries %{buildroot}%{_bindir}/%{name}-config

# (tpg) use rootcerts's certificates #35917
find %{buildroot} -name ca-bundle.crt -exec rm -f '{}' \;

# we don't package mk-ca-bundle so we don't need man for it
rm -f %{buildroot}%{_mandir}/man1/mk-ca-bundle.1*

# nuke the static lib
rm -f %{buildroot}%{_libdir}/*.a

%files
%{_bindir}/curl
%{_mandir}/man1/curl.1*

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%docdir docs/
%doc docs/BUGS docs/KNOWN_BUGS docs/CONTRIBUTE docs/FAQ CHANGES
%doc docs/FEATURES docs/RESOURCES docs/TODO docs/THANKS docs/INTERNALS
%{_bindir}/curl-config
%{multiarch_bindir}/curl-config
%{_libdir}/libcurl.so
%if %{mdvver} < 201200
%{_libdir}/libcurl.la
%endif
%{_includedir}/curl
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/curl-config.1*
%{_mandir}/man3/*

%files examples
%doc docs/examples
