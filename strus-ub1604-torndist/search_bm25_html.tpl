{% extends "search_base_html.tpl" %}

{% block resultblock %}
{% for message in messages %}
<p><font color="red">Error: {{message}}</font></p>
{% end %}
<table border=1>
<tr>
<th align='left'>Docno</th>
<th align='left'>Weight</th>
<th align='left'>Docid</th>
<th align='left'>Title</th>
<th align='left'>Abstract</th>
</tr>
{% for result in results %}
<tr>
<td>{{ result.docno }}</td>
<td>{{ "%.4f" % result.weight }}</td>
<td>{{ result.docid }}</td>
<td>{{ result.title }}</td>
<td>{% raw result.abstract %}</td>
</tr>
{% end %}
</table>
{% end %}

