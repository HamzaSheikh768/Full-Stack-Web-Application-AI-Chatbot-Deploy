# Helm AI Patterns

AI-enhanced Helm chart patterns for intelligent Kubernetes deployments.

## AI-Driven Deployment Strategies

### 1. Predictive Scaling

Use AI to predict load and scale proactively:

```yaml
# values.yaml
autoscaling:
  enabled: true
  ai:
    enabled: true
    provider: "claude"  # or "openai"
    model: "claude-sonnet-4-20250514"
    metrics:
      - type: "http_requests"
        lookback: "7d"
        forecast: "1h"
      - type: "cpu_usage"
        lookback: "24h"
        forecast: "15m"
  minReplicas: 2
  maxReplicas: 20
  targetCPU: 70
  predictive:
    enabled: true
    scaleUpThreshold: 0.8  # Scale when predicted load > 80% capacity
    scaleDownThreshold: 0.3  # Scale down when predicted < 30%
```

**Implementation in deployment template**:

```yaml
# templates/hpa.yaml
{{- if .Values.autoscaling.ai.enabled }}
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{ include "app.fullname" . }}-ai-hpa
  annotations:
    ai.kubernetes.io/enabled: "true"
    ai.kubernetes.io/provider: {{ .Values.autoscaling.ai.provider }}
    ai.kubernetes.io/model: {{ .Values.autoscaling.ai.model }}
    ai.kubernetes.io/prediction-window: {{ .Values.autoscaling.ai.metrics[0].forecast }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ include "app.fullname" . }}
  minReplicas: {{ .Values.autoscaling.minReplicas }}
  maxReplicas: {{ .Values.autoscaling.maxReplicas }}
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 60
      - type: Pods
        value: 4
        periodSeconds: 60
      selectPolicy: Max
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
{{- end }}
```

### 2. Intelligent Health Checks

AI-generated health check configurations based on application analysis:

```yaml
# values.yaml
healthChecks:
  ai:
    enabled: true
    analyze: true  # AI analyzes app to suggest optimal settings
  liveness:
    path: /health
    port: http
    initialDelaySeconds: 30  # AI-suggested based on startup time
    periodSeconds: 10
    timeoutSeconds: 5
    failureThreshold: 3
  readiness:
    path: /ready
    port: http
    initialDelaySeconds: 5   # AI-optimized
    periodSeconds: 5
    timeoutSeconds: 3
    failureThreshold: 3
  startup:
    path: /health
    port: http
    initialDelaySeconds: 0
    periodSeconds: 5
    timeoutSeconds: 5
    failureThreshold: 30  # AI calculates based on worst-case startup
```

**Template with AI analysis**:

```yaml
# templates/deployment.yaml
livenessProbe:
  httpGet:
    path: {{ .Values.healthChecks.liveness.path }}
    port: {{ .Values.healthChecks.liveness.port }}
  {{- if .Values.healthChecks.ai.analyze }}
  # AI-optimized based on historical data
  initialDelaySeconds: {{ .Values.healthChecks.liveness.initialDelaySeconds }}
  periodSeconds: {{ .Values.healthChecks.liveness.periodSeconds }}
  {{- else }}
  # Conservative defaults
  initialDelaySeconds: 60
  periodSeconds: 30
  {{- end }}
```

### 3. Resource Optimization with AI

AI recommends optimal resource requests and limits:

```yaml
# values.yaml
resources:
  ai:
    enabled: true
    mode: "optimize"  # optimize, recommend, enforce
    provider: "claude"
    analyze_period: "7d"
  # AI-suggested values based on historical usage
  requests:
    cpu: 100m      # AI: actual avg usage is 95m
    memory: 128Mi  # AI: 95th percentile is 120Mi
  limits:
    cpu: 500m      # AI: peak is 450m
    memory: 512Mi  # AI: max observed is 480Mi
  # AI confidence and suggestions
  ai_confidence: 0.92
  ai_suggestions:
    - "CPU request can be reduced to 90m (saves 10%)"
    - "Memory limit can be reduced to 384Mi (saves 25%)"
    - "Consider burstable QoS class"
```

**Helper to apply AI recommendations**:

```yaml
# templates/_helpers.tpl
{{- define "app.resources" -}}
{{- if .Values.resources.ai.mode -}}
{{- if eq .Values.resources.ai.mode "optimize" -}}
resources:
  requests:
    cpu: {{ .Values.resources.ai_optimized.requests.cpu | default .Values.resources.requests.cpu }}
    memory: {{ .Values.resources.ai_optimized.requests.memory | default .Values.resources.requests.memory }}
  limits:
    cpu: {{ .Values.resources.ai_optimized.limits.cpu | default .Values.resources.limits.cpu }}
    memory: {{ .Values.resources.ai_optimized.limits.memory | default .Values.resources.limits.memory }}
{{- end }}
{{- end }}
{{- end }}
```

