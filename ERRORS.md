# Error codes
Error code views like
```json
{
	'detail': {
		'msg': 'Error message',
		'code': code
	}
}
```

## Errors documentation

|  Code  | Message | Reason  |
| ------------ | ------------ | ------------ |
| 1  | 	Invalid token  | Access token is not valid  |
| 2  | Token expired  | Token expired  |
| 3  |  User with this email or login already exists  | Try another login or email  |
| 4  |  Could not validate credentials  |   |
| 5  | Code is not found  | Email verify code is not found   |
| 6  | Mail code is not valid  | Email verify code incorrect   |
| 7  | Login or password is not valid | Login or password is invalid |