import * as cdk from 'aws-cdk-lib';
import { Effect, PolicyDocument, PolicyStatement, Role, ServicePrincipal } from 'aws-cdk-lib/aws-iam';
import { Construct } from 'constructs';

export class AssignmentStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const userTable = new cdk.aws_dynamodb.Table(this, "UserTable", {
      partitionKey: {
        name: "PhoneNumber",
        type: cdk.aws_dynamodb.AttributeType.STRING
      },
      billingMode: cdk.aws_dynamodb.BillingMode.PAY_PER_REQUEST
    });

    const fulfillmentLambda = new cdk.aws_lambda.Function(this, "FulfillmentLambda", {
      handler: "lambda_function.lambda_handler",
      code: cdk.aws_lambda.Code.fromAsset("lib/FulfillmentHandler"),
      runtime: cdk.aws_lambda.Runtime.PYTHON_3_12,
      timeout: cdk.Duration.seconds(30),
      environment: {
        "USER_TABLE": userTable.tableName
      },
      role: new Role(this, "FulfillmentRole", {
        assumedBy: new ServicePrincipal("lambda.amazonaws.com"),
        inlinePolicies: {
          "DynamoDbPolicy": new PolicyDocument({
            statements: [
              new PolicyStatement({
                actions: ["dynamodb:Get*", "dynamodb:Query*"],
                effect: Effect.ALLOW,
                resources: [userTable.tableArn]
              }),
              new PolicyStatement({
                actions: ['cloudwatch:*', "logs:*"],
                effect: Effect.ALLOW,
                resources: ["*"]
              })
            ]
          })
      }
      })
    });

  }
}
