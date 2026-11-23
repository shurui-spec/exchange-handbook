---
layout: default
title: 首頁
---
# 交換生手冊

給中山大學交換生的手冊：從申請、與交換校對接，到抵達後的日常生活，依階段整理，並附上每項資訊的來源。

<div class="stages">
  <div class="stage-box"><span class="tag stage-apply">申請期</span><strong>選校與準備文件</strong><p>語言門檻、名額、讀書計畫</p></div>
  <div class="stage-box"><span class="tag stage-pre-departure">出發前</span><strong>與交換校對接</strong><p>選課、住宿、簽證</p></div>
  <div class="stage-box"><span class="tag stage-arrival">抵達後</span><strong>當地日常</strong><p>居留、開戶、交通、就醫</p></div>
</div>

{% assign groups = "school:學校|country:國家生活|guide:指南" | split: "|" %}
{% for g in groups %}
{% assign kv = g | split: ":" %}
{% assign items = site.pages | where: "type", kv[0] | sort: "title" %}
## {{ kv[1] }}

<div class="cards">
{% for p in items %}
  <a class="card" href="{{ p.url | relative_url }}">
    <h3>{{ p.title }}</h3>
    <p>{{ p.summary }}</p>
  </a>
{% endfor %}
</div>
{% endfor %}
