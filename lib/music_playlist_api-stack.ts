import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ddb from 'aws-cdk-lib/aws-dynamodb';
import * as lambda from 'aws-cdk-lib/aws-lambda'
import { CfnOutput } from 'aws-cdk-lib';


export class MusicPlaylistApiStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // DynamoDB table resource to store playlists
    const table = new ddb.Table(this,  "Playlists", {
      partitionKey: { name: "playlist_id", type: ddb.AttributeType.STRING },
      billingMode: ddb.BillingMode.PAY_PER_REQUEST,
      timeToLiveAttribute: "tt1"
    });

    // ad GSI based on user_id
    table.addGlobalSecondaryIndex({
      indexName: "user-index",
      partitionKey: { name: "user_id", type: ddb.AttributeType.STRING },
      sortKey: { name: "created_timr", type: ddb.AttributeType.NUMBER}
    });


    // create lambda function resource
    const api = new lambda.Function(this, "API", {
      runtime: lambda.Runtime.PYTHON_3_9,
      code: lambda.Code.fromAsset("./api/lambda_function.zip"),
      handler: "main.handler",
      environment: {
        TABLE_NAME: table.tableName,
      },
    });

    const functionURL = api.addFunctionUrl({
      authType: lambda.FunctionUrlAuthType.NONE,
      cors: {
        allowedOrigins: ["*"],
        allowedMethods: [lambda.HttpMethod.ALL],
        allowedHeaders: ["*"]
      },
    });


    // out the API Function URL
    new CfnOutput(this, "APIUrl", {
      value: functionURL.url
    });

    // grant access to dynamodb
    table.grantReadWriteData(api);


  }
}
