SELECT qz.uid as quiz_uid, qs.question 
FROM public.quiz as qz
INNER JOIN public.question as qs
ON qz.uid = qs.quiz_id
where qz.uid = 5;
