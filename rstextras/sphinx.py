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
from .collector import MetaEnvCol
from .abstract import *
from .link import *
from .shellblock import *

# Visit None
def visit_none(self, node):
    raise nodes.SkipNode

# Setup Module
def setup(app):
    """ Function to configure Sphinx Meta Builder"""
    #app.add_builder(MetaBuilder)

    # Add Environment Collector
    app.add_env_collector(MetaEnvCol)

    # Add Directive
    app.add_directive('abstract', AbstractDirective)
    app.add_directive('shell-block', ShellBlockDirective)

    # Add Roles
    app.add_role('link', link_role)

    # Add Nodes
    app.add_node(
            shellblock_node,
            html=(visit_shellblock_html, depart_shellblock_html),
            latex=(visit_none, None),
            text=(visit_none, None))
    app.add_node(
            abstract_node,
            html=(visit_abstract_html, depart_abstract_html),
            latex=(visit_none, None),
            text=(visit_none, None))
    app.add_node(
            link_node,
            html=(visit_link_html, depart_link_html),
            latex=(visit_none, None),
            text=(visit_none, None))

    # Add Events
    app.connect('doctree-resolved', process_links)

    # Configuration
    config = [
            ('rstextras_show_abstract', False, True),
            ('rstextras_prompt', {}, True),

    ]

    for (name, default, rebuild) in config:
        app.add_config_value(name, default, config)
    



