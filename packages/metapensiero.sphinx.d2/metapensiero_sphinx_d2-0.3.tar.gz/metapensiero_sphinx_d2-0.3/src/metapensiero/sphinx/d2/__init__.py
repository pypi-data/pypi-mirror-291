# -*- coding: utf-8 -*-
# :Project:   metapensiero.sphinx.d2 — Implement a d2 Sphinx directive
# :Created:   sab 10 ago 2024, 16:45:05
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2024 Lele Gaifax
#

from __future__ import annotations

from hashlib import md5
from pathlib import Path
from re import finditer
from re import sub
from subprocess import CalledProcessError
from subprocess import run
from typing import ClassVar
from typing import Generator
from typing import TYPE_CHECKING

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx import errors
from sphinx.addnodes import pending_xref
from sphinx.util.docutils import SphinxDirective
from sphinx.util.i18n import search_image_for_language
from sphinx.util.nodes import set_source_info


if TYPE_CHECKING:
    from collections.abc import Sequence

    from docutils.nodes import Node
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata
    from sphinx.util.typing import OptionSpec
    from sphinx.writers.html5 import HTML5Translator
    from sphinx.writers.latex import LaTeXTranslator
    from sphinx.writers.manpage import ManualPageTranslator
    from sphinx.writers.texinfo import TexinfoTranslator
    from sphinx.writers.text import TextTranslator


__version__ = '0.3'


class D2Error(errors.SphinxError):
    "Something's wrong in a D2 directive"

    category = "D2 error"


def booloption(argument: str) -> bool:
    """A boolean option.

    If no argument, or when its lowercase value is either ``"1"``, ``"true"``, ``"yes"`` or
    ``on``, return ``True``, otherwise ``False``.
    """

    if argument and argument.strip():
        return argument.strip().lower() in ('1', 'true', 'yes', 'on')
    else:
        return True


class d2node(nodes.General, nodes.Inline, nodes.Element):
    """Node holding all details of a d2 diagram, in particular its `code`."""

    def find_internal_links(self) -> Generator[tuple[int, int]]:
        "Generator yielding start and end positions of internals links in the d2 code."

        code = self['code']
        for match in finditer(r'(?m)^\s*link:\s*(:\w+:.*)', code):
            yield match.start(1), match.end(1)


def figure_wrapper(directive: SphinxDirective, node: d2node, caption: str) -> nodes.figure:
    figure_node = nodes.figure('', node)
    if 'align' in node:
        figure_node['align'] = node.attributes.pop('align')
    if 'width' in node:
        figure_node['width'] = node.attributes.pop('width')

    inodes, messages = directive.state.inline_text(caption, directive.lineno)
    caption_node = nodes.caption(caption, '', *inodes)
    caption_node.extend(messages)
    set_source_info(directive, caption_node)
    figure_node += caption_node
    return figure_node


class D2Directive(SphinxDirective):
    "Implementation of the ``d2`` directive."

    required_arguments = 0
    optional_arguments = 1
    has_content = True
    final_argument_whitespace = False
    option_spec: ClassVar[OptionSpec] = {
        'align': directives.unchanged,
        'alt': directives.unchanged,
        'caption': directives.unchanged,
        'center': booloption,
        'class': directives.class_option,
        'format': lambda arg: directives.choice(arg, ('png', 'svg')),
        'layout': lambda arg: directives.choice(arg, ('dagre', 'elk')),
        'pad': directives.positive_int,
        'redirect_links_to_blank_page': directives.flag,
        'sketch': booloption,
        'theme': directives.nonnegative_int,
        'width': lambda arg: directives.get_measure(arg, directives.length_units + ['%'])
    }

    def _parse_internal_links(self, node: d2node) -> Generator[Node]:
        "Parse internal links and yield corresponding ``Node``."

        code = node['code']
        for start, end in node.find_internal_links():
            link = code[start:end]
            nodes, _ = self.state.inline_text(link, self.lineno)
            if len(nodes) != 1 or not isinstance(nodes[0], pending_xref):
                raise D2Error(f'Invalid link in d2 directive at'
                              f' {self.get_location()}: {link!r}')
            yield nodes[0]

    def run(self) -> Sequence[Node]:
        if self.arguments:
            document = self.state.document
            if self.content:
                return [document.reporter.warning(
                    'Directive d2 cannot have both a content and a filename argument',
                    line=self.lineno)]
            argument = search_image_for_language(self.arguments[0], self.env)
            rel_filename, filename = self.env.relfn2path(argument)
            self.env.note_dependency(rel_filename)
            try:
                with open(filename, encoding='utf-8') as fp:
                    d2code = fp.read()
            except OSError:
                return [document.reporter.warning(
                    f'External d2 file {filename} not found or reading it failed',
                    line=self.lineno)]
        else:
            d2code = '\n'.join(self.content)
            rel_filename = None
            if not d2code.strip():
                return [self.state_machine.reporter.warning(
                    'Ignoring d2 directive without content',
                    line=self.lineno)]

        node = d2node()
        node['code'] = d2code

        # Collect internal "link" references, that will replaced later at render time
        for link in self._parse_internal_links(node):
            node += link

        options = dict(self.options)
        caption = options.pop('caption', None)
        if 'class' in options:
            node['classes'] = options.pop('class')
        for option in ('align', 'alt', 'caption', 'redirect_links_to_blank_page', 'width'):
            if option in options:
                node[option] = options.pop(option)

        node_options = node['options'] = {'docname': self.env.docname}
        node_options.update(options)

        config = self.env.app.config
        for option in self.option_spec:
            cfgopt = f'd2_{option}'
            if option not in node_options and cfgopt in config:
                node_options[option] = config[cfgopt]

        if caption is not None:
            figure = figure_wrapper(self, node, caption)
            self.add_name(figure)
            return [figure]
        else:
            self.add_name(node)
            return [node]


