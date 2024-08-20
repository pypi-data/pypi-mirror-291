-- target: statute
-- is: mentioned
-- by: statute units in the future
-- mentions: number of times same statute unit refers to target
select
	sr.statute_id target,
  su.id,
	su.item,
	su.caption,
	su.content,
	su.material_path,
	su.statute_id,
	st.text serial,
	su.date,
  count(su.id) mentions
from
	statute_references sr
	join statute_units su on su.id = sr.affector_statute_unit_id
	join statute_titles st on st.statute_id = su.statute_id and st.cat = 'serial'
GROUP BY
	su.id
ORDER BY
	target desc, su.date desc
