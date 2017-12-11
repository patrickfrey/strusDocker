{% extends "search_base_html.tpl" %}

{% block resultblock %}
  <table border=1>
  <tr>
  <th align='left'>Weight</th>
  <th align='left'>Title</th>
  </tr>
  {% for result in results %}
	<tr>
	<td>{{ "%.4f" % result['weight'] }}</td>
	<td>{{ result['title'] }}</td>
	</tr>
  {% end %}
  </table>
{% end %}

