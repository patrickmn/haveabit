from django.utils.html import linebreaks

import settings
if settings.use_strftime:
    import gregtime

class Quote:

    def __init__(self):
        self.link = self.getLink()

    def renderTeaser(self):
        output = ''
        if self.img_url:
            output = '<img src="%s" title="%s" alt="%s"%s%s />' % (self.img_url, self.name, self.name, ' width="%s"' % (self.img_width,) if self.img_width else '', ' height="%s"' % (self.img_height,) if self.img_height else '')
        elif self.html:
            output = self.html
        elif self.author.img_url:
            output = '<img src="%s" title="%s" alt="%s"%s%s />' % (self.author.img_url, self.author.name, self.author.name, ' width="%s"' % (self.author.img_width,) if self.author.img_width else '', ' height="%s"' % (self.author.img_height,) if self.author.img_height else '')
        output = output + '<br /><br />' if output else ''
        return output

    def renderQuote(self, with_title=True):
        output = []
        if self.author.date_birth:
            dob = gregtime.strftime(self.author.date_birth, settings.strftime_format) if settings.use_strftime else str(self.author.date_birth.year)
            if self.author.date_death:
                dod = gregtime.strftime(self.author.date_death, settings.strftime_format) if settings.use_strftime else str(self.author.date_death.year)
                lifestr = ' (' + dob + '&ndash;' + dod + ')'
            else:
                in_prop = '' if settings.use_strftime else 'in '
                lifestr = ' (born ' + in_prop + dob + ')'
        else:
            lifestr = ''
        if with_title:
            output.append('<h1>' + self.name + '</h1>')
        output.append('<p><em>' + self.description + '</em></p>' if self.description else '')
        output.append('<div id="left">')
        if self.text:
            output.append("""<div id="quote">
<div>""" + linebreaks(self.text) + """<br />
</div>
</div>""")
        else:
            output.append('<br />')
        output.append("""</div>
<div id="right">
<p>&mdash; <strong>""" + self.author.name + '</strong>' + lifestr + '<br />' + self.author.description + '</p>')
        output.append('</div>')
        return '\r\n'.join(output)

    def getLink(self):
        return '%s/%s/%s' % (settings.address, self.author.slug, self.key().id())
