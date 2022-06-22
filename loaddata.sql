DELETE FROM app_api_curator;
DELETE FROM auth_user;
DELETE FROM authtoken_token;

UPDATE authtoken_token
SET user_id = 1
WHERE user_id = 2

UPDATE authtoken_token
SET user_id = 1
WHERE user_id = 3


DELETE FROM app_api_artist
WHERE id = 7;