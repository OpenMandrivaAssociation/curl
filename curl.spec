# curl is used by steam
# We don't need all the different crypto providers for the 32bit
# builds though - one will do.
# Let's go with openssl because it's the most common.
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

%global optflags %{optflags} -Oz

%define major 4
%define libname %mklibname %{name}
%define gnutlsname %mklibname %{name}-gnutls
%define mbedtlsname %mklibname %{name}-mbedtls
%define devname %mklibname %{name} -d
%define gnutlsdev %mklibname %{name}-gnutls -d
%define mbedtlsdev %mklibname %{name}-mbedtls -d
%define devstatic %mklibname %{name} -d -s
%define gnutlsstatic %mklibname %{name}-gnutls -d -s
%define mbedtlsstatic %mklibname %{name}-mbedtls -d -s
%define lib32name libcurl%{major}
%define dev32name libcurl-devel

%bcond_without openssl
%bcond_without gnutls
%bcond_without mbedtls

%global ssl_implementations %{nil}
%if %{with mbedtls}
%global ssl_implementations %{ssl_implementations} mbedtls
%endif
%if %{with gnutls}
%global ssl_implementations %{ssl_implementations} gnutls
%endif
%if %{with openssl}
%global ssl_implementations %{ssl_implementations} openssl
%endif

Summary:	Gets a file from a FTP, GOPHER or HTTP server
Name:		curl
Version:	8.13.0
Release:	1
License:	BSD-like
Group:		Networking/Other
Url:		https://curl.haxx.se
Source0:	https://curl.haxx.se/download/%{name}-%{version}.tar.xz
# (tpg) patches from OpenSuse
# (tpg) temp disable it unless Suse will publish new version of this patch
# Patch0:		libcurl-ocloexec.patch
Patch1:		dont-mess-with-rpmoptflags.diff
# (tpg) from Debian
Patch2:		04_workaround_as_needed_bug.patch
Patch3:		curl-mbedtls-no-Llib.patch
Patch4:		%{name}-7.26.0-multilib.patch
# Try to be binary compatible with ancient versions
# used by non-free games such as Civilization Beyond Earth
#Patch5:		curl-7.66.0-CURL_GNUTLS_3.patch

BuildRequires:	groff-base
BuildRequires:	stunnel
BuildRequires:	patchelf
BuildRequires:	pkgconfig(krb5-gssapi)
# (tpg) we prefer OpenSSL over GnuTLS or nettle
BuildRequires:	pkgconfig(openssl)
# (bero) let's also build the gnutls version for
# compatibility with some binaries
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(nettle)
BuildRequires:	mbedtls-devel
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libbrotlidec)
BuildRequires:	pkgconfig(libidn2)
BuildRequires:	pkgconfig(libssh)
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	pkgconfig(libnghttp2)
BuildRequires:	pkgconfig(libpsl)
BuildRequires:	pkgconfig(ldap)
BuildRequires:	nghttp2
BuildRequires:	cmake
BuildRequires:	ninja
Provides:	webfetch
%if %{with compat32}
BuildRequires:	libc6
BuildRequires:	devel(libz)
BuildRequires:	devel(libidn2)
BuildRequires:	devel(libssl)
%endif

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
%rename %{mklibname %{name} %{major}}

%description -n %{libname}
libcurl is a library of functions for sending and receiving files through
various protocols, including http and ftp.

You should install this package if you plan to use any applications that
use libcurl.

%package -n %{gnutlsname}
Summary:	A library of functions for file transfer
Group:		Networking/Other
Requires:	rootcerts >= 1:20070713.00
%rename %{mklibname %{name}-gnutls %{major}}

%description -n %{gnutlsname}
libcurl is a library of functions for sending and receiving files through
various protocols, including http and ftp.

This version uses gnutls rather than OpenSSL for encryption. It is provided
primarily for binary compatibility with some third party applications.

%package -n %{mbedtlsname}
Summary:	A library of functions for file transfer
Group:		Networking/Other
Requires:	rootcerts >= 1:20070713.00
%rename %{mklibname %{name}-mbedtls %{major}}

%description -n %{mbedtlsname}
libcurl is a library of functions for sending and receiving files through
various protocols, including http and ftp.

This version uses mbedtls rather than OpenSSL for encryption. It is provided
primarily for binary compatibility with some third party applications.

%package -n %{devname}
Summary:	Header files and static libraries for libcurl
Group:		Development/C
Requires:	%{name} = %{EVRD}
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
libcurl is a library of functions for sending and receiving files through
various protocols, including http and ftp.

You should install this package if you wish to develop applications that
use libcurl.

%package -n %{gnutlsdev}
Summary:	Header files and static libraries for libcurl
Group:		Development/C
Requires:	%{devname} = %{EVRD}

%description -n %{gnutlsdev}
libcurl is a library of functions for sending and receiving files through
various protocols, including http and ftp.

