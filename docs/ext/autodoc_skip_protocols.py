PROTOCOL_METHODS = [
    "act",
    "answered_by",
    "aside",
    "attach",
    "beat",
    "describe",
    "error",
    "forget",
    "perform_as",
    "scene",
]


def autodoc_skip_member(_, what, name, ____, skip, options):
    if what != "class":
        return skip

    return skip or (name in PROTOCOL_METHODS and not options.undoc_members)


def setup(app):
    app.connect(event="autodoc-skip-member", callback=autodoc_skip_member)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
