-- target: statute
-- is: mentioned
-- by: codifications in the future
-- mentions: number of times codifications refers to target
WITH statute_base(id) AS (
	SELECT
		s.id
	FROM
		statutes s
		join codifications c
	WHERE
		s.cat = c.cat
		and s.num = c.num
		and c.id = cs.codification_id
),
serial_statute_title(text) AS (
	SELECT
		st.text
	FROM
		statute_titles st
	WHERE
		st.cat = 'serial'
		and st.statute_id = (
			select
				id
			from
				statute_base
		)
),
official_statute_title(text) AS (
	SELECT
		st.text
	FROM
		statute_titles st
	WHERE
		st.cat = 'official'
		and st.statute_id = (
			select
				id
			from
				statute_base
		)
)
SELECT
	cs.statute_id target,
	cs.codification_id,
	(
		SELECT
			title
		FROM
			codifications
		WHERE
			id = cs.codification_id
	) title,
	(
		SELECT
			text
		FROM
			serial_statute_title
	) base_serial_title,
	(
		SELECT
			text
		FROM
			official_statute_title
	) base_official_title,
	count(cs.statute_id) mentions
FROM
	codification_statutes cs
GROUP BY
	cs.statute_id
