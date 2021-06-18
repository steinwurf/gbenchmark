#! /usr/bin/env python
# encoding: utf-8

APPNAME = "gbenchmark"
VERSION = "0.0.0"


def configure(conf):

    if conf.is_mkspec_platform("linux"):
        if not conf.env["LIB_PTHREAD"]:
            # If we have not looked for pthread yet
            conf.check_cxx(lib="pthread")

    if conf.is_mkspec_platform("windows"):
        if not conf.env["LIB_SHLWAPI"]:
            # If we have not looked for shlwapi yet
            conf.check_cxx(lib="shlwapi")

def build(bld):

    bld.env.append_unique(
        "DEFINES_STEINWURF_VERSION", 'STEINWURF_GBENCHMARK_VERSION="{}"'.format(VERSION)
    )

    use_flags = []
    if bld.is_mkspec_platform("linux"):
        use_flags += ["PTHREAD"]

    if bld.is_mkspec_platform("windows"):
        use_flags += ["LIB_SHLWAPI"]

    src = bld.dependency_node("gbenchmark-source")
    includes = src.find_dir("include")

    bld.stlib(
        features="cxx",
        source=src.ant_glob("src/*.cc"),
        target="gbenchmark",
        includes=[includes, src],
        export_includes=[includes],
        use=use_flags,
    )

    if bld.is_toplevel():

        bld.recurse("test")
