%define major	4
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d
%ifarch aarch64
%define debug_package	%{nil}
%endif

Summary:	Gets a file from a FTP, GOPHER or HTTP server
Name:		curl
Epoch:		1
Version:	7.48.0
Release:	0.1
License:	BSD-like
Group:		Networking/Other
Url:		http://curl.haxx.se
Source0:	http://curl.haxx.se/download/%{name}-%{version}.tar.lzma
Patch4:		%{name}-7.26.0-multilib.patch
Patch6:		%{name}-7.26.0-do-not-build-examples.patch
BuildRequires:	groff-base
BuildRequires:	stunnel
BuildRequires:	krb5-devel
BuildRequires:	openldap-devel
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libidn)
BuildRequires:	pkgconfig(libssh2)
Provides:	webfetch

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

%package -n %{devname}
Summary:	Header files and static libraries for libcurl
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
libcurl is a library of functions for sending and receiving files through
various protocols, including http and ftp.

You should install this package if you wish to develop applications that
use libcurl.

%package examples
Summary:	Example files for %{name} development
Group:		Development/C
Requires:       %{name}-devel = %{EVRD}
BuildArch:	noarch

%description examples
Example files for %{name} development.

%package -n zsh-curl
Summary:	ZSH completion and functions related to curl
Group:		Networking/Other
Requires:	%{name} = %{EVRD}

%description -n zsh-curl
ZSH completion and functions related to curl

%prep
%setup -q
%apply_patches

%build
autoreconf -fiv

%configure \
	--disable-static \
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


%make

# we don't want them in curl-examples:
rm -r docs/examples/.deps ||:

# disable tests that want to connect/run sshd, which is quite impossible
#%check
# Some tests fail at random inside ABF (timeouts?), but work in local builds.
# Let's make a test failure non-fatal for the moment.
#make test TEST_Q='-a -p -v !SCP !SFTP !SOCKS4 !SOCKS5 !TFTP !198' || :

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

%files
%{_bindir}/curl
%{_mandir}/man1/curl.1*

%files -n %{libname}
%{_libdir}/libcurl.so.%{major}*

%files -n %{devname}
%docdir docs/
%doc docs/BUGS docs/KNOWN_BUGS docs/CONTRIBUTE docs/FAQ CHANGES
%doc docs/FEATURES docs/RESOURCES docs/TODO docs/THANKS docs/INTERNALS
%{_bindir}/curl-config
%{multiarch_bindir}/curl-config
%{_libdir}/libcurl.so
%{_includedir}/curl
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/*.m4
%{_mandir}/man1/curl-config.1*
%{_mandir}/man3/*

%files examples
%doc docs/examples

%files -n zsh-curl
%{_datadir}/zsh/site-functions/_curl
