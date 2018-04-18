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

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.utils.code_analyzer import Lexer
import re


# Node
class shellblock_node(nodes.Element):
    pass

def visit_shellblock_html(self, node):
    self.body.append('<pre class="shell-block">')

def depart_shellblock_html(self, node):
    self.body.append('</pre>')

class shell:

    def __init__(self, conf, line):
        self.lines = []
        self.ps1 = ""
        self.ps2 = ""
        self.conf = conf
        self.parse_conf()
        self.add(line)
        self.flines = []

    def add(self, line):
        self.lines += [line]

    def parse_conf(self):
        for i in ['ps1', 'ps2', 'lang']:
            check = self.add_conf(i)
        if not check:
            self.lang = 'text'

    def add_conf(self, val):
        if val in self.conf:
            setattr(self, val, self.conf[val])
            return True
        else:
            setattr(self, val, "")
            return False

    def parse_content(self):
        for i in range(len(self.lines)):
            base = self.lines[i]
            l = re.sub("^[\S]*?> ", "", base)

            if i == 0:
                prompt = nodes.Text('\n' + self.ps1)
            else:
                prompt = nodes.Text(self.ps2)

            text = nodes.Text(l + '\n')

            node = nodes.strong()
            node.append(text)

            self.flines.append([prompt, node])
        return self.flines 








class ShellBlockDirective(Directive):

    has_content = True
    option_spec = {
        'caption': directives.unchanged_required,
        'class': directives.class_option,
        'name': directives.unchanged
    }

    def run(self):
        document = self.state.document
        env = document.settings.env
        new = []
        
        # Find Prompt Text
        for i in self.content:

            if re.match("^-> .*?$", i):
                try:
                    new[-1].add(i)
                except:
                   self.join_prompt(new, i) 
            elif re.match("[\S]*?> .*?$", i):
                key = re.sub("> .*?$", "", i)
                if key in env.config.rstextras_prompt:
                    conf = env.config.rstextras_prompt[key]
                    s = shell(conf, i)
                    new.append(s)
            else:
                self.join_prompt(new, i)

        # Build Document
        node = shellblock_node() 

        for i in new:
            if isinstance(i, str):
                node.append(nodes.Text(i))
            else:
                prompt = i.parse_content()
                for [p, code] in prompt:
                    node.append(p)
                    node.append(code)
        return [node]

    def join_prompt(self, block, add):
        
        try:
            block[-1] = '\n'.join([block[-1], add])
        except:
            block.append(add)


                




