# Monitoring

Logs estruturados são enviados para CloudWatch quando configurado.

O middleware `PerformanceMiddleware` registra requisições lentas e o pacote
`django-prometheus` exporta métricas para o Prometheus quando habilitado.