### 4. Canary Deployment with AI Analysis

Progressive delivery with ML-driven rollout decisions:

```yaml
# values.yaml
deployment:
  strategy:
    type: "ai-canary"
    canary:
      enabled: true
      ai:
        enabled: true
        provider: "claude"
        analysis:
          metrics:
            - name: "error_rate"
              threshold: 0.01  # 1% error rate
              weight: 0.4
            - name: "latency_p99"
              threshold: 500   # 500ms
              weight: 0.3
            - name: "success_rate"
              threshold: 0.99  # 99% success
              weight: 0.3
          decision: "automatic"  # AI decides to promote or rollback
      steps:
        - weight: 10
          duration: 5m
        - weight: 25
          duration: 10m
        - weight: 50
          duration: 15m
        - weight: 100
          duration: 0
```

**Flagger integration for AI canary**:

```yaml
# templates/canary.yaml
{{- if .Values.deployment.strategy.canary.enabled }}
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: {{ include "app.fullname" . }}
  annotations:
    ai.flagger.io/enabled: "true"
    ai.flagger.io/provider: {{ .Values.deployment.strategy.canary.ai.provider }}
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ include "app.fullname" . }}
  progressDeadlineSeconds: 600
  service:
    port: {{ .Values.service.port }}
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 100
    stepWeight: 10
    ai:
      enabled: {{ .Values.deployment.strategy.canary.ai.enabled }}
      analysis_endpoint: "http://ai-analyzer.kube-system.svc/analyze"
    metrics:
    {{- range .Values.deployment.strategy.canary.ai.analysis.metrics }}
    - name: {{ .name }}
      templateRef:
        name: {{ .name }}
      thresholdRange:
        max: {{ .threshold }}
      interval: 1m
      weight: {{ .weight }}
    {{- end }}
{{- end }}
```

## AI-Enhanced Monitoring

### Auto-Generated Dashboards

```yaml
# values.yaml
monitoring:
  ai:
    enabled: true
    auto_dashboard: true
    provider: "claude"
  grafana:
    enabled: true
    dashboards:
      ai_generated: true
      metrics:
        - http_request_duration
        - http_requests_total
        - cpu_usage
        - memory_usage
        - event_processing_lag
```

**Generated ConfigMap for Grafana**:

```yaml
# templates/grafana-dashboard.yaml
{{- if .Values.monitoring.ai.auto_dashboard }}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "app.fullname" . }}-dashboard
  labels:
    grafana_dashboard: "1"
  annotations:
    ai.grafana.io/generated: "true"
    ai.grafana.io/provider: {{ .Values.monitoring.ai.provider }}
data:
  dashboard.json: |
    {
      "dashboard": {
        "title": "{{ include "app.fullname" . }} - AI Generated",
        "panels": [
          {
            "title": "Request Rate",
            "targets": [
              {
                "expr": "rate(http_requests_total{app='{{ include "app.fullname" . }}'}[5m])"
              }
            ]
          },
          {
            "title": "AI Anomaly Detection",
            "targets": [
              {
                "expr": "ai_anomaly_score{app='{{ include "app.fullname" . }}'}"
              }
            ]
          }
        ]
      }
    }
{{- end }}
```

### Intelligent Alerting

```yaml
# values.yaml
alerting:
  ai:
    enabled: true
    provider: "claude"
    mode: "smart"  # smart, baseline, threshold
    learning_period: "7d"
  rules:
    - name: high_error_rate
      ai_threshold: true  # AI calculates threshold
      baseline: 0.01      # Fallback if AI unavailable
      severity: critical
    - name: high_latency
      ai_threshold: true
      baseline: 1000      # ms
      severity: warning
```

**PrometheusRule with AI**:

```yaml
# templates/prometheusrule.yaml
{{- if .Values.alerting.ai.enabled }}
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: {{ include "app.fullname" . }}-ai-alerts
  annotations:
    ai.prometheus.io/enabled: "true"
    ai.prometheus.io/provider: {{ .Values.alerting.ai.provider }}
spec:
  groups:
  - name: {{ include "app.fullname" . }}.rules
    interval: 30s
    rules:
    {{- range .Values.alerting.rules }}
    - alert: {{ .name }}
      expr: |
        {{- if .ai_threshold }}
        ai_dynamic_threshold{alert="{{ .name }}", app="{{ include "app.fullname" $ }}"} == 1
        {{- else }}
        rate(errors_total{app="{{ include "app.fullname" $ }}"}[5m]) > {{ .baseline }}
        {{- end }}
      for: 5m
      labels:
        severity: {{ .severity }}
        ai_managed: "true"
      annotations:
        summary: "AI-detected anomaly: {{ .name }}"
        ai_confidence: "{{ "{{" }} $labels.ai_confidence {{ "}}" }}"
    {{- end }}
{{- end }}
```

