# Weather Finder  
  
  
Weather finder is a django application to get weather details of any given city. Weather data is retrieved using [Open weather map apis](https://openweathermap.org/api).  

Weather finder supports English, German and French languages.
  
## Major frameworks/libraries used  
  
- django  
- django rest framework  
- marshmallow   
- django-redis  
- pytest  
- flake8  
  
## Development  
  
Make sure you have docker up and running with docker compose version >= 1.22.0

**Clone repo locally**

   
    git clone https://github.com/sreekanthkaralmanna/weather-finder.git
    
	cd weather-finder

**Update environment variables**

Create an API key from [https://openweathermap.org/](https://openweathermap.org/) and update  the value of the key `OPEN_WEATHER_API_KEY` in `docker/dev/weather_finder.env` and `docker/prod/weather_finder.env`

**Run app using django runserver**

    make docker-dev-up
	
app should be up and running at http://localhost:8000/

**Run app using gunicorn workers**

    make docker-prod-up
	
app should be up and running at http://localhost:5000/

## Improvements and Next steps
-  Translation texts are created using google translator. Might need improvement.
- List of cities are fetched using openweathermap api now. This can be stored in database on production release to reduce number of external api calls.
- Openweathermap bulk API is returning multiple cities from same country for few city queries (Eg: `q=Dubai` is returning two entries, both in UAE).