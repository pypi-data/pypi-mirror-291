[![GitHub](https://img.shields.io/github/license/gammarers/aws-rds-database-running-schedule-stack?style=flat-square)](https://github.com/gammarers/aws-rds-database-running-schedule-stack/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@gammarer/aws-rds-database-running-schedule-stack?style=flat-square)](https://www.npmjs.com/package/@gammarer/aws-rds-database-running-schedule-stack)
[![PyPI](https://img.shields.io/pypi/v/gammarer.aws-rds-database-running-schedule-stack?style=flat-square)](https://pypi.org/project/gammarer.aws-rds-database-running-schedule-stack/)
[![Nuget](https://img.shields.io/nuget/v/Gammarer.CDK.AWS.RdsDatabaseRunningScheduleStack?style=flat-square)](https://www.nuget.org/packages/Gammarers.CDK.AWS.RdsDatabaseRunningScheduler/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/gammarers/aws-rds-database-running-schedule-stack/release.yml?branch=main&label=release&style=flat-square)](https://github.com/gammarers/aws-rds-database-running-schedule-stack/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/gammarers/aws-rds-database-running-schedule-stack?sort=semver&style=flat-square)](https://github.com/gammarers/aws-rds-database-running-schedule-stack/releases)

# AWS RDS Database Running Scheduler

This is an AWS CDK Construct to make RDS Database running schedule (only running while working hours(start/stop)).

## Fixed

* RDS Aurora Cluster
* RDS Instance

## Resources

This construct creating resource list.

* EventBridge Scheduler execution role
* EventBridge Scheduler

## Install

### TypeScript

```shell
npm install @gammarers/aws-rds-database-running-schedule-stack
# or
yarn add @gammarers/aws-rds-database-running-schedule-stack
```

### Python

```shell
pip install gammarers.aws-rds-database-running-schedule-stack
```

### C# / .NET

```shell
dotnet add package Gammarers.CDK.AWS.RdsDatabaseRunningScheduleStack
```

## Example

```python
import { RdsDatabaseRunningScheduler, DatabaseType } from '@gammarer/aws-rds-database-running-schedule-stack';

new RdsDatabaseRunningScheduleStack(stack, 'RdsDatabaseRunningScheduleStack', {
  targets: [
    {
      type: DatabaseType.CLUSTER,
      identifiers: ['db-cluster-1a'],
      startSchedule: {
        timezone: 'UTC',
      },
      stopSchedule: {
        timezone: 'UTC',
      },
    },
    {
      type: DatabaseType.INSTANCE,
      identifiers: ['db-instance-1a'],
      startSchedule: {
        timezone: 'UTC',
      },
      stopSchedule: {
        timezone: 'UTC',
      },
    },
  ],
});
```

## License

This project is licensed under the Apache-2.0 License.
