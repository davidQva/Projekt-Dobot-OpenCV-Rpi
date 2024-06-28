Does mermaid graph work!?

``` mermaid
graph TD
    A[Start main] -->|Initialize| B[Server]
    B -->|Create and start| C[opencv_thread]
    B -->|Create and start| D[server_thread]
    B -->|Initialize| E[MessageLogger]
    E -->|Register| F[logger to server]
    F -->|Initialize| G[scenario_actions dictionary]
    G --> H[Loop: Check for order updates]
    H -->|Condition| I{Is order updated?}
    I -->|Yes| J[Set oldOrder to order]
    J -->|Extract scenario| K{Is scenario in actions?}
    K -->|Yes| L[Execute scenario action]
    K -->|No| M[Execute default_scenario]
    I -->|No| N[Sleep for 1 second]
    L --> N
    M --> N
    N --> H
    H -->|Loop ends| O[Join threads]
    O --> P[Clean up resources]

```
