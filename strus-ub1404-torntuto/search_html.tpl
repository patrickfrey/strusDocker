<html>
  <head>
  <title>A search engine with Python, Tornado and Strus</title>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  </head>
  <body>
  <h1>A search engine with Python, Tornado and Strus</h1>

  <form name="search" class method="GET" action="query">
  <input id="search_input" class="textinput" type="text" maxlength="256" size="32" name="q" tabindex="1" value="{{querystr}}"/>
  <input type="hidden" name="i" value="0"/>
  <input type="hidden" name="n" value="{{nofranks}}"/>
  <input type="hidden" name="s" value="{{scheme}}"/>
  <input type="radio" name="s" value="NBLNK" {% if scheme == "NBLNK" %}checked{% end %}/>NBLNK
  <input type="radio" name="s" value="BM25"      {% if scheme == "BM25" %}checked{% end %}/>BM25
  <input type="submit" value="FIND"/>
  </form>

  {% block ranklist %}
  <table border=1>
  <tr>
  <th align='left'>Docno</th>
  <th align='left'>Weight</th>
  <th align='left'>Title</th>
  <th align='left'>Abstract</th>
  </tr>
  {% for result in results %}
	{% set content = "" %}
	{% set title = "" %}
	{% for attribute in result.attributes() %}
		{% if attribute.name() == 'CONTENT' %}
			{% if content != "" %}
			{%	set content += ' ... ' %}
			{% end %}
			{% set content += attribute.value() %}
		{% elif attribute.name() == 'TITLE' %}
			{% set title += attribute.value() %}
		{% end %}
	{% end %}
	<tr>
	<td>{{result.docno()}}</td>
	<td>{{ "%.4f" % result.weight()}}</td>
	<td>{{title}}</td>
	<td>{% raw content %}</td>
	</tr>
  {% end %}
  </table>
  {% if firstrank > 0 %}
	{% if firstrank > nofranks %}
		{% set nextrank = firstrank - nofranks %}
	{% else %}
		{% set nextrank = 0 %}
	{% end %}
	<form name="nav_prev" class method="GET" action="query">
	<input type="hidden" name="q" value="{{querystr}}"/>
	<input type="hidden" name="n" value="{{nofranks}}"/>
	<input type="hidden" name="i" value="{{nextrank}}"/>
	<input type="hidden" name="s" value="{{scheme}}"/>
	<input type="submit" value="PREV"/>
	</form>
  {% end %}
  {% if nofranks == len(results) %}
	{% set nextrank = firstrank + nofranks %}

	<form name="nav_next" class method="GET" action="query">
	<input type="hidden" name="q" value="{{querystr}}"/>
	<input type="hidden" name="n" value="{{nofranks}}"/>
	<input type="hidden" name="i" value="{{nextrank}}"/>
	<input type="hidden" name="s" value="{{scheme}}"/>
	<input type="submit" value="NEXT"/>
	</form>
  {% end %}
  {% end %}
</body>
</html>

