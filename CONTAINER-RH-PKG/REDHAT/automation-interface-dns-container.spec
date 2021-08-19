Name:       automation-interface-dns-container
Version:    RH_VERSION
Release:    RH_RELEASE
Summary:    Automation Interface Consul server agent, container image

License:    GPLv3+
Source0:    RPM_SOURCE

Requires:   podman, buildah, at

BuildArch:  noarch

%description
automation-interface-dns-container

%include %{_topdir}/SPECS/preinst.spec
%include %{_topdir}/SPECS/postinst.spec
%include %{_topdir}/SPECS/prerm.spec

%prep
%setup  -q #unpack tarball

%install
cp -rfa * %{buildroot}

%include %{_topdir}/SPECS/files.spec



