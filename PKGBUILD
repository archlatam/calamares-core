# Maintainer: TNE <TNE[at]Core linux[dot]org>
# Contributor: Philip Müller <philm[at]manjaro[dog]org>

pkgname=calamares-core
pkgver=3.4.3.r2.gfe8c67bace
pkgrel=4
_commit=fe8c67bace
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
source=(
  git+https://codeberg.org/m4teo/calamares.git#commit=${_commit}
  "calamares.desktop"
  "calamares_polkit"
  "49-nopasswd-calamares.rules"
)

sha256sums=(
  'SKIP'
  '2a3a9f55004c08230613f982a0ebedcba2d39e03a89d21071e34afc045e5ac8b'
  'c176b28007bd1c1f23d8dbb2c936fa54d0c01bacfb67290ddad597606c129df3'
  '56d85ff6bf860b9559b8c9f997ad9b1002f3fccc782073760eca505e3bddd176'
)

prepare() {
  cd "${srcdir}/calamares"
  # Opcional: modificar versión en CMakeLists si es necesario
  # sed -i -e "s|set(CALAMARES_VERSION .*|set(CALAMARES_VERSION ${pkgver})|" CMakeLists.txt
}

build() {
  cd "${srcdir}/calamares" || exit

  export CXXFLAGS+=" -fPIC"

  mkdir -p build && cd build || exit
  cmake -S .. -B. \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/usr \
    -DCMAKE_INSTALL_LIBDIR=lib \
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
