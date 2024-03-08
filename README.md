# pierrot
Photostream delivery

## Research
* Check Flickr API to list photos/files and possible filtering.

## Design (C4 Model)
### 1. System Context
![Alt text](docs/architecture/diagrams/structurizr-SystemContext.png?raw=true "System Context")

### 2. Container
![Alt text](docs/architecture/diagrams/structurizr-Containers.png?raw=true "System Context")

### 3. Component
![Alt text](docs/architecture/diagrams/structurizr-Components.png?raw=true "System Context")

### 4. Code
#### Pierrot DB Sync Service
This service keeps Pierrot DB on sync. Pierrot has two _databases_: 
* `pierrot-meta.json` to store the total number of photos in Pierrot DB.
* `pierrot-db.json` to store all metadata (URLs) of all photos registered by Flickr.

Updating `pierrot-db.json` is expensive, so we use `pierrot-meta.json` as a Pierrot state to verify if there are changes (more photos were added to Flickr) then we update both states `pierrot-db.json` and `pierrot-meta.json`. This service runs daily allowing the publish service to check `pierrot-db.json` to select a new photo to publish instead of check directly in Flickr (to publish a photo is required to consume Flickr to download the photo first). 


```mermaid
sequenceDiagram
    participant PCJ as Pierrot CronJob
    participant PSL as Photo Storage Lambda
    participant PA as Pierrot API
    participant PFC as Pierrot Flicker Client
    participant FA as Flickr
    participant PS3C as Pierrot S3 Client
    participant S3 as S3

    PCJ->>+PSL: Sync Pierrot DB
    PSL->>+PA: Sync Pierrot DB with Flickr Storage
    PA->>+PFC: Get total photos count metadata
    PFC->>+FA: Get media by person (page=1, items=1)
    FA-->>-PFC: Media by person payload
    PFC-->>-PA: Total photos count metadata
    PA->>+PS3C: Read pierrot-meta.json
    PS3C->>+S3: Load pierrot-meta.json
    S3-->>-PS3C: Return pierrot-meta.json content
    PS3C-->>-PA: Return total photos count

    alt pierrot photos count < flickr photos count
        PA->>+PFC: Get photos metadata
        PFC->>+FA: Get media by person (page=all, items=all)
        FA-->>-PFC: Media by person payload
        PFC-->>-PA: Photos metadata

        PA->>+PS3C: Update pierrot-db.json
        PS3C->>+S3: Save pierrot-db.json
        S3-->>-PS3C: Return save ACK
        PS3C-->>-PA: pierrot-db.json updated

        PA->>+PS3C: Update pierrot-meta.json
        PS3C->>+S3: Save pierrot-meta.json
        S3-->>-PS3C: Return save ACK
        PS3C-->>-PA: pierrot-meta.json updated
    end

    PA-->>-PSL: Pierrot DB synced
```

#### Pierrot Photo Publish Service
This service publish a photo on Twitter. The service runs weekly and checks `pierrot-db.json` and `pierrot-wal.json` to randomly select an unpublished photo, download it from Flickr and publish it on Twitter.

```mermaid
sequenceDiagram
    participant PCJ as Pierrot CronJob
    participant PPL as Photo Publisher Lambda
    participant PA as Pierrot API
    participant PS3C as Pierrot S3 Client
    participant S3 as S3
    participant PFC as Pierrot Flicker Client
    participant FA as Flickr
    participant FS as File System
    participant TC as Twitter Client
    participant T as Twitter

    PCJ->>+PPL: Publish a photo
    PPL->>+PA: Publish a random photo
    PA->>+PS3C: Get published photos DB
    PS3C->>+S3: Load pierrot-wal.json
    S3-->>-PS3C: Return pierrot-wal.json content
    PS3C-->>-PA: Return a list with published photo metadata objects

    PA->>+PS3C: Get photos DB
    PS3C->>+S3: Load pierrot-db.json
    S3-->>-PS3C: Return pierrot-db.json content
    PS3C-->>-PA: Return a list with photo metadata objects

    PA->>+PFC: Get photo not published yet
    PFC-->>-PA: Returns photo (bytes)

    PA->>+FS: Saves photo file
    FS-->>-PA: Photo saved

    PA->>+TC: Publish photo
    TC->>+T: Upload photo
    T-->>-TC: Photo uploaded (media.id)
    TC->>+T: Publish tweet(media.id)
    T-->>-TC: Tweet published
    TC-->>-PA: Tweet published

    PA->>+PS3C: Update published photos DB
    PS3C->>+S3: Save pierrot-wal.json
    S3-->>-PS3C: Return save ACK
    PS3C-->>-PA: Published photos DB updated

    PA-->>-PPL: Photo published
```
