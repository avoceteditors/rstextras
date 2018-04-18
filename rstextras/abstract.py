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

# Module Imports
from docutils.parsers.rst import Directive, directives
from sphinx.util.console import darkgreen, bold
from docutils import nodes


# Abstract Node
class abstract_node(nodes.Element):
    title = ''
    abstract = ''

    def __repr__(self):
        return '<abstract-node title="%s" abstract="%s"/>' % (self.title, self.abstract)

def visit_abstract_html(self, node):
    pass

def depart_abstract_html(self, node):
    pass


class AbstractDirective(Directive):

    has_content = True
    option_spec = {
        'show': directives.flag
    }

    def run(self):
        length = len(self.content)

        work_node = abstract_node('\n'.join(self.content))
        self.state.nested_parse(self.content, self.content_offset, work_node)



        # Set Values
        if 'show' in self.options: 
            node = work_node
        else:
            node = abstract_node()

        node.title = work_node.traverse(nodes.paragraph)[0]
        node.abstract = work_node.astext() 

        return [node]


