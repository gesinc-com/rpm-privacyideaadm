%if 0%{?fedora}
%global with_python3 1
%global _docdir_fmt %{name}
%endif

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%global pkgname privacyideaadm
%global pkgp    p

Name:           python-%{pkgname}
Version:        2.15.1
Release:        1%{?dist}
Summary:        a command line client to manage the privacyIDEA server.
Group:          System/Applications

License:        AGPL3
URL:            https://www.privacyidea.org/

Source0:        https://files.pythonhosted.org/packages/source/%{pkgp}/%{pkgname}/%{pkgname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  pytest
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-setuptools
%endif # with_python3

%description
This is a command line client to manage the privacyIDEA server.

You can use it to fill an LUKS keyslot with the response of a challenge response Yubikey, that is managed with privacyIDEA.

.note:: You will also need the package at https://github.com/cornelinux/yubikey-luks to enable grub to read challenges from the yubikey.

You can also use it to manage SSH keys centrally for all your servers running openssh.

%if 0%{?with_python3}
%package -n python3-%{pkgname}
Summary:        %{summary}
Group:          System/Applications
Requires:       python3

%description -n python3-%{pkgname}
This is a command line client to manage the privacyIDEA server.

You can use it to fill an LUKS keyslot with the response of a challenge response Yubikey, that is managed with privacyIDEA.

.note:: You will also need the package at https://github.com/cornelinux/yubikey-luks to enable grub to read challenges from the yubikey.

You can also use it to manage SSH keys centrally for all your servers running openssh.
%endif # with_python3

%prep
%autosetup -p1 -n %{pkgname}-%{version}


%if 0%{?with_python3}
cp -a . %{py3dir}
%endif # with_python3

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with_python3


%check
export PYTHONPATH=$(pwd)

#py.test-%{python_version} -v %{pkgname}/tests

%if 0%{?with_python3}
pushd %{py3dir}
py.test-%{python3_version} -v %{pkgname}/tests
popd
%endif # with_python3

%files
%{!?_licensedir:%global license %%doc}
#doc README.rst
#license LICENSE
%{python2_sitelib}/*
%{_mandir}/man1/*gz
%{_bindir}/*

%if 0%{?with_python3}
%files -n python3-%{pkgname}
%{python3_sitelib}/*
#license LICENSE
#doc README.rst
%endif # with_python3

%changelog
* Thu Jan 16 2020 Bishop Clark <bishopolis@gmail.com> - 2.15.1-1
- initial
