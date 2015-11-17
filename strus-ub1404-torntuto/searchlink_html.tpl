{% extends "search_html.tpl" %}

{% block ranklist %}
  <table border=1>
  <tr>
  <th align='left'>Weight</th>
  <th align='left'>Title</th>
  </tr>
  {% for result in results %}
	{% set weight = result['weight'] %}
	{% set title = result['title'] %}
	<tr>
	<td>{{ "%.4f" % weight}}</td>
	<td>{{title}}</td>
	</tr>
  {% end %}
  </table>
{% end %}

