find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_MANCHESTERPDU gnuradio-manchesterpdu)

FIND_PATH(
    GR_MANCHESTERPDU_INCLUDE_DIRS
    NAMES gnuradio/manchesterpdu/api.h
    HINTS $ENV{MANCHESTERPDU_DIR}/include
        ${PC_MANCHESTERPDU_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_MANCHESTERPDU_LIBRARIES
    NAMES gnuradio-manchesterpdu
    HINTS $ENV{MANCHESTERPDU_DIR}/lib
        ${PC_MANCHESTERPDU_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-manchesterpduTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_MANCHESTERPDU DEFAULT_MSG GR_MANCHESTERPDU_LIBRARIES GR_MANCHESTERPDU_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_MANCHESTERPDU_LIBRARIES GR_MANCHESTERPDU_INCLUDE_DIRS)
