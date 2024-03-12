#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { PierrotStack } from '../lib/pierrot-stack';

const app = new cdk.App();

const environments = ['Dev', 'Prod'];

environments.forEach(env => new PierrotStack(app, `PierrotStack`, env, {}));
