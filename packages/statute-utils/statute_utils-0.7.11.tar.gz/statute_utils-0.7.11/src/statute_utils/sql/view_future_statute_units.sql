-- Statute units in the future can refer to statutes in the past

with future_mentions(units) AS (
  select
    json_group_array(
      json_object(
        "affector_locator",
        su.item,
        "affector_caption", -- can't use "caption" here for some reason, complains JSON_OBJECT must be TEXT
        su.caption,
        "affector_content", -- can't use "content" here for some reason, complains JSON_OBJECT must be TEXT
        su.content,
        "affector_material_path",
        su.material_path,
        "affector_statute_id",
        su.statute_id,
        "affector_statute",
        (
          select text
          from statute_titles st
          where st.statute_id = su.statute_id and st.cat = 'serial'
        ),
        "affector_statute_date",
        su.date
      )
      order by su.date desc
    )
  from
    statute_references sr
    join statute_units su on su.id = sr.affector_statute_unit_id
  where
    sr.statute_id = s.id
  order by su.date desc
)
select
  s.id,
  (
    select
      units
    from
      future_mentions
  ) future_statute_units,
  (
    select
      json_array_length(units)
    from
      future_mentions
  ) future_statute_units_count
from statutes s
where future_statute_units_count > 0
