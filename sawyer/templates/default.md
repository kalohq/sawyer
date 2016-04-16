## [{{ current_tag }}](https://github.com/{{ owner }}/{{ repo }}/tree/{{ current_tag }}) (Unreleased)

[Compare to previous release](https://github.com/{{ owner }}/{{ repo }}/compare/{{ previous_tag }}...{{ current_tag }})

**Added**:

{% for pr in pull_requests -%}
- {{ pr.raw.title }}
  ([@{{ pr.user }}](https://github.com/{{ pr.user }}/)
  in [\#{{pr.number}}](https://github.com/{{ owner }}/{{ repo }}/pull/{{ pr.number }}/))
{% endfor %}