def render_d2(self: HTML5Translator | LaTeXTranslator | TexinfoTranslator,
              node: d2node, fmt: str) -> Path:
    # When the d2 code contains internal Sphinx links (:ref:`foo` things)
    # replace them with the resolved URIs
    replacements = []

    # The Sphinx references resolver may produce relative: we need to absolutize them within
    # the SVG diagram, so compute the target directory of the containing document
    source_rel_dir = Path(self.document['source']).parent.relative_to(self.builder.srcdir)
    target_dir = self.builder.outdir / source_rel_dir

    for pos, (start, end) in enumerate(node.find_internal_links()):
        ref = node.children[pos]
        # If the child is not a reference then most probably is a broken link,
        # that Sphinx converted into an inline text, ignore it
        if not isinstance(ref, nodes.reference):
            continue
        if 'refuri' in ref:
            uri = ref['refuri']
            if not uri.startswith('/'):
                reluri, fragment = uri.rsplit('#', 1)
                uri = str((target_dir / reluri).resolve().relative_to(self.builder.outdir))
                if fragment:
                    uri += f'#{fragment}'
            uri = uri.replace('#', r'\#')
            replacement = f"/{uri}"
        elif 'refid' in ref:
            # FIXME: this obviously works only when we are generating HTML...
            docname = self.builder.env.path2doc(self.document["source"])
            replacement = rf"/{docname}.html\#{ref['refid']}"
        replacements.append((start, end, replacement))

    code = node['code']
    for start, end, replacement in reversed(replacements):
        code = code[:start] + replacement + code[end:]

    code = code.encode('utf-8')
    options = node['options']
    chash = md5(usedforsecurity=False)
    chash.update(code)
    chash.update(str(options).encode('utf-8'))
    fname = chash.hexdigest() + '.' + fmt
    outfn = Path(self.builder.outdir) / self.builder.imagedir / fname
    if outfn.exists():
        return outfn

    cmd: list[str | Path] = ['d2']
    if options.get('center', False):
        cmd.append('--center')
    if 'layout' in options:
        cmd.append(f"--layout={options['layout']}")
    if 'theme' in options:
        cmd.append(f"--theme={options['theme']}")
    if options.get('sketch', False):
        cmd.append('--sketch')
    if 'pad' in options:
        cmd.append(f"--pad={options['pad']}")
    cmd.append('-')
    cmd.append(outfn)
    try:
        run(cmd, check=True, input=code)
    except CalledProcessError as exc:
        raise D2Error(f"Error: {' '.join(str(a) for a in cmd)}"
                      f" exited with status {exc.returncode}")

    if fmt == 'svg' and options.get('redirect_links_to_blank_page', False):
        svg = outfn.read_text()
        outfn.write_text(sub(r'a (href="(?!\w+://)[^"]*")', r'a target="_blank" \1', svg))

    return outfn


