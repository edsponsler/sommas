```mermaid
graph TD
    subgraph External Events / Input
        A[External Trigger / Sensor Data] -->|Publish Event| B(Pub/Sub Topic: Input Layer)
    end

    subgraph Agent Layer 1 (e.g., Sensory Agents)
        B --> C[Cloud Function: Agent A (e.g., Edge Detector)]
        C -->|Publish Activation State| D(Pub/Sub Topic: L1 Output)
    end

    subgraph Agent Layer 2 (e.g., Feature Recognition Agents)
        D --> E[Cloud Function: Agent B (e.g., Shape Recognizer)]
        E -->|Publish Higher-Level Feature| F(Pub/Sub Topic: L2 Output)
    end

    subgraph Shared State / Blackboard
        C -.->|Read/Write Simple State| G(Firestore / Memorystore)
        E -.->|Read/Write Simple State| G
    end

    subgraph Orchestration / Agency Coordination (Optional)
        F -- Trigger --> H[Cloud Workflow: Task Coordinator]
        H -- Call Function(s) --> I[Cloud Function: Agent C (e.g., Motor Output)]
        I --> J(Pub/Sub Topic: Motor Commands)
    end

    subgraph Monitoring & Analytics
        C, E, I, G, D, F, B --> K(Cloud Logging)
        K --> L(Cloud Monitoring / BigQuery for Analytics)
    end

    subgraph Emergent Behavior
        J --> Z[Actuator / External System]
    end
```