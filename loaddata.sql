DELETE FROM app_api_curator;
DELETE FROM auth_user;

UPDATE authtoken_token
SET user_id = 1
WHERE user_id = 2