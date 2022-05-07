INSERT INTO user (id, public_id, name, password, admin)
VALUES ('1', '6000', 'admin', 'sha256$WzY5OEEKKRNX5ls3$82968952bf67252a4f29558600c33891166ee68f2fc3c1548dd6e29347288c36', true);

INSERT INTO user (id, public_id, name, password, admin)
VALUES ('2', '8000', 'test', 'sha256$WzY5OEEKKRNX5ls3$82968952bf67252a4f29558600c33891166ee68f2fc3c1548dd6e29347288c36', true);

INSERT INTO user (id, public_id, name, password, admin)
VALUES ('3', '2000', 'user', 'sha256$WzY5OEEKKRNX5ls3$82968952bf67252a4f29558600c33891166ee68f2fc3c1548dd6e29347288c36', false);

INSERT INTO review (id, text, rating, user_id, movie_id)
VALUES ('1', 'This was a good movie', '6.6', '1', '500');

INSERT INTO review (id, text, rating, user_id, movie_id)
VALUES ('2', 'This was a bad movie', '8', '2', '1');

INSERT INTO review (id, text, rating, user_id, movie_id)
VALUES ('3', 'This was not a movie at all', '1', '3', '2');

INSERT INTO review (id, text, rating, user_id, movie_id)
VALUES ('4', 'Super nice movie', '10', '1', '2');
