SELECT title FROM movies
    WHERE id IN (SELECT movie_id FROM stars
    WHERE person_id = (SELECT id FROM people WHERE name = "Johnny Depp")
    OR person_id = (SELECT id FROM people WHERE name = "Helena Bonham Carter")
    GROUP BY movie_id
    Having COUNT(movie_id) > 1)
    