This version uses GNUtls rather than OpenSSL.

%package -n %{mbedtlsdev}
Summary:	Header files and static libraries for libcurl
Group:		Development/C
Requires:	%{devname} = %{EVRD}

%description -n %{mbedtlsdev}
libcurl is a library of functions for sending and receiving files through
various protocols, including http and ftp.

This version uses mbedtls rather than OpenSSL.

%package -n %{devstatic}
Summary:	Static libraries for libcurl
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Provides:	%{name}-static-devel = %{EVRD}

%description -n %{devstatic}
libcurl is a library of functions for sending and receiving files through
various protocols, including http and ftp.

You should install this package if you wish to develop applications that
use libcurl.

%package -n %{gnutlsstatic}
Summary:	Static libraries for libcurl-gnutls
Group:		Development/C
Requires:	%{gnutlsdev} = %{EVRD}
Provides:	%{name}-gnutls-static-devel = %{EVRD}

%description -n %{gnutlsstatic}
libcurl is a library of functions for sending and receiving files through
various protocols, including http and ftp.

This version uses gnutls instead of OpenSSL.

%package -n %{mbedtlsstatic}
Summary:	Static libraries for libcurl-mbedtls
Group:		Development/C
Requires:	%{gnutlsdev} = %{EVRD}
Provides:	%{name}-gnutls-static-devel = %{EVRD}

%description -n %{mbedtlsstatic}
libcurl is a library of functions for sending and receiving files through
various protocols, including http and ftp.

You should install this package if you wish to develop applications that
use libcurl.

This version uses mbedtls instead of OpenSSL.

%package examples
Summary:	Example files for %{name} development
Group:		Development/C
Requires:	%{name}-devel = %{EVRD}
BuildArch:	noarch

%description examples
Example files for %{name} development.

%package -n zsh-curl
Summary:	ZSH completion and functions related to curl
Group:		Networking/Other
Requires:	%{name} = %{EVRD}

%description -n zsh-curl
ZSH completion and functions related to curl

%if %{with compat32}
%package -n %{lib32name}
Summary:	A library of functions for file transfer (32-bit)
Group:		Networking/Other
Requires:	rootcerts >= 1:20070713.00

%description -n %{lib32name}
libcurl is a library of functions for sending and receiving files through
various protocols, including http and ftp.

You should install this package if you plan to use any applications that
use libcurl.

%package -n %{dev32name}
Summary:	Header files and static libraries for libcurl (32-bit)
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Requires:	%{lib32name} = %{EVRD}

%description -n %{dev32name}
libcurl is a library of functions for sending and receiving files through
various protocols, including http and ftp.

You should install this package if you wish to develop applications that
use libcurl.
%endif

%prep
%autosetup -p1

%build
autoreconf -fiv

export CONFIGURE_TOP=$(pwd)

EXTRA_CONFIG_openssl="--with-openssl --without-gnutls --without-mbedtls"
EXTRA_CONFIG_gnutls="--without-openssl --with-gnutls --without-mbedtls"
EXTRA_CONFIG_mbedtls="--without-openssl --without-gnutls --with-mbedtls"

%if %{with compat32}
mkdir build32-openssl
cd build32-openssl
%configure32 \
	--with-zlib \
	--with-libidn2 \
	--with-random='/dev/urandom' \
	--enable-hidden-symbols \
	--enable-versioned-symbols \
	--enable-threaded-resolver \
	--disable-optimize \
	--without-libpsl \
	--enable-nonblocking \
	--enable-thread \
	--enable-crypto-auth \
	--enable-libgcc \
	--enable-ipv6 \
	--without-brotli \
	--without-zstd \
	--disable-curldebug \
	$EXTRA_CONFIG_openssl
%make_build
cd ..
%endif

for ssl in %{ssl_implementations}; do
	mkdir build-$ssl
	cd build-$ssl
	%configure \
		--enable-static \
		--with-zlib \
		--with-lber-lib=lber \
		--with-libidn2 \
		--with-nghttp2 \
		--with-libssh \
		--with-random='/dev/urandom' \
  		--with-zsh-functions-dir \
		--enable-hidden-symbols \
		--enable-versioned-symbols \
		--enable-threaded-resolver \
		--enable-optimize \
		--enable-nonblocking \
		--enable-thread \
		--enable-crypto-auth \
		--enable-ipv6 \
		--with-ca-bundle=%{_sysconfdir}/pki/tls/certs/ca-bundle.crt \
		--with-gssapi=%{_prefix} \
		--with-zstd \
		--disable-ares \
		--disable-curldebug \
		$(eval echo \${EXTRA_CONFIG_$ssl})
	%make_build
	cd ..
done

