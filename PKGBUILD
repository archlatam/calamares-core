# Maintainer: TNE <TNE[at]Core linux[dot]org>
# Contributor: Philip Müller <philm[at]manjaro[dog]org>

pkgname=calamares-core
pkgver=3.4.3.r16.g54b561766
# pkgrel 10: nvidiadrivers fixes
#   - error visible para GPU NVIDIA sin driver compatible
#   - reconocer GH1/GB1 (Hopper/Blackwell datacenter)
#   - instalar nvidia-prime (prime-run) sin romper la rama legacy
# pkgrel 9: backport 4K partition alignment fix for LUKS2 (Calamares #2480 / PR #2490)
#           + CachyOS netinstall selection fix (avoid KDE/GNOME accumulation on revisit)
pkgrel=10
_commit=54b56176697f07127feb16f90aa7a2aa7e27b52e
pkgdesc='Distribution-independent installer framework'
arch=('i686' 'x86_64')
url="https://codeberg.org/m4teo/calamares"
license=('LGPL')
conflicts=('calamares' 'calamares-eo' 'calamares-dev')
provides=('calamares' 'calamares-dev')
replaces=('calamares-dev')
depends=(
  kconfig
  kcoreaddons
  kcrash
  kiconthemes
  ki18n
  kparts
  kpmcore
  kservice
  kwidgetsaddons
  solid
  yaml-cpp
  boost-libs
  ckbcomp
  hwinfo
  qt6-svg
  polkit-qt6
  libpwquality
  python
  python-distutils-extra
  cryptsetup
  gptfdisk
  rsync
)
makedepends=(
  boost
  cmake
  extra-cmake-modules
  git
  qt6-tools
  qt6-translations
  ninja
  doxygen
  python-jsonschema
  python-pyaml
  python-unidecode
)

# Fijamos el commit exacto
# Backport: alinea el final de la partición automática a 4K para que
# KPMcore pueda crear LUKS2 con --sector-size 4096.
# Cubre "borrar disco"; "reemplazar partición" existente desalineada queda pendiente.
# Backport: CachyOS netinstall fix (updateSelections) para que al volver
# y cambiar de escritorio no queden KDE y GNOME seleccionados a la vez.
source=(
  git+https://codeberg.org/m4teo/calamares.git#commit=${_commit}
  "netinstall-selection.patch"
  "partition-align-4k.patch"
  "nvidiadrivers-fixes.patch"
  "calamares.desktop"
  "calamares_polkit"
  "49-nopasswd-calamares.rules"
)

sha256sums=(
  'SKIP'
  '19c70cfbbae161102f0653054ff0074104725838dc1f412c3355e616fca11c17'
  '793f9963bd401c697b7844b18be1a40d2b56663f0c45adf7c90875f18d058310'
  '99db5a01d2972a2df471b132a312643b3b36cced3d73506c3a9493ffd28c6459'
  '2a3a9f55004c08230613f982a0ebedcba2d39e03a89d21071e34afc045e5ac8b'
  'c176b28007bd1c1f23d8dbb2c936fa54d0c01bacfb67290ddad597606c129df3'
  '56d85ff6bf860b9559b8c9f997ad9b1002f3fccc782073760eca505e3bddd176'
)

prepare() {
  cd "${srcdir}/calamares"
  patch --batch -Np1 -i "${srcdir}/netinstall-selection.patch"
  patch --batch -Np1 -i "${srcdir}/partition-align-4k.patch"
  patch --batch -Np1 -i "${srcdir}/nvidiadrivers-fixes.patch"
  # Opcional: modificar versión en CMakeLists si es necesario
  # sed -i -e "s|set(CALAMARES_VERSION .*|set(CALAMARES_VERSION ${pkgver})|" CMakeLists.txt
}

build() {
  cd "${srcdir}/calamares" || exit

  # PATH limpio: evita que CMake encuentre un Python en ~/.local/bin (uv, pyenv, etc.)
  export PATH=/usr/bin:/bin:/usr/local/bin
  export CXXFLAGS+=" -fPIC"

  rm -rf build && mkdir -p build && cd build || exit
  cmake -S .. -B. \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DCMAKE_INSTALL_LIBDIR=lib \
    -DPython_EXECUTABLE=/usr/bin/python \
    -DPython3_EXECUTABLE=/usr/bin/python \
    -DPython_FIND_STRATEGY=LOCATION \
    -DBoost_NO_BOOST_CMAKE=ON \
    -DWITH_QT6=ON \
    -DWITH_APPSTREAM=OFF \
    -DSKIP_MODULES="dracutlukscfg \
      dummycpp dummyprocess dummypython dummypythonqt \
      finishedq keyboardq license localeq notesqml oemid \
      openrcdmcryptcfg packagechooserq fsresizer \
      rawfs contextualprocess interactiveterminal \
      plasmalnf services-openrc \
      summaryq tracking usersq webview welcomeq"
  cmake --build .
}

package() {
  cd ${srcdir}/calamares/build
  DESTDIR="${pkgdir}" cmake --build . --target install
  #install -Dm644 "${srcdir}/calamares.desktop" "$pkgdir/etc/xdg/autostart/calamares.desktop"
  install -Dm755 "${srcdir}/calamares_polkit" "$pkgdir/usr/bin/calamares_polkit"
  install -Dm644 "${srcdir}/49-nopasswd-calamares.rules" "$pkgdir/etc/polkit-1/rules.d/49-nopasswd-calamares.rules"
  chmod 750 "$pkgdir/etc/polkit-1/rules.d"
}
