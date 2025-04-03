# programming-challenge
Web development challenge: FastAPI, Docker, NextJS, Object Storage

## Goal

- The overall functionality is to upload a file from the frontend through signed PUT URL to Minio, the object storage. And after the upload is done, the backend should print out the file size as MB.
- It should be runnable as a single docker compose file, consisting of 3 services:
  - FastAPI
  - NextJS
  - Minio
- There is already a boilerplate frontend in NextJS, with a input field to upload a file. Rest of the functionality needs to be implemented.




## Fast API docker
```bash
  docker-compose down && docker-compose up --build
```

### Frontend at - > http://127.0.0.1:3000/
### Minio at -->  "http://localhost:9001/browser/bucket"



