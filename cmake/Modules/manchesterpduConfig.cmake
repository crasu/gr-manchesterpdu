INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_MANCHESTERPDU manchesterpdu)

FIND_PATH(
    MANCHESTERPDU_INCLUDE_DIRS
    NAMES manchesterpdu/api.h
    HINTS $ENV{MANCHESTERPDU_DIR}/include
        ${PC_MANCHESTERPDU_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    MANCHESTERPDU_LIBRARIES
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

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(MANCHESTERPDU DEFAULT_MSG MANCHESTERPDU_LIBRARIES MANCHESTERPDU_INCLUDE_DIRS)
MARK_AS_ADVANCED(MANCHESTERPDU_LIBRARIES MANCHESTERPDU_INCLUDE_DIRS)

