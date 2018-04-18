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

from sphinx.environment.collectors import EnvironmentCollector
from docutils import nodes
import pickle
from os.path import join
from .abstract import abstract_node


class MetaEnvCol(EnvironmentCollector):

    def clear_doc(self, app, env, docname):
        pass

    def process_doc(self, app, doctree):

        doctreedir = app.doctreedir
        self.env = env = app.env
        path = join(doctreedir, "metadata.pickle")

        if hasattr(env, "rstextras_metadata"):
            meta = env.rstextras_metadata
        else:

            try:
                with open(path, "rb") as f:
                    meta = pickle.load(f)
            except:
                meta = ProjectMetadata()

        # Traverse for Section Data
        for section in doctree.traverse(nodes.section):
            self.parse_section(meta, section, env.docname)

        # Traverse Targets for Rubics and Abstracts 
        for target in doctree.traverse(nodes.target):
            self.parse_target(meta, target, env.docname)

        # Save Changes for Next Read
        setattr(env, 'rstextras_metadata', meta)

        try:
            with open(path, "wb") as f:
                pickle.dump(f, meta)
        except:
            pass

    def parse_section(self, meta, section, docname):
        title = section.next_node()
        idrefs = section.get('ids')

        if isinstance(title, nodes.title):
            idref = idrefs[-1]
            meta.add_section(idref, title, None, docname)

    def parse_target(self, meta, target, docname):
        abstract = '' 
        parent = next_node = target.parent
        
        i = 0
        idref = title = target.get('refid')
        check_next = False
        for child in parent:
            if isinstance(child, nodes.target):
                if idref == child.get('refid'):
                    check_next = True
            elif check_next:
                if isinstance(child, nodes.rubric):
                    pass
                elif isinstance(child, abstract_node):
                    title = child.title
                    abstract = child.abstract
                break
            else:
                prev = child


        meta.add_section(idref, title, abstract, docname)


class ProjectMetadata():

    sections = {}

    def add_section(self, idref, title, abstract, docname):
        self.sections[idref] = SectionMetadata(title, idref, abstract, docname)

    def __repr__(self):
        return '<metadata values="%s"/>' % self.sections


class SectionMetadata():

    title = None 
    idref = "" 
    abstract = None
    docname = None

    def __init__(self, title, idref, abstract, docname):
        self.title = title
        self.idref = idref
        self.abstract = abstract
        self.docname = docname

    def __repr__(self):
        return '<section-metadata title="%s" idref="%s" abstract="%s"/>' % (self.title, self.idref, self.abstract)

    def contains(self, idref):
        if idref in idrefs:
            return True
        else:
            return False

    def set_abstract(self, node):
        self.abstract = node




