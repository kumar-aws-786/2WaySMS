# Two Way SMS
* Amazon Connect Two-Way SMS is a feature of Amazon Connect, Amazon Web Services' cloud-based contact center solution.

* It allows businesses to engage with customers through text messaging, supporting bidirectional communication.

* This means customers can send and receive SMS messages directly with contact center agents.

* By integrating two-way SMS into their contact center operations, businesses can offer more flexible and responsive customer service.

* This streamlines support interactions and enhances overall customer satisfaction.

* The feature is easily configured within the Amazon Connect console and supports a range of use cases, from handling customer inquiries and appointment reminders to providing real-time updates and feedback. 


# Deployment

The `cdk.json` file tells the CDK Toolkit how to execute your app.

## Useful commands

* `npm run build`   compile typescript to js
* `npm run watch`   watch for changes and compile
* `npm run test`    perform the jest unit tests
* `npx cdk deploy`  deploy this stack to your default AWS account/region
* `npx cdk diff`    compare deployed stack with current state
* `npx cdk synth`   emits the synthesized CloudFormation template


## Steps
* Make sure the AWS account has an active AWS Connect Instance and a Pinpoint Origination Identity

* Navigate to End User Messaging console and select the Pinpoint Phone Number to enable Two Way SMS

* Select Amazon Connect as the destination type and choose the appropriate AWS Connect Instance and the IAM Role 

* Make sure the IAM role has the trust policy and the permissions provided in the https://docs.aws.amazon.com/sms-voice/latest/userguide/phone-pool-two-way-sms.html?icmpid=docs_console_unmapped

* Once saved, the Phone Number appears in the AWS Connect Instance with SMS as the active channel

* Import the contact flow from the root folder to the AWS Connect Instance

* Import the AWS Lex Bot from the root folder to the AWS Lex V2 Console

* Select the Two Way SMS Phone Number from the Connect Console and select the deployed contact flow as the target

* Update the contact flow to map to the deployed AWS Lex Bot