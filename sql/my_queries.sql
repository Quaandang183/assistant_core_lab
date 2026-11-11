-- Lab 5 Part F: write your queries for the assistant database here.
-- Q1 requests per intent
SELECT intent, COUNT(*) AS requests
FROM interaction
GROUP BY intent
ORDER BY requests DESC, intent;

-- Q2 average latency per intent
SELECT intent, ROUND(AVG(latency_ms), 1) AS avg_latency_ms
FROM interaction
GROUP BY intent
ORDER BY intent;

-- Q3 topics with the most thumbs-down (JOIN feedback with interaction)
SELECT i.topic, COUNT(*) AS thumbs_downs
FROM interaction AS i
JOIN feedback AS f ON f.request_id = i.request_id
WHERE f.rating = -1 AND i.topic IS NOT NULL
GROUP BY i.topic
ORDER BY thumbs_downs DESC, i.topic;

-- H2 What share of answers used a backup (degraded) path?
-- "answers" = interactions the bot could answer (resolved = 1); `degraded` is stored as 0/1.
SELECT intent,
       COUNT(*)                                        AS answers,
       SUM(degraded)                                   AS backup_answers,
       ROUND(100.0 * SUM(degraded) / COUNT(*), 1)      AS backup_pct
FROM interaction
WHERE resolved = 1
GROUP BY intent
ORDER BY backup_pct DESC, intent;
-- result:
--   rule      140 answers | 34 backup | 24.3 %
--   greeting   26 answers |  2 backup |  7.7 %
--   office     47 answers |  1 backup |  2.1 %
--   fee        61 answers |  1 backup |  1.6 %
-- overall: 274 answers, 38 backup = 13.9 %   (SELECT ... WHERE resolved = 1 without GROUP BY)
-- Reading: almost all backup answers are handbook rules, so that is where the AI provider should be hardened first.
