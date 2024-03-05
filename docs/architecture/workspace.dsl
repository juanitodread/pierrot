workspace {

    model {
        flickr = softwareSystem "Flickr" "Photo storage." "Existing System"
        
        twitter = softwareSystem "Twitter" "Social media where photos are published." "Existing System"
        
        pierrotSystem = softwareSystem "Pierrot" "Publish a random photo from Flickr to Twitter and keeps track of what was published to do not repeat photos." {
            pierrotCronJob = container "Pierrot CronJob" "Triggers Pierrot API to publish a photo." "AWS CronJob service"
            awsS3 = container "AWS S3" "Stores photo metadata and tracks published photos." "AWS S3"
            pierrotApi = container "Pierrot API" "Consumes Flickr API to get photos and publish them to Twitter Service." "AWS Lambda" {
                photoStorage = component "Photo Storage" "Syncs Flickr photo info with Pierrot metadata storage." "AWS Lambda"
                s3Client = component "S3 Client" "Adapter for AWS S3 API." "Python module"
                photoPublisher = component "Photo Publisher" "Publish a photo on Twitter and keep track of the published photos in Pierrot DB." "AWS Lambda"
                twitterClient = component "Twitter Client" "Adapter for Twitter API." "Python module"
                pierrot = component "Pierrot" "Exposes API functionality. Fetch photos from Flickr and send them to Twitter. Tracks Pierrot state." "Python module"
                flickrClient = component "Flickr Client" "Adapter for Flickr API." "Python module"
            }
        }
        
        pierrotSystem -> flickr "Makes API call to get a photo" "JSON/HTTP"
        pierrotSystem -> twitter "Makes API call to publish a photo" "JSON/HTTP"
        
        pierrotCronJob -> pierrotApi "Makes API call to invoke" "JSON/HTTP"
        pierrotApi -> awsS3 "Reads from and writes to" "JSON/HTTP"
        pierrotApi -> flickr "Makes API call to get a photo" "JSON/HTTP"
        pierrotApi -> twitter "Makes API call to publish a photo" "JSON/HTTP"
        
        pierrotCronJob -> photoStorage "Makes API call to invoke" "JSON/HTTP"
        pierrotCronJob -> photoPublisher "Makes API call to invoke" "JSON/HTTP"
        s3Client -> awsS3 "Reads from and writes to" "JSON/HTTP"
        photoStorage -> pierrot "Uses" ""
        photoPublisher -> pierrot "Uses" ""
        pierrot -> s3Client "Uses" ""
        pierrot -> flickrClient "Uses" ""
        pierrot -> twitterClient "Uses" ""
        twitterClient -> twitter "Makes API call to publish a photo" "JSON/HTTP"
        flickrClient -> flickr "Makes API call to get a photo" "JSON/HTTP"
    }

    views {
        systemContext pierrotSystem "SystemContext" {
            include *
            autolayout lr
            description "Service to publish personal photos to Twitter in a period basis."
        }

        container pierrotSystem "Containers" {
            include *
            autolayout lr
            description "Service to publish personal photos to Twitter in a period basis."
        }
        
        component pierrotApi "Components" {
            include *
            autolayout lr
            description "Service to publish personal photos to Twitter in a period basis."
        }

        theme default
        
        styles {
            element "Existing System" {
                background #999999
                color #ffffff
            }
            element "AWS S3" {
                shape Cylinder
            }
            element "Failover" {
                opacity 25
            }
        }
    }

}