#! /usr/bin/env python
# encoding: utf-8

APPNAME = "gbenchmark"
VERSION = "0.0.0"


def configure(conf):

    if conf.is_mkspec_platform("linux"):
        if not conf.env["LIB_PTHREAD"]:
            # If we have not looked for pthread yet
            conf.check_cxx(lib="pthread")


def build(bld):

    bld.env.append_unique(
        "DEFINES_STEINWURF_VERSION", 'STEINWURF_GBENCHMARK_VERSION="{}"'.format(VERSION)
    )

    use_flags = []
    if bld.is_mkspec_platform("linux"):
        use_flags += ["PTHREAD"]

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
