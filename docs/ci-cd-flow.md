# CI/CD Pipeline Flow

```
┌─────────────┐    ┌────────────────┐    ┌──────────────┐
│ Code Change ├───►│ Change Detector ├───►│ Matrix Build │
└─────────────┘    └────────────────┘    └──────┬───────┘
                                                 │
                                         ┌───────┴───────┐
                                         │               │
                                   ┌─────▼────┐   ┌──────▼─────┐
                                   │  React   │   │   Python   │
                                   │  Checks  │   │   Checks   │
                                   └─────┬────┘   └──────┬─────┘
                                         │              │
                                         └──────┬───────┘
                                               │
                                        ┌──────▼──────┐
                                        │  Security   │
                                        │    Scan     │
                                        └──────┬──────┘
                                               │
                                        ┌──────▼──────┐
                                        │   Deploy    │
                                        │  (if main)  │
                                        └─────────────┘
```

## Pipeline Steps

1. **Code Changes**: Developer pushes code
2. **Change Detection**: Identifies modified services
3. **Matrix Build**: Parallel builds for each service
4. **Quality Checks**: Language-specific testing
5. **Security Scan**: Vulnerability assessment
6. **Deployment**: Production deploy for main branch

For implementation details, see the [CI/CD workflow configuration](../.github/workflows/ci-cd.yaml).

---

> **Note**: If the ASCII diagram above doesn't render correctly, you can view the [PNG version of the CI/CD flow](../backend-flask/images/ci-cd-flow.png). 