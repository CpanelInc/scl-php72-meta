# Defining the package namespace
%global ns_name ea
%global ns_dir /opt/cpanel

%global _scl_prefix %{ns_dir}
%global scl_name_base    %{ns_name}-php
%global scl_macro_base   %{ns_name}_php
%global scl_name_version 72
%global scl              %{scl_name_base}%{scl_name_version}
%scl_package %scl

# do not produce empty debuginfo package
%global debug_package %{nil}

Summary:       Package that installs PHP 7.2
Name:          %scl_name
Version:       7.2.0
Vendor:        cPanel, Inc.
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4590 for more details
%define        release_prefix 6.RC5
Release:       %{release_prefix}%{?dist}.cpanel
Group:         Development/Languages
License:       GPLv2+

Source0:       macros-build
Source1:       README
Source2:       LICENSE

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: scl-utils-build
BuildRequires: help2man
# Temporary work-around
BuildRequires: iso-codes

Requires:      %{?scl_prefix}php-common
Requires:      %{?scl_prefix}php-cli
Requires:      %{?scl_prefix}pear

%description
This is the main package for %scl Software Collection,
that install PHP 7.2 language.


%package runtime
Summary:   Package that handles %scl Software Collection.
Group:     Development/Languages
Requires:  scl-utils

%description runtime
Package shipping essential scripts to work with %scl Software Collection.

%package build
Summary:   Package shipping basic build configuration
Group:     Development/Languages
Requires:  scl-utils-build

%description build
Package shipping essential configuration macros
to build %scl Software Collection.


%package scldevel
Summary:   Package shipping development files for %scl
Group:     Development/Languages

%description scldevel
Package shipping development files, especially usefull for development of
packages depending on %scl Software Collection.


%prep
%setup -c -T

cat <<EOF | tee enable
export PATH=%{_bindir}:%{_sbindir}\${PATH:+:\${PATH}}
export MANPATH=%{_mandir}:\${MANPATH}
EOF

# generate rpm macros file for depended collections
cat << EOF | tee scldev
%%scl_%{scl_macro_base}         %{scl}
%%scl_prefix_%{scl_macro_base}  %{scl_prefix}
EOF

# This section generates README file from a template and creates man page
# from that file, expanding RPM macros in the template file.
cat >README <<'EOF'
%{expand:%(cat %{SOURCE1})}
EOF

# copy the license file so %%files section sees it
cp %{SOURCE2} .


%build
# generate a helper script that will be used by help2man
cat >h2m_helper <<'EOF'
#!/bin/bash
[ "$1" == "--version" ] && echo "%{scl_name} %{version} Software Collection" || cat README
EOF
chmod a+x h2m_helper

# generate the man page
help2man -N --section 7 ./h2m_helper -o %{scl_name}.7


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -D -m 644 enable %{buildroot}%{_scl_scripts}/enable
install -D -m 644 scldev %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel
install -D -m 644 %{scl_name}.7 %{buildroot}%{_mandir}/man7/%{scl_name}.7
mkdir -p %{buildroot}/opt/cpanel/ea-php72/root/etc
mkdir -p %{buildroot}/opt/cpanel/ea-php72/root/usr/share/doc
mkdir -p %{buildroot}/opt/cpanel/ea-php72/root/usr/include
mkdir -p %{buildroot}/opt/cpanel/ea-php72/root/usr/share/man/man1
mkdir -p %{buildroot}/opt/cpanel/ea-php72/root/usr/bin
mkdir -p %{buildroot}/opt/cpanel/ea-php72/root/usr/var/cache
mkdir -p %{buildroot}/opt/cpanel/ea-php72/root/usr/var/tmp
mkdir -p %{buildroot}/opt/cpanel/ea-php72/root/usr/%{_lib}

%scl_install

tmp_version=$(echo %{scl_name_version} | sed -re 's/([0-9])([0-9])/\1\.\2/')
sed -e 's/@SCL@/%{scl_macro_base}%{scl_name_version}/g' -e "s/@VERSION@/${tmp_version}/g" %{SOURCE0} \
  | tee -a %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl}-config

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files


%files runtime
%defattr(-,root,root)
%doc README LICENSE
%scl_files
%{_mandir}/man7/%{scl_name}.*
%dir /opt/cpanel/ea-php72/root/etc
%dir /opt/cpanel/ea-php72/root/usr
%dir /opt/cpanel/ea-php72/root/usr/share
%dir /opt/cpanel/ea-php72/root/usr/share/doc
%dir /opt/cpanel/ea-php72/root/usr/include
%dir /opt/cpanel/ea-php72/root/usr/share/man
%dir /opt/cpanel/ea-php72/root/usr/share/man/man1
%dir /opt/cpanel/ea-php72/root/usr/bin
%dir /opt/cpanel/ea-php72/root/usr/var
%dir /opt/cpanel/ea-php72/root/usr/var/cache
%dir /opt/cpanel/ea-php72/root/usr/var/tmp
%dir /opt/cpanel/ea-php72/root/usr/%{_lib}

%files build
%defattr(-,root,root)
%{_root_sysconfdir}/rpm/macros.%{scl}-config


%files scldevel
%defattr(-,root,root)
%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel


%changelog
* Fri Nov 03 2017 Dan Muey <dan@cpanel.net> - 7.2.0-6.RC5
- EA-3999: adjust files to get better cleanup on uninstall

* Fri Oct 27 2017 Jacob Perkins <jacob.perkins@cpanel.net> - 7.2.0-5.RC5
- EA-6923: Update 7.2.0 from RC3 to RC5

* Mon Oct 02 2017  <dan@cpanel.net> - 7.2.0-4.RC3
- EA-6857: Update 7.2.0 from RC1 to RC3

* Thu Aug 31 2017 <dan@cpanel.net> - 7.2.0-2.RC1
- EA-6758: Update 7.2.0 from beta3 to RC1

* Thu Aug 17 2017 <dan@cpanel.net> - 7.2.0-1.beta3
- ZC-2785: Initial packaging
