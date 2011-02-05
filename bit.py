from django.utils.html import linebreaks

import settings
if settings.use_strftime:
    import gregtime

class Quote:

    def renderTeaser(self):
        output = ''
        if self.img_url:
            output = '<img src="%s" title="%s" alt="%s" />' % (self.img_url, self.name, self.name)
        elif self.html:
            output = self.html
        elif self.author.img_url:
            output = '<img src="%s" title="%s" alt="%s" />' % (self.author.img_url, self.author.name, self.author.name)
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
        output.append("""<div id="left">
<div id="quote">
<div>""" + linebreaks(self.text) + """<br />
</div>
</div>
</div>
<div id="right">
<p>&mdash; <strong>""" + self.author.name + '</strong>' + lifestr + '<br />' + self.author.description + '</p>')
        output.append('</div>')
        return '\r\n'.join(output)

    def getLink(self):
        return '%s/%s/%s' % (settings.address, self.author.slug, self.key().id())
