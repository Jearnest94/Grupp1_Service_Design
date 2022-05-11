INSERT INTO user (id, public_id, name, password, admin, latesttoken)
VALUES ('1', '1000', 'admin', 'sha256$WzY5OEEKKRNX5ls3$82968952bf67252a4f29558600c33891166ee68f2fc3c1548dd6e29347288c36', true, 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjYwMDAiLCJleHAiOjE2NTIyMjU2ODR9.BTsTglIyLE9QN8zNUKjDIzlldPrivxdtb2GTxcILG88');

INSERT INTO user (id, public_id, name, password, admin, latesttoken)
VALUES ('2', '2000', 'test', 'sha256$WzY5OEEKKRNX5ls3$82968952bf67252a4f29558600c33891166ee68f2fc3c1548dd6e29347288c36', true, 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjYwMDAiLCJleHAiOjE2NTIyMjU2ODR9.BTsTglIyLE9QN8zNUKjDIzlldPrivxdtb2GTxcILG88');

INSERT INTO user (id, public_id, name, password, admin, latesttoken)
VALUES ('3', '3000', 'user', 'sha256$WzY5OEEKKRNX5ls3$82968952bf67252a4f29558600c33891166ee68f2fc3c1548dd6e29347288c36', false, 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjYwMDAiLCJleHAiOjE2NTIyMjU2ODR9.BTsTglIyLE9QN8zNUKjDIzlldPrivxdtb2GTxcILG88');

INSERT INTO user (id, public_id, name, password, admin, latesttoken)
VALUES ('4', '4000', 'daniel', 'sha256$WzY5OEEKKRNX5ls3$82968952bf67252a4f29558600c33891166ee68f2fc3c1548dd6e29347288c36', true, 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjYwMDAiLCJleHAiOjE2NTIyMjU2ODR9.BTsTglIyLE9QN8zNUKjDIzlldPrivxdtb2GTxcILG88');

INSERT INTO user (id, public_id, name, password, admin, latesttoken)
VALUES ('5', '5000', 'movie_man', 'sha256$WzY5OEEKKRNX5ls3$82968952bf67252a4f29558600c33891166ee68f2fc3c1548dd6e29347288c36', true, 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjYwMDAiLCJleHAiOjE2NTIyMjU2ODR9.BTsTglIyLE9QN8zNUKjDIzlldPrivxdtb2GTxcILG88');

INSERT INTO user (id, public_id, name, password, admin, latesttoken)
VALUES ('6', '6000', 'adamsandler_fan', 'sha256$WzY5OEEKKRNX5ls3$82968952bf67252a4f29558600c33891166ee68f2fc3c1548dd6e29347288c36', true, 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjYwMDAiLCJleHAiOjE2NTIyMjU2ODR9.BTsTglIyLE9QN8zNUKjDIzlldPrivxdtb2GTxcILG88');

INSERT INTO user (id, public_id, name, password, admin, latesttoken)
VALUES ('7', '7000', 'realCarlBildt', 'sha256$WzY5OEEKKRNX5ls3$82968952bf67252a4f29558600c33891166ee68f2fc3c1548dd6e29347288c36', true, 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjYwMDAiLCJleHAiOjE2NTIyMjU2ODR9.BTsTglIyLE9QN8zNUKjDIzlldPrivxdtb2GTxcILG88');

INSERT INTO user (id, public_id, name, password, admin, latesttoken)
VALUES ('8', '8000', 'iceskater96', 'sha256$WzY5OEEKKRNX5ls3$82968952bf67252a4f29558600c33891166ee68f2fc3c1548dd6e29347288c36', true, 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjYwMDAiLCJleHAiOjE2NTIyMjU2ODR9.BTsTglIyLE9QN8zNUKjDIzlldPrivxdtb2GTxcILG88');

INSERT INTO review (id, text, rating, user_id, movie_id, title)
VALUES ('1', 'This was a good movie', '6.6', '1', '4', 'Not bad');

INSERT INTO review (id, text, rating, user_id, movie_id, title)
VALUES ('2', 'This was a bad movie', '8', '1', '1', 'Not good');

INSERT INTO review (id, text, rating, user_id, movie_id, title)
VALUES ('3', 'This was not a movie at all', '1', '5', '2', 'I cant believe they call this a movie');

INSERT INTO review (id, text, rating, user_id, movie_id, title)
VALUES ('4', 'I watched this with my little brother John and I fell asleep. Good acting though.', '9', '4', '3', 'Review title 6');

INSERT INTO review (id, text, rating, user_id, movie_id, title)
VALUES ('5', 'I cant remember the last time I saw a movie.', '11', '5', '9', 'Adobe Photoshop');

INSERT INTO review (id, text, rating, user_id, movie_id, title)
VALUES ('6', 'I cant remember the last time I saw a movie.', '11', '5', '10', 'Adobe Photoshop');

INSERT INTO review (id, text, rating, user_id, movie_id, title)
VALUES ('7', 'Good movie, but I really think Adam Sandler should have been in this one', '8', '6', '2', 'Sandler coulda made it better');

INSERT INTO review (id, text, rating, user_id, movie_id, title)
VALUES ('8', 'This is the first movie that made me cry!', '4', '7', '15', 'An emotional trip through life');

INSERT INTO review (id, text, rating, user_id, movie_id, title)
VALUES ('9', 'Best movie I have ever seen. And I dont even like movies', '9', '8', '4', 'It made me think');

