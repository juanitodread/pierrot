import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { Construct } from 'constructs';

export class PierrotStack extends cdk.Stack {
  constructor(scope: Construct, id: string, environment: string, props?: cdk.StackProps) {
    super(scope, `${id}${environment}`, props);

    new s3.Bucket(this, `PierrotDB${environment}`, {
      bucketName: `pierrot-db-${environment.toLowerCase()}`,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      publicReadAccess: false,
      accessControl: s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
    });
  }
}