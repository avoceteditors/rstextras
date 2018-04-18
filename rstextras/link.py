# Copyright (c) 2018, Kenneth P. J. Dyer <kenneth@avoceteditors.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the name of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import re
from docutils import nodes

class link_node(nodes.Inline, nodes.Element):
    content = None
    docname = None
    uri = None
    title = None
    desc = None
    refdocname = None

    def set_values(self, text, rawtext, title, target, docname):
        self.desc = text
        self.rawtext = rawtext
        self.title = title
        self.target = target
        self.docname = docname

    def __repr__(self):
        return '<link-node title="%s" uri="%s"/>' % (self.title, self.uri)

def visit_link_html(self, node):
    try:
        self.body.append('<a class="%s" href="%s" title="%s">%s</a>'
                % ("reference internal rstextras-link",
                    node.uri,
                    node.desc,
                    node.title))
    except Exception as e:
        print(e)
        self.body.append('<a class="link-error">invalid</a>')

def depart_link_html(self, node):
    pass

def link_role(name, rawtext, text, lineo, inliner, options={}, content={}):

    env = inliner.document.settings.env
    docname = env.docname

    # Categorize Link
    if re.match("^.*?<.*?>$", text):
        div = re.split('<', text)
        title = div[0]
        idref = re.split('>', div[1])[0]

    else:
        title = text
        idref = text

    node = link_node()
    node.set_values(text, rawtext, title, idref, docname)

    return [node],[]


def process_links(app, doctree, fromdocname):

    env = app.builder.env

    try:
        meta = env.rstextras_metadata
        for link in doctree.traverse(link_node):
            try:
                data = meta.sections[link.target]
                content = text = data.abstract
                title = data.title
                refdocname = refuri = app.builder.get_relative_uri(link.docname, data.docname)
                refuri += "#%s" % link.target
            except Exception as e:
                print(e)
                content = text = title =link.target
                refdoname = link.docname
                refuri = ''

            link.content = content
            link.refdocname = refdocname
            link.uri = refuri
            link.title = title
            link.desc = text 

    except:
        pass
