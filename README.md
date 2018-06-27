# role_model_match
This is the Role Model Matcher, my Insight project.

## Required Environment Variables
```
export DATABASE_URL="postgres://[username]@[IP]:[port]/[database-name]" <Heroku provides this automatically>
export DATABASE_SSL_MODE="[allow|require]"
```

## Git
### Committing changes
```
git status
git add <modified files>
git status
git commit -m "<description of changes>"
```
### Pushing to github
```
git push
```
### Deploying to Heroku
``` 
git push heroku
```

## Pipenv
### Installing new dependency
```
pipenv install <library names>
```
### Entering environment
```
pipenv shell
```

## Flask
### Starting local development server
```
FLASK_ENV=development FLASK_APP=app.py flask run
```
