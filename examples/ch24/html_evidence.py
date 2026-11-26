"""Parse expected HTML syntax; this does not execute Django or a browser."""
from html.parser import HTMLParser


class PageEvidence(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_title = False
        self.title_text = ""
        self.inputs = {}
        self.active_tags = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "h1" and attributes.get("id") == "note-title":
            self.in_title = True
        if tag == "input" and "name" in attributes:
            self.inputs[attributes["name"]] = attributes.get("value", "")
        if tag in ("script", "img", "iframe"):
            self.active_tags.append(tag)

    def handle_endtag(self, tag):
        if tag == "h1":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title_text += data


if __name__ == "__main__":
    expected_html = '<h1 id="note-title">A &amp; B</h1><input name="title" value="A &amp; B">'
    page = PageEvidence()
    page.feed(expected_html)
    print("HTML source:", expected_html)
    print("parsed title:", page.title_text)
    print("parsed input:", page.inputs["title"])
    assert page.title_text == page.inputs["title"] == "A & B"
