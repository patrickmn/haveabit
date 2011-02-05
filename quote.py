from django.utils.html import linebreaks

import settings

def renderTeaser(q):
    output = ''
    if q.img_url:
        output = '<img src="%s" title="%s" alt="%s" />' % (q.img_url, q.name, q.name)
    elif q.html:
        output = q.html
    elif q.author.img_url:
        output = '<img src="%s" title="%s" alt="%s" />' % (q.author.img_url, q.author.name, q.author.name)
    output = output + '<br /><br />' if output else ''
    return output
                                                                                    
def renderQuote(q, with_title=True):
    output = []
    if q.author.date_birth:
        dob = gregtime.strftime(q.author.date_birth, settings.strftime_format) if settings.use_strftime else str(q.author.date_birth.year)
        if q.author.date_death:
            dod = gregtime.strftime(q.author.date_death, settings.strftime_format) if settings.use_strftime else str(q.author.date_death.year)
            lifestr = ' (' + dob + '&ndash;' + dod + ')'
        else:
            in_prop = '' if settings.use_strftime else 'in '
            lifestr = ' (born ' + in_prop + dob + ')'
    else:
        lifestr = ''
    if with_title:
        output.append('<h1>' + q.name + '</h1>')
    output.append('<p><em>' + q.description + '</em></p>' if q.description else '')
    output.append("""<div id="left">
<div id="quote">
<div>""" + linebreaks(q.text) + """<br />
</div>
</div>
</div>
<div id="right">
<p>&mdash; <strong>""" + q.author.name + '</strong>' + lifestr + '<br />' + q.author.description + '</p>')
    output.append('</div>')
    return '\r\n'.join(output)
