import re
from markdown import markdown
from micawber import bootstrap_basic, parse_html
from bs4 import BeautifulSoup

oembed = bootstrap_basic()


class VisualizableMixin(object):
    def annotate(self, base_str=None, annotations=[], search_for=None):
        """Assume search_annotation has been added already, so replace that with a cleaner value."""

        if base_str is None:
            return ''
        
        HTML_WRAPPER = "<a href='{}' data-bs-toggle='tooltip' class='{}' title='' data-bs-original-title='{}'>{}</a>"
        split_body = []
        init = 0
        for i in annotations:
            label_class = "label"
            label_name = i.label
            # taking care of overlapping labels
            if search_for and search_for in label_name:
                label_class = "search_for"
                label_name = self.add_search_annotation(label_name, search_for)
            # substitute
            split_body.append(
                re.sub(
                    label_name,
                    HTML_WRAPPER.format(
                        "/search?query=" + i.label, label_class, i.category, label_name
                    ),
                    base_str[init : i.span_end],
                    flags=re.IGNORECASE,
                )
            )
            init = i.span_end
        split_body.append(base_str[init:])
        return "".join(split_body)

    @classmethod
    def generate_block_html(cls, string):
        # markdown extensions
        ext = ["tables", "extra", "meta", "smarty", "sane_lists", "toc"]
        html = parse_html(
            markdown(
                "\n".join([i.lstrip() for i in string.split("\n")]),
                extensions=ext,
            ),
            oembed,
            maxwidth=300,
            urlize_all=True,
        )
        return html

    @classmethod
    def beautify(cls, html):
        return BeautifulSoup(html, "lxml").prettify()

    @classmethod
    def add_search_annotation(cls, text, search_for):
        return re.sub(
            search_for,
            '<i class="search_for">' + search_for + "</i>",
            text,
            flags=re.IGNORECASE,
        )

    def html(self, search_for=None, annotations=None):
        if search_for:
            annotated = self.add_search_annotation(self.body, search_for=search_for)
            return self.generate_block_html(self.annotate(annotated, search_for))
        return self.generate_block_html(self.annotate(annotations=annotations))

    def short_html(self, length=400, search_for=None):
        """TODO clean this mess"""

        if not hasattr(self, "body") or not self.body:
            return ""
        # annotate small part of body if searching for something
        if search_for:
            # find first time in text
            index = self.body.find(search_for)
            start = int(index - length / 2)
            start = start if start >= 0 else 0
            end = int(index + length / 2)
            end = end if end <= len(self.body) else -1
            html_body = self.body[start:end]

            if start > 0:
                html_body = " ..." + html_body
            if end != -1:
                html_body += " ..."
            return self.add_search_annotation(html_body, search_for)

        # otherwise
        html_body = self.body[:length] + "..." if length < len(self.body) else self.body
        return html_body
