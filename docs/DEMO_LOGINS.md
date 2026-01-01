# Demo Logins (Assessment Only)

These credentials are for assessment and demo purposes only. Do not use in production.

## Doctors

Default demo doctors created via the management command:
- doctor1 / Test@12345
- doctor2 / Test@12345
- doctor3 / Test@12345
- doctor4 / Test@12345
- doctor5 / Test@12345

If a username already exists, the command skips it and continues.

## Notes for doctor1

If doctor1 exists but is missing a Doctor profile, run:
`heroku run python manage.py bootstrap_demo_doctors --count 5 --password "Test@12345" --approve --repair-existing -a hospital-management-web`

## Notes

- These accounts are intended for assessment and demonstration.
- Remove demo accounts after assessment if required.
