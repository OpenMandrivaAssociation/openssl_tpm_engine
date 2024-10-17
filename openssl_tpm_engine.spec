Summary:	OpenSSL TPM engine
Name:		openssl_tpm_engine
Version:	0.4.1
Release:	%mkrel 5
License:	CPL
Group:		System/Servers
URL:		https://www.sf.net/projects/trousers
Source0:	http://downloads.sourceforge.net/trousers/%{name}-%{version}.tar.gz
Patch0:		openssl_tpm_engine-avoid-version.diff
BuildRequires:	libtool
BuildRequires:	autoconf2.5
BuildRequires:	openssl-devel
BuildRequires:	trousers-devel
Requires:	openssl
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
This package contains 2 sets of code, a command-line utility used to generate a
TSS key blob and write it to disk and an OpenSSL engine which interfaces with
the TSS API.


%prep

%setup -q
%patch0 -p0

# weird bug
mkdir -p py/test
touch py/test/Makefile.in

%build
rm -rf autom4te.cache
%serverbuild
libtoolize --copy --force; aclocal; automake --add-missing -copy --foreign; autoconf

%configure2_5x \
    --with-openssl=%{_prefix}

%make

%install
rm -rf %{buildroot}

%makeinstall_std

install -m0755 test/engine_key_loading %{buildroot}%{_bindir}/

# cleanup
rm -f %{buildroot}%{_libdir}/openssl/engines/libtpm.la

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE README openssl.cnf.sample
%doc test/gentpmcert.sh test/stunnel_connect.sh test/stunnel-server.conf
%attr(0755,root,root) %{_bindir}/create_tpm_key
%attr(0755,root,root) %{_bindir}/engine_key_loading
%{_libdir}/openssl/engines/libtpm.so