## AI-Powered Configuration

### Dynamic Environment Variables

AI suggests environment variables based on application analysis:

```yaml
# values.yaml
env:
  ai:
    enabled: true
    analyze_code: true  # AI analyzes application code
    suggest: true
  # AI-suggested based on code analysis
  variables:
    - name: LOG_LEVEL
      value: "info"
      ai_source: "detected logger usage"
    - name: WORKERS
      value: "4"
      ai_source: "optimal for 2 CPU cores"
    - name: TIMEOUT
      value: "30000"
      ai_source: "analyzed downstream dependencies"
    - name: CACHE_TTL
      value: "3600"
      ai_source: "predicted optimal based on access patterns"
```

### Secret Management with AI

AI detects secrets in config and recommends proper storage:

```yaml
# values.yaml
secrets:
  ai:
    enabled: true
    scan: true  # AI scans for exposed secrets
    recommend_vault: true
  items:
    - name: DATABASE_URL
      ai_detected: true
      ai_recommendation: "Move to Vault or Sealed Secrets"
      valueFrom:
        secretKeyRef:
          name: {{ .Release.Name }}-secrets
          key: database-url
```

## Cost Optimization Patterns

### AI-Driven Node Affinity

```yaml
# values.yaml
nodeAffinity:
  ai:
    enabled: true
    optimize_cost: true
  preferred:
    - weight: 100
      preference:
        matchExpressions:
        - key: node.kubernetes.io/instance-type
          operator: In
          values:
          - t3.medium  # AI suggests this is optimal cost/performance
```

### Spot Instance Integration

```yaml
# values.yaml
spotInstances:
  ai:
    enabled: true
    risk_analysis: true
    provider: "claude"
  enabled: true
  tolerations:
    - key: "spot-instance"
      operator: "Equal"
      value: "true"
      effect: "NoSchedule"
  # AI calculates acceptable interruption rate
  ai_risk_score: 0.15  # 15% interruption probability acceptable
```

## Best Practices

### 1. Version AI Configurations

```yaml
ai:
  version: "1.0"
  provider: "claude"
  model: "claude-sonnet-4-20250514"
  config_hash: "abc123"  # Track AI config changes
```

### 2. Fallback to Defaults

Always provide non-AI defaults:

```yaml
{{- if .Values.ai.enabled }}
{{ .Values.ai.optimized.value }}
{{- else }}
{{ .Values.default.value }}
{{- end }}
```

### 3. Confidence Thresholds

Only apply AI recommendations above confidence threshold:

```yaml
{{- if and .Values.ai.enabled (gt .Values.ai.confidence 0.9) }}
# Use AI recommendation
{{- else }}
# Use conservative default
{{- end }}
```

### 4. Audit AI Decisions

Log all AI-driven decisions:

```yaml
annotations:
  ai.decision.timestamp: "{{ now }}"
  ai.decision.recommendation: "{{ .Values.ai.recommendation }}"
  ai.decision.confidence: "{{ .Values.ai.confidence }}"
  ai.decision.applied: "{{ .Values.ai.applied }}"
```

## kubectl-ai Integration

Use natural language to manage Helm releases:

```bash
# Deploy with AI assistance
kubectl ai "deploy my-app using helm with AI optimization enabled"

# Upgrade with AI analysis
kubectl ai "upgrade my-app and let AI optimize resources"

# Troubleshoot
kubectl ai "why is my-app helm release failing?"

# Cost optimization
kubectl ai "analyze my-app helm costs and suggest optimizations"
```

## Example: Complete AI-Enhanced Chart

See `examples/todo-app-ai/` for a complete Helm chart with:
- AI-driven autoscaling
- Intelligent health checks
- Resource optimization
- Canary deployments with ML
- Auto-generated monitoring
- Cost optimization
- Smart alerting

```bash
helm install todo-app ./todo-app-ai \
  --set ai.enabled=true \
  --set ai.provider=claude \
  --set ai.optimize=true
```

The AI will:
1. Analyze application code and dependencies
2. Optimize resource requests/limits
3. Configure intelligent scaling
4. Set up predictive monitoring
5. Generate dashboards and alerts
6. Recommend cost optimizations
7. Configure canary deployment strategy

## Conclusion

AI-enhanced Helm patterns enable:
- **Predictive scaling** - Scale before load hits
- **Intelligent health checks** - Optimal timing based on app behavior
- **Resource optimization** - Right-size based on actual usage
- **Smart deployments** - ML-driven canary decisions
- **Auto-generated monitoring** - Dashboards and alerts from code analysis
- **Cost optimization** - AI finds savings opportunities

Use these patterns to build self-optimizing, intelligent Kubernetes deployments.