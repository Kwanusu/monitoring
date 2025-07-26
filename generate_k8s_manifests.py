import os
import yaml
import base64

# Create the output directory
os.makedirs("k8s", exist_ok=True)

# ---------------- Deployment ----------------
deployment = {
    "apiVersion": "apps/v1",
    "kind": "Deployment",
    "metadata": {"name": "flask-app"},
    "spec": {
        "replicas": 1,
        "selector": {"matchLabels": {"app": "flask-app"}},
        "template": {
            "metadata": {"labels": {"app": "flask-app"}},
            "spec": {
                "containers": [
                    {
                        "name": "flask-app",
                        "image": "<IMAGE>",
                        "ports": [{"containerPort": 5000}],
                        "env": [
                            {
                                "name": "APP_ENV",
                                "valueFrom": {
                                    "configMapKeyRef": {
                                        "name": "flask-config",
                                        "key": "APP_ENV",
                                    }
                                },
                            },
                            {
                                "name": "SECRET_KEY",
                                "valueFrom": {
                                    "secretKeyRef": {
                                        "name": "flask-secret",
                                        "key": "SECRET_KEY",
                                    }
                                },
                            },
                        ],
                        "volumeMounts": [
                            {"name": "flask-volume", "mountPath": "/app/config"}
                        ],
                        "livenessProbe": {
                            "httpGet": {"path": "/health", "port": 5000},
                            "initialDelaySeconds": 5,
                            "periodSeconds": 10,
                        },
                        "readinessProbe": {
                            "httpGet": {"path": "/ready", "port": 5000},
                            "initialDelaySeconds": 5,
                            "periodSeconds": 5,
                        },
                    }
                ],
                "volumes": [
                    {"name": "flask-volume", "configMap": {"name": "flask-config"}}
                ],
            },
        },
    },
}

# ---------------- Service ----------------
service = {
    "apiVersion": "v1",
    "kind": "Service",
    "metadata": {"name": "flask-service"},
    "spec": {
        "selector": {"app": "flask-app"},
        "ports": [{"protocol": "TCP", "port": 80, "targetPort": 5000}],
        "type": "LoadBalancer",
    },
}

# ---------------- Ingress ----------------
ingress = {
    "apiVersion": "networking.k8s.io/v1",
    "kind": "Ingress",
    "metadata": {
        "name": "flask-ingress",
        "annotations": {"nginx.ingress.kubernetes.io/rewrite-target": "/"},
    },
    "spec": {
        "rules": [
            {
                "host": "flask.local",
                "http": {
                    "paths": [
                        {
                            "path": "/",
                            "pathType": "Prefix",
                            "backend": {
                                "service": {
                                    "name": "flask-service",
                                    "port": {"number": 80},
                                }
                            },
                        }
                    ]
                },
            }
        ]
    },
}

# ---------------- ConfigMap ----------------
configmap = {
    "apiVersion": "v1",
    "kind": "ConfigMap",
    "metadata": {"name": "flask-config"},
    "data": {"APP_ENV": "production", "settings.conf": "debug=False\nlog_level=info"},
}

# ---------------- Secret ----------------
secret_data = {"SECRET_KEY": base64.b64encode(b"supersecret123").decode("utf-8")}

secret = {
    "apiVersion": "v1",
    "kind": "Secret",
    "metadata": {"name": "flask-secret"},
    "type": "Opaque",
    "data": secret_data,
}

# ---------------- HPA ----------------
hpa = {
    "apiVersion": "autoscaling/v2",
    "kind": "HorizontalPodAutoscaler",
    "metadata": {"name": "flask-app-hpa"},
    "spec": {
        "scaleTargetRef": {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "name": "flask-app",
        },
        "minReplicas": 1,
        "maxReplicas": 5,
        "metrics": [
            {
                "type": "Resource",
                "resource": {
                    "name": "cpu",
                    "target": {"type": "Utilization", "averageUtilization": 50},
                },
            }
        ],
    },
}

# ---------------- Write to Files ----------------
manifests = {
    "deployment.yaml": deployment,
    "service.yaml": service,
    "ingress.yaml": ingress,
    "configmap.yaml": configmap,
    "secret.yaml": secret,
    "hpa.yaml": hpa,
}

for filename, content in manifests.items():
    with open(os.path.join("k8s", filename), "w") as f:
        yaml.dump(content, f)

print("✅ All Kubernetes manifests generated in 'k8s/'")
