# Kubernetes Configuration for GHCR Images

This guide explains how to configure Kubernetes to pull Docker images from GitHub Container Registry (GHCR).

## Table of Contents

1. [Public Images](#public-images) - Since our repository is public, no authentication is required
2. [Private Images](#private-images) - For reference, if the repository becomes private
3. [Deployment Examples](#deployment-examples)
4. [Troubleshooting](#troubleshooting)

---

## Public Images

Since the repository is **public**, Kubernetes can pull images from GHCR without any authentication configuration.

### Direct Pull (No Credentials Needed)

For public GHCR images, simply reference the image directly in your Pod/Deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
      - name: flask-app
        image: ghcr.io/lesaloon/2026_s7_esiea_devops_cicd_tp2:latest
        ports:
        - containerPort: 8000
        env:
        - name: APP_DB_PATH
          value: /data/app.db
        volumeMounts:
        - name: data
          mountPath: /data
      volumes:
      - name: data
        emptyDir: {}
```

### Image URL Format

```
ghcr.io/<GITHUB_USERNAME>/<REPOSITORY_NAME>:<TAG>
```

Example:
```
ghcr.io/lesaloon/2026_s7_esiea_devops_cicd_tp2:latest
```

---

## Private Images

If the repository becomes private, follow these steps to configure Kubernetes:

### Step 1: Create a Docker Registry Secret

Create a Kubernetes secret to store GHCR credentials:

```bash
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=<GITHUB_USERNAME> \
  --docker-password=<GHCR_TOKEN> \
  --docker-email=<GITHUB_EMAIL> \
  -n default
```

**Parameters:**
- `<GITHUB_USERNAME>`: Your GitHub username
- `<GHCR_TOKEN>`: GitHub Personal Access Token with `read:packages` scope
- `<GITHUB_EMAIL>`: Your GitHub email

### Step 2: Reference the Secret in Deployment

Add `imagePullSecrets` to your Pod spec:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      imagePullSecrets:
      - name: ghcr-secret
      containers:
      - name: flask-app
        image: ghcr.io/lesaloon/2026_s7_esiea_devops_cicd_tp2:latest
        ports:
        - containerPort: 8000
        env:
        - name: APP_DB_PATH
          value: /data/app.db
        volumeMounts:
        - name: data
          mountPath: /data
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: flask-app-pvc
```

### Step 3: Verify the Secret

```bash
kubectl get secrets ghcr-secret -o jsonpath='{.data.\.dockerconfigjson}' | base64 --decode | jq .
```

---

## Deployment Examples

### Example 1: Simple Pod with Public Image

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: flask-app-pod
spec:
  containers:
  - name: flask-app
    image: ghcr.io/lesaloon/2026_s7_esiea_devops_cicd_tp2:latest
    ports:
    - containerPort: 8000
```

### Example 2: Deployment with Service

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app
  labels:
    app: flask-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
      - name: flask-app
        image: ghcr.io/lesaloon/2026_s7_esiea_devops_cicd_tp2:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8000
          name: http
        env:
        - name: APP_DB_PATH
          value: /data/app.db
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
        volumeMounts:
        - name: data
          mountPath: /data
      volumes:
      - name: data
        emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: flask-app-service
spec:
  selector:
    app: flask-app
  type: LoadBalancer
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
```

### Example 3: With PersistentVolumeClaim

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: flask-app-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
      - name: flask-app
        image: ghcr.io/lesaloon/2026_s7_esiea_devops_cicd_tp2:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
        env:
        - name: APP_DB_PATH
          value: /data/app.db
        volumeMounts:
        - name: data
          mountPath: /data
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: flask-app-pvc
```

---

## Troubleshooting

### Issue: ImagePullBackOff Error

If you see `ImagePullBackOff` errors, check:

1. **Image exists**: Verify the image exists on GHCR
   ```bash
   curl -s https://ghcr.io/v2/lesaloon/2026_s7_esiea_devops_cicd_tp2/manifests/latest \
     -H "Authorization: Bearer $(gh auth token)" | jq .
   ```

2. **Network connectivity**: Ensure your cluster can reach `ghcr.io`
   ```bash
   kubectl run -it --rm debug --image=alpine --restart=Never -- wget -O- https://ghcr.io
   ```

3. **Credentials (if private)**: Verify the secret is correctly configured
   ```bash
   kubectl describe secret ghcr-secret
   ```

### Issue: Authentication Failed for Private Repository

1. Verify the GHCR token has correct scopes:
   ```bash
   gh api user/repos -H "Authorization: token YOUR_TOKEN" | jq .
   ```

2. Recreate the secret if credentials changed:
   ```bash
   kubectl delete secret ghcr-secret
   kubectl create secret docker-registry ghcr-secret \
     --docker-server=ghcr.io \
     --docker-username=<USERNAME> \
     --docker-password=<NEW_TOKEN> \
     --docker-email=<EMAIL>
   ```

3. Force pod restart to pull new credentials:
   ```bash
   kubectl rollout restart deployment flask-app
   ```

### Issue: Image Version Not Found

Ensure the tag exists on GHCR:

```bash
# List available tags
gh api repos/lesaloon/2026_S7_ESIEA_DEVOPS_CICD_TP2/packages -q '.[].package_type'

# Or use docker CLI
docker pull ghcr.io/lesaloon/2026_s7_esiea_devops_cicd_tp2:latest
```

---

## Best Practices

1. **Use Image Pull Policies**:
   - `Always`: Always pull the image (ensures latest)
   - `IfNotPresent`: Use cached image if available (faster)
   - `Never`: Never pull (for offline environments)

2. **Use Specific Tags**: Avoid `:latest` in production; use versioned tags
   ```yaml
   image: ghcr.io/lesaloon/2026_s7_esiea_devops_cicd_tp2:v1.0.0
   ```

3. **Configure Resource Limits**: Prevent resource exhaustion
   ```yaml
   resources:
     requests:
       memory: "128Mi"
       cpu: "100m"
     limits:
       memory: "256Mi"
       cpu: "500m"
   ```

4. **Add Health Checks**: Use liveness and readiness probes
   ```yaml
   livenessProbe:
     httpGet:
       path: /health
       port: 8000
     initialDelaySeconds: 10
     periodSeconds: 30
   ```

5. **Use Secrets for Configuration**: Never hardcode sensitive data
   ```yaml
   env:
   - name: DB_PASSWORD
     valueFrom:
       secretKeyRef:
         name: app-secrets
         key: db-password
   ```

---

## Related Documentation

- [Kubernetes Image Pull Secrets](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/)
- [GitHub Container Registry (GHCR)](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [GHCR Authentication](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-to-the-container-registry)