def html_visit_d2node(self: HTML5Translator, node: d2node) -> None:
    outfn = render_d2(self, node, node['options'].get('format', 'svg'))
    relfn = outfn.relative_to(self.builder.outdir)
    classes = ' '.join(filter(None, ['d2lang', *node.get('classes', [])]))
    if 'align' in node:
        self.body.append(f'<div align="{node["align"]}" class="align-{node["align"]}">')
    self.body.append('<div class="d2lang">')
    if 'alt' in node:
        alt = node['alt']
    else:
        alt = None
    if node['options']['format'] == 'svg':
        self.body.append(f'<object data="/{relfn}" type="image/svg+xml" class="{classes}">\n')
        if alt is not None:
            self.body.append(f'<p class="warning">{self.encode(alt).strip()}</p>')
        self.body.append('</object>\n')
    else:
        if alt is not None:
            alt = f' alt="{self.encode(alt).strip()}"'
        self.body.append(f'<img src="/{relfn}" {alt} class="{classes}" />\n')
    self.body.append('</div>\n')
    if 'align' in node:
        self.body.append('</div>\n')

    raise nodes.SkipNode


def latex_visit_d2node(self: LaTeXTranslator, node: d2node) -> None:
    # FIXME: this is COMPLETELY untested
    outfn = render_d2(self, node, 'png')
    relfn = outfn.relative_to(self.builder.outdir)

    is_inline = self.is_inline(node)

    if not is_inline:
        pre = ''
        post = ''
        if 'align' in node:
            if node['align'] == 'left':
                pre = '{'
                post = r'\hspace*{\fill}}'
            elif node['align'] == 'right':
                pre = r'{\hspace*{\fill}'
                post = '}'
            elif node['align'] == 'center':
                pre = r'{\hfill'
                post = r'\hspace*{\fill}}'
        self.body.append('\n%s' % pre)

    self.body.append(r'\sphinxincludegraphics[]{%s}' % relfn)

    if not is_inline:
        self.body.append('%s\n' % post)

    raise nodes.SkipNode


def man_visit_d2node(self: ManualPageTranslator, node: d2node) -> None:
    if 'alt' in node.attributes:
        self.add_text(f'[d2 diagram: {node["alt"]}]')
    else:
        self.add_text('[d2 diagram]')
    raise nodes.SkipNode


def texinfo_visit_d2node(self: TexinfoTranslator, node: d2node) -> None:
    # FIXME: this is COMPLETELY untested
    outfn = render_d2(self, node, 'png')
    relfn = outfn.relative_to(self.builder.outdir)
    self.body.append(f'@image{{{relfn.with_suffix("")},,,[d2lang],png}}\n')
    raise nodes.SkipNode


def text_visit_d2node(self: TextTranslator, node: d2node) -> None:
    if 'alt' in node.attributes:
        self.add_text(f'[d2 diagram: {node["alt"]}]')
    else:
        self.add_text('[d2 diagram]')
    raise nodes.SkipNode


def setup(app: Sphinx) -> ExtensionMetadata:
    from sphinx.config import ENUM

    app.add_directive("d2", D2Directive)
    app.add_node(d2node,
                 html=(html_visit_d2node, None),
                 latex=(latex_visit_d2node, None),
                 man=(man_visit_d2node, None),
                 texinfo=(texinfo_visit_d2node, None),
                 text=(text_visit_d2node, None))

    app.add_config_value('d2_center', False, 'html', [bool],
                         #'Default value for the d2 ``:center:`` option',
                         )
    app.add_config_value('d2_format', 'svg', 'html', ENUM('svg', 'png'),
                         #'Default value for the d2 ``:format:`` option',
                         )
    app.add_config_value('d2_layout', 'dagre', 'html', ENUM('dagre', 'elk'),
                         #'Default value for the d2 ``:layout:`` option',
                         )
    app.add_config_value('d2_pad', 100, 'html', [int],
                         #'Default value for the d2 ``:pad:`` option',
                         )
    app.add_config_value('d2_redirect_links_to_blank_page', True, 'html', [bool],
                         #'Default value for the d2 ``:redirect_links_to_blank_page:`` option',
                         )
    app.add_config_value('d2_sketch', False, 'html', [bool],
                         #'Default value for the d2 ``:sketch:`` option',
                         )
    app.add_config_value('d2_theme', 0, 'html', [bool],
                         #'Default value for the d2 ``:theme:`` option',
                         )

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
