# DA3408 AIOps Lab - Assignment 2

- Find the 2-pager writeup in `Writeup.pdf`. All conceptual questions have been answered there only.
- The video walkthrough of the solutions is available [here](https://drive.google.com/file/d/1NcskrG-WbV0vkKsi5PJolb0NZCp_FjLU/view?usp=sharing).
- This repository contains 4 directories: one for every question.
- In each directory, `generate_data.py` generates the data required for that question, `train.py` trains the model, `app.py` is the code of the webapp powered by FastAPI `requirements.txt` contains the required dependencies and `Dockerfile` is the Dockerfile needed to build the docker image.

## Q1 Single Stage vs Multi Stage Docker
- Typically models are not trained while building the docker image. However, in order to demonstrate the efficiency introduced in multi-stage Dockerfiles, data generation and model training was also done during the build phase.
- For uniformity, this was followed for all future questions also.

```
# Build the naive single-stage Docker image and run it on port 8000
docker build . -t spam-classifier:naive -f Dockerfile.naive
docker run -p 8000:8000 spam-classifier:naive

# In a separate terminal, test that the predictor app is working by curl command
curl -X GET http://localhost:8000/healthz
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"text":"<SOME-TEXT-TO-TEST>"}'

# Build the multi-stage Docker image and run it on port 8000
docker build . -t spam-classifier:multistage -f Dockerfile.multistage
docker run -p 8000:8000 spam-classifier:multistage

# In a separate terminal, test that the predictor app is working by curl command
curl -X GET http://localhost:8000/healthz
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"text":"<SOME-TEXT-TO-TEST>"}'

# Compare size of the two images
docker images
```

## Q2 Multi-container Orchestration with Docker Compose
- `app.py` was modified to use Redis cache and `docker-compose.yml` was created.
```
# Build the spam classifier image that uses Redis cache
docker build . -t spam-classifier:latest

# Build and run the two-contained application with docker compose (by default docker-compose.yml is used)
docker compose up --build

# In a separate terminal, test the time taken by the application to predict different input texts
python test_perf.py
```

## Q3 Kubernetes Indexed Job: Parallel Data Validation
- `generate_data.py` generates 8 csvs with 100 entries each. With a probability of 20%, a random field in every entry is set to None (simulating missing data).
- `validate.py` reads a shard and counts the number of invalid rows (rows with missing fields). It prints the node name, pod name (environment variables) and the number of invalid rows in the csv.
- `job.yaml` specifies the Kubernetes Indexed Job, using a parallelism of 4 over 2 nodes with 2 cpus each.
```
# Start two minikube nodes allocating 2 cpus to each
minikube start --nodes 2 --cpus 2

# Build the image specified in Dockerfile in the nodes directly
minikube image build -t signup-validator:latest --all .

# Start the job
kubectl apply -f job.yaml

# Check the status of the allocated pods
kubectl get pods -l app=signup-validator -o wide

# Print the logs produced by every pod
for pod in $(kubectl get pods -l app=signup-validator -o jsonpath='{.items[*].metadata.name}'); do
    kubectl logs $pod
done

# Delete the minikube nodes before leaving
minikube delete
```

## Q4 Kubernetes Deployments: Self-Healing & Rolling Updates
```
# Start a minikube cluster and load the spam classifier image built in Q1
minikube start --cpus 2
minikube image load spam-classifier:multistage

# Deploy the predictor as a service
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# --- Self Healing ---

# Inspect the pods
kubectl get pods

# Delete a pod and re-inspect to see a new pod has taken its place
kubectl delete pods <pod-name>
kubectl get pods

# --- Rolling updates ---

# Make changes to app.py and re-build the image
minikube image build -t spam-classifier:v2 --all .

# Change the image and rollout the changes in all running nodes
kubectl set image deployment/spam-classifier-deployment spam-classifier=spam-classifier:v2
kubectl rollout status deployment/spam-classifier-deployment

# Inspect history to check that the update completed without any downtime
kubectl rollout history deployment/spam-classifier-deployment
```

# LLM Usage Disclosure

**ChatGPT** and **Gemini** were used for understanding, generating boilerplates and debugging. It included:
- Understanding Kubernetes concepts.
- Generating initial drafts of python scripts and yaml files, which were later verified and modified by me.
- Debugging errors like wrong python syntax and image building in kubernetes nodes.

LLMs were NOT used to write the final code or writeup and I take the full responsibility of my work.
