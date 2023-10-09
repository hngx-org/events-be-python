# Documentation
### API ENDPOINTS 
##### 1.  `https://eventspy.pythonanywhere.com/api/events/calendar`
##### 2.` https://eventspy.pythonanywhere.com/api/events/:id`
### Sample Usage
##### 1. Get users calendar event
 ##### Sample request
- Endpoint :  `https://events-be-python.vercel.app/api/events/calendar`
- Method: `GET`
- 'Authorization: Bearer: 
  ```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk3NzQ3NzgzLCJpYXQiOjE2OTY4ODM3ODMsImp0aSI6IjJmM2MxOGUxNGIzMDQyMmNiOWViYjU4ZTJmMzI1OWI3IiwidXNlcl9pZCI6IjQ0NjQ3YzBiLTcyMWMtNGE1Zi04N2YzLWViNjhlMDA2YWI2MCJ9.6SsBy_hiwKZ2A7_HlFHsqE85j0F5sBbwZZtiimYzBOg'
      ```
##### Sample response 
 ```
{
  "calenderDetail": [
    {
      "title": Football,
      "start_date": "2023-10-09",
      "end_date": "2023-10-09",
      "start_time": "00:00:00",
      "end_time": "02:02:02"
    }
  ]
}
```
##### 1. Delete Event
 ##### Sample request
- Endpoint :  `https://events-be-python.vercel.app/api/events/:id`
- Method: `DELETE`
- 'Authorization: Bearer: 
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk3NzQ3NzgzLCJpYXQiOjE2OTY4ODM3ODMsImp0aSI6IjJmM2MxOGUxNGIzMDQyMmNiOWViYjU4ZTJmMzI1OWI3IiwidXNlcl9pZCI6IjQ0NjQ3YzBiLTcyMWMtNGE1Zi04N2YzLWViNjhlMDA2YWI2MCJ9.6SsBy_hiwKZ2A7_HlFHsqE85j0F5sBbwZZtiimYzBOg'
 ```
##### Sample response 
 ```
 status: 204
{"message": "Event deleted successfully."}
```