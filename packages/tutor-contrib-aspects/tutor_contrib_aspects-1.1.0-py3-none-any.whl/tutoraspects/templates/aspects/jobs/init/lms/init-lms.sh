# Create a DOT applicaton so Superset can use Open edX authenticatioon
./manage.py lms manage_user superset superset@apache
./manage.py lms create_dot_application \
    --grant-type authorization-code \
    --redirect-uris "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ SUPERSET_HOST }}/oauth-authorized/openedxsso" \
    --client-id {{ SUPERSET_OAUTH2_CLIENT_ID }} \
    --client-secret {{ SUPERSET_OAUTH2_CLIENT_SECRET }} \
    --scopes "user_id" \
    superset-sso superset
./manage.py lms create_dot_application \
    --grant-type authorization-code \
    --redirect-uris "http://{{ SUPERSET_HOST }}:{{SUPERSET_PORT}}/oauth-authorized/openedxsso" \
    --client-id {{ SUPERSET_OAUTH2_CLIENT_ID_DEV }} \
    --client-secret {{ SUPERSET_OAUTH2_CLIENT_SECRET }} \
    --scopes "user_id" \
    superset-sso-dev superset

{% if RUN_RALPH %}
cat > /tmp/erb_config.json <<EOF
{
  "model": "event_routing_backends.RouterConfiguration",
  "data":
  [
    {
      "enabled": true,
      "backend_name": "xAPI",
    "route_url": "{% if RUN_RALPH %}http://ralph:{{ RALPH_PORT }}{% else %}{% if RALPH_RUN_HTTPS %}https://{% else %}http://{% endif %}{{ RALPH_HOST }}{% endif %}/xAPI/",
      "auth_scheme": "Basic",
      "username": "{{ RALPH_LMS_USERNAME }}",
      "password": "{{ RALPH_LMS_PASSWORD }}"
    }
  ]
}
EOF

./manage.py lms manage_user tutor-contrib-aspects aspects@axim --unusable-password
./manage.py lms populate_model -f /tmp/erb_config.json -u tutor-contrib-aspects
{% endif %}

{% for model in EVENT_SINK_MODELS_ENABLED %}
(./manage.py lms waffle_flag --list | grep event_sink_clickhouse.{{model}}.enabled) || ./manage.py lms waffle_flag --create event_sink_clickhouse.{{model}}.enabled --everyone
{% endfor %}

{% if ASPECTS_ENABLE_PII %}
  {% for model in EVENT_SINK_PII_MODELS %}
(./manage.py lms waffle_flag --list | grep event_sink_clickhouse.{{model}}.enabled) || ./manage.py lms waffle_flag --create event_sink_clickhouse.{{model}}.enabled --everyone
  {% endfor %}
{% endif %}