# We don't use cmake for the main builds yet, but let's run a cmake build
# to get cmake integration files...
# FIXME when we've made sure it doesn't create ABI issues, just switch
# to cmake for the main build
# While cross-compiling, PERL_EXECUTABLE needs to be set to HOST perl, but
# the cmake files detect TARGET perl, so override it
export CMAKE_BUILD_DIR=build-cmake
%cmake \
%if %{cross_compiling}
	-DPERL_EXECUTABLE=/usr/bin/perl \
%endif
	-G Ninja
%ninja_build

# we don't want them in curl-examples:
rm -r docs/examples/.deps ||:

# disable tests that want to connect/run sshd, which is quite impossible
#%check
# Some tests fail at random inside ABF (timeouts?), but work in local builds.
# Let's make a test failure non-fatal for the moment.
#make test TEST_Q='-a -p -v !SCP !SFTP !SOCKS4 !SOCKS5 !TFTP !198' || :

%install
# Right now, we install the cmake build just to get the cmake files...
# FIXME when we've made sure it doesn't create ABI issues, just switch
# to cmake for the main build
%ninja_install -C build-cmake

# Try to be compatible with the legacy FindCURL.cmake file used
# by a number of projects out there...
cat >>%{buildroot}%{_libdir}/cmake/CURL/CURLTargets.cmake <<'EOF'
set(CURL_LIBRARY "-lcurl")
set(CURL_LIBRARIES "-lcurl")
EOF

%if %{with compat32}
%make_install -C build32-openssl
%endif

for ssl in %{ssl_implementations}; do
	%make_install -C build-$ssl
	if [ "$ssl" != "openssl" ]; then
		pushd %{buildroot}%{_libdir}
		patchelf --set-soname libcurl-$ssl.so.%{major} libcurl.so.%{major}
		for i in libcurl.so.* libcurl.a; do
			mv $i ${i/libcurl/libcurl-$ssl}
		done
		rm libcurl.so
		ln -s libcurl-$ssl.so.%{major} libcurl-$ssl.so
		cd pkgconfig
		sed -e "s,lcurl,lcurl-$ssl,g" libcurl.pc >libcurl-$ssl.pc
		popd
	fi
done
%make_install -C build-openssl/scripts

# [july 2008] HACK. to be replaced by a real fix
sed -i -e 's!-Wl,--as-needed!!' -e 's!-Wl,--no-undefined!!' %{buildroot}%{_bindir}/%{name}-config
sed -i -e 's!-Wl,--as-needed!!' -e 's!-Wl,--no-undefined!!' -e 's!-L${libdir} !!' %{buildroot}%{_libdir}/pkgconfig/*.pc

# (tpg) use rootcerts's certificates #35917
find %{buildroot} -name ca-bundle.crt -exec rm -f '{}' \;

# we don't package mk-ca-bundle so we don't need man for it
rm -f %{buildroot}%{_mandir}/man1/mk-ca-bundle.1*

# Does anyone actually use fish?
rm -rf %{buildroot}%{_datadir}/fish

%files
%{_bindir}/curl
%doc %{_mandir}/man1/curl.1*

%files -n %{libname}
%{_libdir}/libcurl.so.%{major}*

%if %{with gnutls}
%files -n %{gnutlsname}
%{_libdir}/libcurl-gnutls.so.%{major}*
%endif

%if %{with mbedtls}
%files -n %{mbedtlsname}
%{_libdir}/libcurl-mbedtls.so.%{major}*
%endif

%files -n %{devname}
%doc docs/KNOWN_BUGS docs/FAQ
%doc docs/TODO docs/THANKS
%{_bindir}/curl-config
%{_libdir}/libcurl.so
%{_includedir}/curl
%{_libdir}/pkgconfig/libcurl.pc
%{_libdir}/cmake/CURL
%{_datadir}/aclocal/*.m4
%doc %{_mandir}/man1/curl-config.1*
%doc %{_mandir}/man3/*

%if %{with gnutls}
%files -n %{gnutlsdev}
%{_libdir}/libcurl-gnutls.so
%{_libdir}/pkgconfig/libcurl-gnutls.pc
%endif

%if %{with mbedtls}
%files -n %{mbedtlsdev}
%{_libdir}/libcurl-mbedtls.so
%{_libdir}/pkgconfig/libcurl-mbedtls.pc
%endif

%files -n %{devstatic}
%{_libdir}/libcurl.a

%if %{with gnutls}
%files -n %{gnutlsstatic}
%{_libdir}/libcurl-gnutls.a
%endif

%if %{with mbedtls}
%files -n %{mbedtlsstatic}
%{_libdir}/libcurl-mbedtls.a
%endif

%files examples
%{_bindir}/mk-ca-bundle.pl
%doc docs/examples

%if ! %{cross_compiling}
%files -n zsh-curl
%{_datadir}/zsh/site-functions/_curl
%endif

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libcurl.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/libcurl.so
%{_prefix}/lib/pkgconfig/libcurl.pc
%endif
