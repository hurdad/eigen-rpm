Name:           eigen
Version:        %{VERSION}
Release:        %{RELEASE}%{?dist}
Summary:        A lightweight C++ template library for vector and matrix math
License:        MPLv2.0 and LGPLv2+ and BSD
URL:            http://eigen.tuxfamily.org/index.php?title=Main_Page
Source:         %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  atlas-devel
BuildRequires:  fftw-devel
BuildRequires:  glew-devel
BuildRequires:  gmp-devel
BuildRequires:  gsl-devel
BuildRequires:  mpfr-devel
#BuildRequires:  sparsehash-devel
#BuildRequires:  suitesparse-devel
BuildRequires:  gcc-gfortran
BuildRequires:  SuperLU-devel
BuildRequires:  qt-devel
#BuildRequires:  scotch-devel
BuildRequires:  metis-devel

BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc-c++
BuildRequires:  doxygen
BuildRequires:  graphviz
#BuildRequires:  tex(latex)

%description
%{summary}.


%package devel
Summary:        A lightweight C++ template library for vector and matrix math
BuildArch:      noarch
# -devel subpkg only atm, compat with other distros
Provides:       %{name} = %{version}-%{release}
# not *strictly* a -static pkg, but the results are the same
Provides:       %{name}-static = %{version}-%{release}

%description devel
%{summary}.

%package doc
Summary:        Developer documentation for Eigen
Requires:       %{name}-devel = %{version}-%{release}
BuildArch:      noarch

%description doc
Developer documentation for Eigen.

%prep
%autosetup -p1 -n eigen-git-mirror-%{version}

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%cmake .. -DINCLUDE_INSTALL_DIR=%{_includedir}/eigen3 \
  -DBLAS_LIBRARIES="cblas" \
  -DSUPERLU_INCLUDES=%{_includedir}/SuperLU \
  -DSCOTCH_INCLUDES=%{_includedir} -DSCOTCH_LIBRARIES="scotch" \
  -DMETIS_INCLUDES=%{_includedir} -DMETIS_LIBRARIES="metis" \
  -DCMAKEPACKAGE_INSTALL_DIR=%{_datadir}/%{name}
popd

%make_build -C %{_target_platform}
%make_build doc -C %{_target_platform}

rm -f %{_target_platform}/doc/html/installdox
rm -f %{_target_platform}/doc/html/unsupported/installdox

%install
%make_install -C %{_target_platform}

%check
# Run tests but make failures non-fatal. Note that upstream doesn't expect the
# tests to pass consistently since they're seeded randomly.
#make_build buildtests -C %{_target_platform}
#make_build test -C %{_target_platform} test ARGS="-V" || :


%files devel
%license COPYING.README COPYING.BSD COPYING.MPL2 COPYING.LGPL
%{_includedir}/eigen3
%{_datadir}/%{name}
%{_datadir}/pkgconfig/*
%{_datadir}/cmake/Modules/*.cmake

%files doc
%doc %{_target_platform}/doc/html

%changelog
