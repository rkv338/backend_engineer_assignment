## Goal

Build a simple search engine on top of our data source.

Your system should expose a simple API endpoint (for example /search) that we can query and receive matching records from our data source.

## API

Use the `GET /messages` endpoint described in Swagger:
👉 https://november7-730026606190.europe-west1.run.app/docs#/default/get_messages_messages__get

## Requirements

1. Build a small API service that accepts a query and returns a paginated list of matching records. It should be implemented in latest stable version of Python. You can use web framework that you are most comfortable with. 
2. The service must be deployed and publicly accessible.
3. Endpoint should return results in under 100ms. 

## Bonus Goals
### Bonus 1: Design Notes

In your README.md, describe several alternative approaches you considered for building the search engine.

### Bonus 2: Data Insights

Explain how we can reduce the latency to 30ms. 



## Submission

1. Create a public GitHub repository.
2. Deploy your service.
3. Share your work with us.
